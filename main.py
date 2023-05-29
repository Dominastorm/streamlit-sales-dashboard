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

# Get the unique models and metrics
unique_models = sorted(df["Model"].unique())
metric_types = sorted(df["Metric"].unique())

# Add the models as columns to the dataframe
for i in range(len(unique_models)):
    model = unique_models[i]
    df_user[f"Model - {i}"] = model


print("RUN \n\n\n\n\n\n\n")
# Output is unique for unique (input_idx, model pairs)
# Add Output
for i in range(len(unique_input_idx)):
    for j in range(len(unique_models)):
        row = df.query(f"input_idx == @unique_input_idx[{i}] & Model == @unique_models[{j}]")
        if row.size:
            df_user.at[i, f"Output - {j}"] = list(row["Output"])[0]
        else:
            df_user.at[i, f"Output - {j}"] = None

st.header("User View")
st.dataframe(df_user)
