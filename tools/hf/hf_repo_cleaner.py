import argparse
import os
import re
from typing import Iterable, List

from huggingface_hub import HfApi
from huggingface_hub.errors import HfHubHTTPError


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Delete Hugging Face repos by regex, with a mandatory dry-run first."
    )
    p.add_argument("--owner", required=True, help="User or org (e.g., tokyotech-llm)")
    p.add_argument("--repo-type", choices=["model", "dataset", "space"], default="model")
    p.add_argument("--name-regex", required=True, help="Regex to match repos to delete")
    p.add_argument(
        "--execute",
        action="store_true",
        help="Actually delete the repos AFTER printing the dry-run list",
    )
    p.add_argument(
        "--yes",
        action="store_true",
        help="Skip the interactive 'yes' confirmation (effective only with --execute)",
    )
    return p.parse_args()


def iter_repo_ids(api: HfApi, owner: str, repo_type: str) -> Iterable[str]:
    """
    Yield repo IDs as 'owner/name' for the given owner and repo type.
    Uses official listing APIs only.
    """
    if repo_type == "model":
        # ModelInfo has .modelId (preferred), sometimes .id exists too.
        for info in api.list_models(author=owner):
            rid = getattr(info, "modelId", None) or getattr(info, "id", None)
            if rid:
                yield rid
    elif repo_type == "dataset":
        for info in api.list_datasets(author=owner):
            rid = getattr(info, "id", None)
            if rid:
                yield rid
    else:  # space
        for info in api.list_spaces(author=owner):
            rid = getattr(info, "id", None)
            if rid:
                yield rid


def main() -> None:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_HUB_TOKEN")
    if not token:
        print("ERROR: Please set HF_TOKEN (or HUGGINGFACE_HUB_TOKEN).")
        raise SystemExit(2)

    args = parse_args()
    api = HfApi(token=token)

    rgx = re.compile(args.name_regex)

    # Collect targets (apply regex to both 'owner/name' and the short 'name').
    targets: List[str] = []
    for rid in iter_repo_ids(api, args.owner, args.repo_type):
        short = rid.split("/", 1)[1] if "/" in rid else rid
        if rgx.search(rid) or rgx.search(short):
            targets.append(rid)

    # ---- DRY-RUN (always shown) ----
    print("\n[DRY-RUN] Matching repositories:")
    if targets:
        for rid in sorted(targets):
            print(f"  - {rid}")
    else:
        print("  (no matches)")

    if not args.execute:
        print("\nDry-run only. No deletions performed. Re-run with --execute to delete.")
        return

    if not targets:
        print("\nNo matches. Nothing to delete.")
        return

    if not args.yes:
        resp = input(
            "\nThe above repositories will be permanently deleted. "
            "Type 'yes' to proceed: "
        ).strip().lower()
        if resp != "yes":
            print("Aborted.")
            return

    # ---- Deletion phase ----
    print("\nDeleting...")
    for rid in sorted(targets):
        try:
            api.delete_repo(repo_id=rid, repo_type=args.repo_type)
            print(f"Deleted: {rid}")
        except HfHubHTTPError as e:
            print(f"[ERROR] Failed to delete {rid}: {e}")
            raise SystemExit(1)
        except Exception as e:
            print(f"[ERROR] Unexpected error for {rid}: {e}")
            raise SystemExit(1)

    print("\nDone.")


if __name__ == "__main__":
    main()
