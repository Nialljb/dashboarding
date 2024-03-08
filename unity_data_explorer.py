import streamlit as st
import pandas as pd
import numpy as np
import streamlit_option_menu
from streamlit_option_menu import option_menu
from synthetic_data_explorer import home

with st.sidebar:
    selected = option_menu(
    menu_title = "Main Menu",
    options = ["Home","Warehouse","Inferential Statistics","Contact Us"],
    icons = ["house","gear","activity","envelope"],
    menu_icon = "cast",
    default_index = 0,
)
    
if selected == "Home":
   
   home()

    # st.header('Unity Data Visualisation App')
    # # Create a row layout
    # c1, c2= st.columns(2)
    # c3, c4= st.columns(2)

    # with st.container():
    #     c1.write("c1")
    #     c2.write("c2")

    # with st.container():
    #     c3.write("c3")
    #     c4.write("c4")

    # with c1:
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    #     st.area_chart(chart_data)
           
    # with c2:
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=["a", "b", "c"])
    #     st.bar_chart(chart_data)

    # with c3:
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    #     st.line_chart(chart_data)

    # with c4:
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    #     st.line_chart(chart_data)
        
    
if selected == "Warehouse":
    st.subheader(f"**You Have selected {selected}**")

    
if selected == "Contact":
    st.subheader(f"**You Have selected {selected}**")
