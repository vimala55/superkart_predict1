
import streamlit as st
import pandas as pd
import requests

# ---------------------------------------------------------
# Streamlit UI - Product Store Sales Prediction
# ---------------------------------------------------------

st.title("🛒 Product Store Sales Prediction App")

st.write(
    "This app predicts Product Store Sales based on product and store characteristics."
)

st.write("Enter the product and store details below to get a sales prediction.")


# ---------------------------------------------------------
# Product Information
# ---------------------------------------------------------

st.subheader("Product Information")

Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    max_value=30.0,
    value=12.66,
    step=0.01
)

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    max_value=1.0,
    value=0.027,
    step=0.001
)

Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    max_value=500.0,
    value=117.08,
    step=0.01
)

Product_Id_char = st.selectbox(
    "Product ID Category",
    ["FD", "DR", "NC"]
)

Product_Type = st.text_input(
    "Product Type",
    value="Non Perishables"
)

Product_Type_Category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)


# ---------------------------------------------------------
# Store Information
# ---------------------------------------------------------

st.subheader("Store Information")

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

Store_Type = st.selectbox(
    "Store Type",
    [
        "Grocery Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3"
    ]
)

Store_Id = st.text_input(
    "Store ID",
    value="OUT049"
)

Store_Establishment_Year = st.number_input(
    "Store Establishment Year",
    min_value=1980,
    max_value=2026,
    value=2010,
    step=1
)

Store_Age = st.number_input(
    "Store Age (Years)",
    min_value=0,
    max_value=100,
    value=16,
    step=1
)


# ---------------------------------------------------------
# Create Input DataFrame
# ---------------------------------------------------------

input_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age,
    "Product_Type_Category": Product_Type_Category,

    # Required by the trained preprocessor
    "Store_Age": Store_Age,
    "Store_Establishment_Year": Store_Establishment_Year,
    "Product_Type": Product_Type,
    "Store_Id": Store_Id
}


# ---------------------------------------------------------
# Single Prediction
# ---------------------------------------------------------

if st.button("Predict Sales", type="primary"):

    try:

        response = requests.post(
            "https://vimala55-superkart-predict.hf.space/v1/predict",
            json=input_data
        )

        if response.status_code == 200:

            result = response.json()

            predicted_sales = result.get(
                "prediction",
                result.get("Predicted_Sales")
            )

            if predicted_sales is not None:

                st.success(
                    f"🛒 Predicted Product Store Sales: "
                    f"**{predicted_sales:.2f}**"
                )

            else:
                st.error("Prediction value was not found in API response.")

        else:

            st.error(
                f"Error in API request. "
                f"Status code: {response.status_code}"
            )

            st.write(response.text)

    except Exception as e:

        st.error(f"Unable to connect to the backend API: {e}")


# ---------------------------------------------------------
# Batch Prediction
# ---------------------------------------------------------

st.subheader("📊 Batch Prediction")

st.write(
    "Upload a CSV file containing multiple product/store records "
    "to generate predictions for all records."
)

file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)


if file is not None:

    st.write("Uploaded file preview:")

    uploaded_data = pd.read_csv(file)

    st.dataframe(uploaded_data.head())

    if st.button("Predict for Batch", type="primary"):

        try:

            # Reset file position before sending it
            file.seek(0)

            response = requests.post(
                "https://vimala55-superkart-predict.hf.space/v1/predict_batch",
                files={
                    "file": (
                        file.name,
                        file,
                        "text/csv"
                    )
                }
            )

            if response.status_code == 200:

                result = response.json()

                st.header("Batch Prediction Results")

                st.write(result)

            else:

                st.error(
                    f"Error in batch API request. "
                    f"Status code: {response.status_code}"
                )

                st.write(response.text)

        except Exception as e:

            st.error(
                f"Unable to connect to the backend API: {e}"
            )
