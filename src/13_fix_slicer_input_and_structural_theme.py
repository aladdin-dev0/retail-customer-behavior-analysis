"""
13_fix_slicer_input_and_structural_theme.py
-------------------------------------------
Fixes the bottom-left percentage box visibility and structural theme colors:
  1. Sets root structural colors in Fluent2-CY26SU09.json:
     - firstLevelElements: #F8FAFC (fixes invisible text inside slicer input box & donut center)
     - secondLevelElements: #94A3B8 (clean input outlines)
     - thirdLevelElements: #334155
     - fourthLevelElements: #1E293B
     - secondaryBackground: #0F172A (dark clean input box background)
  2. Updates visualStyles.slicer items & slider in the theme.
  3. Updates slicer_female_adoption_rate/visual.json objects:
     - replaces 'input' with official 'items' object (fontColor: #F8FAFC, background: #0F172A)
  4. Updates chart_fulfillment_channel/visual.json to render center total in white #F8FAFC.
  5. Syncs everything to scratch repo.
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

    # 1. Structural color classes (ensures all input boxes & default text are bright and readable)
    theme["firstLevelElements"] = "#F8FAFC"
    theme["secondLevelElements"] = "#94A3B8"
    theme["thirdLevelElements"] = "#334155"
    theme["fourthLevelElements"] = "#1E293B"
    theme["secondaryBackground"] = "#0F172A"

    # 2. Slicer visual styles
    slicer_styles = theme.setdefault("visualStyles", {}).setdefault("slicer", {}).setdefault("*", {})
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

    # 3. Donut chart center value
    donut_styles = theme.setdefault("visualStyles", {}).setdefault("donutChart", {}).setdefault("*", {})
    donut_styles["centerValue"] = [
        {
            "show": True,
            "fontColor": {"solid": {"color": "#F8FAFC"}},
            "fontSize": 14
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

    # Use standard objects supported by Power BI slicer
    v["visual"]["objects"] = {
        "header": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "false"}}}
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


def update_donut_visual(root_dir: Path):
    donut_path = root_dir / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "visuals" / "chart_fulfillment_channel" / "visual.json"
    if not donut_path.exists():
        print(f"Warning: Donut visual not found at {donut_path}")
        return

    with open(donut_path, "r", encoding="utf-8") as f:
        v = json.load(f)

    # Ensure centerValue is explicitly white in visual objects
    v["visual"]["objects"]["centerValue"] = [
        {
            "properties": {
                "show": {"expr": {"Literal": {"Value": "true"}}},
                "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                "fontSize": {"expr": {"Literal": {"Value": "14D"}}}
            }
        }
    ]

    with open(donut_path, "w", encoding="utf-8") as f:
        json.dump(v, f, indent=2)
    print(f"Updated donut visual at: {donut_path}")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated files to scratch directory...")
    src_pbi = BASE_DIR / "power_bi"
    dst_pbi = SCRATCH_DIR / "power_bi"
    if src_pbi.exists():
        shutil.copytree(src_pbi, dst_pbi, dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "13_fix_slicer_input_and_structural_theme.py", SCRATCH_DIR / "src" / "13_fix_slicer_input_and_structural_theme.py")
    print("Sync complete.")


def main():
    print("=== Fixing Slicer Percentage Box & Structural Theme Colors ===")
    update_theme(BASE_DIR)
    update_slicer_visual(BASE_DIR)
    update_donut_visual(BASE_DIR)
    sync_to_scratch()
    print("=== Successfully completed slicer and theme fixes! ===")


if __name__ == "__main__":
    main()
