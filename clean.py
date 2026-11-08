import pandas as pd

df = pd.read_csv("data/sales_raw.csv")

df = df.drop_duplicates()
df["city"] = df["city"].str.strip()  #Η εντολή που αφαιρεί κενά από αρχή και τέλος 
df["customer_name"] = df["customer_name"].str.strip()
df["product"] = df["product"].str.strip()

city_map = {
    "Λαρισα":"Λάρισα",
    "Πατρα":"Πάτρα",
    "ΠΑΤΡΑ":"Πάτρα",
    "thessaloniki":"Θεσσαλονίκη",
    "Θεσ/νίκη":"Θεσσαλονίκη",
    "ΘΕΣΣΑΛΟΝΙΚΗ":"Θεσσαλονίκη",
    "Αθηνα":"Αθήνα",
    "ΑΘΗΝΑ":"Αθήνα",
    "athens":"Αθήνα",
    "ΗΡΑΚΛΕΙΟ":"Ηράκλειο",
}
df["city"] = df["city"].replace(city_map)

payment_method_map = {
    "ΚΑΡΤΑ":"Κάρτα",
    "card":"Κάρτα",
    "μετρητα":"Μετρητά",
}
df["payment_method"] = df["payment_method"].replace(payment_method_map)
df["payment_method"] = df["payment_method"].fillna("Άγνωστο")

df["unit_price"] = df["unit_price"].str.strip()
df["unit_price"] = df["unit_price"].str.replace(",",".")
df["unit_price"] = df["unit_price"].str.replace("€","")
df["unit_price"] = pd.to_numeric(df["unit_price"])
df.loc[df["unit_price"]==650,"unit_price"] = 6.5

df["quantity"] = df["quantity"].str.replace(" τεμ","")
df["quantity"] = pd.to_numeric(df["quantity"])
df = df[df["quantity"] > 0]
df["quantity"] = df["quantity"].astype(int)  

d1 = pd.to_datetime(df["order_date"], format="%Y-%m-%d",errors="coerce")
d2 = pd.to_datetime(df["order_date"], format="%d/%m/%Y",errors="coerce")
d3 = pd.to_datetime(df["order_date"], format="%d-%m-%Y",errors="coerce")
df["order_date"] = d1.fillna(d2).fillna(d3)

df = df.dropna(subset=["order_date","customer_name"])

product_map = {
    "ΚΑΦΈΣ ESPRESSO 250G":"Καφές Espresso 250g",
    "ΤΣΆΙ ΠΡΆΣΙΝΟ":"Τσάι Πράσινο",
    "ΤΣΆΙ ΒΟΥΝΟΎ":"Τσάι Βουνού",
    "ΚΟΎΠΑ ΚΕΡΑΜΙΚΉ":"Κούπα Κεραμική",
    "ΣΟΚΟΛΆΤΑ ΥΓΕΊΑΣ":"Σοκολάτα Υγείας",
    }
df["product"] = df["product"].replace(product_map)

product_category = {
    "Τσάι Βουνού":"Τσάι",
    "Κούπα Κεραμική":"Αξεσουάρ",
    "Καφές Φίλτρου 500g":"Καφές",
    "Καφές Espresso 250g":"Καφές",
    "Σοκολάτα Υγείας":"Σνακ",
    "Θερμός 500ml":"Αξεσουάρ",
    "Τσάι Πράσινο":"Τσάι",
    "Μπισκότα Βρώμης":"Σνακ",
}
df["category"] = df["product"].map(product_category)

df["customer_name"]=df["customer_name"].str.title()

print(df.shape)
print(df["city"].value_counts(),end="\n\n")
print(df["payment_method"].value_counts(dropna=False),end="\n\n")
print(df["unit_price"].dtype,end="\n\n")
print(df["unit_price"].value_counts(),end="\n\n")
print(df["quantity"].value_counts(),end="\n\n")
print(df["order_date"].isna().sum())
print(df["order_date"].min(), df["order_date"].max(),end="\n\n")
print(df["product"].value_counts(),end="\n\n")
print(df["category"].value_counts(dropna=False))
print(df["category"].isna().sum(),end="\n\n")
print(df["category"].value_counts(dropna=False),end="\n\n")
print(df["customer_name"].nunique(),end="\n\n")

df.to_csv("data/sales_clean.csv", index=False, encoding="utf-8-sig")
print("Αποθηκεύτηκε στο data/sales_clean.csv ✅")
