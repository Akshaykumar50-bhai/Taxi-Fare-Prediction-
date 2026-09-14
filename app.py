import streamlit as st
import requests


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Taxi Fare Prediction",
    page_icon="🚕",
    layout="centered"
)


st.title("🚕 Taxi Fare Prediction")

st.write("Enter the trip details")

st.divider()


# --------------------------------------------------
# Location Details
# --------------------------------------------------

st.subheader("📍 Location Details")

st.info(
    "Valid NYC coordinate range: "
    "Longitude -75 to -72 | Latitude 39 to 42"
)


pickup_longitude = st.number_input(
    "Pickup Longitude",
    value=-73.985,
    format="%.6f"
)


pickup_latitude = st.number_input(
    "Pickup Latitude",
    value=40.780,
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


# --------------------------------------------------
# Trip Details
# --------------------------------------------------

st.subheader("🚕 Trip Details")


passenger_count = st.number_input(
    "Passenger Count",
    min_value=1,
    max_value=6,
    value=2,
    step=1
)


# Trip distance is NOT entered by the user.
# FastAPI calculates it using the Haversine formula.


# --------------------------------------------------
# Pickup Time
# --------------------------------------------------

st.subheader("🕐 Pickup Time")


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
    1 if pickup_day_of_week >= 5 else 0
)


st.write(
    f"Weekend: {'Yes' if is_weekend else 'No'}"
)


st.divider()


# --------------------------------------------------
# Prediction
# --------------------------------------------------

if st.button(
    "💰 Predict Fare",
    use_container_width=True
):

    # --------------------------------------------------
    # Data sent to FastAPI
    # --------------------------------------------------

    data = {

        "pickup_longitude": pickup_longitude,

        "pickup_latitude": pickup_latitude,

        "dropoff_longitude": dropoff_longitude,

        "dropoff_latitude": dropoff_latitude,

        "passenger_count": passenger_count,

        "pickup_hour": pickup_hour,

        "pickup_day_of_week": pickup_day_of_week,

        "is_weekend": is_weekend
    }


    try:

        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json=data,
            timeout=10
        )


        # --------------------------------------------------
        # Successful Prediction
        # --------------------------------------------------

        if response.status_code == 200:

            result = response.json()

            fare = result["predicted_fare"]

            trip_distance = result["trip_distance"]


            st.success(
                "Prediction successful!"
            )


            st.metric(
                label="Estimated Taxi Fare",
                value=f"${fare:.2f}"
            )


            st.info(
                f"📏 Calculated Trip Distance: "
                f"{trip_distance:.2f} km"
            )


        # --------------------------------------------------
        # Validation Error
        # --------------------------------------------------

        elif response.status_code == 400:

            error_data = response.json()

            st.error(
                f"❌ {error_data['detail']}"
            )


        # --------------------------------------------------
        # Other API Errors
        # --------------------------------------------------

        else:

            st.error(
                f"API Error: {response.status_code}"
            )


    # --------------------------------------------------
    # Connection Error
    # --------------------------------------------------

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to FastAPI. "
            "Make sure the FastAPI server is running."
        )


    # --------------------------------------------------
    # Timeout Error
    # --------------------------------------------------

    except requests.exceptions.Timeout:

        st.error(
            "❌ FastAPI request timed out."
        )


    # --------------------------------------------------
    # Unexpected Error
    # --------------------------------------------------

    except Exception as e:

        st.error(
            f"❌ Unexpected Error: {e}"
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
