#!/usr/bin/env python3
"""
Track Record — new post generator

Scaffolds a new post page from templates/post_template.html and inserts a
matching card on the homepage. This is the "semi-automated" building block:
each week, fill in a config (by hand or by having Claude draft one from a
fresh dataset), run this script, review the generated HTML, then publish
by uploading the track-record/ folder to hosting.

Usage:
    python3 scripts/new_post.py path/to/config.json

Config JSON fields:
    post_num        e.g. "02"
    slug            e.g. "valence-by-decade"        -> posts/post-02-valence-by-decade.html
    tag             e.g. "Music History"
    title           full post title
    hook            1-2 sentence opening hook (plain text, can include basic <em>/<strong>)
    img_file        filename already saved in assets/, e.g. "post02_chart.png"
    img_alt         alt text for the chart
    dataset_name    short dataset name for the byline
    dataset_desc    paragraph describing the dataset + source + license
    dataset_links   list of {"file": "data/xyz.csv", "label": "xyz.csv — description"}
    method_steps    list of strings, each an ordered-list method step
    code            code snippet shown in the post (plain text)
    findings        list of strings, each a paragraph under "What it showed"
                    (first item may instead be an HTML <table> string)
    takeaway        closing takeaway paragraph
    card_summary    1-2 sentence summary for the homepage card
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render_post(cfg):
    template = (ROOT / "templates" / "post_template.html").read_text()

    method_html = "<ol>\n" + "\n".join(f"    <li>{s}</li>" for s in cfg["method_steps"]) + "\n  </ol>"

    findings_html = "\n".join(f"  <p>{f}</p>" if not f.strip().startswith("<") else f for f in cfg["findings"])

    links_html = "<br>\n      ".join(
        f'<a href="../{l["file"]}" download>{l["label"]}</a>' for l in cfg["dataset_links"]
    )

    replacements = {
        "{{TITLE}}": cfg["title"],
        "{{TAG}}": cfg["tag"],
        "{{POST_NUM}}": cfg["post_num"],
        "{{HOOK}}": cfg["hook"],
        "{{IMG_FILE}}": cfg["img_file"],
        "{{IMG_ALT}}": cfg["img_alt"],
        "{{DATASET_NAME}}": cfg["dataset_name"],
        "{{DATASET_DESC}}": cfg["dataset_desc"],
        "{{DATASET_LINKS}}": links_html,
        "{{METHOD_STEPS}}": method_html,
        "{{CODE}}": cfg["code"],
        "{{FINDINGS}}": findings_html,
        "{{TAKEAWAY}}": cfg["takeaway"],
    }
    for k, v in replacements.items():
        template = template.replace(k, v)

    out_path = ROOT / "posts" / f"post-{cfg['post_num']}-{cfg['slug']}.html"
    out_path.write_text(template)
    return out_path


def insert_card(cfg, post_path):
    index_path = ROOT / "index.html"
    html = index_path.read_text()

    card = f'''
  <a class="card" href="posts/{post_path.name}" style="text-decoration:none;">
    <img src="assets/{cfg['img_file']}" alt="{cfg['img_alt']}">
    <div class="card-body">
      <div class="card-tag">{cfg['tag']}</div>
      <h3>{cfg['title']}</h3>
      <p>{cfg['card_summary']}</p>
      <span class="read">Read the breakdown →</span>
    </div>
  </a>
'''

    marker = '<section class="grid wrap">'
    idx = html.find(marker)
    if idx == -1:
        raise RuntimeError("Could not find grid marker in index.html")
    insert_at = idx + len(marker)
    html = html[:insert_at] + card + html[insert_at:]
    index_path.write_text(html)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 scripts/new_post.py path/to/config.json")
        sys.exit(1)

    cfg = json.loads(Path(sys.argv[1]).read_text())
    post_path = render_post(cfg)
    insert_card(cfg, post_path)
    print(f"Draft created: {post_path}")
    print(f"Card added to index.html — review both, then it's ready to publish.")


if __name__ == "__main__":
    main()
