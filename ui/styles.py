# ==========================================================
# Mentor AI Style System
# Theme: Dracula
#
# UI Philosophy
# ----------------------------------------------------------

from ui.colors import *
from ui.fonts import *
from ui.sizes import *

# ----------------------------
# Primary Button
# ----------------------------

PRIMARY_BUTTON = {
    "bg": PRIMARY,
    "fg": BUTTON_TEXT,
    "font": BUTTON_FONT,
    "activebackground": PRIMARY_HOVER,
    "activeforeground": BUTTON_TEXT,
    "borderwidth": 0,
    "cursor": "hand2"
}

# ----------------------------
# Mode Button
# ----------------------------

MODE_BUTTON = {
    "bg": PANEL_BG,
    "fg": TEXT,
    "font": BUTTON_FONT,
    "activebackground": PRIMARY,
    "activeforeground": TEXT,
    "borderwidth": 0,
    "cursor": "hand2"
}

# ----------------------------
# File Button
# ----------------------------

FILE_BUTTON = {
    "bg": PANEL_BG,
    "fg": TEXT,
    "font": BUTTON_FONT,
    "borderwidth": 0,
    "cursor": "hand2"
}

# ----------------------------
# Settings Button
# ----------------------------

SETTINGS_BUTTON = {
    "bg": PANEL_BG,
    "fg": TEXT,
    "font": BUTTON_FONT,
    "borderwidth": 0,
    "cursor": "hand2"
}

# ----------------------------
# AI Input
# ----------------------------

AI_INPUT = {
    "bg": AI_INPUT_BG,
    "fg": TEXT,
    "font": INPUT_FONT,
    "insertbackground": EDITOR_CURSOR,
    "selectbackground": EDITOR_SELECTION,
    "borderwidth": 1,
    "highlightthickness": 1,
    "highlightbackground": BORDER
}

# ----------------------------
# Code Editor
# ----------------------------

CODE_EDITOR = {
    "bg": EDITOR_BG,
    "fg": TEXT,
    "font": CODE_FONT,
    "insertbackground": EDITOR_CURSOR,
    "selectbackground": EDITOR_SELECTION,
    "borderwidth": 0
}

# ----------------------------
# Labels
# ----------------------------

TITLE_LABEL = {
    "bg": PANEL_BG,
    "fg": TEXT,
    "font": TITLE_FONT
}

BODY_LABEL = {
    "bg": PANEL_BG,
    "fg": TEXT,
    "font": BODY_FONT
}