import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# ---- Track Record brand palette ----
BG = "#0f1226"
CARD = "#1b1f40"
PINK = "#ff5da2"
CYAN = "#5ad1e6"
YELLOW = "#ffd166"
TEXT = "#f4f4fb"
MUTED = "#a6acd6"

plt.rcParams["figure.facecolor"] = BG
plt.rcParams["axes.facecolor"] = CARD
plt.rcParams["savefig.facecolor"] = BG
plt.rcParams["text.color"] = TEXT
plt.rcParams["axes.edgecolor"] = MUTED
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = MUTED
plt.rcParams["ytick.color"] = MUTED
plt.rcParams["font.family"] = "DejaVu Sans"

# ---- Load data ----
comp = pd.read_csv("../data/post07_tiny_desk_comparison.csv")
growth = pd.read_csv("../data/post07_ca7riel_growth_timeline.csv")

comp = comp.sort_values("views_millions", ascending=True).reset_index(drop=True)

n_latin = (comp["is_latin"] == "Yes").sum()
n_total = len(comp)
print(f"Latin artists in sample: {n_latin}/{n_total} = {n_latin/n_total:.1%}")

ca7riel_rank_in_sample = (comp["views_millions"] > 51.0).sum() + 1
print(f"Ca7riel & Paco Amoroso rank within this 20-video sample: #{ca7riel_rank_in_sample} of {n_total}")

# Growth rate stats
growth["days_since_release"] = growth["days_since_release"].astype(float)
first = growth.iloc[0]
last = growth.iloc[-1]
avg_daily_views_first5 = first["views_millions"] * 1_000_000 / first["days_since_release"]
avg_daily_views_to_now = last["views_millions"] * 1_000_000 / last["days_since_release"]
print(f"Avg views/day in first 5 days: {avg_daily_views_first5:,.0f}")
print(f"Avg views/day across full {last['days_since_release']:.0f}-day span: {avg_daily_views_to_now:,.0f}")

# ---- Figure ----
fig = plt.figure(figsize=(13, 13.8))
gs = fig.add_gridspec(2, 1, height_ratios=[1.35, 1], hspace=0.5, top=0.88, bottom=0.05)

# --- Panel A: ranked comparison bar chart ---
ax1 = fig.add_subplot(gs[0])
colors = []
for _, row in comp.iterrows():
    if row["artist"] == "Ca7riel & Paco Amoroso":
        colors.append(PINK)
    elif row["is_latin"] == "Yes":
        colors.append(YELLOW)
    else:
        colors.append(CYAN)

bars = ax1.barh(comp["artist"], comp["views_millions"], color=colors, height=0.62, zorder=3)

for bar, val in zip(bars, comp["views_millions"]):
    ax1.text(val + 1.5, bar.get_y() + bar.get_height() / 2, f"{val:.1f}M",
              va="center", ha="left", fontsize=9.5, color=TEXT)

ax1.set_xlabel("YouTube views (millions) — each figure individually sourced, see dataset notes", fontsize=10, color=MUTED)
ax1.set_title("Ca7riel & Paco Amoroso vs. 19 other landmark Tiny Desk Concerts\n"
               "A 17-minute set in Spanish is now one of the most-watched Tiny Desks ever recorded",
               fontsize=14, color=TEXT, fontweight="bold", loc="left", pad=16, linespacing=1.6)

ax1.set_xlim(0, 145)
ax1.grid(axis="x", color=MUTED, alpha=0.15, zorder=0)
ax1.spines[["top", "right"]].set_visible(False)
ax1.tick_params(axis="y", labelsize=9.5)

from matplotlib.patches import Patch
legend_elems = [
    Patch(facecolor=PINK, label="Ca7riel & Paco Amoroso (this post's focus)"),
    Patch(facecolor=YELLOW, label="Other Latin-market artist"),
    Patch(facecolor=CYAN, label="Other artist"),
]
ax1.legend(handles=legend_elems, loc="lower right", frameon=False, fontsize=9, labelcolor=TEXT)

# --- Panel B: growth trajectory ---
ax2 = fig.add_subplot(gs[1])
ax2.plot(growth["days_since_release"], growth["views_millions"], color=PINK, linewidth=2.5,
          marker="o", markersize=7, markerfacecolor=YELLOW, markeredgecolor=PINK, zorder=3)

for _, row in growth.iterrows():
    label = f"{row['views_millions']:.1f}M"
    offset = 6 if row["views_millions"] < 45 else -14
    ax2.annotate(label, (row["days_since_release"], row["views_millions"]),
                 textcoords="offset points", xytext=(0, 10), fontsize=9, color=TEXT, ha="center")

ax2.set_xlabel("Days since Tiny Desk release (Oct 4, 2024)", fontsize=10, color=MUTED)
ax2.set_ylabel("Cumulative YouTube views (millions)", fontsize=10, color=MUTED)
ax2.set_title("How the view count actually climbed\n"
              "Milestones pulled from press coverage at each point in time — a real (if bumpy) curve, not a smooth model",
              fontsize=13, color=TEXT, fontweight="bold", loc="left", pad=14, linespacing=1.7)
ax2.grid(color=MUTED, alpha=0.15, zorder=0)
ax2.spines[["top", "right"]].set_visible(False)
ax2.set_ylim(0, 58)

fig.suptitle("Track Record", x=0.02, y=0.985, ha="left", fontsize=13, color=TEXT, fontweight="bold")

plt.savefig("../assets/post07_ca7riel_tiny_desk.png", dpi=180, bbox_inches="tight")
print("Saved ../assets/post07_ca7riel_tiny_desk.png")
