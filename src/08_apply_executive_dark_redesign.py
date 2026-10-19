"""
08_apply_executive_dark_redesign.py
-----------------------------------
Implements the 6 concrete executive dashboard fixes:
  1. Fixes DAX 'Dynamic Executive Insight' to prevent .NET FormatException on '+'.
  2. Enforces explicit Dark Slate background (#1E293B) and borders (#334155) on ALL visual containers
     eliminating the checkerboard/patchwork white boxes.
  3. Disables 'categoryLabels' on all cards and sets large, centered callout metrics,
     eliminating clipped/cut-off labels.
  4. Configures 'card_dynamic_insight' with readable 13pt callout font and cyan accent border (#38BDF8).
  5. Enables Data Labels on the Category column chart and themes axes to dark slate.
  6. Refines Executive Header banner with high-contrast, professional typography.
"""

import json
import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\BAH\Desktop\data01\retail-customer-behavior-analysis")
SCRATCH_DIR = Path(r"C:\Users\BAH\.gemini\antigravity\scratch\retail-customer-behavior-analysis")
PAGE_GUID = "e2d88bab65d02ef79d4f"


def update_dax_measures(root_dir: Path):
    tmdl_path = root_dir / "power_bi" / "powerbi report.SemanticModel" / "definition" / "tables" / "_Measures.tmdl"
    if not tmdl_path.exists():
        print(f"Warning: {tmdl_path} does not exist.")
        return

    content = tmdl_path.read_text(encoding="utf-8")
    
    # Robust measure definition avoiding unescaped + in FORMAT
    fixed_measure = """\tmeasure 'Executive Dashboard Header' = "RETAIL REVENUE & GROWTH COCKPIT: UNLOCKING THE FEMALE MARKET"
\t\tlineageTag: e1a2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c

\tmeasure 'Dynamic Executive Insight' = 
\t\tVAR _Rate = [Female Adoption Rate Value]
\t\tVAR _Inc = [Simulated Incremental Revenue]
\t\tVAR _Lift = [Projected Revenue Lift %]
\t\tRETURN
\t\t\t"Targeting " & FORMAT(_Rate, "0%") & " female adoption unlocks " & FORMAT(_Inc, "$#,##0") & " new revenue (+" & FORMAT(_Lift, "0.0%") & " lift) with zero customer acquisition spend."
\t\tlineageTag: f2b3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d
"""

    if "measure 'Executive Dashboard Header'" in content:
        # Replace existing measure block up to 'column Placeholder'
        start_idx = content.find("\tmeasure 'Executive Dashboard Header'")
        end_idx = content.find("\tcolumn Placeholder")
        content = content[:start_idx] + fixed_measure + "\n" + content[end_idx:]
    else:
        end_idx = content.find("\tcolumn Placeholder")
        content = content[:end_idx] + fixed_measure + "\n" + content[end_idx:]

    tmdl_path.write_text(content, encoding="utf-8")
    print(f"Updated DAX measures in {tmdl_path}")


def make_container(name, x, y, width, height, z, visual_dict, title=None, subtitle=None, 
                   bg_color="#1E293B", border_color="#334155", border_width=1, border_radius=12,
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
                    "fontSize": {"expr": {"Literal": {"Value": "11D"}}},
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
                    "fontSize": {"expr": {"Literal": {"Value": "9D"}}},
                    "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": f"'{subtitle_color}'"}}}}}
                }
            }
        ]

    container["visual"]["visualContainerObjects"] = v_objs
    return container


def make_card_visual(measure_name, font_size=32, font_color="#F8FAFC"):
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

    # 1. Header Banner (x: 40, y: 20, w: 1840, h: 75)
    header_visual = make_card_visual("Executive Dashboard Header", font_size=16, font_color="#F8FAFC")
    visuals.append((
        "header_banner",
        make_container(
            "Header_Banner",
            40, 20, 1840, 75, 500,
            header_visual,
            title="STRATEGIC EXECUTIVE COCKPIT | BOARD OF DIRECTORS BRIEFING",
            subtitle="Core Objective: Baseline Revenue Structure & Quantifying Female Subscription Growth Opportunity",
            bg_color="#0F172A",
            border_color="#334155",
            title_color="#38BDF8",
            subtitle_color="#94A3B8"
        )
    ))

    # 2. KPI 1: Total Revenue (x: 40, y: 110, w: 435, h: 120)
    visuals.append((
        "card_total_revenue",
        make_container(
            "Card_Total_Revenue",
            40, 110, 435, 120, 1000,
            make_card_visual("Total Revenue", font_size=32, font_color="#F8FAFC"),
            title="TOTAL REVENUE (BASELINE)",
            subtitle="Current Gross Sales ($233K)"
        )
    ))

    # 3. KPI 2: Average Order Value (x: 505, y: 110, w: 435, h: 120)
    visuals.append((
        "card_aov",
        make_container(
            "Card_AOV",
            505, 110, 435, 120, 2000,
            make_card_visual("Average Order Value", font_size=32, font_color="#F8FAFC"),
            title="AVERAGE ORDER VALUE (AOV)",
            subtitle="Combined Male & Female Basket ($59.76)"
        )
    ))

    # 4. KPI 3: Customer Rating (x: 970, y: 110, w: 435, h: 120)
    visuals.append((
        "card_rating",
        make_container(
            "Card_Rating",
            970, 110, 435, 120, 3000,
            make_card_visual("Average Customer Rating", font_size=32, font_color="#F8FAFC"),
            title="CUSTOMER SATISFACTION",
            subtitle="Average Review Rating (3.75 / 5.0 ★)"
        )
    ))

    # 5. KPI 4: Subscription Rate (x: 1435, y: 110, w: 435, h: 120)
    visuals.append((
        "card_subscription_rate",
        make_container(
            "Card_Subscription_Rate",
            1435, 110, 435, 120, 4000,
            make_card_visual("Subscription Rate %", font_size=32, font_color="#38BDF8"),
            title="SUBSCRIPTION PENETRATION",
            subtitle="27.0% Overall (100% Male - Legacy Model)"
        )
    ))

    # 6. Chart: Category Revenue (x: 40, y: 245, w: 1080, h: 360)
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
            40, 245, 1080, 360, 5000,
            chart_cat,
            title="REVENUE BY PRODUCT CATEGORY",
            subtitle="Clothing ($104K) & Accessories ($74K) drive 76.5% of total sales"
        )
    ))

    # 7. Chart: Fulfillment Channel (x: 1145, y: 245, w: 735, h: 360)
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
                        "labelColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#94A3B8'"}}}}}
                    }
                }
            ]
        }
    }
    visuals.append((
        "chart_fulfillment_channel",
        make_container(
            "Chart_Fulfillment_Channel",
            1145, 245, 735, 360, 6000,
            chart_ful,
            title="FULFILLMENT CHANNEL SPLIT",
            subtitle="Online Shipping ($194K, 83.3%) vs In-Store Pickup ($39K, 16.7%)"
        )
    ))

    # 8. Slicer: Female Adoption Rate (x: 40, y: 620, w: 440, h: 195)
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
        }
    }
    visuals.append((
        "slicer_female_adoption_rate",
        make_container(
            "Slicer_Female_Adoption_Rate",
            40, 620, 440, 195, 7000,
            slicer,
            title="🎮 SIMULATION LEVER: FEMALE ADOPTION RATE",
            subtitle="Slide to test target adoption (0% to 100%)"
        )
    ))

    # 9. Dynamic Executive Insight Box (x: 40, y: 830, w: 440, h: 215)
    card_insight = make_card_visual("Dynamic Executive Insight", font_size=13, font_color="#38BDF8")
    visuals.append((
        "card_dynamic_insight",
        make_container(
            "Card_Dynamic_Insight",
            40, 830, 440, 215, 7500,
            card_insight,
            title="💡 REAL-TIME EXECUTIVE TAKEAWAY",
            subtitle="Live calculation driven by simulation slider",
            border_color="#38BDF8",  # Cyan accent border
            title_color="#38BDF8"
        )
    ))

    # 10. Card: HERO Simulated Incremental Revenue (x: 505, y: 620, w: 455, h: 425)
    card_sim = make_card_visual("Simulated Incremental Revenue", font_size=38, font_color="#34D399")
    visuals.append((
        "card_simulated_incremental_revenue",
        make_container(
            "Card_Simulated_Incremental_Revenue",
            505, 620, 455, 425, 8000,
            card_sim,
            title="⭐ PROJECTED INCREMENTAL REVENUE (HERO METRIC)",
            subtitle="Unlocks up to +$84.2K at 50% target adoption",
            bg_color="#064E3B",      # Deep emerald
            border_color="#10B981",  # Glowing emerald border
            border_width=2,
            border_radius=14,
            title_color="#34D399",
            subtitle_color="#10B981"
        )
    ))

    # 11. Card: Total Projected Revenue (x: 985, y: 620, w: 425, h: 425)
    visuals.append((
        "card_total_projected_revenue",
        make_container(
            "Card_Total_Projected_Revenue",
            985, 620, 425, 425, 9000,
            make_card_visual("Total Projected Revenue", font_size=32, font_color="#F8FAFC"),
            title="TOTAL PROJECTED REVENUE",
            subtitle="Baseline $233K + Simulated Incremental"
        )
    ))

    # 12. Card: Projected Revenue Lift % (x: 1435, y: 620, w: 435, h: 425)
    visuals.append((
        "card_projected_revenue_lift",
        make_container(
            "Card_Projected_Revenue_Lift",
            1435, 620, 435, 425, 10000,
            make_card_visual("Projected Revenue Lift %", font_size=32, font_color="#38BDF8"),
            title="NET REVENUE LIFT %",
            subtitle="Top-line growth surge over current baseline"
        )
    ))

    # Write all visuals to disk
    for folder_name, v_json in visuals:
        v_dir = visuals_dir / folder_name
        v_dir.mkdir(parents=True, exist_ok=True)
        v_file = v_dir / "visual.json"
        with open(v_file, "w", encoding="utf-8") as f:
            json.dump(v_json, f, indent=2)
        print(f"Created visual container: {folder_name}/visual.json")


def sync_to_scratch():
    if not SCRATCH_DIR.exists():
        return
    print("Syncing updated PBIP files to scratch directory...")
    src_pbi = BASE_DIR / "power_bi"
    dst_pbi = SCRATCH_DIR / "power_bi"
    if src_pbi.exists():
        shutil.copytree(src_pbi, dst_pbi, dirs_exist_ok=True)
    shutil.copy2(BASE_DIR / "src" / "08_apply_executive_dark_redesign.py", SCRATCH_DIR / "src" / "08_apply_executive_dark_redesign.py")
    print("Sync complete.")


def main():
    print("=== Applying Complete Executive Dark Cockpit Redesign ===")
    update_dax_measures(BASE_DIR)
    build_all_visuals(BASE_DIR)
    sync_to_scratch()
    print("=== Successfully completed 100% of executive redesign! ===")


if __name__ == "__main__":
    main()
