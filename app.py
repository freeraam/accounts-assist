import streamlit as st
import os
import json
from modules.scanner import get_companies, scan_category
from modules.extractor import extract_data
from modules.validator import validate_invoice, is_duplicate
from modules.sheets import append_to_sheet
from modules.file_manager import move_to_processed, move_to_error
from modules.db import load_logs, save_log
from config import CATEGORIES

st.set_page_config(page_title="Accounting Automation Tool", layout="wide")

st.title("📊 Accounting Automation Prototype")
st.markdown("Automate your invoice processing with Gemini AI and Google Sheets.")

# Sidebar Controls
st.sidebar.header("Setup Status")
api_key_ok = bool(os.getenv("GEMINI_API_KEY"))
creds_ok = os.path.exists("credentials.json")

if api_key_ok:
    st.sidebar.success("✅ Gemini API Key found")
else:
    st.sidebar.error("❌ Gemini API Key missing")

if creds_ok:
    st.sidebar.success("✅ Google Sheets Credentials found")
else:
    st.sidebar.warning("⚠️ credentials.json missing (Sheets sync disabled)")

st.sidebar.divider()
st.sidebar.header("Controls")
companies = get_companies()
selected_company = st.sidebar.selectbox("Select Company", ["None"] + companies)

category_options = ["All"] + CATEGORIES
selected_category = st.sidebar.selectbox("Select Category", category_options)

process_all = st.sidebar.checkbox("Process All Companies")

if st.sidebar.button("Process Files"):
    if selected_company == "None" and not process_all:
        st.error("Please select a company or check 'Process All Companies'")
    else:
        companies_to_process = companies if process_all else [selected_company]
        categories_to_process = CATEGORIES if selected_category == "All" else [selected_category]
        
        for company in companies_to_process:
            st.subheader(f"Processing: {company}")
            logs = load_logs(company)
            
            for category in categories_to_process:
                files = scan_category(company, category)
                if not files:
                    st.info(f"No new files in {category}")
                    continue
                
                st.write(f"Found {len(files)} files in {category}")
                
                for file_path in files:
                    file_name = os.path.basename(file_path)
                    st.write(f"Processing: {file_name}...")
                    
                    # 1. Extract Data
                    data = extract_data(file_path)
                    if not data:
                        st.error(f"Failed to extract data from {file_name}")
                        move_to_error(company, file_path)
                        save_log(company, file_name, None, "error", "Extraction failed")
                        continue
                    
                    # 2. Validate Data
                    errors = validate_invoice(data, category)
                    if errors:
                        st.warning(f"Validation errors for {file_name}: {', '.join(errors)}")
                        move_to_error(company, file_path)
                        save_log(company, file_name, data, "error", ", ".join(errors))
                        continue
                        
                    # 3. Check for Duplicates
                    if is_duplicate(data, logs):
                        st.warning(f"Duplicate detected for {file_name}")
                        move_to_error(company, file_path)
                        save_log(company, file_name, data, "error", "Duplicate record")
                        continue
                        
                    # 4. Write to Google Sheets
                    success = append_to_sheet(company, category, data, file_name)
                    if not success:
                        st.error(f"Failed to write to Google Sheets for {file_name}")
                        # We still move to error if sheets fail, or maybe keep it for retry?
                        # For now, move to error.
                        move_to_error(company, file_path)
                        save_log(company, file_name, data, "error", "Google Sheets write failed")
                        continue
                        
                    # 5. Move to Processed
                    move_to_processed(company, file_path)
                    save_log(company, file_name, data, "processed")
                    st.success(f"Successfully processed {file_name}")
                    st.json(data)

# Display Logs and Previews
if selected_company != "None":
    st.divider()
    st.subheader(f"Logs for {selected_company}")
    logs = load_logs(selected_company)
    if logs:
        st.table(logs[-10:])  # Show last 10 logs
    else:
        st.info("No logs found for this company.")
else:
    st.info("Select a company to view logs.")
