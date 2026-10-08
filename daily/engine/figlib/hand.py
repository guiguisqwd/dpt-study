#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Right distal forearm and hand, palmar view in anatomical position (palm toward the viewer, thumb on
the viewer's LEFT). Distal palmar wrist crease y = WRIST; 1 forearm cun = CUN px (so LU8 is 1 cun
and LU7 1.5 cun above the crease). Reused for LU / PC / HT distal points and the LI hand points."""
from .fig import *

WRIST, CUN = 560, 80
ARTERY = "#d9746a"   # arteries: lighter than the meridian red so the two never look alike
RAD_X, ULN_X = 380, 640


def above(cun):
    return WRIST - cun * CUN


HAND = ("M380,170 L378,500 C366,512 362,540 374,556 "                                   # radial border, styloid bump
        "C352,600 334,650 336,700 "                                                     # thenar
        "C320,742 296,786 274,822 C262,842 258,868 272,878 C288,888 304,874 314,858 "    # thumb (radial edge → tip)
        "C336,822 362,786 390,758 "                                                     # thumb web
        "C398,840 402,960 406,1050 C408,1080 418,1096 438,1096 C456,1096 466,1080 466,1050 L468,870 "  # index
        "C472,950 474,1040 478,1086 C480,1112 494,1124 510,1122 C526,1120 534,1104 534,1080 L534,872 "  # middle
        "C538,950 540,1020 544,1060 C546,1086 560,1096 572,1094 C586,1092 592,1076 592,1052 L594,880 "   # ring
        "C598,930 602,990 606,1010 C608,1032 620,1040 632,1038 C644,1036 650,1020 648,1000 "          # little
        "C646,940 646,880 644,820 L640,560 L640,170")
THENAR = "M376,580 C352,620 342,670 344,712 C360,744 384,752 404,740 C420,700 424,640 410,590 Z"


def hand_palmar_base(f, tendons=True, artery=True):
    f.path(HAND + " Z", "none", 0, "#fffaf1", rough=False)
    f.path(THENAR, "#d8c4ad", 1.2, "#f4e6d4")
    f.path("M392,758 C420,770 470,786 520,796", "#d8c4ad", 1.1, rough=False)                               # thenar crease hint
    f.path("M430,840 C490,846 560,850 640,836", "#d8c4ad", 1.1, rough=False)                               # distal palmar crease hint
    f.path("M590,860 C610,800 626,740 634,680 C640,640 640,600 636,580", "#d8c4ad", 1.2, rough=False)      # hypothenar edge
    if tendons:
        f.path(f"M396,{above(4)} L392,{WRIST - 20}", "#c6a789", 5, rough=False, op=0.8)                      # brachioradialis tendon
        f.path(f"M386,{above(2.4)} C386,{WRIST - 60} 384,{WRIST} 372,{WRIST + 40}", "#b98c64", 4, rough=False)  # APL tendon (radial margin)
        f.path(f"M462,{above(4)} C462,{WRIST - 80} 456,{WRIST + 10} 446,{WRIST + 70}", "#c6a789", 6, rough=False)   # FCR tendon
        f.path(f"M516,{above(4)} L514,{WRIST + 30}", "#d3b89c", 4, rough=False)                                 # palmaris longus
        f.path(f"M612,{above(4)} C614,{WRIST - 60} 612,{WRIST - 10} 604,{WRIST + 20}", "#c6a789", 6, rough=False)   # FCU tendon
        f.raw(f'<circle cx="604" cy="{WRIST + 26}" r="12" fill="{BONE}" stroke="{BONE_E}" stroke-width="1.4"/>')   # pisiform
        f.path(f"M500,{above(4)} L498,{WRIST + 40}", GOLD, 3, rough=False, op=0.8)                              # median nerve
        f.raw(f'<rect x="398" y="{WRIST - 105}" width="232" height="80" rx="10" fill="none" stroke="#b9ab94" stroke-width="1.4" stroke-dasharray="6 5"/>')  # pronator quadratus (deep)
    if artery:
        f.path(f"M428,{above(4.6)} C426,{WRIST - 120} 424,{WRIST - 30} 420,{WRIST + 4}", ARTERY, 2.6, rough=False)
        f.path(f"M420,{WRIST + 4} C410,{WRIST + 24} 392,{WRIST + 38} 372,{WRIST + 44}", ARTERY, 2.2, dash="5 4", rough=False)  # to the snuffbox (dorsal)
        f.path(f"M594,{above(4.6)} C592,{WRIST - 100} 590,{WRIST - 20} 588,{WRIST + 30}", ARTERY, 2.2, rough=False, op=0.7)   # ulnar artery
    f.path(HAND, INK, 2.2, rough=False)
    f.path(f"M{RAD_X - 4},{WRIST} L{ULN_X},{WRIST}", "#8f8a7e", 1.3, dash="4 4", rough=False)                    # distal palmar wrist crease
    for x, y in ((436, 1090), (506, 1116), (568, 1088), (628, 1032)):
        f.path(f"M{x - 13},{y - 34} Q{x},{y - 44} {x + 13},{y - 34}", "#c9bfae", 1, rough=False)              # fingertip pads hint
