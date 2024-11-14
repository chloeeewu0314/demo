import pandas as pd
import streamlit as st
import os

def extract_and_save_excel_data(file, model_name, today_date, columns, max_lines=1900):
    # Load the Excel file into a pandas DataFrame
    df = pd.read_excel(file)

    # Select the specified columns
    selected_columns = df[columns]

    # Track duplicates and missing values
    duplicates = selected_columns[selected_columns.duplicated()]
    missing_values = selected_columns[selected_columns.isna().any(axis=1)]

    # Display duplicates and missing values
    if not duplicates.empty:
        st.write("Duplicates found:")
        st.write(duplicates)
    else:
        st.write("No duplicates found.")
    
    if not missing_values.empty:
        st.write("Rows with missing values found:")
        st.write(missing_values)
    else:
        st.write("No missing values found.")

    # Remove duplicates and rows with missing values
    cleaned_data = selected_columns.drop_duplicates().dropna()

    # Convert the cleaned data into a comma-separated string for each row
    result = cleaned_data.apply(lambda row: ','.join(row.astype(str)), axis=1)

    # Generate the base filename format
    base_filename = f"{model_name}_SN_IMEI1_IMEI2_EID_{today_date}"

    # Write the result to multiple files if the data exceeds max_lines per file
    line_count = 0
    file_index = 1
    output_files = []  # To track created file names

    # Writing to Streamlit file objects and keeping track of them
    while line_count < len(result):
        # Define current output filename
        output_filename = f"{base_filename}_{file_index}.txt"
        output_files.append(output_filename)

        # Select lines for this chunk
        chunk = result[line_count:line_count + max_lines]
        line_count += max_lines
        file_index += 1

        # Create a downloadable file in Streamlit
        st.download_button(
            label=f"Download {output_filename}",
            data='\n'.join(chunk),  # Convert to a single string
            file_name=output_filename,
            mime="text/plain"
        )

    st.write(f"Created {file_index - 1} output files.")

# Streamlit Interface
st.title("Verizon Commerical Devices Data Extractor🎈")

# File upload
uploaded_file = st.file_uploader("Please upload the Excel file", type=["xls", "xlsx"])

if uploaded_file:
    # Prompt for model name and today's date
    model_name = st.text_input("Enter the model name")
    today_date = st.text_input("Enter today's date (format: mmddyy)")

    if model_name and today_date:
        # Define columns to extract
        columns = ['Serial Number', 'IMEI', 'IMEI2', 'EID']

        # Extract data when the user clicks the button
        if st.button("Process File"):
            extract_and_save_excel_data(uploaded_file, model_name, today_date, columns)
