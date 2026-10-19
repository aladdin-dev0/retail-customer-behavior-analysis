"""
16_upgrade_slicer_font_bold_cyan.py
-----------------------------------
Solves the font legibility and eye-strain issue in the slicer box:
  1. Increases font size from 10/11pt to 14pt (large, clear, readable from afar).
  2. Sets font weight to Bold ('Segoe UI Bold').
  3. Uses Vibrant Neon Cyan (#38BDF8) - matches the cockpit's glowing accents
     and eliminates dark-mode halation / eye strain.
  4. Bumps theme version to ExecutiveDarkCockpit-v2.json (cache-busting).
  5. Updates slicer visual.json with fontSize: 14D, bold, and color: #38BDF8.
  6. Updates report.json and syncs to scratch.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\BAH\Desktop\data01\retail-customer-behavior-analysis")
SCRATCH_DIR = Path(r"C:\Users\BAH\.gemini\antigravity\scratch\retail-customer-behavior-analysis")
PAGE_GUID = "e2d88bab65d02ef79d4f"

THEME_NAME = "ExecutiveDarkCockpit-v2.json"


def build_and_register_theme():
    report_dir = BASE_DIR / "power_bi" / "powerbi report.Report"
    reg_dir1 = report_dir / "StaticResources" / "RegisteredResources"
    reg_dir2 = report_dir / "StaticResources" / "SharedResources" / "RegisteredResources"
    reg_dir1.mkdir(parents=True, exist_ok=True)
    reg_dir2.mkdir(parents=True, exist_ok=True)

    theme = {
        "name": "ExecutiveDarkCockpit-v2",
        "dataColors": [
            "#3B82F6", "#10B981", "#6366F1", "#F59E0B",
            "#EC4899", "#8B5CF6", "#14B8A6", "#38BDF8"
        ],
        "foreground": "#F8FAFC",
        "firstLevelElements": "#38BDF8",       # Luminous Neon Cyan for input values
        "secondLevelElements": "#38BDF8",      # Cyan borders
        "thirdLevelElements": "#1E293B",
        "fourthLevelElements": "#0F172A",
        "secondaryBackground": "#0F172A",
        "background": "#0B1120",
        "backgroundLight": "#1E293B",
        "backgroundNeutral": "#0F172A",
        "backgroundDark": "#020617",
        "tableAccent": "#38BDF8",
        "textClasses": {
            "callout": {"fontSize": 24, "fontFace": "Segoe UI Semibold", "color": "#F8FAFC"},
            "title": {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": "#F8FAFC"},
            "header": {"fontSize": 11, "fontFace": "Segoe UI Semibold", "color": "#F8FAFC"},
            "label": {"fontSize": 10, "fontFace": "Segoe UI", "color": "#94A3B8"}
        },
        "visualStyles": {
            "slicer": {
                "*": {
                    "header": [{"show": False}],
                    "data": [
                        {
                            "fontColor": {"solid": {"color": "#38BDF8"}},
                            "background": {"solid": {"color": "#0F172A"}},
                            "textSize": 14,
                            "fontSize": 14,
                            "fontFamily": "Segoe UI Bold"
                        }
                    ],
                    "items": [
                        {
                            "fontColor": {"solid": {"color": "#38BDF8"}},
                            "background": {"solid": {"color": "#0F172A"}},
                            "outline": "Frame",
                            "textSize": 14,
                            "fontSize": 14,
                            "fontFamily": "Segoe UI Bold"
                        }
                    ],
                    "values": [
                        {
                            "fontColor": {"solid": {"color": "#38BDF8"}},
                            "background": {"solid": {"color": "#0F172A"}},
                            "fontSize": 14,
                            "fontFamily": "Segoe UI Bold"
                        }
                    ],
                    "slider": [
                        {
                            "color": {"solid": {"color": "#38BDF8"}}
                        }
                    ]
                }
            },
            "donutChart": {
                "*": {
                    "centerValue": [
                        {
                            "show": True,
                            "fontColor": {"solid": {"color": "#F8FAFC"}}
                        }
                    ]
                }
            }
        }
    }

    for d in [reg_dir1, reg_dir2]:
        out_file = d / THEME_NAME
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(theme, f, indent=2)
        print(f"Created theme file: {out_file}")

    # Also update BaseThemes/Fluent2-CY26SU09.json just in case
    base_theme = report_dir / "StaticResources" / "SharedResources" / "BaseThemes" / "Fluent2-CY26SU09.json"
    if base_theme.exists():
        with open(base_theme, "r", encoding="utf-8") as f:
            bt = json.load(f)
        bt["firstLevelElements"] = "#38BDF8"
        bt["secondLevelElements"] = "#38BDF8"
        slicer_bt = bt.setdefault("visualStyles", {}).setdefault("slicer", {}).setdefault("*", {})
        slicer_bt["data"] = [{"fontColor": {"solid": {"color": "#38BDF8"}}, "textSize": 14, "fontFamily": "Segoe UI Bold"}]
        slicer_bt["items"] = [{"fontColor": {"solid": {"color": "#38BDF8"}}, "textSize": 14, "fontFamily": "Segoe UI Bold"}]
        with open(base_theme, "w", encoding="utf-8") as f:
            json.dump(bt, f, indent=2)

    # Update report.json to point to THEME_NAME
    rep_file = report_dir / "definition" / "report.json"
    with open(rep_file, "r", encoding="utf-8") as f:
        rep = json.load(f)

    rep["themeCollection"]["customTheme"] = {
        "name": THEME_NAME,
        "reportVersionAtImport": {
            "visual": "2.13.0",
            "report": "3.4.0",
            "page": "2.3.1"
        },
        "type": "RegisteredResources"
    }

    pkgs = rep.get("resourcePackages", [])
    pkgs = [p for p in pkgs if p.get("name") != "RegisteredResources"]
    pkgs.append({
        "name": "RegisteredResources",
        "type": "RegisteredResources",
        "items": [
            {
                "name": THEME_NAME,
                "path": THEME_NAME,
                "type": "CustomTheme"
            }
        ]
    })
    rep["resourcePackages"] = pkgs

    with open(rep_file, "w", encoding="utf-8") as f:
        json.dump(rep, f, indent=2)
    print(f"Updated report.json with customTheme {THEME_NAME}")


def update_slicer_visual():
    slicer_file = BASE_DIR / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "visuals" / "slicer_female_adoption_rate" / "visual.json"
    with open(slicer_file, "r", encoding="utf-8") as f:
        v = json.load(f)

    v["visual"]["objects"] = {
        "header": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "false"}}}
                }
            }
        ],
        "data": [
            {
                "properties": {
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#38BDF8'"}}}}},
                    "background": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                    "textSize": {"expr": {"Literal": {"Value": "14D"}}},
                    "fontSize": {"expr": {"Literal": {"Value": "14D"}}},
                    "bold": {"expr": {"Literal": {"Value": "true"}}}
                }
            }
        ],
        "items": [
            {
                "properties": {
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#38BDF8'"}}}}},
                    "background": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                    "textSize": {"expr": {"Literal": {"Value": "14D"}}},
                    "fontSize": {"expr": {"Literal": {"Value": "14D"}}},
                    "bold": {"expr": {"Literal": {"Value": "true"}}}
                }
            }
        ],
        "values": [
            {
                "properties": {
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#38BDF8'"}}}}},
                    "background": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                    "fontSize": {"expr": {"Literal": {"Value": "14D"}}},
                    "bold": {"expr": {"Literal": {"Value": "true"}}}
                }
            }
        ],
        "slider": [
            {
                "properties": {
                    "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#38BDF8'"}}}}}
                }
            }
        ]
    }

    with open(slicer_file, "w", encoding="utf-8") as f:
        json.dump(v, f, indent=2)
    print(f"Updated slicer visual at: {slicer_file}")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated files to scratch directory...")
    shutil.copytree(BASE_DIR / "power_bi", SCRATCH_DIR / "power_bi", dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "16_upgrade_slicer_font_bold_cyan.py", SCRATCH_DIR / "src" / "16_upgrade_slicer_font_bold_cyan.py")
    print("Sync complete.")


def main():
    print("=== Upgrading Slicer Font to Bold Neon Cyan 14pt ===")
    build_and_register_theme()
    update_slicer_visual()
    sync_to_scratch()
    print("=== Successfully completed slicer font upgrade! ===")


if __name__ == "__main__":
    main()
