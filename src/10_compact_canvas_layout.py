"""
10_compact_canvas_layout.py
---------------------------
Re-engineers the Power BI canvas dimensions and visual coordinates into an
ultra-compact Executive Panoramic Layout (1920 x 840 px):
  - Canvas height: 840 px (aspect ratio ~2.28:1 matching Power BI Desktop viewport perfectly).
  - Eliminates all vertical scrolling and cuts in both 'Fit to page' and 'Fit to width' modes.
  - Header: y=15, h=55
  - Row 1 (KPIs): y=85, h=95
  - Row 2 (Charts): y=195, h=310
  - Row 3 (Simulation): y=520, h=300
  - Total vertical footprint: 820 px (comfortably within 840 px canvas).
"""

import json
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\BAH\Desktop\data01\retail-customer-behavior-analysis")
SCRATCH_DIR = Path(r"C:\Users\BAH\.gemini\antigravity\scratch\retail-customer-behavior-analysis")
PAGE_GUID = "e2d88bab65d02ef79d4f"

CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 840


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
    print(f"Updated page.json with compact height {CANVAS_HEIGHT}: {page_path}")


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
    print(f"Updated base theme page size to {CANVAS_WIDTH}x{CANVAS_HEIGHT}: {theme_path}")


def make_container(name, x, y, width, height, z, visual_dict, title=None, subtitle=None, 
                   bg_color="#1E293B", border_color="#334155", border_width=1, border_radius=10,
                   title_color="#F8FAFC", subtitle_color="#94A3B8"):
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
                    "fontSize": {"expr": {"Literal": {"Value": "10D"}}},
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
                    "fontSize": {"expr": {"Literal": {"Value": "8.5D"}}},
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{subtitle_color}'"}}}}}
                }
            }
        ]

    container["visual"]["visualContainerObjects"] = v_objs
    return container


def make_card_visual(measure_name, font_size=26, font_color="#F8FAFC"):
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

    # 1. Header Banner (x: 40, y: 15, w: 1840, h: 55)
    header_visual = make_card_visual("Total Revenue", font_size=1, font_color="#0F172A")
    visuals.append((
        "header_banner",
        make_container(
            "Header_Banner",
            40, 15, 1840, 55, 500,
            header_visual,
            title="STRATEGIC EXECUTIVE COCKPIT: UNLOCKING THE FEMALE MARKET OPPORTUNITY",
            subtitle="Core Objective: Baseline Revenue Structure ($233K) & Quantifying Financial Impact of Female Subscriptions",
            bg_color="#0F172A",
            border_color="#334155",
            title_color="#F8FAFC",
            subtitle_color="#38BDF8"
        )
    ))

    # 2. Row 1: KPI 1 - Total Revenue (x: 40, y: 85, w: 435, h: 95)
    visuals.append((
        "card_total_revenue",
        make_container(
            "Card_Total_Revenue",
            40, 85, 435, 95, 1000,
            make_card_visual("Total Revenue", font_size=26, font_color="#F8FAFC"),
            title="TOTAL REVENUE (BASELINE)",
            subtitle="Current Gross Sales ($233K)"
        )
    ))

    # 3. Row 1: KPI 2 - Average Order Value (x: 505, y: 85, w: 435, h: 95)
    visuals.append((
        "card_aov",
        make_container(
            "Card_AOV",
            505, 85, 435, 95, 2000,
            make_card_visual("Average Order Value", font_size=26, font_color="#F8FAFC"),
            title="AVERAGE ORDER VALUE (AOV)",
            subtitle="Combined Male & Female Basket ($59.76)"
        )
    ))

    # 4. Row 1: KPI 3 - Customer Rating (x: 970, y: 85, w: 435, h: 95)
    visuals.append((
        "card_rating",
        make_container(
            "Card_Rating",
            970, 85, 435, 95, 3000,
            make_card_visual("Average Customer Rating", font_size=26, font_color="#F8FAFC"),
            title="CUSTOMER SATISFACTION",
            subtitle="Average Review Rating (3.75 / 5.0 ★)"
        )
    ))

    # 5. Row 1: KPI 4 - Subscription Rate (x: 1435, y: 85, w: 435, h: 95)
    visuals.append((
        "card_subscription_rate",
        make_container(
            "Card_Subscription_Rate",
            1435, 85, 435, 95, 4000,
            make_card_visual("Subscription Rate %", font_size=26, font_color="#38BDF8"),
            title="SUBSCRIPTION PENETRATION",
            subtitle="27.0% Overall (100% Male - Legacy Model)"
        )
    ))

    # 6. Row 2: Category Revenue Chart (x: 40, y: 195, w: 1080, h: 310)
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
                        "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
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
            40, 195, 1080, 310, 5000,
            chart_cat,
            title="REVENUE BY PRODUCT CATEGORY",
            subtitle="Clothing ($104K) & Accessories ($74K) drive 76.5% of total sales"
        )
    ))

    # 7. Row 2: Fulfillment Channel Donut (x: 1145, y: 195, w: 735, h: 310)
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
                        "fontSize": {"expr": {"Literal": {"Value": "10D"}}}
                    }
                }
            ]
        }
    }
    visuals.append((
        "chart_fulfillment_channel",
        make_container(
            "Chart_Fulfillment_Channel",
            1145, 195, 735, 310, 6000,
            chart_ful,
            title="FULFILLMENT CHANNEL SPLIT",
            subtitle="Online Shipping ($194K, 83.3%) vs In-Store Pickup ($39K, 16.7%)"
        )
    ))

    # 8. Row 3: Slicer Female Adoption Rate (x: 40, y: 520, w: 440, h: 140)
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
            40, 520, 440, 140, 7000,
            slicer,
            title="🎮 SIMULATION LEVER: FEMALE ADOPTION RATE",
            subtitle="Slide to test target adoption (0% to 100%)"
        )
    ))

    # 9. Row 3: New Female Subscribers Card (x: 40, y: 675, w: 440, h: 145)
    card_subs_unlocked = make_card_visual("Simulated Female Subscribers", font_size=30, font_color="#38BDF8")
    visuals.append((
        "card_simulated_subscribers",
        make_container(
            "Card_Simulated_Subscribers",
            40, 675, 440, 145, 7500,
            card_subs_unlocked,
            title="👥 NEW FEMALE SUBSCRIBERS UNLOCKED",
            subtitle="Active shoppers converting to membership",
            border_color="#38BDF8",
            title_color="#38BDF8"
        )
    ))

    # 10. Row 3: HERO Simulated Incremental Revenue (x: 505, y: 520, w: 455, h: 300)
    card_sim = make_card_visual("Simulated Incremental Revenue", font_size=38, font_color="#34D399")
    visuals.append((
        "card_simulated_incremental_revenue",
        make_container(
            "Card_Simulated_Incremental_Revenue",
            505, 520, 455, 300, 8000,
            card_sim,
            title="⭐ PROJECTED INCREMENTAL REVENUE (HERO METRIC)",
            subtitle="Unlocks up to +$84.2K at 50% target adoption (CAC = $0)",
            bg_color="#064E3B",
            border_color="#10B981",
            border_width=2,
            border_radius=12,
            title_color="#34D399",
            subtitle_color="#10B981"
        )
    ))

    # 11. Row 3: Total Projected Revenue (x: 985, y: 520, w: 425, h: 300)
    visuals.append((
        "card_total_projected_revenue",
        make_container(
            "Card_Total_Projected_Revenue",
            985, 520, 425, 300, 9000,
            make_card_visual("Total Projected Revenue", font_size=32, font_color="#F8FAFC"),
            title="TOTAL PROJECTED REVENUE",
            subtitle="Baseline $233K + Simulated Incremental"
        )
    ))

    # 12. Row 3: Projected Revenue Lift % (x: 1435, y: 520, w: 435, h: 300)
    visuals.append((
        "card_projected_revenue_lift",
        make_container(
            "Card_Projected_Revenue_Lift",
            1435, 520, 435, 300, 10000,
            make_card_visual("Projected Revenue Lift %", font_size=32, font_color="#38BDF8"),
            title="NET REVENUE LIFT %",
            subtitle="Top-line growth surge over current baseline"
        )
    ))

    for folder_name, v_json in visuals:
        v_dir = visuals_dir / folder_name
        v_dir.mkdir(parents=True, exist_ok=True)
        v_file = v_dir / "visual.json"
        with open(v_file, "w", encoding="utf-8") as f:
            json.dump(v_json, f, indent=2)
        print(f"Created compact visual: {folder_name}/visual.json")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated PBIP files to scratch directory...")
    src_pbi = BASE_DIR / "power_bi"
    dst_pbi = SCRATCH_DIR / "power_bi"
    if src_pbi.exists():
        shutil.copytree(src_pbi, dst_pbi, dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "10_compact_canvas_layout.py", SCRATCH_DIR / "src" / "10_compact_canvas_layout.py")
    print("Sync complete.")


def main():
    print("=== Rebuilding into Ultra-Compact Panoramic Layout (1920 x 840) ===")
    update_page_json(BASE_DIR)
    update_base_theme(BASE_DIR)
    build_all_visuals(BASE_DIR)
    sync_to_scratch()
    print("=== Successfully completed compact redesign! ===")


if __name__ == "__main__":
    main()
