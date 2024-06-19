import streamlit as st
import pandas as pd
import os
import zipfile
import io

uploaded_file = st.file_uploader("Upload ZIP file", type=["zip"])
file_name = st.text_input("Enter file name:")

if file_name:
    if uploaded_file:
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            # Extract the contents of the ZIP file to a temporary directory
            temp_dir = 'temp_extracted_files'
            zip_ref.extractall(temp_dir)

        merged_data = pd.DataFrame()

        # Iterate over files in the extracted directory
        for root, dirs, files in os.walk(temp_dir):
            for filename in files:
                if filename.endswith('.csv') or filename.endswith('.xlsx'):
                    filepath = os.path.join(root, filename)
                    try:
                        if filename.endswith('.csv'):
                            data = pd.read_csv(filepath, encoding='ISO-8859-1').fillna("")
                        elif filename.endswith('.xlsx'):
                            data = pd.read_excel(filepath)
                    except Exception as e:
                        st.error(f"Error reading file: {filename}. Skipping...")
                        st.error(e)
                        continue
                    data['File_Name'] = filename
                    merged_data = pd.concat([merged_data, data], ignore_index=True)

        # Reset index starting from 1
        merged_data.index = merged_data.index + 1

        # Use io.StringIO to handle CSV in memory
        csv_buffer = io.StringIO()
        merged_data.to_csv(csv_buffer, index=True, encoding='utf-8')
        csv_buffer.seek(0)

        # Add a download button to download the generated CSV file
        st.download_button(
            label="Download CSV",
            data=csv_buffer,
            file_name=f"{file_name}.csv",
            mime='text/csv'
        )
    else:
        st.warning('Please upload a ZIP file.')
else:
    st.warning('Enter File Name')
