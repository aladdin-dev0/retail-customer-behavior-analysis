"""
14_fix_slicer_data_font_color.py
--------------------------------
Fixes the slicer numeric input box text visibility:
In Power BI PBIR, the slicer values formatting object is 'data' (not 'input' or 'items').
This script:
  1. Injects 'data', 'items', and 'values' with fontColor: #F8FAFC into Fluent2-CY26SU09.json.
  2. Updates slicer_female_adoption_rate/visual.json objects:
     - Sets 'data' with fontColor: #F8FAFC, background: #0F172A, textSize: 11D
     - Sets 'items' with fontColor: #F8FAFC, background: #0F172A, textSize: 11D
     - Sets 'values' with fontColor: #F8FAFC, background: #0F172A, fontSize: 11D
     - Sets 'slider' with color: #38BDF8
     - Sets 'header' show: false
  3. Syncs to scratch repository.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\BAH\Desktop\data01\retail-customer-behavior-analysis")
SCRATCH_DIR = Path(r"C:\Users\BAH\.gemini\antigravity\scratch\retail-customer-behavior-analysis")
PAGE_GUID = "e2d88bab65d02ef79d4f"


def update_theme(root_dir: Path):
    theme_path = root_dir / "power_bi" / "powerbi report.Report" / "StaticResources" / "SharedResources" / "BaseThemes" / "Fluent2-CY26SU09.json"
    if not theme_path.exists():
        print(f"Warning: Theme not found at {theme_path}")
        return

    with open(theme_path, "r", encoding="utf-8") as f:
        theme = json.load(f)

    # Root structural classes
    theme["firstLevelElements"] = "#F8FAFC"
    theme["secondLevelElements"] = "#94A3B8"
    theme["thirdLevelElements"] = "#334155"
    theme["fourthLevelElements"] = "#1E293B"
    theme["secondaryBackground"] = "#0F172A"

    slicer_styles = theme.setdefault("visualStyles", {}).setdefault("slicer", {}).setdefault("*", {})

    # 'data' is the official PBIR card for slicer values/input text
    slicer_styles["data"] = [
        {
            "fontColor": {"solid": {"color": "#F8FAFC"}},
            "background": {"solid": {"color": "#0F172A"}},
            "textSize": 11,
            "fontFamily": "Segoe UI Semibold"
        }
    ]

    slicer_styles["items"] = [
        {
            "fontColor": {"solid": {"color": "#F8FAFC"}},
            "background": {"solid": {"color": "#0F172A"}},
            "outline": "Frame",
            "textSize": 11,
            "fontFamily": "Segoe UI Semibold"
        }
    ]

    slicer_styles["slider"] = [
        {
            "color": {"solid": {"color": "#38BDF8"}}
        }
    ]

    with open(theme_path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2)
    print(f"Updated theme at: {theme_path}")


def update_slicer_visual(root_dir: Path):
    slicer_path = root_dir / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "visuals" / "slicer_female_adoption_rate" / "visual.json"
    if not slicer_path.exists():
        print(f"Warning: Slicer visual not found at {slicer_path}")
        return

    with open(slicer_path, "r", encoding="utf-8") as f:
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
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                    "background": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                    "textSize": {"expr": {"Literal": {"Value": "11D"}}}
                }
            }
        ],
        "items": [
            {
                "properties": {
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                    "background": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                    "textSize": {"expr": {"Literal": {"Value": "11D"}}}
                }
            }
        ],
        "values": [
            {
                "properties": {
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                    "background": {"solid": {"color": {"expr": {"Literal": {"Value": "'#0F172A'"}}}}},
                    "fontSize": {"expr": {"Literal": {"Value": "11D"}}}
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

    with open(slicer_path, "w", encoding="utf-8") as f:
        json.dump(v, f, indent=2)
    print(f"Updated slicer visual at: {slicer_path}")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated files to scratch directory...")
    src_pbi = BASE_DIR / "power_bi"
    dst_pbi = SCRATCH_DIR / "power_bi"
    if src_pbi.exists():
        shutil.copytree(src_pbi, dst_pbi, dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "14_fix_slicer_data_font_color.py", SCRATCH_DIR / "src" / "14_fix_slicer_data_font_color.py")
    print("Sync complete.")


def main():
    print("=== Fixing Slicer Data Font Color to White (#F8FAFC) ===")
    update_theme(BASE_DIR)
    update_slicer_visual(BASE_DIR)
    sync_to_scratch()
    print("=== Successfully completed slicer font color update! ===")


if __name__ == "__main__":
    main()
