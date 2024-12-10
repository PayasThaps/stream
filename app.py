# -- coding: utf-8 --
"""Enhanced Marketing Dashboard"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Set up Streamlit app configuration
st.set_page_config(page_title="Enhanced Marketing Dashboard", layout="wide")

# Load dataset
uploaded_file = "https://github.com/vaidyamohit/Marketing-Dashboard/raw/main/Dataset%20Marketing.xlsx"

@st.cache_data
def load_data():
    return pd.read_excel(uploaded_file, engine="openpyxl")

data = load_data()

# Title
st.title("Enhanced Marketing Dashboard 📊")

# Sidebar Filters
st.sidebar.header("Filters")
category_column = st.sidebar.selectbox(
    "Select a Category Column:",
    [col for col in data.columns if data[col].dtype == "object"]
)
numerical_column = st.sidebar.selectbox(
    "Select a Numerical Column:",
    [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
)
data_filter = st.sidebar.text_input(
    "Apply Filter (e.g., Sales > 5000 or Category == 'Electronics'):",
    value=""
)
apply_filter = st.sidebar.button("Apply Filter")

# Apply filter
filtered_df = data.copy()
if apply_filter and data_filter:
    try:
        filtered_df = filtered_df.query(data_filter)
        st.sidebar.success("Filter applied successfully!")
    except Exception as e:
        st.sidebar.error(f"Invalid filter: {e}")

# Insights Section
st.subheader("Key Insights")
col1, col2, col3, col4 = st.columns(4)
try:
    total_value = filtered_df[numerical_column].sum()
    avg_value = filtered_df[numerical_column].mean()
    max_value = filtered_df[numerical_column].max()
    min_value = filtered_df[numerical_column].min()

    col1.metric(f"Total {numerical_column}", f"{total_value:,.2f}")
    col2.metric(f"Average {numerical_column}", f"{avg_value:,.2f}")
    col3.metric(f"Max {numerical_column}", f"{max_value:,.2f}")
    col4.metric(f"Min {numerical_column}", f"{min_value:,.2f}")
except Exception as e:
    st.error(f"Error calculating insights: {e}")

# Graphs Section
st.subheader("Visualizations")

# Bar Chart
if not filtered_df.empty:
    st.plotly_chart(
        px.bar(
            filtered_df.groupby(category_column)[numerical_column].sum().reset_index(),
            x=category_column,
            y=numerical_column,
            title=f"Bar Chart: {numerical_column} by {category_column}",
            labels={category_column: category_column, numerical_column: numerical_column}
        ),
        use_container_width=True
    )

    # Pie Chart
    st.plotly_chart(
        px.pie(
            filtered_df.groupby(category_column)[numerical_column].sum().reset_index(),
            names=category_column,
            values=numerical_column,
            title=f"Pie Chart: {numerical_column} Distribution by {category_column}"
        ),
        use_container_width=True
    )

    # Scatter Plot
    st.plotly_chart(
        px.scatter(
            filtered_df,
            x=category_column,
            y=numerical_column,
            title=f"Scatter Plot: {numerical_column} vs {category_column}",
            labels={category_column: category_column, numerical_column: numerical_column}
        ),
        use_container_width=True
    )
else:
    st.warning("No data available for the selected filters.")

# Data Table Section
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)

# Download Option
st.subheader("Download Filtered Data")
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)
