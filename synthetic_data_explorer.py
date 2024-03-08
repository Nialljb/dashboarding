import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def home():

    # Load the synthetic data CSV file
    # @st.cache_data
    def load_data():
        data = pd.read_csv("synthetic_data.csv")
        return data

    df = load_data()

    # Title
    st.title("Synthetic Data Exploration")

    # # Sidebar filters
    # st.sidebar.header("Filters")
    # unique_sites = df['site'].unique()
    # selected_site = st.sidebar.selectbox("Select Site", options=["All"] + list(unique_sites))

    # if selected_site != "All":
    #     df = df[df['site'] == selected_site]

    # # Sidebar for selecting y-axis variable
    # y_axis_options = df.columns.drop(['subjectID', 'sessionID', 'site', 'sex'])
    # selected_y_axis = st.sidebar.selectbox("Select variable for Y-axis", options=y_axis_options, index=y_axis_options.get_loc('TICV'))

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




    # Assuming 'df' is your DataFrame variable name and it's already loaded with data

    # Identify categorical columns in the DataFrame (excluding 'site' since it's used on x-axis)
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    categorical_columns.remove('site')  # Assuming 'site' should not be in the dropdown

    # Create a dropdown for selecting a categorical variable for coloring
    # Set 'sex' as the default selection if it's among the categorical columns
    default_color_value = 'sex' if 'sex' in categorical_columns else categorical_columns[0]
    color_selection = st.selectbox('Select a categorical variable for coloring:', 
                                options=categorical_columns, 
                                index=categorical_columns.index(default_color_value))

    # Create a boxplot with 'site' on the x-axis, 'age' on the y-axis, and color based on the selected categorical variable
    fig_boxplot = px.box(df, x='site', y='age', color=color_selection,
                        labels={'site': 'Site', 'age': 'Age', color_selection: color_selection},
                        title=f'Age Distribution by Site, colored by {color_selection}')

    # Display the figure in the Streamlit app
    st.plotly_chart(fig_boxplot)





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
    # Exclude non-numeric columns before calculating correlation
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
    st.plotly_chart(fig_corr)


