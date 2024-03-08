import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from scipy.stats import pearsonr

def home():

    # Load the synthetic data CSV file
    # @st.cache_data
    def load_data():
        data = pd.read_csv("synthetic_data.csv")
        return data

    df = load_data()

    # Title
    st.title("Synthetic Data Exploration")

    # --- Main Panel ---
    # Display dataframe
    # st.write("Data Overview:", df)

    # Visualization for counts of observations per site
    st.write("### Number of scanning sessions per Site")
    fig_counts_per_site = px.bar(df.groupby('site').size().reset_index(name='counts'), x='site', y='counts', text='counts')
    fig_counts_per_site.update_traces(texttemplate='%{text}', textposition='outside')
    fig_counts_per_site.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    st.plotly_chart(fig_counts_per_site)


    # Create a boxplot with 'site' on the x-axis, 'age' on the y-axis, and color based on the selected categorical variable
    fig_boxplot = px.box(df, x='site', y='age', color='sex',
                        labels={'site': 'Site', 'age': 'Age', 'Sex': 'sex'},
                        title=f'Age Distribution by Site')

    # Display the figure in the Streamlit app
    st.plotly_chart(fig_boxplot)



def warehouse():

    # Load the synthetic data CSV file
    # @st.cache_data
    def load_data():
        data = pd.read_csv("synthetic_data.csv")
        return data

    df = load_data()

    # Title
    st.title("Synthetic Data Exploration")

    # --- Main Panel ---
    # Display dataframe
    st.write("Data Overview:", df)
    


def stats():

    # Load the synthetic data CSV file
    # @st.cache_data
    def load_data():
        data = pd.read_csv("synthetic_data.csv")
        return data

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    unique_sites = df['site'].unique()
    selected_site = st.sidebar.selectbox("Select Site", options=["All"] + list(unique_sites))

    if selected_site != "All":
        df = df[df['site'] == selected_site]

    # Title
    st.title("Study Descriptive Statistics")
    st.write("### Select study filter in the sidebar")

    # User selection for categorical variable
    categorical_vars = ['sex', 'group']  # List of categorical columns
    selected_cat_var = st.selectbox('Select a categorical variable for statistics:', options=categorical_vars)

    # User selection for continuous variable
    continuous_vars = ['age', 'weight']  # List of continuous columns
    selected_cont_var = st.selectbox('Select a continuous variable for statistics:', options=continuous_vars)

    # Placeholder for the descriptive statistics table
    stats_placeholder = st.empty()

    # Calculate and display descriptive statistics for the selected variable, grouped by the selected categorical variable
    if selected_cat_var and selected_cont_var:
        # Calculate descriptive statistics for the selected continuous variable
        descriptive_stats = df.groupby(selected_cat_var)[selected_cont_var].describe()

        # Display the statistics
        stats_placeholder.write(f"Descriptive Statistics for {selected_cont_var} based on {selected_cat_var}:")
        stats_placeholder.dataframe(descriptive_stats)


    # Title
    st.title("Synthetic Data Exploration")

    # Name of plot..
    if 'color_selection' not in st.session_state:
        st.session_state.color_selection = 'sex'  # Default value

    # Placeholder to display the plot
    plot_placeholder = st.empty()

    # Render the plot (initially with the default or stored color selection)
    fig = px.box(df, x='site', y='age', color=st.session_state.color_selection,
                labels={'site': 'Site', 'age': 'Age'},
                title=f'Age Distribution by Site, grouped by {st.session_state.color_selection}')
    plot_placeholder.plotly_chart(fig)

    # Color selection widget (below the plot)
    color_selection = st.selectbox('Select a categorical variable for group comparison:',
                                options=['sex'],  # Extend this list with your categorical columns
                                index=0,
                                key='color_selector')

    # Update the plot based on the new selection
    if color_selection != st.session_state.color_selection:
        st.session_state.color_selection = color_selection
        fig = px.box(df, x='site', y='age', color=color_selection,
                    labels={'site': 'Site', 'age': 'Age'},
                    title=f'Age Distribution by Site, grouped by {color_selection}')
        plot_placeholder.plotly_chart(fig)


    # Scatter plot for variable selection with age as default X-axis
    st.write(f"### Scatter Plot over Age")
    # Dropdown for selecting y-axis variable
    y_axis_options = df.columns.drop(['subjectID', 'sessionID', 'site', 'sex'])
    selected_y_axis = st.selectbox("Select variable for Y-axis", options=y_axis_options, index=y_axis_options.get_loc('TICV'))
    model_options = st.selectbox("Select Model for Best Fit", ["None", "Linear (OLS)", "Polynomial", "GLM"])
    show_summary_stats = st.checkbox("Show Summary Statistics", False)

    # Determine trendline based on selected model
    if model_options == "Linear (OLS)":
        trendline = "ols"
    elif model_options == "Polynomial":
        trendline = "lowess"  # Using lowess as a proxy for polynomial fit
    elif model_options == "GLM":
        trendline = "lowess"  # Placeholder, customization needed for actual GLM
    else:
        trendline = None

    # Checkbox to show correlation coefficient
    show_corr = st.checkbox('Show correlation coefficient between selected variables')

    # Create scatter plot
    fig = px.scatter(df, x="age", y=selected_y_axis, color="sex", title=f"{selected_y_axis} vs Age", trendline=trendline)
    st.plotly_chart(fig)

    # # Calculate and display correlation coefficient if checkbox is selected
    # if show_corr:
    #     corr_coef = df[["age", selected_y_axis]].corr().iloc[0, 1]  # Calculating the correlation coefficient
    #     st.write(f'Correlation coefficient between age and {selected_y_axis}: {corr_coef:.3f}')

    # Calculate and display correlation coefficient and p-value if checkbox is selected
    if show_corr:
        corr_coef, p_value = pearsonr(df["age"], df[selected_y_axis])  # Calculating the correlation coefficient and p-value
        st.write(f'Correlation coefficient between age and {selected_y_axis}: {corr_coef:.3f}')
        st.write(f'P-value: {p_value:.3g}')  # Using general format for scientific notation if needed

    # Show summary statistics if option is selected
    if show_summary_stats:
        st.write(df[selected_y_axis].describe())

    st.write("### Correlation Matrix")
    # Exclude non-numeric columns before calculating correlation
    numeric_df = df.select_dtypes(include=[np.number])
    corr = numeric_df.corr()
    fig_corr = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Matrix")
    st.plotly_chart(fig_corr)



