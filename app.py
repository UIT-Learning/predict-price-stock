from datetime import datetime
from unicodedata import category
from flask import Flask, escape, request, render_template
import  pickle
from matplotlib.pyplot import close
# from xgboost import XGBRegressor
import numpy as np
# from datetime import datetime
# import oss

app = Flask(__name__)

# port
# port = int(os.environ.get("PORT", 5000))

# app.run(host='0.0.0.0', port=port, debug=True)

model = pickle.load(open('stock_pred_tree', 'rb'))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        open_prices = request.form.get("open_prices")
        close_prices = request.form.get("close_prices")
        high_prices = request.form.get("high_prices")
        low_prices = request.form.get("low_prices")
        volume = request.form.get("volume")
        date = datetime.strptime(request.form['date'],'%Y-%m-%d')
        date_year = date.year
        date_month = date.month
        date_day = date.day
        print(date)
        print(date_year)
        data = [open_prices, high_prices, low_prices,  close_prices, volume, date_year, date_month, date_day]
        dataOutput = data + [date]
        data = np.array(data).reshape(1, -1)
        prediction = model.predict(data)
        output = float(prediction[0])
        return render_template("result.html", prediction_text=output, dataInput=dataOutput)
    else:
        return render_template('index.html')

@app.route("/predict")
def predict():
    return render_template('result.html')

if __name__ == "__main__":
    app.run()