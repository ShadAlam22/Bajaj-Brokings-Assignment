
import requests
BASE = "http://127.0.0.1:8000/api/v1"

def show(label, r):
	print("\n--", label, "--")
	print("Status:", r.status_code)
	try:
		print(r.json())
	except:
		print(r.text)

def test_instruments():
	r = requests.get(BASE+"/instruments/")
	show("Instruments", r)
	return r

def test_place_market_order():
	order = {"symbol": "AAPL", "orderType": "BUY", "orderStyle": "MARKET", "quantity": 5}
	r = requests.post(BASE+"/orders/", json=order)
	show("Place Market Order", r)
	return r

def test_place_limit_order():
	order = {"symbol": "AAPL", "orderType": "SELL", "orderStyle": "LIMIT", "quantity": 2, "price": 200}
	r = requests.post(BASE+"/orders/", json=order)
	show("Place Limit Order", r)
	return r

def test_order_status(order_id):
	r = requests.get(BASE+f"/orders/{order_id}")
	show("Order Status", r)
	return r

def test_trades():
	r = requests.get(BASE+"/trades/")
	show("Trades", r)
	return r

def test_portfolio():
	r = requests.get(BASE+"/portfolio/")
	show("Portfolio", r)
	return r

def test_error_limit_order_missing_price():
	order = {"symbol": "AAPL", "orderType": "SELL", "orderStyle": "LIMIT", "quantity": 2}
	r = requests.post(BASE+"/orders/", json=order)
	show("Error: Limit Order Missing Price", r)
	return r

def test_error_invalid_quantity():
	order = {"symbol": "AAPL", "orderType": "BUY", "orderStyle": "MARKET", "quantity": 0}
	r = requests.post(BASE+"/orders/", json=order)
	show("Error: Invalid Quantity", r)
	return r

if __name__ == "__main__":
	test_instruments()
	m = test_place_market_order()
	l = test_place_limit_order()
	if m.ok:
		test_order_status(m.json()["id"])
	test_trades()
	test_portfolio()
	test_error_limit_order_missing_price()
	test_error_invalid_quantity()
