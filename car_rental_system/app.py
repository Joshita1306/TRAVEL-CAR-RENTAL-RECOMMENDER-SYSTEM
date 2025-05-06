from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session

# Load car data
def load_car_data():
    csv_path = "C:/Users/ruths/Desktop/car_rental_system/data/car_data_final.csv"
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df.to_dict('records')
    return [
        {"id": 1, "name": "Toyota Corolla", "type": "Sedan", "seats": 5, "price": 50},
        {"id": 2, "name": "Honda CR-V", "type": "SUV", "seats": 5, "price": 70}
    ]

cars = load_car_data()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Extract all form data
        form_data = {
            'email': request.form["email"],
            'destination': request.form["destination"],
            'pickup_date': request.form["pickup_date"],
            'return_date': request.form["return_date"],
            'adults': int(request.form["adults"]),
            'children': int(request.form["children"]),
            'car_type': request.form["car_type"],
            'budget_min': float(request.form["budget_min"]),
            'budget_max': float(request.form["budget_max"]),
            'rental_purpose': request.form.get("rental_purpose", "vacation")
        }

        # Calculate total passengers
        total_passengers = form_data['adults'] + form_data['children']

        # Filter cars
        recommended_cars = [
            car for car in cars
            if (car["seats"] >= total_passengers and
                car["type"].lower() == form_data['car_type'].lower() and
                form_data['budget_min'] <= car["price"] <= form_data['budget_max'])
        ]

        # Store in session for pagination
        session['filtered_cars'] = recommended_cars
        session['current_index'] = 0
        session['form_data'] = form_data  # Store all form data

        # Prepare results
        return render_template(
            "results.html",
            cars=recommended_cars[:7],
            more_available=len(recommended_cars) > 7,
            remaining_cars=max(0, len(recommended_cars) - 7),
            **form_data  # Unpack all form data to template
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return redirect(url_for('index'))

@app.route("/show_more", methods=["POST"])
def show_more():
    filtered_cars = session.get('filtered_cars', [])
    current_index = session.get('current_index', 0)
    form_data = session.get('form_data', {})

    # Rotate through cars (7 at a time)
    new_index = (current_index + 7) % len(filtered_cars)
    session['current_index'] = new_index

    # Get next 7 cars with wrap-around
    next_cars = filtered_cars[new_index:new_index+7]
    if len(next_cars) < 7:
        next_cars += filtered_cars[:7 - len(next_cars)]

    return render_template(
        "results.html",
        cars=next_cars,
        more_available=len(filtered_cars) > 7,
        remaining_cars=max(0, len(filtered_cars) - (new_index + 7)),
        **form_data
    )

@app.route("/car_details/<int:car_id>",methods=["GET"] )
def car_details(car_id):
    car = next((car for car in cars if car["id"] == car_id), None)
    if not car:
        return redirect(url_for('index'))

    # Get dates and purpose from URL params
    pickup_date = request.args.get("pickup_date")
    return_date = request.args.get("return_date")
    rental_purpose = request.args.get("rental_purpose", "vacation")

    # Calculate rental details
    try:
        days = (datetime.strptime(return_date, "%Y-%m-%d") - 
               datetime.strptime(pickup_date, "%Y-%m-%d")).days
        total_cost = car["price"] * days
    except:
        return redirect(url_for('index'))

    return render_template(
        "car_details.html",
        car=car,
        pickup_date=pickup_date,
        return_date=return_date,
        rental_days=days,
        total_cost=total_cost,
        rental_purpose=rental_purpose
    )

@app.route("/confirm_booking", methods=["POST"])
def confirm_booking():
    try:
        car_id = int(request.form["car_id"])
        car = next((car for car in cars if car["id"] == car_id), None)
        if not car:
            return redirect(url_for('index'))

        return render_template(
            "confirmation.html",
            car=car,
            total_cost=float(request.form["total_cost"]),
            rental_days=int(request.form["rental_days"]),
            pickup_date=request.form["pickup_date"],
            return_date=request.form["return_date"],
            pickup_location=request.form.get("pickup_location","Airport"),
            rental_purpose=request.form.get("rental_purpose", "vacation")
        )
    except:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)