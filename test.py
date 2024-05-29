import streamlit as st
import pandas as pd
import os
import zipfile

filepath = 'temp_extracted_files/S4084 Data V2 20240417.xlsx'
data = pd.read_excel(filepath)

st.write(data)
