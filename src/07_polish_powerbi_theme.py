"""
07_polish_powerbi_theme.py
--------------------------
Transforms the Power BI Project (PBIP) into an Executive Modern Dark Cockpit.
Applies:
  1. Base theme update (Fluent2-CY26SU09.json) with Dark Slate palette, rounded cards (#1E293B),
     crisp borders (#334155), drop shadows, and executive data colors.
  2. Canvas background update in page.json (#0B1120).
  3. Two new DAX measures in _Measures.tmdl:
     - 'Executive Dashboard Header'
     - 'Dynamic Executive Insight'
  4. 12 precisely dimensioned, aligned, and styled PBIR visual containers (visual.json),
     including:
     - Executive Header Banner
     - 4 Top KPI Cards
     - 2 Core Driver Visuals (Category Column Chart & Fulfillment Donut Chart)
     - Slicer Scenario Lever (0% to 100%)
     - Dynamic Executive Insight Narrative Box
     - Hero Metric Card (Glowing Emerald Border & Background for Incremental Revenue)
     - Total Projected Revenue Card
     - Revenue Lift % Card
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
    
    new_measures = """\tmeasure 'Executive Dashboard Header' = "RETAIL REVENUE & GROWTH COCKPIT: UNLOCKING THE FEMALE MARKET"
\t\tlineageTag: e1a2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c

\tmeasure 'Dynamic Executive Insight' = 
\t\tVAR _Rate = [Female Adoption Rate Value]
\t\tVAR _Inc = [Simulated Incremental Revenue]
\t\tVAR _Lift = [Projected Revenue Lift %]
\t\tRETURN
\t\t\t"Targeting a " & FORMAT(_Rate, "0%") & " female subscription adoption unlocks " & FORMAT(_Inc, "$#,##0") & " in incremental annual revenue (a " & FORMAT(_Lift, "+0.0%") & " total revenue lift) with ZERO extra customer acquisition cost (CAC)."
\t\tlineageTag: f2b3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d

"""
    if "Executive Dashboard Header" not in content:
        idx = content.find("\tcolumn Placeholder")
        if idx != -1:
            updated_content = content[:idx] + new_measures + content[idx:]
            tmdl_path.write_text(updated_content, encoding="utf-8")
            print(f"Added executive DAX measures to {tmdl_path}")
        else:
            print("Could not find insertion point in TMDL.")
    else:
        print("Executive DAX measures already exist in TMDL.")


def update_base_theme(root_dir: Path):
    theme_path = root_dir / "power_bi" / "powerbi report.Report" / "StaticResources" / "SharedResources" / "BaseThemes" / "Fluent2-CY26SU09.json"
    if not theme_path.exists():
        print(f"Warning: {theme_path} not found.")
        return

    with open(theme_path, "r", encoding="utf-8") as f:
        theme = json.load(f)

    # 1. Colors
    theme["dataColors"] = [
        "#3B82F6",  # Royal Blue
        "#10B981",  # Emerald Green (Hero Growth)
        "#6366F1",  # Indigo
        "#F59E0B",  # Amber Gold
        "#EC4899",  # Rose Pink
        "#8B5CF6",  # Violet
        "#14B8A6",  # Teal
        "#38BDF8",  # Sky Blue
    ]
    theme["foreground"] = "#F8FAFC"
    theme["foregroundNeutralSecondary"] = "#94A3B8"
    theme["foregroundNeutralTertiary"] = "#64748B"
    theme["foregroundNeutralLight"] = "#475569"
    theme["background"] = "#0B1120"
    theme["backgroundLight"] = "#1E293B"
    theme["backgroundNeutral"] = "#0F172A"
    theme["backgroundDark"] = "#020617"
    theme["tableAccent"] = "#3B82F6"
    theme["shapeStroke"] = "#334155"

    # 2. Text classes
    theme["textClasses"] = {
        "callout": {
            "fontSize": 24,
            "fontFace": "Segoe UI Semibold",
            "color": "#F8FAFC",
        },
        "title": {
            "fontSize": 12,
            "fontFace": "Segoe UI Semibold",
            "color": "#F8FAFC",
        },
        "header": {
            "fontSize": 11,
            "fontFace": "Segoe UI Semibold",
            "color": "#F8FAFC",
        },
        "label": {
            "fontSize": 10,
            "fontFace": "Segoe UI",
            "color": "#94A3B8",
        },
    }

    # 3. Visual styles
    vs = theme.setdefault("visualStyles", {})
    star_star = vs.setdefault("*", {}).setdefault("*", {})

    star_star["background"] = [
        {
            "show": True,
            "transparency": 0,
            "color": {"solid": {"color": "#1E293B"}},
        }
    ]
    star_star["border"] = [
        {
            "show": True,
            "width": 1,
            "radius": 12,
            "color": {"solid": {"color": "#334155"}},
        }
    ]
    star_star["dropShadow"] = [
        {
            "show": True,
            "preset": "Custom",
            "angle": 90,
            "shadowDistance": 4,
            "shadowBlur": 10,
            "shadowSpread": 0,
            "transparency": 60,
            "color": {"solid": {"color": "#000000"}},
        }
    ]
    star_star["title"] = [
        {
            "show": True,
            "fontSize": 12,
            "titleWrap": True,
            "fontColor": {"solid": {"color": "#F8FAFC"}},
        }
    ]
    star_star["subTitle"] = [
        {
            "show": True,
            "fontSize": 9.5,
            "fontColor": {"solid": {"color": "#94A3B8"}},
        }
    ]
    star_star["categoryAxis"] = [
        {
            "showAxisTitle": False,
            "maxMarginFactor": 50,
            "gridlineStyle": "solid",
            "gridlineColor": {"solid": {"color": "#334155"}},
            "concatenateLabels": False,
            "titleFontSize": 10,
            "fontSize": 10,
            "labelColor": {"solid": {"color": "#94A3B8"}},
        }
    ]
    star_star["valueAxis"] = [
        {
            "showAxisTitle": False,
            "maxMarginFactor": 50,
            "gridlineStyle": "solid",
            "gridlineColor": {"solid": {"color": "#334155"}},
            "titleFontSize": 10,
            "fontSize": 10,
            "labelColor": {"solid": {"color": "#94A3B8"}},
        }
    ]
    star_star["legend"] = [
        {
            "show": True,
            "position": "Right",
            "showTitle": False,
            "labelColor": {"solid": {"color": "#94A3B8"}},
        }
    ]

    # Page styling
    page_star = vs.setdefault("page", {}).setdefault("*", {})
    page_star["background"] = [
        {
            "color": {"solid": {"color": "#0B1120"}},
            "transparency": 0,
        }
    ]
    page_star["outspace"] = [
        {
            "color": {"solid": {"color": "#0B1120"}},
        }
    ]

    # Card visual styles
    card_star = vs.setdefault("card", {}).setdefault("*", {})
    card_star["labels"] = [
        {
            "color": {"solid": {"color": "#F8FAFC"}},
            "fontSize": 26,
        }
    ]
    card_star["categoryLabels"] = [
        {
            "show": True,
            "color": {"solid": {"color": "#94A3B8"}},
            "fontSize": 10,
        }
    ]

    with open(theme_path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2)
    print(f"Base theme updated to Dark Slate Executive: {theme_path}")


def update_page_json(root_dir: Path):
    page_path = root_dir / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "page.json"
    page_data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": PAGE_GUID,
        "displayName": "Executive Revenue Cockpit",
        "displayOption": "FitToPage",
        "height": 1080,
        "width": 1920,
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
                                            "Value": "'#0B1120'"
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
    print(f"Updated {page_path}")


def make_visual_container(name, x, y, width, height, z, visual_dict, title=None, subtitle=None, is_hero=False):
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

    # Custom container styling
    v_objs = {}
    if title:
        v_objs["title"] = [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{title}'"}}},
                    "fontSize": {"expr": {"Literal": {"Value": "11.5D"}}},
                    "bold": {"expr": {"Literal": {"Value": "true"}}},
                    "fontColor": {
                        "solid": {
                            "color": {
                                "expr": {
                                    "Literal": {
                                        "Value": "'#34D399'" if is_hero else "'#F8FAFC'"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ]
    if subtitle:
        v_objs["subTitle"] = [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "text": {"expr": {"Literal": {"Value": f"'{subtitle}'"}}},
                    "fontSize": {"expr": {"Literal": {"Value": "9.5D"}}},
                    "fontColor": {
                        "solid": {
                            "color": {
                                "expr": {
                                    "Literal": {
                                        "Value": "'#10B981'" if is_hero else "'#94A3B8'"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        ]

    if is_hero:
        v_objs["background"] = [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {
                        "solid": {
                            "color": {
                                "expr": {
                                    "Literal": {
                                        "Value": "'#064E3B'"
                                    }
                                }
                            }
                        }
                    },
                    "transparency": {
                        "expr": {
                            "Literal": {
                                "Value": "30D"
                            }
                        }
                    }
                }
            }
        ]
        v_objs["border"] = [
            {
                "properties": {
                    "show": {"expr": {"Literal": {"Value": "true"}}},
                    "color": {
                        "solid": {
                            "color": {
                                "expr": {
                                    "Literal": {
                                        "Value": "'#10B981'"
                                    }
                                }
                            }
                        }
                    },
                    "radius": {
                        "expr": {
                            "Literal": {
                                "Value": "14D"
                            }
                        }
                    },
                    "width": {
                        "expr": {
                            "Literal": {
                                "Value": "2D"
                            }
                        }
                    }
                }
            }
        ]
    
    if v_objs:
        container["visual"]["visualContainerObjects"] = v_objs

    return container


def build_all_visuals(root_dir: Path):
    visuals_dir = root_dir / "power_bi" / "powerbi report.Report" / "definition" / "pages" / PAGE_GUID / "visuals"
    
    # Clean existing visuals
    if visuals_dir.exists():
        shutil.rmtree(visuals_dir)
    visuals_dir.mkdir(parents=True, exist_ok=True)

    visuals = []

    # 1. Header Banner Visual (x: 40, y: 20, w: 1840, h: 75)
    header_visual = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Executive Dashboard Header",
                                }
                            },
                            "queryRef": "_Measures.Executive Dashboard Header",
                            "nativeQueryRef": "Executive Dashboard Header",
                        }
                    ]
                }
            }
        },
        "objects": {
            "categoryLabels": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
        }
    }
    visuals.append((
        "header_banner",
        make_visual_container(
            "Header_Banner",
            40, 20, 1840, 75, 500,
            header_visual,
            title="STRATEGIC EXECUTIVE COCKPIT | BOARD OF DIRECTORS BRIEFING",
            subtitle="Core Question: Where does revenue come from today, and what is the exact financial impact of unlocking female subscriptions?"
        )
    ))

    # 2. KPI 1: Total Revenue (x: 40, y: 110, w: 435, h: 120)
    card_rev = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
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
        }
    }
    visuals.append((
        "card_total_revenue",
        make_visual_container(
            "Card_Total_Revenue",
            40, 110, 435, 120, 1000,
            card_rev,
            title="TOTAL REVENUE (BASELINE)",
            subtitle="Current Gross Sales ($233K)"
        )
    ))

    # 3. KPI 2: Average Order Value (x: 505, y: 110, w: 435, h: 120)
    card_aov = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Average Order Value",
                                }
                            },
                            "queryRef": "_Measures.Average Order Value",
                            "nativeQueryRef": "Average Order Value",
                        }
                    ]
                }
            }
        }
    }
    visuals.append((
        "card_aov",
        make_visual_container(
            "Card_AOV",
            505, 110, 435, 120, 2000,
            card_aov,
            title="AVERAGE ORDER VALUE (AOV)",
            subtitle="Combined Male & Female Basket ($59.76)"
        )
    ))

    # 4. KPI 3: Customer Rating (x: 970, y: 110, w: 435, h: 120)
    card_rating = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Average Customer Rating",
                                }
                            },
                            "queryRef": "_Measures.Average Customer Rating",
                            "nativeQueryRef": "Average Customer Rating",
                        }
                    ]
                }
            }
        }
    }
    visuals.append((
        "card_rating",
        make_visual_container(
            "Card_Rating",
            970, 110, 435, 120, 3000,
            card_rating,
            title="CUSTOMER SATISFACTION",
            subtitle="Average Review Rating (3.75 / 5.0 ★)"
        )
    ))

    # 5. KPI 4: Subscription Rate (x: 1435, y: 110, w: 435, h: 120)
    card_sub = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Subscription Rate %",
                                }
                            },
                            "queryRef": "_Measures.Subscription Rate %",
                            "nativeQueryRef": "Subscription Rate %",
                        }
                    ]
                }
            }
        }
    }
    visuals.append((
        "card_subscription_rate",
        make_visual_container(
            "Card_Subscription_Rate",
            1435, 110, 435, 120, 4000,
            card_sub,
            title="SUBSCRIPTION PENETRATION",
            subtitle="27.0% Overall (100% Male - Legacy Roots)"
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
        }
    }
    visuals.append((
        "chart_category_revenue",
        make_visual_container(
            "Chart_Category_Revenue",
            40, 245, 1080, 360, 5000,
            chart_cat,
            title="REVENUE BY PRODUCT CATEGORY",
            subtitle="Clothing ($104K) & Accessories ($74K) drive 76.5% of total gross sales"
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
        }
    }
    visuals.append((
        "chart_fulfillment_channel",
        make_visual_container(
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
        make_visual_container(
            "Slicer_Female_Adoption_Rate",
            40, 620, 440, 195, 7000,
            slicer,
            title="🎮 SIMULATION LEVER: FEMALE ADOPTION RATE",
            subtitle="Slide to test target adoption (0% to 100%)"
        )
    ))

    # 9. Dynamic Executive Insight Box (x: 40, y: 830, w: 440, h: 215)
    card_insight = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Dynamic Executive Insight",
                                }
                            },
                            "queryRef": "_Measures.Dynamic Executive Insight",
                            "nativeQueryRef": "Dynamic Executive Insight",
                        }
                    ]
                }
            }
        },
        "objects": {
            "categoryLabels": [{"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}]
        }
    }
    visuals.append((
        "card_dynamic_insight",
        make_visual_container(
            "Card_Dynamic_Insight",
            40, 830, 440, 215, 7500,
            card_insight,
            title="💡 KEY EXECUTIVE TAKEAWAY",
            subtitle="Real-time calculation based on slider lever"
        )
    ))

    # 10. Card: HERO Simulated Incremental Revenue (x: 505, y: 620, w: 455, h: 425)
    card_sim = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Simulated Incremental Revenue",
                                }
                            },
                            "queryRef": "_Measures.Simulated Incremental Revenue",
                            "nativeQueryRef": "Simulated Incremental Revenue",
                        }
                    ]
                }
            }
        },
        "objects": {
            "labels": [
                {
                    "properties": {
                        "color": {
                            "solid": {
                                "color": {
                                    "expr": {
                                        "Literal": {
                                            "Value": "'#34D399'"
                                        }
                                    }
                                }
                            }
                        },
                        "fontSize": {
                            "expr": {
                                "Literal": {
                                    "Value": "40D"
                                }
                            }
                        }
                    }
                }
            ]
        }
    }
    visuals.append((
        "card_simulated_incremental_revenue",
        make_visual_container(
            "Card_Simulated_Incremental_Revenue",
            505, 620, 455, 425, 8000,
            card_sim,
            title="⭐ PROJECTED INCREMENTAL REVENUE (HERO METRIC)",
            subtitle="Unlocks up to +$84.2K at 50% target adoption",
            is_hero=True
        )
    ))

    # 11. Card: Total Projected Revenue (x: 985, y: 620, w: 425, h: 425)
    card_tot = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Total Projected Revenue",
                                }
                            },
                            "queryRef": "_Measures.Total Projected Revenue",
                            "nativeQueryRef": "Total Projected Revenue",
                        }
                    ]
                }
            }
        }
    }
    visuals.append((
        "card_total_projected_revenue",
        make_visual_container(
            "Card_Total_Projected_Revenue",
            985, 620, 425, 425, 9000,
            card_tot,
            title="TOTAL PROJECTED REVENUE",
            subtitle="Baseline $233K + Simulated Incremental"
        )
    ))

    # 12. Card: Projected Revenue Lift % (x: 1435, y: 620, w: 435, h: 425)
    card_lift = {
        "visualType": "card",
        "query": {
            "queryState": {
                "Values": {
                    "projections": [
                        {
                            "field": {
                                "Measure": {
                                    "Expression": {"SourceRef": {"Entity": "_Measures"}},
                                    "Property": "Projected Revenue Lift %",
                                }
                            },
                            "queryRef": "_Measures.Projected Revenue Lift %",
                            "nativeQueryRef": "Projected Revenue Lift %",
                        }
                    ]
                }
            }
        }
    }
    visuals.append((
        "card_projected_revenue_lift",
        make_visual_container(
            "Card_Projected_Revenue_Lift",
            1435, 620, 435, 425, 10000,
            card_lift,
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
    # Copy power_bi directory
    src_pbi = BASE_DIR / "power_bi"
    dst_pbi = SCRATCH_DIR / "power_bi"
    if src_pbi.exists():
        shutil.copytree(src_pbi, dst_pbi, dirs_exist_ok=True)
    # Copy src script
    shutil.copy2(BASE_DIR / "src" / "07_polish_powerbi_theme.py", SCRATCH_DIR / "src" / "07_polish_powerbi_theme.py")
    print("Sync complete.")


def main():
    print("=== Upgrading Power BI Report to Executive Dark Modern Cockpit ===")
    update_dax_measures(BASE_DIR)
    update_base_theme(BASE_DIR)
    update_page_json(BASE_DIR)
    build_all_visuals(BASE_DIR)
    sync_to_scratch()
    print("=== Successfully completed Executive Cockpit redesign! ===")


if __name__ == "__main__":
    main()
