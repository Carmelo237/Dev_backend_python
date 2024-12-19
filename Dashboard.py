from pymongo import MongoClient
import pandas as pd
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']
# Charger la collection "orders" en DataFrame
orders = pd.DataFrame(list(db.orders.find()))
print(orders.head())
