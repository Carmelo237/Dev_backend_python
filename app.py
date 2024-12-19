import requests

response = requests.request(method="get",url="http://localhost:8000/total_sales")
print(response.text)
