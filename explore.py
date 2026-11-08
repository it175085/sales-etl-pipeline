import pandas as pd

df = pd.read_csv("data/sales_raw.csv")

print(df.head(), end="\n\n")#Διαβάζει το CSV σε DataFrame.
print(df.shape, end="\n\n")#Δείχνει τις πρώτες γραμμές.
df.info()#Δείχνει πόσες γραμμές και στήλες έχει.
print()
print(df.isna().sum(), end="\n\n")#Δείχνει τον τύπο κάθε στήλης (αριθμός; κείμενο;).
print(df.duplicated().sum(), end="\n\n")#Μετράει τα κενά σε κάθε στήλη.
print(df["city"].value_counts(), end="\n\n")#Μετράει τις διπλές γραμμές.
print(df["payment_method"].value_counts(), end="\n\n")#Δείχνει τις μοναδικές τιμές των στηλών city και payment_method.

print(df["product"].value_counts(), end="\n\n")
print(df["quantity"].value_counts(), end="\n\n")
print(df["unit_price"].value_counts(), end="\n\n")


