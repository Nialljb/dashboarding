
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the synthetic data CSV file
@st.cache_data
def load_data():
    data = pd.read_csv("synthetic_data.csv")
    return data

df = load_data()

# Title
st.title("Synthetic Data Exploration")

# Sidebar filters
st.sidebar.header("Filters")
unique_sites = df['site'].unique()
selected_site = st.sidebar.selectbox("Select Site", options=["All"] + list(unique_sites))

if selected_site != "All":
    df = df[df['site'] == selected_site]

# Sidebar for selecting y-axis variable
y_axis_options = df.columns.drop(['subjectID', 'sessionID', 'site', 'sex'])
selected_y_axis = st.sidebar.selectbox("Select variable for Y-axis", options=y_axis_options, index=y_axis_options.get_loc('TICV'))


# --- Main Panel ---
# Display dataframe
st.write("Data Overview:", df)
model_options = st.sidebar.selectbox("Select Model for Best Fit", ["None", "Linear (OLS)", "Polynomial", "GLM"])
show_summary_stats = st.sidebar.checkbox("Show Summary Statistics", False)

# Visualization for counts of observations per site
st.write("### Number of scanning sessions per Site")
fig_counts_per_site = px.bar(df.groupby('site').size().reset_index(name='counts'), x='site', y='counts', text='counts')
fig_counts_per_site.update_traces(texttemplate='%{text}', textposition='outside')
fig_counts_per_site.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
st.plotly_chart(fig_counts_per_site)

# Scatter plot for variable selection with age as default X-axis
st.write(f"### Scatter Plot of {selected_y_axis} over Age")

# Determine trendline based on selected model
if model_options == "Linear (OLS)":
    trendline = "ols"
elif model_options == "Polynomial":
    trendline = "lowess"  # Using lowess as a proxy for polynomial fit
elif model_options == "GLM":
    trendline = "lowess"  # Placeholder, customization needed for actual GLM
else:
    trendline = None

fig = px.scatter(df, x="age", y=selected_y_axis, color="sex", title=f"{selected_y_axis} vs Age", trendline=trendline)
st.plotly_chart(fig)

# Show summary statistics if option is selected
if show_summary_stats:
    st.write(df[selected_y_axis].describe())


st.write("### Correlation Matrix")
corr = df.corr()
fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
st.plotly_chart(fig_corr)


