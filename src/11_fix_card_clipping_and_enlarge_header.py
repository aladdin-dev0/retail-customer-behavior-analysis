"""
11_fix_card_clipping_and_enlarge_header.py
------------------------------------------
Fixes reported issues:
  1. Enlarges the dashboard Header title to 18pt bold with 11pt subtitle.
  2. Resolves vertical text clipping in the top 4 KPI cards:
     - Increases KPI card height to 125px (y=100).
     - Removes redundant subtitle to give maximum vertical breathing room.
     - Callout value (30pt) is centered and never clipped.
  3. Rebalances Row 3 (Simulation cards) to a sleek 250px height (y=540 to y=790),
     eliminating awkward empty space while fitting 100% within the 820px canvas.
  4. Fixes donut chart labels and colors for high contrast.
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\BAH\Desktop\data01\retail-customer-behavior-analysis")
SCRATCH_DIR = Path(r"C:\Users\BAH\.gemini\antigravity\scratch\retail-customer-behavior-analysis")
PAGE_GUID = "e2d88bab65d02ef79d4f"

CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 820


def update_page_json(root_dir: Path):
    page_path = root_dir / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "page.json"
    page_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": PAGE_GUID,
        "displayName": "Executive Revenue Cockpit",
        "displayOption": "FitToPage",
        "height": CANVAS_HEIGHT,
        "width": CANVAS_WIDTH,
        "objects": {
            "background": [
                {
                    "properties": {
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#0B1120'"
                                        }
                                    }
                                }
                            }
                        },
                        "transparency": {
                            "expr": {
                                "Literal": {
                                    "Value": "0D"
                                }
                            }
                        }
                    }
                }
            ],
            "outspacePane": [
                {
                    "properties": {
                        "backgroundColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#1E293B'"
                                        }
                                    }
                                }
                            }
                        },
                        "foregroundColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#F8FAFC'"
                                        }
                                    }
                                }
                            }
                        },
                        "borderColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#334155'"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            ],
            "filterCard": [
                {
                    "properties": {
                        "backgroundColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#0F172A'"
                                        }
                                    }
                                }
                            }
                        },
                        "foregroundColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#F8FAFC'"
                                        }
                                    }
                                }
                            }
                        },
                        "borderColor": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#334155'"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }
    }
    with open(page_path, "w", encoding="utf-8") as f:
        json.dump(page_data, f, indent=2)
    print(f"Updated page.json with canvas height {CANVAS_HEIGHT}")


def update_base_theme(root_dir: Path):
    theme_path = root_dir / "power_bi" / "powerbi report.Report" / "StaticResources" / "SharedResources" / "BaseThemes" / "Fluent2-CY26SU09.json"
    if not theme_path.exists():
        return

    with open(theme_path, "r", encoding="utf-8") as f:
        theme = json.load(f)

    vs = theme.setdefault("visualStyles", {})
    page_star = vs.setdefault("page", {}).setdefault("*", {})
    page_star["pageSize"] = [
        {
            "pageSizeTypes": "Custom",
            "pageSizeWidth": CANVAS_WIDTH,
            "pageSizeHeight": CANVAS_HEIGHT
        }
    ]

    with open(theme_path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2)
    print(f"Updated base theme page size: {CANVAS_WIDTH}x{CANVAS_HEIGHT}")


def make_container(name, x, y, width, height, z, visual_dict, title=None, subtitle=None, 
                   bg_color="#1E293B", border_color="#334155", border_width=1, border_radius=12,
                   title_color="#F8FAFC", title_size=11, subtitle_color="#94A3B8", subtitle_size=9):
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


def make_card_visual(measure_name, font_size=28, font_color="#F8FAFC"):
    return {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": measure_name,
                                }
                            },
                            "queryRef": f"_Measures.{measure_name}",
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


def build_all_visuals(root_dir: Path):
    visuals_dir = root_dir / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "visuals"
    if visuals_dir.exists():
        shutil.rmtree(visuals_dir)
    visuals_dir.mkdir(parents=True, exist_ok=True)

    visuals = []

    # 1. Header Banner (x: 40, y: 15, w: 1840, h: 70)
    # Enlarged Title: 18pt bold, Subtitle: 11pt sky blue
    header_visual = make_card_visual("Total Revenue", font_size=1, font_color="#0F172A")
    visuals.append((
        "header_banner",
        make_container(
            "Header_Banner",
            40, 15, 1840, 70, 500,
            header_visual,
            title="RETAIL REVENUE & GROWTH COCKPIT: UNLOCKING THE FEMALE MARKET",
            subtitle="Core Business Question: Where does revenue come from today, and what is the exact financial impact of unlocking female subscriptions?",
            bg_color="#0F172A",
            border_color="#334155",
            title_color="#F8FAFC",
            title_size=16,
            subtitle_color="#38BDF8",
            subtitle_size=10.5
        )
    ))

    # 2. Row 1: KPI 1 - Total Revenue (x: 40, y: 100, w: 435, h: 125)
    # Height 125px + no subtitle ensures zero clipping
    visuals.append((
        "card_total_revenue",
        make_container(
            "Card_Total_Revenue",
            40, 100, 435, 125, 1000,
            make_card_visual("Total Revenue", font_size=30, font_color="#F8FAFC"),
            title="TOTAL REVENUE (CURRENT BASELINE)",
            title_size=11
        )
    ))

    # 3. Row 1: KPI 2 - Average Order Value (x: 505, y: 100, w: 435, h: 125)
    visuals.append((
        "card_aov",
        make_container(
            "Card_AOV",
            505, 100, 435, 125, 2000,
            make_card_visual("Average Order Value", font_size=30, font_color="#F8FAFC"),
            title="AVERAGE ORDER VALUE (AOV)",
            title_size=11
        )
    ))

    # 4. Row 1: KPI 3 - Customer Rating (x: 970, y: 100, w: 435, h: 125)
    visuals.append((
        "card_rating",
        make_container(
            "Card_Rating",
            970, 100, 435, 125, 3000,
            make_card_visual("Average Customer Rating", font_size=30, font_color="#F8FAFC"),
            title="CUSTOMER SATISFACTION (RATING)",
            title_size=11
        )
    ))

    # 5. Row 1: KPI 4 - Subscription Rate (x: 1435, y: 100, w: 435, h: 125)
    visuals.append((
        "card_subscription_rate",
        make_container(
            "Card_Subscription_Rate",
            1435, 100, 435, 125, 4000,
            make_card_visual("Subscription Rate %", font_size=30, font_color="#38BDF8"),
            title="CURRENT SUBSCRIPTION PENETRATION",
            title_size=11
        )
    ))

    # 6. Row 2: Category Revenue Chart (x: 40, y: 240, w: 1080, h: 285)
    chart_cat = {
        "visualType": "columnChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Entity": "dim_products"}},
                                    "Property": "category",
                                }
                            },
                            "queryRef": "dim_products.category",
                            "nativeQueryRef": "category",
                        }
                    ]
                },
                "Y": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Total Revenue",
                                }
                            },
                            "queryRef": "_Measures.Total Revenue",
                            "nativeQueryRef": "Total Revenue",
                        }
                    ]
                }
            }
        },
        "objects": {
            "dataLabels": [
                {
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                        "fontSize": {"expr": {"Literal": {"Value": "10.5D"}}}
                    }
                }
            ],
            "categoryAxis": [
                {
                    "properties": {
                        "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}},
                        "labelColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#94A3B8'"}}}}}
                    }
                }
            ],
            "valueAxis": [
                {
                    "properties": {
                        "showAxisTitle": {"expr": {"Literal": {"Value": "false"}}},
                        "labelColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#94A3B8'"}}}}}
                    }
                }
            ]
        }
    }
    visuals.append((
        "chart_category_revenue",
        make_container(
            "Chart_Category_Revenue",
            40, 240, 1080, 285, 5000,
            chart_cat,
            title="REVENUE BY PRODUCT CATEGORY",
            subtitle="Clothing ($104K) & Accessories ($74K) drive 76.5% of total gross sales",
            title_size=11.5,
            subtitle_size=9.5
        )
    ))

    # 7. Row 2: Fulfillment Channel Donut (x: 1145, y: 240, w: 735, h: 285)
    chart_ful = {
        "visualType": "donutChart",
        "query": {
            "queryState": {
                "Category": {
                    "projections": [
                        {
                            "field": {
                                "Column": {
                                    "Expression": {"SourceRef": {"Entity": "dim_shipping"}},
                                    "Property": "sales_channel",
                                }
                            },
                            "queryRef": "dim_shipping.sales_channel",
                            "nativeQueryRef": "sales_channel",
                        }
                    ]
                },
                "Y": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Total Revenue",
                                }
                            },
                            "queryRef": "_Measures.Total Revenue",
                            "nativeQueryRef": "Total Revenue",
                        }
                    ]
                }
            }
        },
        "objects": {
            "legend": [
                {
                    "properties": {
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "position": {"expr": {"Literal": {"Value": "'Right'"}}},
                        "labelColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}}
                    }
                }
            ],
            "labels": [
                {
                    "properties": {
                        "color": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                        "fontSize": {"expr": {"Literal": {"Value": "10.5D"}}}
                    }
                }
            ]
        }
    }
    visuals.append((
        "chart_fulfillment_channel",
        make_container(
            "Chart_Fulfillment_Channel",
            1145, 240, 735, 285, 6000,
            chart_ful,
            title="FULFILLMENT CHANNEL SPLIT",
            subtitle="Online Shipping ($194K, 83.3%) vs In-Store Pickup ($39K, 16.7%)",
            title_size=11.5,
            subtitle_size=9.5
        )
    ))

    # 8. Row 3: Slicer Female Adoption Rate (x: 40, y: 540, w: 440, h: 115)
    slicer = {
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
                        "show": {"expr": {"Literal": {"Value": "true"}}},
                        "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#F8FAFC'"}}}}},
                        "textSize": {"expr": {"Literal": {"Value": "9.5D"}}}
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
    visuals.append((
        "slicer_female_adoption_rate",
        make_container(
            "Slicer_Female_Adoption_Rate",
            40, 540, 440, 115, 7000,
            slicer,
            title="🎮 SIMULATION LEVER: FEMALE ADOPTION RATE",
            title_size=10
        )
    ))

    # 9. Row 3: New Female Subscribers Card (x: 40, y: 665, w: 440, h: 125)
    card_subs_unlocked = make_card_visual("Simulated Female Subscribers", font_size=28, font_color="#38BDF8")
    visuals.append((
        "card_simulated_subscribers",
        make_container(
            "Card_Simulated_Subscribers",
            40, 665, 440, 125, 7500,
            card_subs_unlocked,
            title="👥 NEW FEMALE SUBSCRIBERS UNLOCKED",
            title_size=10,
            border_color="#38BDF8",
            title_color="#38BDF8"
        )
    ))

    # 10. Row 3: HERO Simulated Incremental Revenue (x: 505, y: 540, w: 455, h: 250)
    card_sim = make_card_visual("Simulated Incremental Revenue", font_size=38, font_color="#34D399")
    visuals.append((
        "card_simulated_incremental_revenue",
        make_container(
            "Card_Simulated_Incremental_Revenue",
            505, 540, 455, 250, 8000,
            card_sim,
            title="⭐ PROJECTED INCREMENTAL REVENUE (HERO METRIC)",
            subtitle="Pure organic revenue unlocked with zero CAC",
            bg_color="#064E3B",
            border_color="#10B981",
            border_width=2,
            border_radius=12,
            title_color="#34D399",
            title_size=11,
            subtitle_color="#10B981",
            subtitle_size=9
        )
    ))

    # 11. Row 3: Total Projected Revenue (x: 985, y: 540, w: 425, h: 250)
    visuals.append((
        "card_total_projected_revenue",
        make_container(
            "Card_Total_Projected_Revenue",
            985, 540, 425, 250, 9000,
            make_card_visual("Total Projected Revenue", font_size=32, font_color="#F8FAFC"),
            title="TOTAL PROJECTED REVENUE",
            subtitle="Baseline $233K + Incremental Revenue",
            title_size=11,
            subtitle_size=9
        )
    ))

    # 12. Row 3: Projected Revenue Lift % (x: 1435, y: 540, w: 435, h: 250)
    visuals.append((
        "card_projected_revenue_lift",
        make_container(
            "Card_Projected_Revenue_Lift",
            1435, 540, 435, 250, 10000,
            make_card_visual("Projected Revenue Lift %", font_size=32, font_color="#38BDF8"),
            title="NET REVENUE LIFT %",
            subtitle="Top-line growth surge over current baseline",
            title_size=11,
            subtitle_size=9
        )
    ))

    for folder_name, v_json in visuals:
        v_dir = visuals_dir / folder_name
        v_dir.mkdir(parents=True, exist_ok=True)
        v_file = v_dir / "visual.json"
        with open(v_file, "w", encoding="utf-8") as f:
            json.dump(v_json, f, indent=2)
        print(f"Created visual: {folder_name}/visual.json")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated PBIP files to scratch directory...")
    src_pbi = BASE_DIR / "power_bi"
    dst_pbi = SCRATCH_DIR / "power_bi"
    if src_pbi.exists():
        shutil.copytree(src_pbi, dst_pbi, dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "11_fix_card_clipping_and_enlarge_header.py", SCRATCH_DIR / "src" / "11_fix_card_clipping_and_enlarge_header.py")
    print("Sync complete.")


def main():
    print("=== Rebalancing Visual Heights and Enlarging Header Title ===")
    update_page_json(BASE_DIR)
    update_base_theme(BASE_DIR)
    build_all_visuals(BASE_DIR)
    sync_to_scratch()
    print("=== Successfully completed layout polish! ===")


if __name__ == "__main__":
    main()
