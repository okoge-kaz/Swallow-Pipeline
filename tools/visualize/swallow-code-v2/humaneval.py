import matplotlib.pyplot as plt
import seaborn as sns
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot HumanEval and HumanEval+ scores for selected experiments.")
parser.add_argument(
    "--exp",
    type=str,
    default="1,2,4,6,7,8",
    help='Comma-separated list of experiment IDs to plot (e.g., "1,2,3")',
)
parser.add_argument(
    "--labels",
    type=str,
    default="SwallowCode-v1,1-stage (High Quality),1-stage (Medium Quality),2-stage (Medium Quality),1-stage (2507-Instruct medium),1-stage (2507-Instruct medium + Q&A)",
    help="Comma-separated list of labels for the experiments (must match --exp order and length)",
)
args = parser.parse_args()

# Convert comma-separated experiment IDs to a list of integers
experiments_to_plot = [int(exp_id.strip()) for exp_id in args.exp.split(",")]
# Convert comma-separated labels to a list
exp_labels = [label.strip() for label in args.labels.split(",")]

# Validate that the number of labels matches the number of experiments
if len(experiments_to_plot) != len(exp_labels):
    raise ValueError("The number of labels must match the number of experiment IDs")

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman"],
        "text.usetex": False,
        "axes.labelsize": 14,
        "axes.titlesize": 16,
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
        "legend.fontsize": 10,
    }
)

sns.set_theme(style="whitegrid")

experiments_data = [
    {  # Experiment 1 (SwallowCode-v1)
        "id": 1,
        "humaneval": [
            0.530,
            0.494,
            0.537,
            0.506,
            0.494,
            0.555,
            0.537,
            0.579,
            0.591,
            0.610,
            0.567,
            0.579,
            0.591,
            0.591,
            0.598,
        ],
        "humaneval_plus": [
            0.457,
            0.427,
            0.463,
            0.445,
            0.457,
            0.482,
            0.463,
            0.543,
            0.530,
            0.543,
            0.512,
            0.537,
            0.543,
            0.537,
            0.537,
        ],
    },
    {  # Experiment 2 (Qwen3-235B-A22B high quality 1-stage)
        "id": 2,
        "humaneval": [
            0.439,
            0.470,
            0.451,
            0.451,
            0.470,
            0.476,
            0.506,
            0.518,
            0.500,
            0.530,
            0.537,
            0.549,
            0.543,
            0.567,
            0.555,
        ],
        "humaneval_plus": [
            0.366,
            0.421,
            0.390,
            0.409,
            0.415,
            0.421,
            0.445,
            0.457,
            0.463,
            0.463,
            0.488,
            0.500,
            0.482,
            0.512,
            0.500,
        ],
    },
    {  # Experiment 4 (Qwen3-235B-A22B medium quality 1-stage)
        "id": 4,
        "humaneval": [
            0.506,
            0.518,
            0.494,
            0.524,
            0.524,
            0.463,
            0.567,
            0.555,
            0.555,
            0.543,
            0.561,
            0.555,
            0.579,
            0.598,
            0.561,
        ],
        "humaneval_plus": [
            0.470,
            0.470,
            0.457,
            0.482,
            0.482,
            0.421,
            0.512,
            0.500,
            0.512,
            0.494,
            0.500,
            0.500,
            0.518,
            0.543,
            0.512,
        ],
    },
    {  # Experiment 6 (Exp4 -> Qwen3-235B-A22B-2507-Instruct medium quality 2-stage)
        "id": 6,
        "humaneval": [
            0.402,
            0.494,
            0.500,
            0.506,
            0.488,
            0.518,
            0.518,
            0.512,
            0.591,
            0.524,
            0.573,
            0.543,
            0.585,
            0.610,
            0.591,
        ],
        "humaneval_plus": [
            0.360,
            0.451,
            0.451,
            0.457,
            0.451,
            0.476,
            0.463,
            0.470,
            0.543,
            0.482,
            0.524,
            0.500,
            0.537,
            0.543,
            0.530,
        ],
    },
    {  # Experiment 7 (Qwen3-235B-A22B-2507-Instruct medium quality 1-stage)
        "id": 7,
        "humaneval": [
            0.500,
            0.494,
            0.518,
            0.543,
            0.573,
            0.579,
            0.579,
            0.579,
            0.543,
            0.585,
            0.579,
            0.573,
            0.567,
            0.573,
            0.604,
        ],
        "humaneval_plus": [
            0.439,
            0.421,
            0.470,
            0.470,
            0.512,
            0.518,
            0.518,
            0.524,
            0.488,
            0.506,
            0.506,
            0.518,
            0.512,
            0.518,
            0.543,
        ],
    },
    {  # Experiment 8
        "id": 8,
        "humaneval": [
            0.4630,
            0.4940,
            0.518,
            0.4880,
            0.5370,
            0.5300,
            0.5370,
            0.5490,
            0.567,
            0.6040,
            0.5910,
            0.6160,
            0.5980,
            0.5980,
            0.6280,
        ],
        "humaneval_plus": [
            0.4150,
            0.4330,
            0.463,
            0.4210,
            0.4630,
            0.4700,
            0.4880,
            0.4940,
            0.494,
            0.5370,
            0.5300,
            0.5550,
            0.5610,
            0.5490,
            0.5670,
        ],
    },
]

training_tokens_15 = [
    4.19,
    8.39,
    10.49,
    12.58,
    16.78,
    20.97,
    25.17,
    29.36,
    31.46,
    33.55,
    37.75,
    41.94,
    46.14,
    50.33,
    52.43,
]

colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b", "#9467bd"]
markers = ["o", "s", "^", "d", "P", "v"]

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300, facecolor="white")

# Plot HumanEval
for exp_data in experiments_data:
    if exp_data["id"] in experiments_to_plot:
        label_idx = experiments_to_plot.index(exp_data["id"])
        if exp_data["id"] == 1:  # SwallowCode-v1
            # Only plot dashed line for final score without label
            final_score = exp_data["humaneval"][-1]
            ax1.axhline(
                y=final_score,
                color=colors[label_idx % len(colors)],
                linestyle="--",
                linewidth=1.5,
                alpha=0.6,
            )
        else:
            # Plot score progression for other experiments
            ax1.plot(
                training_tokens_15,
                exp_data["humaneval"],
                marker=markers[label_idx % len(markers)],
                linewidth=2.2,
                linestyle="-",
                color=colors[label_idx % len(colors)],
                label=exp_labels[label_idx],
                markeredgecolor="white",
                markeredgewidth=1,
                markersize=6,
                alpha=0.8,
            )
ax1.set_xlabel("Training Tokens (Billions)", fontsize=14, fontweight="bold")
ax1.set_ylabel("Score", fontsize=14, fontweight="bold")
ax1.set_title("HumanEval", fontsize=16, fontweight="bold")
ax1.grid(True, linestyle="--", alpha=0.3)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Plot HumanEval+
for exp_data in experiments_data:
    if exp_data["id"] in experiments_to_plot:
        label_idx = experiments_to_plot.index(exp_data["id"])
        if exp_data["id"] == 1:  # SwallowCode-v1
            # Only plot dashed line for final score without label
            final_score = exp_data["humaneval_plus"][-1]
            ax2.axhline(
                y=final_score,
                color=colors[label_idx % len(colors)],
                linestyle="--",
                linewidth=1.5,
                alpha=0.6,
            )
        else:
            # Plot score progression for other experiments
            ax2.plot(
                training_tokens_15,
                exp_data["humaneval_plus"],
                marker=markers[label_idx % len(markers)],
                linewidth=2.2,
                linestyle="-",
                color=colors[label_idx % len(colors)],
                label=exp_labels[label_idx],
                markeredgecolor="white",
                markeredgewidth=1,
                markersize=6,
                alpha=0.8,
            )
ax2.set_xlabel("Training Tokens (Billions)", fontsize=14, fontweight="bold")
ax2.set_ylabel("Score", fontsize=14, fontweight="bold")
ax2.set_title("HumanEval+", fontsize=16, fontweight="bold")
ax2.grid(True, linestyle="--", alpha=0.3)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# Create legend with only the plotted experiment labels (excluding Experiment 1's dashed line)
legend_labels = []
legend_handles = []
for i, exp_id in enumerate(experiments_to_plot):
    if exp_id != 1:  # Exclude Experiment 1 from legend
        legend_labels.append(exp_labels[i])
        # Create a handle for the legend with the correct color and marker
        line = plt.Line2D(
            [],
            [],
            color=colors[i % len(colors)],
            marker=markers[i % len(markers)],
            linewidth=2.2,
            markersize=6,
            markeredgecolor="white",
            markeredgewidth=1,
            alpha=0.8,
            label=exp_labels[i],
        )
        legend_handles.append(line)

fig.legend(
    handles=legend_handles,
    labels=legend_labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.05),
    ncol=3,
    fontsize=12,
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)  # Make space for the bottom legend
plt.savefig("figures/swallow-code-v2/humaneval.png", bbox_inches="tight", dpi=300)
