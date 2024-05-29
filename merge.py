import streamlit as st
import pandas as pd
import os
import zipfile

st.set_page_config(page_title='Multiple Polygons',page_icon=':earth_asia:',layout='wide')
custom_css = """
<style>
body {
    background-color: #0E1117; 
    secondary-background {
    background-color: #262730; 
    padding: 10px; 
}
</style>
"""
st.write(custom_css, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)


uploaded_file = st.file_uploader("Upload ZIP file", type=["zip"])
file_name=st.text_input("Enter file name:")


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
                            data = pd.read_csv(filepath, encoding='ISO-8859-1').fillna("")
                            st.write("Success")
                            
                        elif filename.endswith('.xlsx'):
                            data = pd.read_excel(filepath)
                            st.write("Success")
                            
                    except Exception as e:
                        st.write(f"Error reading file: {filename}. Skipping...")
                        st.write(e)
                        continue
                    data['File_Name'] = filename
                    merged_data = pd.concat([merged_data, data], ignore_index=True)

        # Reset index starting from 1
        merged_data.index = merged_data.index + 1

        fileNames = merged_data.File_Name.unique()
        

        industry_list = ['File_Name','Record_SuppliedDate','Record_SuppliedJobNo','Record_SuppliedClient_1','Remark','Campaign_Name','Email_Platform']
        user_coordinates = []
        
        default_values = []
        for i in range(len(fileNames)):
            default_values1 = [fileNames[i],f'User Loc {i+1}']
            default_values.append(default_values1)

        
        location_data1 = []
        
        
        Record_SuppliedDate = []
        File_Name = []
        Record_SuppliedJobNo = []
        Record_SuppliedClient_1 = []
        Remark = []
        Campaign_Name = []
        Email_Platform = []
        
            
            
        for idx in range(len(fileNames)):
            lon_lat_location_data=[]
            row = st.columns((7))

            # Get the default values for the current location
            default_value = default_values[idx] if idx < len(default_values) else ['0.0,0.0','',0.0]

            for i, industry in enumerate(industry_list):
                if industry == 'Record_SuppliedDate':
                    # Display the location identifier separately
                    location_identifier = row[i].text_input(f"{industry} - {idx + 1}", value="2/6/2024")
                    Record_SuppliedDate.append(location_identifier)
                    
                elif industry == 'File_Name':
                    lon_lat_location_identifier = row[i].text_input(f"{industry} - {idx + 1}", value=default_value[i])
                    File_Name.append(lon_lat_location_identifier)
                    
                elif industry == 'Record_SuppliedJobNo':
                    Record_SuppliedJobNo_identifiew = row[i].text_input(f"{industry} - {idx + 1}", value="S3949")
                    Record_SuppliedJobNo.append(Record_SuppliedJobNo_identifiew)
                    
                elif industry == 'Record_SuppliedClient_1':
                    Record_SuppliedClient_1_identifiew = row[i].text_input(f"{industry} - {idx + 1}", value="LifeLight")
                    Record_SuppliedClient_1.append(Record_SuppliedClient_1_identifiew)
                
                elif industry == 'Remark':
                    Remark_identifiew = row[i].text_input(f"{industry} - {idx + 1}", value="Buzzsaw")
                    Remark.append(Remark_identifiew)
                    
                elif industry == 'Campaign_Name':
                    Campaign_Name_identifiew = row[i].text_input(f"{industry} - {idx + 1}", value="S3949 RSL Art Union Draw 413 Campaign 1")
                    Campaign_Name.append(Campaign_Name_identifiew)
                    
                elif industry == 'Email_Platform':
                    Email_Platform_identifiew = row[i].text_input(f"{industry} - {idx + 1}", value="Gcast-BSM Presents")
                    Email_Platform.append(Email_Platform_identifiew)
                
                    
        # st.write(File_Name)
        # st.write(Record_SuppliedDate)
        # st.write(Record_SuppliedJobNo)
        # st.write(Record_SuppliedClient_1)
        # st.write(Remark)
        # st.write(Campaign_Name)
        # st.write(Email_Platform)
        
        
        
        file_dict = {}

        # Loop through the indices of the lists
        for i in range(len(File_Name)):
            file_dict[File_Name[i]] = {"Record_SuppliedDate": Record_SuppliedDate[i], "Record_SuppliedJobNo": Record_SuppliedJobNo[i],
                                       "Record_SuppliedClient_1": Record_SuppliedClient_1[i], "Remark":Remark[i],
                                       "Campaign_Name":Campaign_Name[i], "Email_Platform":Email_Platform[i]}
            
        for idx, row in merged_data.iterrows():
            file_name = row['File_Name']
            if file_name in file_dict:
                # Update the row with the values from the corresponding dictionary
                for col in file_dict[file_name]:
                    merged_data.at[idx, col] = file_dict[file_name][col]

        
        merged_data['FullName'] = merged_data['FirstName'] +" "+ merged_data['SurName']
        
        desired_order = [
        "ID","URN","Email","Record_SuppliedDate","Record_SuppliedJobNo",
        "File_Name","Record_SuppliedClient_1","JobType","Remark","Campaign_Name",
        "Email_Platform","Title","FirstName","SurName","FullName"]

        # Reindex the DataFrame to match the desired column order
        merged_data = merged_data.reindex(columns=desired_order)
        
        
        # merged_data.to_csv('opened_merged_data.csv')

        # Add a download button to download the generated CSV file
        st.download_button(
            label="Download CSV",
            data=merged_data.to_csv(index=True).encode('utf-8'),
            file_name=f"{file_name}.csv",
            mime='text/csv'
        )
else:
    st.warning('Enter File Name')
