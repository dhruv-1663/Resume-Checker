import streamlit as st
import os
import polars as pl
from io import BytesIO
import urllib.request
from dotenv import load_dotenv
import genai
from PyPDF2 import PdfReader
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR)

def getPdfBytes(url):
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Referer': 'https://cssspritegenerator.com',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

        req = urllib.request.Request(str(url), headers=hdr)
        with urllib.request.urlopen(req) as f:
            pdf_bytes = BytesIO(f.read())
        return pdf_bytes
    except urllib.error.URLError as e:
        st.error(f"Error accessing URL {url}: {e}")
        logging.error(f"URL Error: {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred while fetching URL {url}: {e}")
        logging.error(f"URL Fetch Error: {e}")
        return None

def responseModel(model, pdf_bytes, jd):
    try:
        reader = PdfReader(pdf_bytes)
        extracted_text = ""
        for page in reader.pages:
            extracted_text += page.extract_text()

        input_prompt = f"""
        Here is the Job Description:
        {jd}
        And here is the resume text:
        {extracted_text}
        Please provide feedback on the resume in relation to the job description.
        """

        response = model.generate_content(input_prompt)
        return response.text
    except Exception as e:
        st.error(f"Error processing PDF: {e}")
        logging.error(f"PDF Processing Error: {e}")
        return "Error processing PDF"

def main():
    st.title("Internship Resume Evaluation")
    st.markdown("Please upload an Excel file containing applicant data. The file *must* have columns named 'Name', 'LastName', 'Email', and 'Resume' (case-insensitive).  The 'Resume' column should contain URLs to the applicants' resumes in PDF format.")

    jd_text = st.text_area("Enter the Job Description", height=300)

    uploaded_file = st.file_uploader("Upload your Excel File", type=["xlsx"])

    if uploaded_file is not None and jd_text:
        if not jd_text.strip():
            st.error("Please enter a Job Description.")
            return

        try:
            data = pl.read_excel(uploaded_file)
            print(data.columns)  # Print columns for debugging

            required_cols = []
            for col in ["Name", "LastName", "Email", "Resume"]:
                matching_cols = [c for c in data.columns if col.lower() == c.lower()]
                if matching_cols:
                    required_cols.append(matching_cols[0])
                else:
                    st.error(f"Column '{col}' not found (case-insensitive). Please check your Excel file.")
                    return

            renamed_cols = {col: col_name for col, col_name in zip(required_cols, ["Name", "LastName", "Email", "Resume"])}

            req_data = data.select(required_cols).rename(renamed_cols).drop_nulls()

            load_dotenv()
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            model = genai.GenerativeModel('gemini-pro')

            final_df = req_data.with_columns(
                pl.col("Resume").map_elements(
                    lambda x: responseModel(model, getPdfBytes(x), jd_text) if x else None,
                    pl.datatypes.String
                ).alias("Review")
            )

            st.subheader("Generated Reviews")
            st.write(final_df)

            final_file = "Final_data.xlsx"
            final_df.write_excel(final_file)

            with open(final_file, "rb") as f:
                st.download_button("Download Final Data", f, file_name=final_file)

        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            logging.exception("An unexpected error occurred")

if __name__ == "__main__":
    main()