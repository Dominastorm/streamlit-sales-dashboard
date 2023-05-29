# pip install plotly-express

import pandas as pd  
import plotly.express as px   
import streamlit as st  

st.set_page_config(page_title="LLM Dashboard")

# ---- READ CSV ----
@st.cache
def get_data_from_csv():
    df = pd.read_csv(
        "LLM.csv",
        sep=",",
        nrows=1000,
    )
    return df

# Create dataframe
df = get_data_from_csv()

# ---- FILTERING ----
def filter_template(attribute):
    return st.multiselect(
        f"Select the {attribute}:",
        options=df[attribute].unique(),
        default=df[attribute].unique()
    )

# Create filters
model = filter_template("Model")
feature = filter_template("Feature")
metric = filter_template("Metric")

# Apply filters
df_selection = df.query(
    "Model == @model & Feature == @feature & Metric == @metric"
)

st.dataframe(df_selection)
