from fastapi import FastAPI
from pymongo import MongoClient
import uvicorn

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']

@app.on_event("startup")
async def create_indexes():
    db.Customers.create_index("Customer ID")
    db.Products.create_index("Products ID")
    db.Location.create_index("Postal Code")
    db.Orders.create_index("Order Date")
    print("✅ Indexes created successfully")

@app.get("/orders-with-details")
def get_orders_with_details():
    pipeline = [
        {
            '$lookup': {
                'from': 'Customers',
                'localField': 'Customer ID',
                'foreignField': 'Customer ID',
                'as': 'CustomerDetails'
            }
        },
        {
            '$lookup': {
                'from': 'Products',
                'localField': 'Products ID',
                'foreignField': 'Products ID',
                'as': 'ProductsDetails'
            }
        },
        {
            '$lookup': {
                'from': 'Location',
                'localField': 'Postal Code',
                'foreignField': 'Postal Code',
                'as': 'LocationDetails'
            }
        }
    ]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/total_sales")
def total_sales():
    pipeline = [
 {
            '$group': {
                '_id': None,
                'totalSales': {
                    '$sum': '$Sales'
                }
            }
        }
    ]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/total_profits")
def total_profits():
    pipeline = [
 {
            '$group': {
                '_id': None,
                'totalProfit': {
                    '$sum': '$Profit'
                }
            }
        }
    ]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/total_orders")
def total_orders():
    pipeline = [
{
            '$count': 'Order ID'
        }
    ]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/average_sales")
def average_sales():
    pipeline = [
{
        '$group': {
            '_id': None,
            'totalSales': {
                '$sum': '$Sales'
            },
            'orderCount': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 0,
            'averageSalesPerOrder': {
                '$divide': [
                    '$totalSales', '$orderCount'
                ]
            }
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/total_quantity")
def total_quantity():
    pipeline = [
{
        '$group': {
            '_id': None,
            'totalQuantity': {
                '$sum': '$Quantity'
            }
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/total_client")
def total_client():
    pipeline = [
    {
        '$count': 'Customers ID'
    }
]

    result = list(db.Customers.aggregate(pipeline))
    return result

@app.get("/orders_by_customers")
def orders_by_customers():
    pipeline = [
{
        '$group': {
            '_id': '$Customer ID',
            'orderCount': {
                '$sum': 1
            }
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/average_orders_by_customers")
def average_orders_by_customers():
    pipeline = [
    {
        '$group': {
            '_id': '$Customer ID',
            'orderCount': {
                '$sum': 1
            }
        }
    }, {
        '$group': {
            '_id': None,
            'averageOrdersPerCustomer': {
                '$avg': '$orderCount'
            }
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/retention_by_customers")
def retention_by_customers():
    pipeline = [
{
        '$group': {
            '_id': '$Customer ID',
            'firstOrderDate': {
                '$min': '$Order Date'
            },
            'lastOrderDate': {
                '$max': '$Order Date'
            },
            'orderCount': {
                '$sum': 1
            }
        }
    }, {
        '$project': {
            '_id': 1,
            'firstOrderDate': 1,
            'lastOrderDate': 1,
            'orderCount': 1,
            'retentionPeriodDays': {
                '$divide': [
                    {
                        '$subtract': [
                            '$lastOrderDate', '$firstOrderDate'
                        ]
                    }, 1000 * 60 * 60 * 24
                ]
            }
        }
    }, {
        '$match': {
            'orderCount': {
                '$gt': 1
            }
        }
    }
]
    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/quantity_per_products")
def quantity_per_products():
    pipeline = [
{
        '$group': {
            '_id': '$Product ID',
            'quantity_per_products': {
                '$sum': '$Quantity'
            }
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/total_orders_per_products")
def total_orders_per_products():
    pipeline = [
{
        '$group': {
            '_id': '$Product ID',
            'total_orders_per_products': {
                '$count': {}
            }
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result

@app.get("/revenus_by_products")
def revenus_by_products():
    pipeline = [
{
        '$group': {
            '_id': '$Product ID',
            'totalRevenue': {
                '$sum': '$Sales'
            }
        }
    }, {
        '$sort': {
            'totalRevenue': -1
        }
    }
]

    result = list(db.Orders.aggregate(pipeline))
    return result



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)