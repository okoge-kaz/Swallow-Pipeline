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

# Experiment data for GSM-Plus and BBH
experiments_data = [
    {  # SwallowMath
        "id": 1,
        "gsm_plus": [
            0.4124,
            0.4431,
            0.4372,
            0.4475,
            0.4587,
            0.4736,
            0.4742,
            0.4743,
            0.4940,
            0.4896,
            0.5001,
            0.5047,
            0.5055,
            0.5133,
            0.5145,
        ],
        "bbh": [
            0.6515,
            0.6460,
            0.6372,
            0.6669,
            0.6557,
            0.6716,
            0.6703,
            0.6727,
            0.6727,
            0.6733,
            0.6784,
            0.6769,
            0.6729,
            0.6847,
            0.6813,
        ],
    },
    {  # Finemath-3+
        "id": 2,
        "gsm_plus": [
            0.3232,
            0.3106,
            0.3186,
            0.3345,
            0.3380,
            0.3555,
            0.3570,
            0.3740,
            0.3786,
            0.3741,
            0.3641,
            0.3723,
            0.3813,
            0.3826,
            0.3785,
        ],
        "bbh": [
            0.6173,
            0.6096,
            0.6205,
            0.6143,
            0.6099,
            0.6312,
            0.6080,
            0.6279,
            0.6208,
            0.6335,
            0.6358,
            0.6314,
            0.6429,
            0.6428,
            0.6406,
        ],
    },
    {  # text
        "id": 3,
        "gsm_plus": [
            0.3398,
            0.3619,
            0.3677,
            0.3724,
            0.3819,
            0.4143,
            0.4065,
            0.4169,
            0.4210,
            0.4063,
            0.4184,
            0.4318,
            0.4313,
            0.4459,
            0.4425,
        ],
        "bbh": [
            0.6382,
            0.6216,
            0.6288,
            0.6282,
            0.6414,
            0.6469,
            0.6472,
            0.6534,
            0.6537,
            0.6607,
            0.6598,
            0.6555,
            0.6640,
            0.6742,
            0.6704,
        ],
    },
    {  # textbook
        "id": 4,
        "gsm_plus": [
            0.3546,
            0.3519,
            0.3672,
            0.3803,
            0.4079,
            0.4190,
            0.4170,
            0.4293,
            0.4249,
            0.4303,
            0.4402,
            0.4523,
            0.4470,
            0.4597,
            0.4587,
        ],
        "bbh": [
            0.6676,
            0.6518,
            0.6696,
            0.6612,
            0.6601,
            0.6790,
            0.6649,
            0.6838,
            0.6871,
            0.6835,
            0.6901,
            0.6876,
            0.6962,
            0.6901,
            0.6970,
        ],
    },
    {  # QA
        "id": 5,
        "gsm_plus": [
            0.3710,
            0.3872,
            0.3851,
            0.3881,
            0.4038,
            0.4233,
            0.4282,
            0.4526,
            0.4404,
            0.4445,
            0.4454,
            0.4526,
            0.4562,
            0.4643,
            0.4622,
        ],
        "bbh": [
            0.6494,
            0.6385,
            0.6397,
            0.6355,
            0.6460,
            0.6633,
            0.6523,
            0.6772,
            0.6848,
            0.6781,
            0.6851,
            0.6804,
            0.6789,
            0.6891,
            0.6887,
        ],
    },
    {  # Socratic
        "id": 6,
        "gsm_plus": [
            0.3543,
            0.3524,
            0.3759,
            0.3744,
            0.3948,
            0.4000,
            0.3943,
            0.4152,
            0.4160,
            0.4167,
            0.4204,
            0.4158,
            0.4199,
            0.4273,
            0.4252,
        ],
        "bbh": [
            0.6448,
            0.6415,
            0.6577,
            0.6514,
            0.6627,
            0.6835,
            0.6767,
            0.6899,
            0.6781,
            0.6901,
            0.6881,
            0.6848,
            0.6890,
            0.6893,
            0.6928,
        ],
    },
    {  # Multiple solution
        "id": 7,
        "gsm_plus": [
            0.3478,
            0.3439,
            0.3630,
            0.3746,
            0.3841,
            0.3971,
            0.4000,
            0.4189,
            0.4074,
            0.4074,
            0.4139,
            0.4225,
            0.4238,
            0.4302,
            0.4339,
        ],
        "bbh": [
            0.6546,
            0.6395,
            0.6515,
            0.6478,
            0.6452,
            0.6696,
            0.6544,
            0.6590,
            0.6719,
            0.6672,
            0.6782,
            0.6667,
            0.6778,
            0.6819,
            0.6816,
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
    "SwallowMath",
    "Finemath-3+",
    "text",
    "textbook",
    "QA",
    "Socratic",
    "Multiple solution",
]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"]
markers = ["o", "s", "^", "d", "v", "P", "*"]

# Create figure with subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), dpi=300, facecolor="white")

# Plot GSM-Plus
for i, exp_data in enumerate(experiments_data):
    tokens = training_tokens_15
    ax1.plot(
        tokens,
        exp_data["gsm_plus"],
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
ax1.set_title("GSM-Plus", fontsize=16, fontweight="bold")
ax1.grid(True, linestyle="--", alpha=0.3)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# Plot BBH
for i, exp_data in enumerate(experiments_data):
    tokens = training_tokens_15
    ax2.plot(
        tokens,
        exp_data["bbh"],
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
ax2.set_title("BBH", fontsize=16, fontweight="bold")
ax2.grid(True, linestyle="--", alpha=0.3)
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

fig.legend(
    exp_labels, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=4, fontsize=12
)

plt.tight_layout()
plt.subplots_adjust(bottom=0.10)

plt.savefig("figures/swallow-math-v2/gsm_plus_bbh.png", bbox_inches="tight", dpi=300)
plt.show()
