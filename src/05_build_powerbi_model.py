"""
05_build_powerbi_model.py
Programmatically constructs the Microsoft Fabric TMDL Semantic Model for Power BI Desktop.
"""

import os
import uuid
import json

def build_powerbi_model():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    processed_data_dir = os.path.join(base_dir, "data", "processed")
    pbi_dir = os.path.join(base_dir, "power_bi")
    sem_dir = os.path.join(pbi_dir, "powerbi report.SemanticModel", "definition")
    tables_dir = os.path.join(sem_dir, "tables")
    os.makedirs(tables_dir, exist_ok=True)

    norm_path = lambda filename: os.path.join(processed_data_dir, filename).replace("/", "\\")

    def gen_tmdl(template, replacements):
        res = template
        for k, v in replacements.items():
            res = res.replace(k, v)
        # Replace any remaining @U@ with fresh uuid
        while "@U@" in res:
            res = res.replace("@U@", str(uuid.uuid4()), 1)
        return res

    # 1. dim_customers
    dim_cust_tpl = """table dim_customers
\tlineageTag: @U@

\tcolumn customer_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: customer_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn age
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: age

\t\tannotation SummarizationSetBy = User

\tcolumn age_group
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: age_group

\t\tannotation SummarizationSetBy = Automatic

\tcolumn gender
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: gender

\t\tannotation SummarizationSetBy = Automatic

\tcolumn location
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: location

\t\tannotation SummarizationSetBy = Automatic

\tcolumn subscription_status
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: subscription_status

\t\tannotation SummarizationSetBy = Automatic

\tcolumn loyalty_tier
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: loyalty_tier

\t\tannotation SummarizationSetBy = Automatic

\tcolumn cluster_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: count
\t\tsourceColumn: cluster_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn customer_segment
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: customer_segment

\t\tannotation SummarizationSetBy = Automatic

\tpartition dim_customers = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("@PATH@"),[Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"customer_id", Int64.Type}, {"age", Int64.Type}, {"age_group", type text}, {"gender", type text}, {"location", type text}, {"subscription_status", type text}, {"loyalty_tier", type text}, {"cluster_id", Int64.Type}, {"customer_segment", type text}})
\t\t\tin
\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(tables_dir, "dim_customers.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(dim_cust_tpl, {"@PATH@": norm_path("dim_customers.csv")}))

    # 2. dim_products
    dim_prod_tpl = """table dim_products
\tlineageTag: @U@

\tcolumn product_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: product_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn item_purchased
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: item_purchased

\t\tannotation SummarizationSetBy = Automatic

\tcolumn category
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: category

\t\tannotation SummarizationSetBy = Automatic

\tcolumn size
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: size

\t\tannotation SummarizationSetBy = Automatic

\tcolumn color
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: color

\t\tannotation SummarizationSetBy = Automatic

\tpartition dim_products = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("@PATH@"),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"product_id", Int64.Type}, {"item_purchased", type text}, {"category", type text}, {"size", type text}, {"color", type text}})
\t\t\tin
\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(tables_dir, "dim_products.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(dim_prod_tpl, {"@PATH@": norm_path("dim_products.csv")}))

    # 3. dim_shipping
    dim_ship_tpl = """table dim_shipping
\tlineageTag: @U@

\tcolumn shipping_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: shipping_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn shipping_type
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: shipping_type

\t\tannotation SummarizationSetBy = Automatic

\tcolumn sales_channel
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: sales_channel

\t\tannotation SummarizationSetBy = Automatic

\tpartition dim_shipping = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("@PATH@"),[Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"shipping_id", Int64.Type}, {"shipping_type", type text}, {"sales_channel", type text}})
\t\t\tin
\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(tables_dir, "dim_shipping.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(dim_ship_tpl, {"@PATH@": norm_path("dim_shipping.csv")}))

    # 4. dim_payment
    dim_pay_tpl = """table dim_payment
\tlineageTag: @U@

\tcolumn payment_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: payment_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn payment_method
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: payment_method

\t\tannotation SummarizationSetBy = Automatic

\tpartition dim_payment = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("@PATH@"),[Delimiter=",", Columns=2, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"payment_id", Int64.Type}, {"payment_method", type text}})
\t\t\tin
\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(tables_dir, "dim_payment.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(dim_pay_tpl, {"@PATH@": norm_path("dim_payment.csv")}))

    # 5. fact_transactions
    fact_tpl = """table fact_transactions
\tlineageTag: @U@

\tcolumn transaction_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: count
\t\tsourceColumn: transaction_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn customer_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: customer_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn product_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: product_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn shipping_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: shipping_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn payment_id
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: payment_id

\t\tannotation SummarizationSetBy = Automatic

\tcolumn season
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: season

\t\tannotation SummarizationSetBy = Automatic

\tcolumn purchase_amount_usd
\t\tdataType: double
\t\tformatString: \\$#,##0.00
\t\tlineageTag: @U@
\t\tsummarizeBy: sum
\t\tsourceColumn: purchase_amount_usd

\t\tannotation SummarizationSetBy = Automatic

\tcolumn review_rating
\t\tdataType: double
\t\tformatString: 0.00
\t\tlineageTag: @U@
\t\tsummarizeBy: average
\t\tsourceColumn: review_rating

\t\tannotation SummarizationSetBy = Automatic

\tcolumn review_rating_imputed
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: sum
\t\tsourceColumn: review_rating_imputed

\t\tannotation SummarizationSetBy = Automatic

\tcolumn discount_applied
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: discount_applied

\t\tannotation SummarizationSetBy = Automatic

\tcolumn promo_code_used
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: promo_code_used

\t\tannotation SummarizationSetBy = Automatic

\tcolumn previous_purchases
\t\tdataType: int64
\t\tformatString: 0
\t\tlineageTag: @U@
\t\tsummarizeBy: sum
\t\tsourceColumn: previous_purchases

\t\tannotation SummarizationSetBy = Automatic

\tcolumn frequency_of_purchases
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: frequency_of_purchases

\t\tannotation SummarizationSetBy = Automatic

\tcolumn annual_purchase_frequency
\t\tdataType: double
\t\tformatString: 0.0
\t\tlineageTag: @U@
\t\tsummarizeBy: average
\t\tsourceColumn: annual_purchase_frequency

\t\tannotation SummarizationSetBy = Automatic

\tcolumn estimated_annual_spend
\t\tdataType: double
\t\tformatString: \\$#,##0.00
\t\tlineageTag: @U@
\t\tsummarizeBy: sum
\t\tsourceColumn: estimated_annual_spend

\t\tannotation SummarizationSetBy = Automatic

\tcolumn estimated_clv
\t\tdataType: double
\t\tformatString: \\$#,##0.00
\t\tlineageTag: @U@
\t\tsummarizeBy: sum
\t\tsourceColumn: estimated_clv

\t\tannotation SummarizationSetBy = Automatic

\tcolumn spending_tier
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: spending_tier

\t\tannotation SummarizationSetBy = Automatic

\tcolumn satisfaction_level
\t\tdataType: string
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: satisfaction_level

\t\tannotation SummarizationSetBy = Automatic

\tpartition fact_transactions = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Csv.Document(File.Contents("@PATH@"),[Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.None]),
\t\t\t    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
\t\t\t    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"transaction_id", Int64.Type}, {"customer_id", Int64.Type}, {"product_id", Int64.Type}, {"shipping_id", Int64.Type}, {"payment_id", Int64.Type}, {"season", type text}, {"purchase_amount_usd", type number}, {"review_rating", type number}, {"review_rating_imputed", Int64.Type}, {"discount_applied", type text}, {"promo_code_used", type text}, {"previous_purchases", Int64.Type}, {"frequency_of_purchases", type text}, {"annual_purchase_frequency", type number}, {"estimated_annual_spend", type number}, {"estimated_clv", type number}, {"spending_tier", type text}, {"satisfaction_level", type text}})
\t\t\tin
\t\t\t    #"Changed Type"

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(tables_dir, "fact_transactions.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(fact_tpl, {"@PATH@": norm_path("fact_transactions.csv")}))

    # 6. _Measures
    measures_tpl = """table _Measures
\tlineageTag: @U@

\tmeasure 'Total Revenue' = SUM(fact_transactions[purchase_amount_usd])
\t\tformatString: \\$#,##0
\t\tlineageTag: @U@

\tmeasure 'Total Transactions' = COUNTROWS(fact_transactions)
\t\tformatString: #,##0
\t\tlineageTag: @U@

\tmeasure 'Total Customers' = DISTINCTCOUNT(fact_transactions[customer_id])
\t\tformatString: #,##0
\t\tlineageTag: @U@

\tmeasure 'Average Order Value' = DIVIDE([Total Revenue], [Total Transactions], 0)
\t\tformatString: \\$#,##0.00
\t\tlineageTag: @U@

\tmeasure 'Average Customer Rating' = AVERAGE(fact_transactions[review_rating])
\t\tformatString: 0.00
\t\tlineageTag: @U@

\tmeasure 'Subscription Rate %' = DIVIDE(CALCULATE(DISTINCTCOUNT(fact_transactions[customer_id]), dim_customers[subscription_status] = "Yes"), [Total Customers], 0)
\t\tformatString: 0.0%
\t\tlineageTag: @U@

\tmeasure 'Discount Penetration %' = DIVIDE(CALCULATE([Total Transactions], fact_transactions[discount_applied] = "Yes"), [Total Transactions], 0)
\t\tformatString: 0.0%
\t\tlineageTag: @U@

\tmeasure 'Online Shipping Share %' = DIVIDE(CALCULATE([Total Revenue], dim_shipping[sales_channel] = "Online Shipping"), [Total Revenue], 0)
\t\tformatString: 0.0%
\t\tlineageTag: @U@

\tmeasure 'In-Store Pickup Share %' = DIVIDE(CALCULATE([Total Revenue], dim_shipping[sales_channel] = "In-Store Pickup"), [Total Revenue], 0)
\t\tformatString: 0.0%
\t\tlineageTag: @U@

\tmeasure 'Female Revenue' = CALCULATE([Total Revenue], dim_customers[gender] = "Female")
\t\tformatString: \\$#,##0
\t\tlineageTag: @U@

\tmeasure 'Male Revenue' = CALCULATE([Total Revenue], dim_customers[gender] = "Male")
\t\tformatString: \\$#,##0
\t\tlineageTag: @U@

\tmeasure 'Female Customers' = CALCULATE([Total Customers], dim_customers[gender] = "Female")
\t\tformatString: #,##0
\t\tlineageTag: @U@

\tmeasure 'Male Customers' = CALCULATE([Total Customers], dim_customers[gender] = "Male")
\t\tformatString: #,##0
\t\tlineageTag: @U@

\tmeasure 'Female AOV' = CALCULATE([Average Order Value], dim_customers[gender] = "Female")
\t\tformatString: \\$#,##0.00
\t\tlineageTag: @U@

\tmeasure 'Male AOV' = CALCULATE([Average Order Value], dim_customers[gender] = "Male")
\t\tformatString: \\$#,##0.00
\t\tlineageTag: @U@

\tmeasure 'Simulated Female Subscribers' = ROUND([Female Customers] * [Female Adoption Rate Value], 0)
\t\tformatString: #,##0
\t\tlineageTag: @U@

\tmeasure 'Simulated Incremental Revenue' = [Simulated Female Subscribers] * [Female AOV] * 2.8
\t\tformatString: \\$#,##0
\t\tlineageTag: @U@

\tmeasure 'Total Projected Revenue' = [Total Revenue] + [Simulated Incremental Revenue]
\t\tformatString: \\$#,##0
\t\tlineageTag: @U@

\tmeasure 'Projected Revenue Lift %' = DIVIDE([Simulated Incremental Revenue], [Total Revenue], 0)
\t\tformatString: +0.0%
\t\tlineageTag: @U@

\tcolumn Placeholder
\t\tdataType: string
\t\tisHidden
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tsourceColumn: Placeholder

\t\tannotation SummarizationSetBy = Automatic

\tpartition _Measures = m
\t\tmode: import
\t\tsource =
\t\t\tlet
\t\t\t    Source = Table.FromRows(Json.Document(Binary.Decompress(Binary.FromText("i44FAA==", BinaryEncoding.Base64), Compression.Deflate)), let _t = ((type nullable text) meta [Serialized.Text = true]) in type table [Placeholder = _t])
\t\t\tin
\t\t\t    Source

\tannotation PBI_ResultType = Table
"""
    with open(os.path.join(tables_dir, "_Measures.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(measures_tpl, {}))

    # 7. Female Subscription Adoption Rate
    param_tpl = """table 'Female Subscription Adoption Rate'
\tlineageTag: @U@

\tmeasure 'Female Adoption Rate Value' = SELECTEDVALUE('Female Subscription Adoption Rate'[Female Subscription Adoption Rate], 0.0)
\t\tformatString: 0.0%
\t\tlineageTag: @U@

\tcolumn 'Female Subscription Adoption Rate'
\t\tdataType: double
\t\tformatString: 0.0%
\t\tlineageTag: @U@
\t\tsummarizeBy: none
\t\tisDataTypeInferred
\t\tsourceColumn: [Value]

\t\textendedProperty ParameterMetadata =
\t\t\t{
\t\t\t  "version": 0,
\t\t\t  "parameterKind": 0
\t\t\t}

\t\tannotation SummarizationSetBy = User

\tpartition 'Female Subscription Adoption Rate' = calculated
\t\tmode: import
\t\tsource = GENERATESERIES(0.0, 1.0, 0.05)

\tannotation PBI_Id = 9b8a7c6d5e4f3a2b1c0d
"""
    with open(os.path.join(tables_dir, "Female Subscription Adoption Rate.tmdl"), "w", encoding="utf-8") as f:
        f.write(gen_tmdl(param_tpl, {}))

    # 8. relationships.tmdl
    rel_tpl = """relationship rel_fact_to_dim_customers
\tfromColumn: fact_transactions.customer_id
\ttoColumn: dim_customers.customer_id

relationship rel_fact_to_dim_products
\tfromColumn: fact_transactions.product_id
\ttoColumn: dim_products.product_id

relationship rel_fact_to_dim_shipping
\tfromColumn: fact_transactions.shipping_id
\ttoColumn: dim_shipping.shipping_id

relationship rel_fact_to_dim_payment
\tfromColumn: fact_transactions.payment_id
\ttoColumn: dim_payment.payment_id
"""
    with open(os.path.join(sem_dir, "relationships.tmdl"), "w", encoding="utf-8") as f:
        f.write(rel_tpl)

    # 9. model.tmdl
    model_tpl = """model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tvalueFilterBehavior: independent
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

annotation __PBI_TimeIntelligenceEnabled = 1

annotation PBI_ProTooling = ["DevMode"]

ref table dim_customers
ref table dim_products
ref table dim_shipping
ref table dim_payment
ref table fact_transactions
ref table _Measures
ref table 'Female Subscription Adoption Rate'

ref cultureInfo en-US
"""
    with open(os.path.join(sem_dir, "model.tmdl"), "w", encoding="utf-8") as f:
        f.write(model_tpl)

    # 10. Update Page Name in Report
    page_json_path = os.path.join(pbi_dir, "powerbi report.Report", "definition", "pages", "e2d88bab65d02ef79d4f", "page.json")
    if os.path.exists(page_json_path):
        with open(page_json_path, "r", encoding="utf-8") as f:
            p_data = json.load(f)
        p_data["displayName"] = "Executive Revenue Cockpit"
        with open(page_json_path, "w", encoding="utf-8") as f:
            json.dump(p_data, f, indent=2)

    print("Power BI Semantic Model & TMDL Architecture successfully built!")

if __name__ == "__main__":
    build_powerbi_model()
