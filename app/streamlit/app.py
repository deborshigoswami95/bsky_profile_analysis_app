import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

SRC_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src/')
sys.path.append(SRC_PATH)

from follows import follows

st.set_page_config(layout="wide")
if 'handle' not in st.session_state:
    st.session_state['handle'] = ''

def clear_input():
    st.session_state['handle'] = ''

# Title and description
st.title("Bluesky User Analysis App")
st.write("No data is collected or stored in the backend.\nThis app uses an end-to-end data science pipeline to analyze bluesky profile data given an input user")

follows = follows()

col1, col2 = st.columns([1,3])

with col1:
    st.header('BSKY Handle')
    st.write('Please input the desired user\'s Bluesky handle')

    with st.form(key='handle_form', clear_on_submit=True):
        handle = st.text_input("Enter Handle", value=st.session_state['handle'], key='handle_input')
        submit_button = st.form_submit_button(label = 'submit')

    if submit_button:
        st.session_state['handle'] = handle
        

if handle:
    with col2:
        follows.handle = handle
        st.markdown(f"### Processing handle: {st.session_state['handle']}")

        with st.spinner('Querying Follows Data... '):
            follows.get_all_follows()
        
        with st.spinner('Processing Bios... '):
            follows.compile_bios_to_DF()

        with st.spinner('Generating Plot... '):
            plot = follows.plot_follow_bio_stats()

        st.pyplot(plot)
        st.session_state['handle'] = ''