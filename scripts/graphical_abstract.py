#!/usr/bin/env python3
"""
graphical_abstract.py -- build the graphical abstract.

One 960-sample official test run, the injection instant at 161, the two
labeling conventions laid over it, and the macro-F1 each one yields for the
same frozen model. Elsevier asks for a single image, minimum 531 x 1328 px,
readable at 200 x 500 px.

    python3 scripts/graphical_abstract.py --out article/figures/graphical_abstract.pdf
"""
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ap = argparse.ArgumentParser()
ap.add_argument("--out", default="graphical_abstract.pdf")
args = ap.parse_args()

NORMAL = "#8FA8BF"     # pre-onset segment: nominal operation
FAULT = "#1F4E68"      # post-onset segment: fault present
WRONG = "#C4553B"      # scored against the fault label though nominal
TEXT = "#22303A"

fig, ax = plt.subplots(figsize=(13.28, 5.31), dpi=100)
ax.set_xlim(0, 1000)
ax.set_ylim(0, 100)
ax.axis("off")

# ---------------------------------------------------------------- the run ---
ax.text(20, 92, "One official test run: 960 samples, fault injected at sample 161",
        fontsize=17, color=TEXT, weight="bold")

x0, w = 78, 640
onset = x0 + w * 160 / 960

# plant state
ax.add_patch(Rectangle((x0, 70), onset - x0, 9, facecolor=NORMAL, edgecolor="none"))
ax.add_patch(Rectangle((onset, 70), x0 + w - onset, 9, facecolor=FAULT, edgecolor="none"))
ax.text(x0 - 8, 74.5, "plant\nstate", fontsize=13, color=TEXT, ha="right", va="center")
ax.text((x0 + onset) / 2, 74.5, "nominal", fontsize=12, color="white",
        ha="center", va="center")
ax.text((onset + x0 + w) / 2, 74.5, "fault present", fontsize=12, color="white",
        ha="center", va="center")

ax.plot([onset, onset], [55, 86], color=TEXT, lw=1.6, ls="--")
ax.text(onset, 88, "injection", fontsize=12, color=TEXT, ha="center")

# literal labelling
ax.add_patch(Rectangle((x0, 48), onset - x0, 9, facecolor=WRONG, edgecolor="none"))
ax.add_patch(Rectangle((onset, 48), x0 + w - onset, 9, facecolor=FAULT, edgecolor="none"))
ax.text(x0 - 8, 52.5, "literal\nlabels", fontsize=13, color=TEXT, ha="right", va="center")
ax.text((x0 + onset) / 2, 52.5, "scored as\nfault", fontsize=10.5, color="white",
        ha="center", va="center")
ax.text((onset + x0 + w) / 2, 52.5, "960 samples scored against the fault label",
        fontsize=12, color="white", ha="center", va="center")

# post-onset labelling
ax.add_patch(Rectangle((x0, 26), onset - x0, 9, facecolor="none",
                       edgecolor=TEXT, lw=1.2, ls=":"))
ax.add_patch(Rectangle((onset, 26), x0 + w - onset, 9, facecolor=FAULT, edgecolor="none"))
ax.text(x0 - 8, 30.5, "post-onset\nlabels", fontsize=13, color=TEXT, ha="right", va="center")
ax.text((x0 + onset) / 2, 30.5, "excluded", fontsize=10.5, color=TEXT,
        ha="center", va="center")
ax.text((onset + x0 + w) / 2, 30.5, "800 samples scored",
        fontsize=12, color="white", ha="center", va="center")

# ------------------------------------------------------------- the result ---
bx = 870
ax.text(bx, 84, "Same frozen model,\nsame predictions", fontsize=14, color=TEXT, ha="center",
        weight="bold")

ax.text(bx, 68, "0.7200", fontsize=34, color=WRONG, ha="center", weight="bold")
ax.text(bx, 62, "macro-F1", fontsize=12, color=TEXT, ha="center")

ax.annotate("", xy=(bx, 48), xytext=(bx, 58),
            arrowprops=dict(arrowstyle="-|>", color=TEXT, lw=1.6))

ax.text(bx, 34, "0.8054", fontsize=34, color=FAULT, ha="center", weight="bold")
ax.text(bx, 28, "macro-F1", fontsize=12, color=TEXT, ha="center")

# ------------------------------------------------------------ the message ---
ax.text(20, 10,
        "The recall of every fault class is capped at 800/960 = 0.8333 under "
        "literal labels. Across seven classifiers the",
        fontsize=14, color=TEXT)
ax.text(20, 3.5,
        "relative accuracy gain is 0.142-0.150, against a structural bound of "
        "0.1587: the effect is the convention, not the model.",
        fontsize=14, color=TEXT)

plt.tight_layout(pad=0.4)
fig.savefig(args.out, bbox_inches="tight", facecolor="white")
png = args.out.rsplit(".", 1)[0] + ".png"
fig.savefig(png, bbox_inches="tight", facecolor="white", dpi=120)
print("Wrote", args.out, "and", png)
