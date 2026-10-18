"""
06_build_powerbi_visuals.py
Programmatically constructs the PBIR visualContainer JSON definitions
for the Executive Revenue Cockpit page in Power BI Desktop.
Fulfills the rule:
"A real dashboard answers one business question, it's intuitive and highlights the insight without having them to hunt for it."
"""

import os
import json
import uuid

def u():
    return str(uuid.uuid4()).replace("-", "")[:20]

def build_visuals():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pbi_dir = os.path.join(base_dir, "power_bi")
    page_dir = os.path.join(pbi_dir, "powerbi report.Report", "definition", "pages", "e2d88bab65d02ef79d4f")
    visuals_dir = os.path.join(page_dir, "visuals")
    os.makedirs(visuals_dir, exist_ok=True)

    schema_vc = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.1.0/schema.json"

    def write_visual(v_name, v_data):
        v_folder = os.path.join(visuals_dir, v_name)
        os.makedirs(v_folder, exist_ok=True)
        v_path = os.path.join(v_folder, "visual.json")
        with open(v_path, "w", encoding="utf-8") as f:
            json.dump(v_data, f, indent=2)

    # ================= 1. KPI Cards (Top Ribbon) =================
    # Card 1: Total Revenue ($233K)
    card_rev = {
        "$schema": schema_vc,
        "name": "Card_Total_Revenue",
        "position": {
            "x": 40.0,
            "y": 50.0,
            "z": 1000.0,
            "width": 430.0,
            "height": 170.0,
            "tabOrder": 1000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Total Revenue"
                                    }
                                },
                                "queryRef": "_Measures.Total Revenue",
                                "nativeQueryRef": "Total Revenue"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_total_revenue", card_rev)

    # Card 2: Average Order Value ($59.76)
    card_aov = {
        "$schema": schema_vc,
        "name": "Card_AOV",
        "position": {
            "x": 500.0,
            "y": 50.0,
            "z": 2000.0,
            "width": 430.0,
            "height": 170.0,
            "tabOrder": 2000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Average Order Value"
                                    }
                                },
                                "queryRef": "_Measures.Average Order Value",
                                "nativeQueryRef": "Average Order Value"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_aov", card_aov)

    # Card 3: Average Rating (3.75)
    card_rating = {
        "$schema": schema_vc,
        "name": "Card_Rating",
        "position": {
            "x": 960.0,
            "y": 50.0,
            "z": 3000.0,
            "width": 430.0,
            "height": 170.0,
            "tabOrder": 3000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Average Customer Rating"
                                    }
                                },
                                "queryRef": "_Measures.Average Customer Rating",
                                "nativeQueryRef": "Average Customer Rating"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_rating", card_rating)

    # Card 4: Subscription Rate (27.0%)
    card_sub = {
        "$schema": schema_vc,
        "name": "Card_Subscription_Rate",
        "position": {
            "x": 1420.0,
            "y": 50.0,
            "z": 4000.0,
            "width": 460.0,
            "height": 170.0,
            "tabOrder": 4000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Subscription Rate %"
                                    }
                                },
                                "queryRef": "_Measures.Subscription Rate %",
                                "nativeQueryRef": "Subscription Rate %"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_subscription_rate", card_sub)

    # ================= 2. Middle Row: Revenue Concentration & Fulfillment =================
    # Visual 5: Column Chart - Total Revenue by Product Category
    chart_category = {
        "$schema": schema_vc,
        "name": "Chart_Category_Revenue",
        "position": {
            "x": 40.0,
            "y": 250.0,
            "z": 5000.0,
            "width": 1050.0,
            "height": 380.0,
            "tabOrder": 5000.0
        },
        "visual": {
            "visualType": "columnChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "dim_products"
                                            }
                                        },
                                        "Property": "category"
                                    }
                                },
                                "queryRef": "dim_products.category",
                                "nativeQueryRef": "category"
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Total Revenue"
                                    }
                                },
                                "queryRef": "_Measures.Total Revenue",
                                "nativeQueryRef": "Total Revenue"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("chart_category_revenue", chart_category)

    # Visual 6: Donut Chart - Sales Fulfillment Channel Share
    chart_fulfillment = {
        "$schema": schema_vc,
        "name": "Chart_Fulfillment_Channel",
        "position": {
            "x": 1120.0,
            "y": 250.0,
            "z": 6000.0,
            "width": 760.0,
            "height": 380.0,
            "tabOrder": 6000.0
        },
        "visual": {
            "visualType": "donutChart",
            "query": {
                "queryState": {
                    "Category": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "dim_shipping"
                                            }
                                        },
                                        "Property": "sales_channel"
                                    }
                                },
                                "queryRef": "dim_shipping.sales_channel",
                                "nativeQueryRef": "sales_channel"
                            }
                        ]
                    },
                    "Y": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Total Revenue"
                                    }
                                },
                                "queryRef": "_Measures.Total Revenue",
                                "nativeQueryRef": "Total Revenue"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("chart_fulfillment_channel", chart_fulfillment)

    # ================= 3. Bottom Row: Interactive What-If Simulation Panel =================
    # Visual 7: Slicer Slider for What-If Parameter
    slicer_param = {
        "$schema": schema_vc,
        "name": "Slicer_Female_Adoption_Rate",
        "position": {
            "x": 40.0,
            "y": 660.0,
            "z": 7000.0,
            "width": 560.0,
            "height": 370.0,
            "tabOrder": 7000.0
        },
        "visual": {
            "visualType": "slicer",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "Female Subscription Adoption Rate"
                                            }
                                        },
                                        "Property": "Female Subscription Adoption Rate"
                                    }
                                },
                                "queryRef": "Female Subscription Adoption Rate.Female Subscription Adoption Rate",
                                "nativeQueryRef": "Female Subscription Adoption Rate"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("slicer_female_adoption_rate", slicer_param)

    # Visual 8: Card - Simulated Incremental Revenue (The Highlighted Insight!)
    card_sim_rev = {
        "$schema": schema_vc,
        "name": "Card_Simulated_Incremental_Revenue",
        "position": {
            "x": 630.0,
            "y": 660.0,
            "z": 8000.0,
            "width": 460.0,
            "height": 370.0,
            "tabOrder": 8000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Simulated Incremental Revenue"
                                    }
                                },
                                "queryRef": "_Measures.Simulated Incremental Revenue",
                                "nativeQueryRef": "Simulated Incremental Revenue"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_simulated_incremental_revenue", card_sim_rev)

    # Visual 9: Card - Total Projected Revenue
    card_proj_rev = {
        "$schema": schema_vc,
        "name": "Card_Total_Projected_Revenue",
        "position": {
            "x": 1120.0,
            "y": 660.0,
            "z": 9000.0,
            "width": 360.0,
            "height": 370.0,
            "tabOrder": 9000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Total Projected Revenue"
                                    }
                                },
                                "queryRef": "_Measures.Total Projected Revenue",
                                "nativeQueryRef": "Total Projected Revenue"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_total_projected_revenue", card_proj_rev)

    # Visual 10: Card - Projected Revenue Lift %
    card_lift = {
        "$schema": schema_vc,
        "name": "Card_Projected_Revenue_Lift",
        "position": {
            "x": 1510.0,
            "y": 660.0,
            "z": 10000.0,
            "width": 370.0,
            "height": 370.0,
            "tabOrder": 10000.0
        },
        "visual": {
            "visualType": "card",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [
                            {
                                "field": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Entity": "_Measures"
                                            }
                                        },
                                        "Property": "Projected Revenue Lift %"
                                    }
                                },
                                "queryRef": "_Measures.Projected Revenue Lift %",
                                "nativeQueryRef": "Projected Revenue Lift %"
                            }
                        ]
                    }
                }
            }
        }
    }
    write_visual("card_projected_revenue_lift", card_lift)

    print(f"Successfully generated 10 PBIR visuals in: {visuals_dir}")

if __name__ == "__main__":
    build_visuals()
