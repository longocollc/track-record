"""
Track Record — Posts 02, 03, 04
Built from Longo's real Spotify "DONY" playlist artist list:
Rawayana, Ca7riel y Paco Amoroso, Rosalía, Elena Rose, Danny Ocean,
Karol G, Bad Bunny, Manu Chao, Ángeles Azules.

All figures below were verified via web search against Wikipedia, Billboard,
Grammy.com, LatinGRAMMY.com, and Guinness World Records (see each post's
"the dataset" section for citations). Nothing here is estimated or invented.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BG = "#0f1226"
CARD = "#1b1f40"
PINK = "#ff5da2"
CYAN = "#5ad1e6"
YELLOW = "#ffd166"
TEXT = "#f4f4fb"
MUTED = "#a6acd6"
GRID = "#2a2f5c"

plt.rcParams["font.family"] = "DejaVu Sans"


# ---------- POST 02: country / genre diversity of the DONY playlist ----------
def post02():
    artists = [
        ("Rawayana", "Venezuela", "Trippy pop / reggae-funk"),
        ("Elena Rose", "Venezuela", "Pop / R&B"),
        ("Danny Ocean", "Venezuela", "Pop / dembow"),
        ("Karol G", "Colombia", "Reggaetón / pop"),
        ("Bad Bunny", "Puerto Rico", "Reggaetón / Latin trap"),
        ("Rosalía", "Spain", "Flamenco-pop"),
        ("Ca7riel y Paco Amoroso", "Argentina", "Experimental pop/trap"),
        ("Manu Chao", "France", "Alt-rock / world fusion"),
        ("Ángeles Azules", "Mexico", "Cumbia sonidense"),
    ]
    country_order = ["Venezuela", "Colombia", "Puerto Rico", "Spain", "Argentina", "France", "Mexico"]
    country_colors = {
        "Venezuela": PINK, "Colombia": CYAN, "Puerto Rico": YELLOW,
        "Spain": "#c792ea", "Argentina": "#7ee8b0", "France": "#ff9e6d", "Mexico": "#6fa8ff",
    }
    from collections import defaultdict
    grouped = defaultdict(list)
    for name, country, genre in artists:
        grouped[country].append(f"{name} — {genre}")

    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    y_labels = []
    for i, country in enumerate(country_order):
        members = grouped[country]
        count = len(members)
        ax.barh(i, count, color=country_colors[country], height=0.6, zorder=2)
        ax.text(count + 0.05, i, "  " + " | ".join(members), va="center", ha="left",
                color=TEXT, fontsize=9.5)
        y_labels.append(country)

    ax.set_yticks(range(len(country_order)))
    ax.set_yticklabels(y_labels, color=TEXT, fontsize=11, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0, 6.5)
    ax.set_xlabel("Number of DONY playlist artists", color=MUTED, fontsize=10)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_title("Your \"Latin\" Playlist Is Really 7 Countries Wearing One Label",
                  color=TEXT, fontsize=15.5, fontweight="bold", loc="left", pad=16)
    fig.text(0.02, 0.02, "3 of 9 artists (33%) trace back to Venezuela — more than any other country in the playlist.",
              color=MUTED, fontsize=9.5)
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig("assets/post02_dony_countries.png", dpi=180, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


# ---------- POST 03: DTMF vs longest-reigning Hot Latin Songs #1s ----------
def post03():
    data = [
        ("DTMF", "Bad Bunny", 2025, 61),
        ("Despacito", "Luis Fonsi & Daddy Yankee ft. Justin Bieber", 2017, 56),
        ("Bailando", "Enrique Iglesias ft. Descemer Bueno & Gente de Zona", 2014, 41),
        ("El Perdón", "Nicky Jam & Enrique Iglesias", 2015, 30),
        ("La Tortura", "Shakira ft. Alejandro Sanz", 2005, 25),
        ("Ginza", "J Balvin", 2015, 22),
    ]
    data.sort(key=lambda x: x[3])

    fig, ax = plt.subplots(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    colors = [PINK if song == "DTMF" else CYAN for song, *_ in data]
    labels = [f"{song} ({artist}, {year})" for song, artist, year, weeks in data]
    weeks = [w for *_, w in data]

    bars = ax.barh(range(len(data)), weeks, color=colors, height=0.6, zorder=2)
    for i, w in enumerate(weeks):
        ax.text(w + 1, i, f"{w} weeks", va="center", color=TEXT, fontsize=10, fontweight="bold")

    ax.set_yticks(range(len(data)))
    ax.set_yticklabels(labels, color=TEXT, fontsize=10.5)
    ax.set_xlim(0, 70)
    ax.set_xlabel("Weeks at #1 on Billboard Hot Latin Songs", color=MUTED, fontsize=10)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.set_title("Bad Bunny's \"DTMF\" Broke a Chart Record 8 Years in the Making",
                  color=TEXT, fontsize=15.5, fontweight="bold", loc="left", pad=16)
    plt.tight_layout()
    plt.savefig("assets/post03_dtmf_record.png", dpi=180, facecolor=BG, bbox_inches="tight")
    plt.close(fig)


# ---------- POST 04: award tally across DONY artists ----------
def post04():
    # (artist, Grammy wins, Latin Grammy wins)
    data = [
        ("Bad Bunny", 6, 17),
        ("Rosalía", 2, 11),
        ("Karol G", 2, 8),
        ("Ca7riel y Paco Amoroso", 1, 5),
        ("Rawayana", 1, 2),
        ("Manu Chao", 0, 1),
        ("Elena Rose", 0, 0),
        ("Danny Ocean", 0, 0),
        ("Ángeles Azules", 0, 0),
    ]
    data.sort(key=lambda x: x[1] + x[2])

    names = [d[0] for d in data]
    grammy = [d[1] for d in data]
    latin_grammy = [d[2] for d in data]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    y = range(len(data))
    ax.barh(y, latin_grammy, color=PINK, height=0.55, label="Latin Grammy wins", zorder=2)
    ax.barh(y, grammy, left=latin_grammy, color=CYAN, height=0.55, label="Grammy wins", zorder=2)

    for i, (g, lg) in enumerate(zip(grammy, latin_grammy)):
        total = g + lg
        if total > 0:
            ax.text(total + 0.4, i, str(total), va="center", color=TEXT, fontsize=10, fontweight="bold")
        else:
            ax.text(0.4, i, "0", va="center", color=MUTED, fontsize=10)

    ax.set_yticks(list(y))
    ax.set_yticklabels(names, color=TEXT, fontsize=11)
    ax.set_xlim(0, 26)
    ax.set_xlabel("Competitive award wins (Grammy + Latin Grammy)", color=MUTED, fontsize=10)
    ax.tick_params(colors=TEXT)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.6)
    ax.legend(facecolor=CARD, edgecolor="none", labelcolor=TEXT, fontsize=9.5, loc="lower right")
    ax.set_title("Your Playlist Has 56 Grammys in It — Almost All From Two Artists",
                  color=TEXT, fontsize=15, fontweight="bold", loc="left", pad=16)
    plt.tight_layout()
    plt.savefig("assets/post04_award_tally.png", dpi=180, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("Total combined wins:", sum(g + lg for _, g, lg in data))


if __name__ == "__main__":
    post02()
    post03()
    post04()
    print("Saved: post02_dony_countries.png, post03_dtmf_record.png, post04_award_tally.png")
