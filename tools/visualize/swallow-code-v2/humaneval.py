import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
exp_labels = [
    "SwallowCode-v1",
    "1-stage (High Quality)",
    "1-stage (Medium Quality)",
    "2-stage (Medium Quality)",
    "1-stage (2507-Instruct medium)",
]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b", "#e377c2"]
markers = ["o", "s", "^", "d", "P", "*"]

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300, facecolor="white")

# Plot HumanEval
for i, exp_data in enumerate(experiments_data):
    tokens = training_tokens_15
    ax1.plot(
        tokens,
        exp_data["humaneval"],
        marker=markers[i],
        linewidth=2.2,
        linestyle="-",
        color=colors[i],
        label=exp_labels[i],
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
for i, exp_data in enumerate(experiments_data):
    tokens = training_tokens_15
    ax2.plot(
        tokens,
        exp_data["humaneval_plus"],
        marker=markers[i],
        linewidth=2.2,
        linestyle="-",
        color=colors[i],
        label=exp_labels[i],
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

fig.legend(
    exp_labels, loc="lower center", bbox_to_anchor=(0.5, -0.05), ncol=3, fontsize=12
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.15)  # Make space for the bottom legend

plt.savefig("figures/swallow-code-v2/humaneval.png", bbox_inches="tight", dpi=300)
