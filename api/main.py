from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import math  # 🔴 CHANGED

# Create FastAPI App
app = FastAPI(
    title="Taxi Fare Prediction",
    version="1.0.0"
)

model = joblib.load(
    r"taxi_Fare_model.pkl"
)


# Input data structure
class TaxiInput(BaseModel):

    pickup_longitude: float
    pickup_latitude: float

    dropoff_longitude: float
    dropoff_latitude: float

    passenger_count: int
    pickup_hour: int
    pickup_day_of_week: int
    is_weekend: int

    # 🔴 CHANGED
    # trip_distance is removed because FastAPI will calculate it


# Home route
@app.get("/")
def home():
    return {"message": "Taxi Fare prediction API is running"}


# 🔴 CHANGED
# Haversine distance calculation
def calculate_distance(
    pickup_longitude,
    pickup_latitude,
    dropoff_longitude,
    dropoff_latitude
):

    # Convert degrees to radians
    lon1 = math.radians(pickup_longitude)
    lat1 = math.radians(pickup_latitude)

    lon2 = math.radians(dropoff_longitude)
    lat2 = math.radians(dropoff_latitude)

    # Difference
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.asin(math.sqrt(a))

    # Earth's radius in kilometers
    radius = 6371

    distance = radius * c

    return distance


# Prediction route
@app.post("/predict")
def predict(data: TaxiInput):

    # 🔴 CHANGED
    # Calculate trip distance automatically
    trip_distance = calculate_distance(
        data.pickup_longitude,
        data.pickup_latitude,
        data.dropoff_longitude,
        data.dropoff_latitude
    )

    features = [[
        data.pickup_longitude,
        data.pickup_latitude,
        data.dropoff_longitude,
        data.dropoff_latitude,
        data.passenger_count,
        data.pickup_hour,
        data.pickup_day_of_week,
        data.is_weekend,
        trip_distance
    ]]

    prediction = model.predict(features)

    return {
        "predicted_fare": round(float(prediction[0]), 2),
        "trip_distance": round(trip_distance, 2)  # 🔴 CHANGED
    }











# from fastapi import FastAPI
# from pydantic import BaseModel
# import joblib

# # Create fastApi App

# app = FastAPI(title="Taxi Fare Prediction" , version= "1.0.0")
# model = joblib.load(r"C:/Users/aksha/OneDrive\Desktop/Machine learning/ML Projects/taxi_Fare_model.pkl")

# # Input data structure
# class TaxiInput(BaseModel):
#     pickup_longitude: float
#     pickup_latitude: float
#     dropoff_longitude: float
#     dropoff_latitude: float
#     passenger_count: int
#     pickup_hour: int
#     pickup_day_of_week: int
#     is_weekend: int
#     trip_distance: float

# @app.get("/")
# def home():
#     return{"message ":"Taxi Fare prediction API is running" }

# # prediction route
# # @app.get("/predict")
# # def predict(
# #     pickup_longitude: float,
# #     pickup_latitude: float,
# #     dropoff_longitude: float,
# #     dropoff_latitude: float,
# #     passenger_count: int,
# #     pickup_hour: int,
# #     pickup_day_of_week: int,
# #     is_weekend: int,
# #     trip_distance: float
# # ):

# #     features = [[
# #         pickup_longitude,
# #         pickup_latitude,
# #         dropoff_longitude,
# #         dropoff_latitude,
# #         passenger_count,
# #         pickup_hour,
# #         pickup_day_of_week,
# #         is_weekend,
# #         trip_distance
# #     ]]

# #     prediction = model.predict(features)

# #     return {
# #         "predicted_fare": round(float(prediction[0]), 2)
# #     }
# @app.post("/predict")
# def predict(data: TaxiInput):

#     features = [[
#         data.pickup_longitude,
#         data.pickup_latitude,
#         data.dropoff_longitude,
#         data.dropoff_latitude,
#         data.passenger_count,
#         data.pickup_hour,
#         data.pickup_day_of_week,
#         data.is_weekend,
#         data.trip_distance
#     ]]

#     prediction = model.predict(features)

#     return {
#         "predicted_fare": round(float(prediction[0]), 2)
#     }