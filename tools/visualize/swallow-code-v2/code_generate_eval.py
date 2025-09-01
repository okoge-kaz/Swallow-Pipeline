import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "text.usetex": False,
        "axes.labelsize": 20,
        "axes.titlesize": 20,
        "xtick.labelsize": 18,
        "ytick.labelsize": 18,
        "legend.fontsize": 16,
    }
)

sns.set_theme(style="whitegrid")

tokens = [10, 20, 30, 40, 50]

# Experimental results
data = {
    "exp1": {
        "label": "SwallowCode-v1",
        "color": "#1f77b4",
        "marker": "o",
        "values": [
            [0.537, 0.463, 0.0966, 0.3175],
            [0.555, 0.482, 0.1179, 0.3333],
            [0.591, 0.53, 0.1191, 0.3649],
            [0.579, 0.537, 0.1226, 0.3553],
            [0.598, 0.537, 0.1227, 0.3750],
        ],
    },
    "exp2": {
        "label": "Qwen3 1-stage (high quality)",
        "color": "#ff7f0e",
        "marker": "s",
        "values": [
            [0.451, 0.39, 0.0914, 0.3096],
            [0.476, 0.421, 0.0993, 0.3079],
            [0.5, 0.463, 0.0839, 0.2912],
            [0.549, 0.5, 0.0907, 0.3079],
            [0.555, 0.5, 0.1010, 0.3420],
        ],
    },
    "exp3": {
        "label": "Qwen3 1-stage + thinking",
        "color": "#2ca02c",
        "marker": "^",
        "values": [
            [0.329, 0.28, 0.0984, 0.3140],
            [0.433, 0.378, 0.1077, 0.3123],
            [0.421, 0.36, 0.1045, 0.3193],
            [0.402, 0.354, 0.1157, 0.3289],
            [0.451, 0.39, 0.1172, 0.3211],
        ],
    },
    "exp4": {
        "label": "Qwen3 1-stage (medium quality)",
        "color": "#d62728",
        "marker": "d",
        "values": [
            [0.494, 0.457, 0.1065, 0.3035],
            [0.463, 0.421, 0.0994, 0.3123],
            [0.555, 0.512, 0.1009, 0.3281],
            [0.555, 0.5, 0.1072, 0.3289],
            [0.561, 0.512, 0.1103, 0.3340],
        ],
    },
    "exp6": {
        "label": "Qwen3 Instruct 2-stage (medium quality)",
        "color": "#9467bd",
        "marker": "P",
        "values": [
            [0.5, 0.451, 0.1015, 0.3377],
            [0.518, 0.476, 0.1054, 0.3588],
            [0.591, 0.543, 0.1114, 0.3614],
            [0.543, 0.5, 0.1137, 0.3702],
            [0.591, 0.53, 0.1173, 0.3588],
        ],
    },
}

benchmarks = ["HumanEval", "HumanEval+", "LiveCodeBench", "BigCodeBench"]

fig, axes = plt.subplots(2, 2, figsize=(12, 8), dpi=300, facecolor="white")
axes = axes.flatten()
baselines = [data["exp1"]["values"][0][i] for i in range(4)]

# Plot
for i, ax in enumerate(axes):
    ax.axhline(y=baselines[i], color="gray", linestyle="--", alpha=0.5, linewidth=2.0)
    for key, exp in data.items():
        vals = [row[i] for row in exp["values"]]
        ax.plot(
            tokens,
            vals,
            marker=exp["marker"],
            linewidth=2.5,
            linestyle="-",
            color=exp["color"],
            label=exp["label"] if i == 0 else None,  # Only label in first subplot
            markeredgecolor="white",
            markeredgewidth=1.5,
            markersize=8,
        )
    ax.set_title(benchmarks[i], fontsize=16, fontweight="bold")
    ax.set_xlabel("Billion Tokens", fontsize=14, fontweight="bold", color="#000000")
    ax.set_xticks(tokens)
    ax.tick_params(axis="both", width=1.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(True, linestyle="--", alpha=0.2)
    if i in [0, 2]:  # left column only
        ax.set_ylabel("Score", fontsize=14, fontweight="bold", color="#000000")

# Legend (shared)
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles,
    labels,
    loc="upper center",
    bbox_to_anchor=(0.5, 0.02),
    ncol=3,
    frameon=True,
    fancybox=True,
    shadow=False,
    framealpha=0.9,
    edgecolor="#dddddd",
    fontsize=14,
)

plt.tight_layout(pad=0.3)
fig.subplots_adjust(bottom=0.12, top=0.92, hspace=0.3, wspace=0.15)

# Save
plt.savefig("figures/swallow-code-v2/code_gen_eval.png", bbox_inches="tight", dpi=300)
plt.close()
