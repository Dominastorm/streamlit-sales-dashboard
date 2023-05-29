# pip install plotly-express

import pandas as pd  
import plotly.express as px   
import streamlit as st  

st.set_page_config(page_title="LLM Dashboard")
st.header("LLM Dashboard")

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

# ---- INTERNAL STORAGE ----

st.header("Internal Storage")
st.dataframe(df_selection)


# ---- USER VIEW ---- 

df_user = df_selection.copy()

# Get the unique models and metrics
model_types = sorted(df["Model"].unique())
metric_types = sorted(df["Metric"].unique())

# Add the models as columns to the dataframe
for i in range(len(model_types)):
    model = model_types[i]
    df_user[f"Model-{i}"] = model

print('\n\n')


# Drop row_idx and Model columns
df_user = df_user.drop(columns=["row_idx", "Model"])

st.header("User View")
st.dataframe(df_user)

