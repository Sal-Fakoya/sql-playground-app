import streamlit as st
from home import *
from about import *

home_page = st.Page("home.py", title = "Home") 
about_page = st.Page("about.py", title = "About", icon=":material/edit:") 
pg = st.navigation([about_page, home_page])

# st.set_page_config(page_title="SQL Playground App") 
pg.run()


def main():
    pass
    
    

if __name__ == "__main__":
    main()
