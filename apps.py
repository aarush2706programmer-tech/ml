import streamlit as st
import pandas as pd

st.title("CSV Cleaner App")

uploaded_file = st.file_uploader("Upload CSV")

if uploaded_file:

    # Read CSV
    df = pd.read_csv(uploaded_file)

    st.subheader("Original Data")
    st.write(df)

    # Remove duplicates
    df = df.drop_duplicates()

    # Replace common missing values
    df = df.replace(["None", "NONE", "null", "NULL", ""], pd.NA)

    # Clean columns
    for col in df.columns:

        # Try converting column to numeric
        numeric_col = pd.to_numeric(df[col], errors="coerce")

        # If column is mostly numeric
        if numeric_col.notna().sum() > 0:

            df[col] = numeric_col
            df[col] = df[col].fillna(df[col].mean())

        # Otherwise treat as text
        else:

            df[col] = df[col].astype(str)

            df[col] = df[col].str.strip().str.title()

            df[col] = df[col].replace({
                "M": "Male",
                "F": "Female"
            })

            # Fill missing values with mode
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    st.subheader("Cleaned Data")
    st.write(df)

    # Download cleaned CSV
    csv = df.to_csv(index=False)

    st.download_button(
        "Download Cleaned CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )