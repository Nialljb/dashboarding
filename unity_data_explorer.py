import streamlit as st
from streamlit_option_menu import option_menu
from app.synthetic_data_explorer import home
from app.synthetic_data_explorer import warehouse
from app.synthetic_data_explorer import stats

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
if selected == "Warehouse":
    st.subheader(f"**You Have selected {selected}**")
    warehouse()
if selected == "Contact":
    st.subheader(f"**You Have selected {selected}**")
    stats()
