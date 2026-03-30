# Accounting Automation Tool

This is a local-first accounting automation prototype using Gemini AI and Streamlit.

## Features
- **File Scanning**: Automatically detects new invoices in `data/Company_X/Category/` folders.
- **Data Extraction**: Uses Gemini 2.0 Flash to extract structured JSON from images and PDFs.
- **Validation**: Checks for correct categories, valid GST formats, and duplicates.
- **Google Sheets Integration**: Appends processed data to a Google Sheet for each company.
- **File Management**: Moves processed files to `Processed/` or `Error/` folders.
- **Streamlit UI**: Simple interface to control the automation process.

## Setup Instructions

1. **API Keys**:
   - Ensure `GEMINI_API_KEY` is set in your environment or AI Studio Secrets.
   - For Google Sheets, place your `credentials.json` (Service Account) in the root directory.

2. **Folder Structure**:
   - The app expects a `data/` folder with company subfolders.
   - Example: `data/Company_A/Purchase/`, `data/Company_A/Sales/`, etc.

3. **Run the App**:
   - The app will automatically install dependencies and start Streamlit on port 3000 when you run `npm run dev`.

## Usage
1. Select a company from the sidebar.
2. Select a category (or "All").
3. Click "Process Files".
4. View the results and logs in the UI.
