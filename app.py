import streamlit as st
import requests

st.set_page_config(
    page_title="Taxi Fare prediction",
    page_icon="🚕",
    layout="centered"
)

st.title("🚕 Taxi Fare Prediction")

st.write("Enter the trip details")

st.divider()

st.subheader("Location Details")

pickup_longitude = st.number_input(
    "Pickup Longitude",
    value=-73.985,
    format="%.6f"
)

pickup_latitude = st.number_input(
    "Pickup Latitude",
    value=40.78,
    format="%.6f"
)

dropoff_longitude = st.number_input(
    "Dropoff Longitude",
    value=-73.985,
    format="%.6f"
)

dropoff_latitude = st.number_input(
    "Dropoff Latitude",
    value=40.785,
    format="%.6f"
)


st.subheader("Trip Details")

passenger_count = st.number_input(
    "Passenger Count",
    min_value=1,
    max_value=6,
    value=2,
    step=1
)

# 🔴 CHANGED
# Trip distance input removed.
# FastAPI calculates it using Haversine formula.


st.subheader("Pickup Time")

pickup_hour = st.slider(
    "Pickup Hour",
    min_value=0,
    max_value=23,
    value=18
)

days = {
    "Monday": 0,
    "Tuesday": 1,
    "Wednesday": 2,
    "Thursday": 3,
    "Friday": 4,
    "Saturday": 5,
    "Sunday": 6
}

selected_day = st.selectbox(
    "Pickup Day",
    list(days.keys())
)

pickup_day_of_week = days[selected_day]

is_weekend = (
    1 if days[selected_day] >= 5 else 0
)

st.write(
    f"Weekend: {'Yes' if is_weekend else 'No'}"
)

st.divider()


# -----------------------------
# Prediction
# -----------------------------

if st.button(
    "💰 Predict Fare",
    use_container_width=True
):

    data = {

        "pickup_longitude": pickup_longitude,

        "pickup_latitude": pickup_latitude,

        "dropoff_longitude": dropoff_longitude,

        "dropoff_latitude": dropoff_latitude,

        "passenger_count": passenger_count,

        "pickup_hour": pickup_hour,

        "pickup_day_of_week": pickup_day_of_week,

        "is_weekend": is_weekend

        # 🔴 CHANGED
        # trip_distance is no longer sent.
    }


    try:

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=data,
            timeout=10
        )

        st.write(
            "Status:",
            response.status_code
        )

        st.write(
            "Response:",
            response.text
        )


        if response.status_code == 200:

            result = response.json()

            fare = result["predicted_fare"]

            # 🔴 CHANGED
            trip_distance = result["trip_distance"]

            st.success(
                "Prediction successful!"
            )

            st.metric(
                label="Estimated Taxi Fare",
                value=f"${fare:.2f}"
            )

            # 🔴 CHANGED
            st.info(
                f"Calculated Trip Distance: "
                f"{trip_distance:.2f} km"
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )


    except requests.exceptions.ConnectionError as e:

        st.error(
            f"Connection Error: {e}"
        )


    except requests.exceptions.Timeout:

        st.error(
            "FastAPI request timed out."
        )


    except Exception as e:

        st.error(
            f"Unexpected Error: {e}"
        )











# import streamlit as st
# import requests
# st.set_page_config(
#     page_title="Taxi Fare prediction",
#     page_icon="🚕",
#     layout="centered"
# )
# st.title("🚕 Taxi Fare Prediction")
# st.write("Enter the trip details")

# st.divider()

# st.subheader("Location Details")

# pickup_longitude = st.number_input("Pickup Longitude",value=-73.985,format="%.6f")

# pickup_latitude = st.number_input("pickup Latitude",value=40.78,format="%.6f")

# dropoff_longitude = st.number_input("Dropoff Longitude",value=-73.985,format="%.6f")

# dropoff_latitude = st.number_input("Dropoff Latitude",value=40.785,format="%.6f")

# st.subheader("Trip details")

# passenger_count = st.number_input("Passenger Count",min_value=1,max_value=6,value=2,step=1)

# trip_distance = st.number_input("Trip Distance", min_value=0.1,value=2.5,step=0.1)

# st.subheader("Pickup Time")

# pickup_hour = st.slider(
#     "Pickup Hour",
#     min_value=0,
#     max_value=23,
#     value=18
# )

# days = {
#     "Monday": 0,
#     "Tuesday": 1,
#     "Wednesday": 2,
#     "Thursday": 3,
#     "Friday": 4,
#     "Saturday": 5,
#     "Sunday": 6
# }

# selected_day = st.selectbox("Pickup Day",list(days.keys()))

# pickup_day_of_week = days[selected_day]

# is_weekend = 1 if days[selected_day] >= 5 else 0

# st.write(
#     f"Weekend: {'Yes' if is_weekend else 'No'}"
# )

# st.divider()


# # -----------------------------
# # Prediction
# # -----------------------------

# if st.button("💰 Predict Fare", use_container_width=True):

#     data = {
#         "pickup_longitude": pickup_longitude,
#         "pickup_latitude": pickup_latitude,
#         "dropoff_longitude": dropoff_longitude,
#         "dropoff_latitude": dropoff_latitude,
#         "passenger_count": passenger_count,
#         "pickup_hour": pickup_hour,
#         "pickup_day_of_week": pickup_day_of_week,
#         "is_weekend": is_weekend,
#         "trip_distance": trip_distance
#     }

#     # try:

#     #     response = requests.post(
#     #         "http://127.0.0.1:8000/predict",
#     #         json=data
#     #     )

#     #     if response.status_code == 200:

#     #         result = response.json()

#     #         fare = result["predicted_fare"]

#     #         st.success("Prediction successful!")

#     #         st.metric(
#     #             label="Estimated Taxi Fare",
#     #             value=f"${fare:.2f}"
#     #         )

#     #     else:

#     #         st.error(
#     #             f"API Error: {response.status_code}"
#     #         )

#     # except requests.exceptions.ConnectionError:

#     #     st.error(
#     #         "Could not connect to FastAPI. "
#     #         "Make sure the FastAPI server is running."
#     #     )
#     try:
#         response = requests.post(
#             "http://127.0.0.1:8000/predict",
#             json=data,
#             timeout=10
#         )

#         st.write("Status:", response.status_code)
#         st.write("Response:", response.text)

#         if response.status_code == 200:

#             result = response.json()

#             fare = result["predicted_fare"]

#             st.success("Prediction successful!")

#             st.metric(
#                 label="Estimated Taxi Fare",
#                 value=f"${fare:.2f}"
#             )

#         else:
#             st.error(f"API Error: {response.status_code}")

#     except requests.exceptions.ConnectionError as e:
#         st.error(f"Connection Error: {e}")

#     except requests.exceptions.Timeout:
#         st.error("FastAPI request timed out.")

#     except Exception as e:
#         st.error(f"Unexpected Error: {e}")