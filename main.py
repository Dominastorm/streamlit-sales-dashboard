# pip install plotly-express

import pandas as pd  
import plotly.express as px   
import streamlit as st  

st.set_page_config(page_title="LLM Dashboard", layout="wide")
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
def filter_template(attribute, default_all=False):
    container = st.container()
    all = st.checkbox(f"Select all {attribute}", value=default_all)
    
    if all:
        selected_options = container.multiselect("Select one or more options:",
            df[attribute].unique(),df[attribute].unique())
    else:
        selected_options =  container.multiselect("Select one or more options:",
            df[attribute].unique())
    return selected_options

# Create filters
model_filter = filter_template("Model")
feature_filter = filter_template("Feature", True)
metric_filter = filter_template("Metric")


# Apply filters
df_selection = df.query(
    "Model == @model_filter & Feature == @feature_filter & Metric == @metric_filter"
)

# ---- INTERNAL STORAGE ----
# st.header("Internal Storage")
# st.dataframe(df_selection)


# ---- USER VIEW ---- 

# Get the unique input_idx
unique_input_idx = sorted(df["input_idx"].unique())

# Create a dataframe for the user view
df_user = pd.DataFrame({"input_idx": unique_input_idx})


# Add Input Var
for i in range(len(unique_input_idx)):
    row = df.query(f"input_idx == @unique_input_idx[{i}]")
    df_user.at[i, "Input - Var1"] = list(row["Input - Var1"])[0]
    df_user.at[i, "Input - Var2"] = list(row["Input - Var2"])[0]
    df_user.at[i, "Input - Var3"] = list(row["Input - Var3"])[0]
    df_user.at[i, "Input - Var4"] = list(row["Input - Var4"])[0]
    feature = list(row["Feature"])[0]
    if feature_filter and feature in feature_filter:
        df_user.at[i, "Feature"] = feature

# Apply feature filter
try:
    if df_user["Feature"] is not None:
        df_user = df_user[df_user["Feature"].isin(feature_filter)]
except KeyError:
    raise KeyError("No Feature is Chosen")

# Add the models as columns to the dataframe
for i in range(len(model_filter)):
    model = model_filter[i]
    df_user[f"Model - {i}"] = model

# Output is unique for unique (input_idx, model pairs)
# Add Output
for i in range(len(unique_input_idx)):
    for j in range(len(model_filter)):
        row = df_selection.query(f"input_idx == @unique_input_idx[{i}] & Model == @model_filter[{j}]")
        if row.size:
            df_user.at[i, f"Output - {j}"] = list(row["Output"])[0]
        else:
            df_user.at[i, f"Output - {j}"] = None

# Add Metrics as Columns
for i in range(len(unique_input_idx)):
    input_idx = unique_input_idx[i]
    for j in range(len(metric_filter)):
        metric = metric_filter[j]
        for k in range(len(model_filter)):
            model = model_filter[k]
            row = df_selection.query(f"input_idx == @input_idx & Model == @model & Metric == @metric")
            if row.size:
                df_user.at[i, f"{metric} - {k}"] = list(row["Score"])[0]
            else:
                df_user.at[i, f"{metric} - {k}"] = None

st.header("User View")
st.dataframe(df_user)
