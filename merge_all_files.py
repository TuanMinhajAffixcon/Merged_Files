import streamlit as st
import pandas as pd
import os
import zipfile

uploaded_file = st.file_uploader("Upload ZIP file", type=["zip"])
skip_rows = st.number_input("Enter the number of rows to skip:", min_value=0, step=1, value=0)
file_name=st.text_input("Enter file name:")

def download_csv(df, filename):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"{filename}.csv",
        mime='text/csv'
    )
    
if file_name is not None:
    if uploaded_file is not None:
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
                            data = pd.read_csv(filepath, encoding='ISO-8859-1',skiprows = skip_rows).fillna("")


                        elif filename.endswith('.xlsx'):
                            data = pd.read_excel(filepath)

                    except Exception as e:
                        print(f"Error reading file: {filename}. Skipping...")
                        print(e)
                        continue
                    data['File_Name'] = filename

                    # st.write(data)

                    merged_data = pd.concat([merged_data, data], ignore_index=True)
        # st.write(merged_data)
                    

        # Reset index starting from 1
        merged_data.index = merged_data.index + 1
        merged_data['ID'] = range(1, len(merged_data) + 1)
        merged_data = merged_data[['ID'] + [col for col in merged_data.columns if col != 'ID']]
        # st.write(merged_data)

        # merged_data.to_csv('opened_merged_data.csv')
        download_csv(merged_data,file_name)

        # Add a download button to download the generated CSV file
        # st.download_button(
        #     label="Download CSV",
        #     data=merged_data.to_csv(index=True).encode('utf-8'),
        #     file_name=f"{file_name}.csv",
        #     mime='text/csv'
        # )
else:
    st.warning('Enter File Name')
