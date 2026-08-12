"""
Track Record — Post 01
"Do Club Remixes Actually Hit Harder? A Data Check."

Dataset: TidyTuesday Spotify Songs (2020-01-21), sourced from Spotify's API,
CC0 / public domain. Full dataset (32,833 tracks):
https://github.com/rfordatascience/tidytuesday/blob/master/data/2020/2020-01-21/readme.md
This post uses a 40-track working sample pulled from three Spotify "Pop Remix" /
"Dance Pop" / "Dance Room" playlists, including several songs that appear in
both their original and remixed form — which is what makes the comparison possible.

Method:
1. Load the sample CSV.
2. Flag each track as "remix" if "Remix" appears in the track name.
3. Compare mean audio-feature values (energy, danceability, tempo, loudness)
   between original and remix versions.
4. Isolate the songs that exist in BOTH forms (true matched pairs) and chart
   the energy shift per song.
5. Plot: (a) a matched-pairs slope chart, (b) an overall group comparison.
"""

import pandas as pd
import matplotlib.pyplot as plt
import re

plt.rcParams["font.family"] = "DejaVu Sans"

df = pd.read_csv("data/spotify_songs_sample.csv")
df["is_remix"] = df["track_name"].str.contains("remix", case=False)

# --- Build a "base title" to find matched original/remix pairs ---
def base_title(name):
    name = re.sub(r"\s*-\s*.*remix.*", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*\[.*remix.*\]", "", name, flags=re.IGNORECASE)
    return name.strip()

df["base_title"] = df["track_name"].apply(base_title)

pairs = []
for (artist, base), g in df.groupby(["track_artist", "base_title"]):
    orig = g[~g["is_remix"]]
    remix = g[g["is_remix"]]
    if len(orig) >= 1 and len(remix) >= 1:
        o = orig.iloc[0]
        for _, r in remix.iterrows():
            if r["track_id"] != o["track_id"]:
                pairs.append({
                    "song": f"{base} — {artist}",
                    "remix_name": r["track_name"],
                    "orig_energy": o["energy"],
                    "remix_energy": r["energy"],
                    "delta": r["energy"] - o["energy"],
                })

pairs_df = pd.DataFrame(pairs).drop_duplicates(subset=["song", "remix_name"])
pairs_df = pairs_df.sort_values("delta")
print(pairs_df.to_string(index=False))

# --- Chart 1: matched-pairs slope chart ---
fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), gridspec_kw={"width_ratios": [1.3, 1]})
fig.patch.set_facecolor("#0f1226")
for ax in axes:
    ax.set_facecolor("#0f1226")

ax = axes[0]
colors = ["#ff5da2" if d >= 0 else "#5ad1e6" for d in pairs_df["delta"]]
y_pos = range(len(pairs_df))
for i, (_, row) in enumerate(pairs_df.iterrows()):
    ax.plot([row["orig_energy"], row["remix_energy"]], [i, i],
            color=colors[i], linewidth=2.5, alpha=0.85, zorder=1)
    ax.scatter(row["orig_energy"], i, color="#ffffff", s=60, zorder=2, edgecolor=colors[i], linewidth=2)
    ax.scatter(row["remix_energy"], i, color=colors[i], s=90, zorder=2)

ax.set_yticks(list(y_pos))
ax.set_yticklabels(pairs_df["song"], color="white", fontsize=9.5)
ax.set_xlabel("Energy (Spotify audio feature, 0–1)", color="white", fontsize=10)
ax.set_xlim(0.5, 1.0)
ax.tick_params(colors="white")
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title("Original (white) → Remix (color)\nEnergy shift, matched pairs", color="white", fontsize=12, loc="left", pad=14)
ax.grid(axis="x", color="#2a2f4f", linewidth=0.6)

# --- Chart 2: overall group comparison ---
ax2 = axes[1]
means = df.groupby("is_remix")[["energy", "danceability"]].mean()
labels = ["Original", "Remix"]
x = range(2)
width = 0.32
ax2.bar([i - width/2 for i in x], means["energy"], width, label="Energy", color="#ff5da2")
ax2.bar([i + width/2 for i in x], means["danceability"], width, label="Danceability", color="#5ad1e6")
ax2.set_xticks(list(x))
ax2.set_xticklabels(labels, color="white", fontsize=11)
ax2.set_ylim(0, 1)
ax2.tick_params(colors="white")
ax2.legend(facecolor="#0f1226", edgecolor="none", labelcolor="white", fontsize=9, loc="upper left")
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.set_title(f"All {len(df)} tracks in sample\n(n={sum(~df['is_remix'])} original, n={sum(df['is_remix'])} remix)",
              color="white", fontsize=12, loc="left", pad=14)
ax2.grid(axis="y", color="#2a2f4f", linewidth=0.6)

fig.suptitle("Do Club Remixes Actually Hit Harder?", color="white", fontsize=17, fontweight="bold", x=0.02, ha="left", y=1.02)
plt.tight_layout()
plt.savefig("assets/post01_remix_energy.png", dpi=180, facecolor=fig.get_facecolor(), bbox_inches="tight")
print("\nSaved assets/post01_remix_energy.png")

pairs_df.to_csv("data/post01_matched_pairs.csv", index=False)
