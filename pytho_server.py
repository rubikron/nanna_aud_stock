from flask import Flask, redirect, url_for,render_template,request,session
import requests
import json
from yahoo_finance_api2 import share
# import api_request.get_val_of_USD_AUD
def get_val_of_USD_AUD(default_Currency = "AUD"):
	# api key: lIw8UEukEd0E95lpfFLl54cptJri8BiSjaya
	# probably not needed since it is mentioned in url
	url = "https://currencyapi.net/api/v1/rates?key=lIw8UEukEd0E95lpfFLl54cptJri8BiSjaya&base=USD"
	response = requests.request("GET", url)
	response = json.loads(response.content)
	USD_to_AUD = (response["rates"][default_Currency])
	my_share = share.Share('LIFX')
	symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,3	,share.FREQUENCY_TYPE_MINUTE,1)["open"][0]
	return {"currency_conversion":USD_to_AUD,"life360_share_price_AUD":round(symbol_data,3),"life360_share_price_USD":round((symbol_data/USD_to_AUD),3)}
app = Flask(__name__)
@app.route("/")
def home():
	web_page_info = get_val_of_USD_AUD()
	return render_template("user_interface.html", AUD_val = str(web_page_info["currency_conversion"]),LIFX_stock_val_AUD = str(web_page_info["life360_share_price_AUD"]), LIFX_stock_val_USD = round(web_page_info["life360_share_price_USD"] * 3,3))

@app.route("/<some_link>")
def invalid_url(some_link):
	return redirect(url_for("home"))

if __name__ == "__main__":
	app.run(debug = True)

