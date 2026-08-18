"""
Track Record — Post 03 (v3, expanded + career-year comparison)
"DTMF Broke the Record — But Bad Bunny Got There Faster Than Anyone Ever Has"

Verified sources (checked via web search, cross-checked internally):
- DTMF: 71 weeks at #1 as of Aug 5, 2026, still running.
- Despacito 56wk / Bailando 41wk / El Perdon 30wk / La Tortura 25wk / Ginza 22wk:
  Billboard Hot Latin Songs chart-beat reporting.
- Enrique Iglesias's full catalog of 27 #1 hits, each individually sourced from
  Wikipedia's "List of Billboard Hot Latin Songs chart achievements and
  milestones." These 27 songs sum to exactly 189 weeks, matching Wikipedia's
  independently-stated career total for Iglesias -- internal consistency check
  passed.
- Bad Bunny's 17 #1 hits, same Wikipedia source. Song count (17) is
  independently confirmed by Billboard reporting ("17th chart-topper, breaking
  his tie with Luis Miguel"). Per-song week figures come from the same
  Wikipedia table as Iglesias's (which checked out exactly), but summing them
  (194 weeks) has NOT been independently confirmed by a news source as
  Bad Bunny's official career total -- treat that combined figure as a
  data-derived estimate, disclosed as such in the post.
"""
import pandas as pd
import matplotlib.pyplot as plt

BG = "#0f1226"
CARD = "#1b1f40"
PINK = "#ff5da2"
CYAN = "#5ad1e6"
YELLOW = "#ffd166"
TEXT = "#f4f4fb"
MUTED = "#a6acd6"
GRID = "#2a2f5c"

plt.rcParams["font.family"] = "DejaVu Sans"

records = pd.read_csv("data/post03_longest_reigning_latin_number_ones.csv").sort_values("weeks_at_number_one")
enrique = pd.read_csv("data/post03_enrique_iglesias_number_ones.csv")
bunny = pd.read_csv("data/post03_bad_bunny_number_ones.csv")

enrique["artist"] = "Enrique Iglesias"
bunny["artist"] = "Bad Bunny"
combined = pd.concat([enrique, bunny], ignore_index=True)

# --- career-relative cumulative trajectory ---
def career_trajectory(df):
    first_year = df["year"].min()
    df = df.copy()
    df["years_since_first"] = df["year"] - first_year
    by_year = df.groupby("years_since_first")["weeks_at_number_one"].sum().sort_index()
    # fill any gap years with 0 so the step line is continuous
    full_index = range(by_year.index.min(), by_year.index.max() + 1)
    by_year = by_year.reindex(full_index, fill_value=0)
    cumulative = by_year.cumsum()
    return cumulative

enrique_traj = career_trajectory(enrique)
bunny_traj = career_trajectory(bunny)

fig = plt.figure(figsize=(13, 17))
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(3, 1, height_ratios=[1, 1.3, 2.3], hspace=0.38)

# --- Panel 1: single-song record progression ---
ax1 = fig.add_subplot(gs[0])
ax1.set_facecolor(BG)
colors1 = [PINK if s == "DTMF" else CYAN for s in records["song"]]
labels1 = [f"{row.song} ({row.artist}, {row.year})" for row in records.itertuples()]
ax1.barh(range(len(records)), records["weeks_at_number_one"], color=colors1, height=0.6, zorder=2)
for i, w in enumerate(records["weeks_at_number_one"]):
    ax1.text(w + 1, i, f"{w} weeks", va="center", color=TEXT, fontsize=10, fontweight="bold")
ax1.set_yticks(range(len(records)))
ax1.set_yticklabels(labels1, color=TEXT, fontsize=9.5)
ax1.set_xlim(0, 80)
ax1.set_xlabel("Weeks at #1 (single song)", color=MUTED, fontsize=9.5)
ax1.tick_params(colors=TEXT)
for spine in ax1.spines.values():
    spine.set_visible(False)
ax1.grid(axis="x", color=GRID, linewidth=0.6)
ax1.set_title("1. The record for one song: DTMF, still climbing (71 weeks, Aug 2026)",
              color=TEXT, fontsize=12.5, fontweight="bold", loc="left", pad=10)

# --- Panel 2: career-relative cumulative trajectory ---
ax2 = fig.add_subplot(gs[1])
ax2.set_facecolor(BG)
ax2.step(bunny_traj.index, bunny_traj.values, where="post", color=PINK, linewidth=3, label="Bad Bunny (first #1: 2018)")
ax2.step(enrique_traj.index, enrique_traj.values, where="post", color=CYAN, linewidth=3, label="Enrique Iglesias (first #1: 1995)")
ax2.scatter([bunny_traj.index[-1]], [bunny_traj.values[-1]], color=PINK, s=90, zorder=3)
ax2.scatter([enrique_traj.index[-1]], [enrique_traj.values[-1]], color=CYAN, s=90, zorder=3)
ax2.annotate(f"Bad Bunny: {bunny_traj.values[-1]} weeks\nin {bunny_traj.index[-1]} years",
             (bunny_traj.index[-1], bunny_traj.values[-1]), color=PINK, fontsize=10, fontweight="bold",
             xytext=(8, -6), textcoords="offset points")
ax2.annotate(f"Enrique Iglesias: {enrique_traj.values[-1]} weeks\nin {enrique_traj.index[-1]} years",
             (enrique_traj.index[-1], enrique_traj.values[-1]), color=CYAN, fontsize=10, fontweight="bold",
             xytext=(-190, -22), textcoords="offset points")
ax2.set_ylim(0, 215)
ax2.set_xlabel("Years since each artist's first #1 hit", color=MUTED, fontsize=9.5)
ax2.set_ylabel("Cumulative weeks at #1\n(career total)", color=MUTED, fontsize=9.5)
ax2.tick_params(colors=TEXT)
for spine in ax2.spines.values():
    spine.set_visible(False)
ax2.grid(axis="y", color=GRID, linewidth=0.6)
ax2.legend(facecolor=CARD, edgecolor="none", labelcolor=TEXT, fontsize=9.5, loc="upper left")
ax2.set_title("2. The record for a career, on the same clock: cumulative weeks at #1 by years since each artist's first #1",
              color=TEXT, fontsize=12.5, fontweight="bold", loc="left", pad=10)

# --- Panel 3: every #1 song from both artists ---
ax3 = fig.add_subplot(gs[2])
ax3.set_facecolor(BG)
combined_sorted = combined.sort_values("weeks_at_number_one")
colors3 = [PINK if a == "Bad Bunny" else CYAN for a in combined_sorted["artist"]]
ax3.barh(range(len(combined_sorted)), combined_sorted["weeks_at_number_one"], color=colors3, height=0.68, zorder=2)
for i, w in enumerate(combined_sorted["weeks_at_number_one"]):
    ax3.text(w + 0.4, i, str(w), va="center", color=TEXT, fontsize=7.3)
ax3.set_yticks(range(len(combined_sorted)))
ax3.set_yticklabels(combined_sorted["song"], color=TEXT, fontsize=7.3)
ax3.set_xlim(0, 76)
ax3.set_xlabel("Weeks at #1 (this song)", color=MUTED, fontsize=9.5)
ax3.tick_params(colors=TEXT)
for spine in ax3.spines.values():
    spine.set_visible(False)
ax3.grid(axis="x", color=GRID, linewidth=0.6)
handles = [plt.Rectangle((0,0),1,1, color=PINK), plt.Rectangle((0,0),1,1, color=CYAN)]
ax3.legend(handles, ["Bad Bunny (17 songs)", "Enrique Iglesias (27 songs)"],
           facecolor=CARD, edgecolor="none", labelcolor=TEXT, fontsize=9.5, loc="lower right")
ax3.set_title("3. All 44 #1 hits between them, ranked",
              color=TEXT, fontsize=12.5, fontweight="bold", loc="left", pad=10)

fig.suptitle("DTMF Broke the Record — But Bad Bunny Got There Faster Than Anyone Ever Has",
             color=TEXT, fontsize=16.5, fontweight="bold", x=0.02, ha="left", y=0.997)

plt.savefig("assets/post03_dtmf_record.png", dpi=165, facecolor=BG, bbox_inches="tight")
plt.close(fig)

print(f"Enrique: {len(enrique)} songs, {enrique['weeks_at_number_one'].sum()} weeks, "
      f"reached {enrique_traj.values[-1]} weeks over {enrique_traj.index[-1]} years")
print(f"Bad Bunny: {len(bunny)} songs, {bunny['weeks_at_number_one'].sum()} weeks, "
      f"reached {bunny_traj.values[-1]} weeks over {bunny_traj.index[-1]} years")
print("Saved assets/post03_dtmf_record.png")
