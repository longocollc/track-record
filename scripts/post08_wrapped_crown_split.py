import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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
df = pd.read_csv("../data/post08_wrapped_top_artist_song.csv")
mau = pd.read_csv("../data/post08_spotify_mau_q4.csv")
df["crown_match"] = df["crown_match"].astype(bool)

# ---- Analysis / sanity checks ----
counts = df["top_artist"].value_counts()
print("Crown wins by artist:\n", counts)
assert counts.sum() == len(df), "Crown win counts should sum to the number of years"

trailing = 0
for _, row in df.iloc[::-1].iterrows():
    if not row["crown_match"]:
        trailing += 1
    else:
        break
print(f"Trailing streak of split crowns through {df['year'].max()}: {trailing} years")

artist_growth = df["artist_streams_billions"].iloc[-1] / df["artist_streams_billions"].iloc[0]
song_growth = df["song_streams_billions"].iloc[-1] / df["song_streams_billions"].iloc[0]
mau_growth = mau["q4_monthly_active_users_millions"].iloc[-1] / mau["q4_monthly_active_users_millions"].iloc[0]
print(f"Top-artist streams growth {df['year'].iloc[0]}->{df['year'].iloc[-1]}: {artist_growth:.2f}x")
print(f"Top-song streams growth {df['year'].iloc[0]}->{df['year'].iloc[-1]}: {song_growth:.2f}x")
print(f"Spotify Q4 MAU growth: {mau_growth:.2f}x")

# Bad Bunny's 4 wins is independently confirmed by Spotify's own 2025 Wrapped
# recap ("first artist ever to claim the top spot four times") -- cross-check note.

# ---- Figure ----
fig = plt.figure(figsize=(13, 11.5))
gs = fig.add_gridspec(3, 2, height_ratios=[1.15, 0.85, 0.85], hspace=0.55, wspace=0.32,
                       left=0.08, right=0.96, top=0.90, bottom=0.07)

ax1 = fig.add_subplot(gs[0, :])
ax2 = fig.add_subplot(gs[1, 0])
ax3 = fig.add_subplot(gs[1, 1])
ax4 = fig.add_subplot(gs[2, :])

fig.suptitle("Track Record", x=0.08, y=0.985, ha="left", fontsize=12, color=TEXT, fontweight="bold")
fig.text(0.08, 0.955, "Spotify Wrapped's Top Artist Hasn't Had the Top Song in 7 Years Straight",
          fontsize=16.5, fontweight="bold", color=TEXT, ha="left")
fig.text(0.08, 0.93, "Global Top Artist streams vs. Global Top Song streams, every Wrapped year, 2016-2025",
          fontsize=11, color=MUTED, ha="left")

# Panel 1: top artist streams by year, colored by crown match
colors1 = [CYAN if m else PINK for m in df["crown_match"]]
ax1.bar(df["year"], df["artist_streams_billions"], color=colors1, width=0.62, zorder=3)
for _, row in df.iterrows():
    ax1.text(row["year"], row["artist_streams_billions"] + 0.4, row["top_artist"],
              ha="center", va="bottom", fontsize=8.6, color=TEXT)
ax1.set_ylabel("Top artist's total streams\nthat year (billions)", color=TEXT, fontsize=9.5)
ax1.set_ylim(0, 29)
ax1.set_xticks(df["year"])
ax1.grid(axis="y", color=MUTED, alpha=0.15, zorder=0)
ax1.spines[["top", "right"]].set_visible(False)
legend_elems = [Patch(facecolor=CYAN, label="Same artist also had the #1 global song"),
                Patch(facecolor=PINK, label="A different artist had the #1 global song")]
ax1.legend(handles=legend_elems, loc="upper left", frameon=False, fontsize=8.8, labelcolor=TEXT)

# Panel 2: crown wins by artist
counts_sorted = counts.sort_values(ascending=True)
bar_colors2 = [PINK if a == "Bad Bunny" else (YELLOW if a == "Taylor Swift" else CYAN) for a in counts_sorted.index]
ax2.barh(counts_sorted.index, counts_sorted.values, color=bar_colors2, height=0.55, zorder=3)
for i, (name, val) in enumerate(counts_sorted.items()):
    ax2.text(val + 0.08, i, str(val), va="center", color=TEXT, fontsize=9.5, fontweight="bold")
ax2.set_xlim(0, 5)
ax2.set_title("Who's worn the Global Top Artist crown, 2016-2025", fontsize=10.5, color=TEXT, loc="left", pad=8)
ax2.grid(axis="x", color=MUTED, alpha=0.15, zorder=0)
ax2.spines[["top", "right"]].set_visible(False)

# Panel 3: top song streams by year (line)
ax3.plot(df["year"], df["song_streams_billions"], color=YELLOW, marker="o", linewidth=2.2, zorder=3)
for _, row in df.iterrows():
    ax3.annotate(row["top_song"], (row["year"], row["song_streams_billions"]),
                 textcoords="offset points", xytext=(0, 8), ha="center", fontsize=7.3, color=MUTED, rotation=28)
ax3.set_ylim(0.6, 2.3)
ax3.set_title("The #1 global song's streams, by year", fontsize=10.5, color=TEXT, loc="left", pad=8)
ax3.set_ylabel("Billions of streams", fontsize=9)
ax3.grid(axis="y", color=MUTED, alpha=0.15, zorder=0)
ax3.spines[["top", "right"]].set_visible(False)
ax3.set_xticks(df["year"])
ax3.tick_params(axis="x", labelsize=8.5)

# Panel 4: growth comparison, indexed to 2016 = 1.0
base_artist = df["artist_streams_billions"].iloc[0]
base_song = df["song_streams_billions"].iloc[0]
base_mau = mau["q4_monthly_active_users_millions"].iloc[0]

ax4.plot(df["year"], df["artist_streams_billions"] / base_artist, color=PINK, marker="o",
          linewidth=2.2, label="Top artist's total streams")
ax4.plot(df["year"], df["song_streams_billions"] / base_song, color=YELLOW, marker="o",
          linewidth=2.2, label="Top song's streams")
ax4.plot(mau["year"], mau["q4_monthly_active_users_millions"] / base_mau, color=CYAN, marker="o",
          linewidth=2.2, linestyle="--", label="Spotify's monthly active users (Q4)")
ax4.set_title("Growth since 2016, indexed (2016 = 1.0x)", fontsize=10.5, color=TEXT, loc="left", pad=8)
ax4.set_ylabel("Multiple of 2016 level", fontsize=9)
ax4.grid(axis="y", color=MUTED, alpha=0.15, zorder=0)
ax4.spines[["top", "right"]].set_visible(False)
ax4.set_xticks(df["year"])
ax4.legend(loc="upper left", frameon=False, fontsize=8.8, labelcolor=TEXT)

fig.text(0.08, 0.018,
          "Source: Spotify Wrapped year-end recaps (Spotify Newsroom), 2016-2025, and Spotify's quarterly MAU disclosures via investor relations. Chart: Track Record.",
          fontsize=8, color=MUTED, ha="left")

plt.savefig("../assets/post08_wrapped_crown_split.png", dpi=180, bbox_inches="tight")
print("Saved ../assets/post08_wrapped_crown_split.png")
