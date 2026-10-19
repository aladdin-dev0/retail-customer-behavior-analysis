"""
17_executive_callout_for_adoption_rate.py
-----------------------------------------
Permanently solves the slicer font legibility issue by introducing an executive KPI card:
  1. Card 'card_target_adoption_rate' (x: 40, y: 540, w: 215, h: 120):
     - Displays 'Female Adoption Rate Value' in massive 30pt Bold Neon Cyan (#38BDF8).
     - Title: '🎯 TARGET ADOPTION'
     - Updates in real-time as the slider moves!
  2. Card 'card_simulated_subscribers' (x: 265, y: 540, w: 215, h: 120):
     - Displays 'Simulated Female Subscribers' in 30pt Bold Neon Cyan (#38BDF8).
     - Title: '👥 NEW SUBSCRIBERS'
     - Sits side-by-side with target adoption card.
  3. Slicer 'slicer_female_adoption_rate' (x: 40, y: 670, w: 440, h: 120):
     - Sits directly below the two KPI cards.
     - Title: '🎮 SIMULATION CONTROLLER (0% – 100%)'
     - Subtitle: 'Drag slider to model female subscriber adoption'
     - Clean wide cyan slider track.
  4. Mathematically perfect alignment matching Hero card (y: 540 to 790, total height 250px).
  5. Syncs to scratch repository.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\BAH\Desktop\data01\retail-customer-behavior-analysis")
SCRATCH_DIR = Path(r"C:\Users\BAH\.gemini\antigravity\scratch\retail-customer-behavior-analysis")
PAGE_GUID = "e2d88bab65d02ef79d4f"
VISUALS_DIR = BASE_DIR / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "visuals"


def make_container(name, x, y, width, height, z, visual_dict, title=None, subtitle=None, 
                   bg_color="#1E293B", border_color="#334155", border_width=1, border_radius=12,
                   title_color="#F8FAFC", title_size=10.5, subtitle_color="#94A3B8", subtitle_size=9):
    container = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.1.0/schema.json",
        "name": name,
        "position": {
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "width": float(width),
            "height": float(height),
            "tabOrder": float(z),
        },
        "visual": visual_dict
    }

    v_objs = {
        "background": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{bg_color}'"}}}}},
                    "transparency": {"expr": {"Literal": {"Value": "0D"}}}
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{border_color}'"}}}}},
                    "radius": {"expr": {"Literal": {"Value": f"{border_radius}D"}}},
                    "width": {"expr": {"Literal": {"Value": f"{border_width}D"}}}
                }
            }
        ],
        "dropShadow": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "preset": {"expr": {"Literal": {"Value": "'BottomRight'"}}}
                }
            }
        ],
        "visualHeader": [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "false"}}}
                }
            }
        ]
    }

    if title:
        v_objs["title"] = [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                    "fontSize": {"expr": {"Literal": {"Value": f"{title_size}D"}}},
                    "bold": {"expr": {"Literal": {"Value": "true"}}},
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{title_color}'"}}}}}
                }
            }
        ]
    if subtitle:
        v_objs["subTitle"] = [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{subtitle}'"}}},
                    "fontSize": {"expr": {"Literal": {"Value": f"{subtitle_size}D"}}},
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{subtitle_color}'"}}}}}
                }
            }
        ]

    container["visual"]["visualContainerObjects"] = v_objs
    return container


def make_card_visual(entity, measure_name, font_size=30, font_color="#38BDF8"):
    return {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": entity}},
                                    "Property": measure_name,
                                }
                            },
                            "queryRef": f"{entity}.{measure_name}",
                            "nativeQueryRef": measure_name,
                        }
                    ]
                }
            }
        },
        "objects": {
            "categoryLabels": [
                {"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}
            ],
            "labels": [
                {
                    "properties": {
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": f"'{font_color}'"
                                        }
                                    }
                                }
                            }
                        },
                        "fontSize": {
                            "expr": {
                                "Literal": {
                                    "Value": f"{font_size}D"
                                }
                            }
                        }
                    }
                }
            ]
        }
    }


def update_column1_visuals():
    # 1. Card: Target Adoption Rate (x: 40, y: 540, w: 215, h: 120)
    card_adoption = make_card_visual(
        entity="Female Subscription Adoption Rate",
        measure_name="Female Adoption Rate Value",
        font_size=30,
        font_color="#38BDF8"
    )
    container_adoption = make_container(
        name="Card_Target_Adoption_Rate",
        x=40, y=540, width=215, height=120, z=7200,
        visual_dict=card_adoption,
        title="🎯 TARGET ADOPTION",
        title_color="#38BDF8",
        border_color="#38BDF8",
        border_width=1.5,
        title_size=10
    )
    dir_adoption = VISUALS_DIR / "card_target_adoption_rate"
    dir_adoption.mkdir(parents=True, exist_ok=True)
    with open(dir_adoption / "visual.json", "w", encoding="utf-8") as f:
        json.dump(container_adoption, f, indent=2)
    print("Created: card_target_adoption_rate/visual.json")

    # 2. Card: Simulated Subscribers (x: 265, y: 540, w: 215, h: 120)
    card_subs = make_card_visual(
        entity="_Measures",
        measure_name="Simulated Female Subscribers",
        font_size=30,
        font_color="#38BDF8"
    )
    container_subs = make_container(
        name="Card_Simulated_Subscribers",
        x=265, y=540, width=215, height=120, z=7500,
        visual_dict=card_subs,
        title="👥 NEW SUBSCRIBERS",
        title_color="#38BDF8",
        border_color="#38BDF8",
        border_width=1.5,
        title_size=10
    )
    dir_subs = VISUALS_DIR / "card_simulated_subscribers"
    dir_subs.mkdir(parents=True, exist_ok=True)
    with open(dir_subs / "visual.json", "w", encoding="utf-8") as f:
        json.dump(container_subs, f, indent=2)
    print("Updated: card_simulated_subscribers/visual.json")

    # 3. Slicer: Simulation Lever (x: 40, y: 670, w: 440, h: 120)
    slicer_visual = {
        "visualType": "slicer",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {"Entity": "Female Subscription Adoption Rate"}
                                    },
                                    "Property": "Female Subscription Adoption Rate",
                                }
                            },
                            "queryRef": "Female Subscription Adoption Rate.Female Subscription Adoption Rate",
                            "nativeQueryRef": "Female Subscription Adoption Rate",
                        }
                    ]
                }
            }
        },
        "objects": {
            "header": [
                {
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "false"}}}
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
    }
    container_slicer = make_container(
        name="Slicer_Female_Adoption_Rate",
        x=40, y=670, width=440, height=120, z=7000,
        visual_dict=slicer_visual,
        title="🎮 SIMULATION CONTROLLER (0.0% – 100.0%)",
        subtitle="Drag slider knob to simulate female adoption rate",
        bg_color="#0F172A",
        border_color="#334155",
        title_size=10.5,
        subtitle_color="#38BDF8",
        subtitle_size=9
    )
    dir_slicer = VISUALS_DIR / "slicer_female_adoption_rate"
    dir_slicer.mkdir(parents=True, exist_ok=True)
    with open(dir_slicer / "visual.json", "w", encoding="utf-8") as f:
        json.dump(container_slicer, f, indent=2)
    print("Updated: slicer_female_adoption_rate/visual.json")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated files to scratch directory...")
    shutil.copytree(BASE_DIR / "power_bi", SCRATCH_DIR / "power_bi", dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "17_executive_callout_for_adoption_rate.py", SCRATCH_DIR / "src" / "17_executive_callout_for_adoption_rate.py")
    print("Sync complete.")


def main():
    print("=== Deploying Executive Callout Metric for Target Adoption Rate ===")
    update_column1_visuals()
    sync_to_scratch()
    print("=== Successfully completed callout deployment! ===")


if __name__ == "__main__":
    main()
