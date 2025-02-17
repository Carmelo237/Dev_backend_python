from fastapi import FastAPI, Query
from pymongo import MongoClient
from datetime import datetime
import uvicorn

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client['ecommerce']

# Helper function to filter by year
def filter_by_year(pipeline, year):
    if year:
        pipeline.insert(0, {
            '$match': {
                'Order Date': {
                    '$gte': datetime(int(year), 1, 1),
                    '$lt': datetime(int(year) + 1, 1, 1)
                }
            }
        })
    return pipeline

@app.get("/total_sales")
def total_sales(year: int = Query(None)):
    pipeline = [
        {'$group': {'_id': None, 'totalSales': {'$sum': '$Sales'}}}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/total_profits")
def total_profits(year: int = Query(None)):
    pipeline = [
        {'$group': {'_id': None, 'totalProfit': {'$sum': '$Profit'}}}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/total_orders")
def total_orders(year: int = Query(None)):
    pipeline = [
        {'$count': 'Order ID'}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/average_sales")
def average_sales(year: int = Query(None)):
    pipeline = [
        {'$group': {
            '_id': None,
            'totalSales': {'$sum': '$Sales'},
            'orderCount': {'$sum': 1}
        }},
        {'$project': {
            '_id': 0,
            'averageSalesPerOrder': {'$divide': ['$totalSales', '$orderCount']}
        }}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/total_quantity")
def total_quantity(year: int = Query(None)):
    pipeline = [
        {'$group': {'_id': None, 'totalQuantity': {'$sum': '$Quantity'}}}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/total_client")
def total_client(year: int = Query(None)):
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customers ID',
            'foreignField': 'Customers ID',
            'as': 'CustomersDetails'
        }
    }, {
        '$group': {
            '_id': '$Customer ID'
        }
    }, {
        '$count': 'Customers ID'
    }
]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/ship_mode")
def ship_mode(year: int = Query(None)):
    pipeline = [
    {
        '$group': {
            '_id': '$Ship Mode',
            'totalOrders': {
                '$sum': 1
            }
        }
    }, {
        '$sort': {
            'totalOrders': 1
        }
    }
]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/average_per_ship_mode")
def average_per_ship_mode(year: int = Query(None)):
    pipeline = [
    {
        '$project': {
            'Ship Mode': 1,
            'DaysDifference': {
                '$dateDiff': {
                    'startDate': '$Order Date',
                    'endDate': '$Ship Date',
                    'unit': 'day'
                }
            }
        }
    }, {
        '$group': {
            '_id': '$Ship Mode',
            'AverageDaysDifference': {
                '$avg': '$DaysDifference'
            }
        }
    }, {
        '$project': {
            '_id': 1,
            'AverageDaysDifference': {
                '$round': [
                    '$AverageDaysDifference', 1
                ]
            }
        }
    }
]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/quantity_by_category")
def quantity_by_category(year: int = Query(None)):
    pipeline = [
        {
            '$lookup': {
                'from': 'Products',
                'localField': 'Product ID',
                'foreignField': 'Product ID',
                'as': 'ProductDetails'
            }
        },
        {
            '$unwind': '$ProductDetails'
        },
        {
            '$group': {
                '_id': '$ProductDetails.Category',
                'totalQuantity': {
                    '$sum': '$Quantity'
                }
            }
        },
        {
            '$project': {
                'Category': '$_id',
                'totalQuantity': 1,
                '_id': 0
            }
        }
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/category_by_segment")
def category_by_segment(year: int = Query(None)):
    pipeline = [
        {
            '$lookup': {
                'from': 'Products',
                'localField': 'Product ID',
                'foreignField': 'Product ID',
                'as': 'ProductDetails'
            }
        },
        {
            '$unwind': '$ProductDetails'
        },
        {
            '$group': {
                '_id': {
                    'Segment': '$Segment',
                    'Category': '$ProductDetails.Category'
                },
                'TotalOrders': {
                    '$sum': 1  # Count the number of orders for each category
                }
            }
        },
        {
            '$sort': {
                '_id.Segment': 1,  # Sort by Segment alphabetically
                'TotalOrders': -1  # Sort by TotalOrders in descending order
            }
        },
        {
            '$group': {
                '_id': '$_id.Segment',
                'TopCategory': {
                    '$first': '$_id.Category'  # Take only the top category for each segment
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'Segment': '$_id',
                'TopCategory': 1
            }
        }
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/total_orders_by_segment")
def total_orders_by_segment(year: int = Query(None)):
    pipeline = [
        {
            '$group': {
                '_id': '$Segment',
                'TotalOrders': {
                    '$sum': 1
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'Segment': '$_id',
                'TotalOrders': 1
            }
        }
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/revenue_by_segment")
def revenue_by_segment(year: int = Query(None)):
    pipeline = [
        {
            '$group': {
                '_id': '$Segment',
                'totalRevenue': {
                    '$sum': '$Sales'
                }
            }
        },
        {
            '$project': {
                '_id': 0,
                'Segment': '$_id',
                'totalRevenue': 1
            }
        }
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/total_orders_by_category")
def total_orders_by_category(year: int = Query(None)):
    pipeline = [
        {
            '$lookup': {
                'from': 'Products',
                'localField': 'Product ID',
                'foreignField': 'Product ID',
                'as': 'ProductDetails'
            }
        },
        {
            '$unwind': '$ProductDetails'
        },
        {
            '$group': {
                '_id': '$ProductDetails.Category',
                'totalOrders': {
                    '$sum': 1
                }
            }
        },
        {
            '$project': {
                'Category': '$_id',
                'totalOrders': 1,
                '_id': 0
            }
        }
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/revenue_by_category")
def revenue_by_category(year: int = Query(None)):
    pipeline = [
        {
            '$lookup': {
                'from': 'Products',
                'localField': 'Product ID',
                'foreignField': 'Product ID',
                'as': 'ProductDetails'
            }
        },
        {
            '$unwind': '$ProductDetails'
        },
        {
            '$group': {
                '_id': '$ProductDetails.Category',
                'totalSales': {
                    '$sum': '$Sales'
                }
            }
        },
        {
            '$project': {
                'Category': '$_id',
                'totalSales': 1,
                '_id': 0
            }
        }
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/average_orders_by_customers")
def average_orders_by_customers(year: int = Query(None)):
    pipeline = [
        {'$group': {'_id': '$Customer ID', 'orderCount': {'$sum': 1}}},
        {'$group': {'_id': None, 'averageOrdersPerCustomer': {'$avg': '$orderCount'}}}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result

@app.get("/retention_by_customers")
def retention_by_customers(year: int = Query(None)):
    pipeline = [
    {
        '$lookup': {
            'from': 'Customers',
            'localField': 'Customer ID',
            'foreignField': 'Customer ID',
            'as': 'CustomerDetails'
        }
    }, {
        '$unwind': '$CustomerDetails'
    }, {
            '$group': {
            '_id': '$CustomerDetails.Customer Name',
            'firstOrderDate': {'$min': '$Order Date'},
            'lastOrderDate': {'$max': '$Order Date'},
            'orderCount': {'$sum': 1}
        }},
        {'$project': {
            'Customer Name': '$_id',
            'firstOrderDate': 1,
            'lastOrderDate': 1,
            'orderCount': 1,
            'retentionPeriodDays': {
                '$divide': [
                    {'$subtract': ['$lastOrderDate', '$firstOrderDate']},
                    1000 * 60 * 60 * 24
                ]
            }
        }},
        {'$match': {'orderCount': {'$gt': 1}}}
    ]
    result = list(db.Orders.aggregate(filter_by_year(pipeline, year)))
    return result


@app.get("/years")
def get_years():
    years = db.Orders.distinct("Order Date")
    unique_years = sorted(set([d.year for d in years]))
    return unique_years

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
