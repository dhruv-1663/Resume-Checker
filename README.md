# README.md

## Cyber Security Internship Resume Evaluation

This Streamlit application evaluates resumes for cyber security internships based on a provided job description.  It processes applicant data from an Excel file, retrieves resumes from URLs, and uses a Generative AI model (Gemini Pro) to provide feedback on each resume in relation to the job description.

### Features

* **Job Description Input:** Allows users to input the job description for the internship.
* **Excel File Upload:** Enables uploading an Excel file containing applicant information. The file *must* have columns named (case-insensitive):
    * `Name` (First Name)
    * `LastName`
    * `Email`
    * `Resume` (containing URLs to PDF resumes)
* **Resume Processing:** Retrieves resumes from the URLs provided in the Excel file.
* **AI-Powered Evaluation:** Uses Gemini Pro to generate feedback on each resume based on the job description.
* **Results Display and Download:** Displays the generated reviews in a table format and allows downloading the results as an Excel file.
* **Error Handling:** Includes robust error handling for invalid URLs, PDF processing issues, and missing columns in the Excel file.

```markdown
## Installation

1. **Clone the Repository:**

   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://www.google.com/search?q=https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)  # Replace with your repo URL
   cd YOUR_REPOSITORY_NAME
   ```

2. **Create a Virtual Environment (Recommended):**

   ```bash
   python3 -m venv .venv        # Create a virtual environment
   source .venv/bin/activate   # Activate the virtual environment (Linux/macOS)
   .venv\Scripts\activate      # Activate the virtual environment (Windows)
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables:**

   * Create a `.env` file in the project directory.
   * Add your Google Cloud API key to the `.env` file:

     ```
     GOOGLE_API_KEY=YOUR_ACTUAL_API_KEY
     ```

## Usage

1. **Run the Streamlit App:**

   ```bash
   streamlit run your_app_name.py  # Replace your_app_name.py with the name of your main script
   ```

2. **Open the App:** The app will open in your web browser.

3. **Enter Job Description:** Paste the job description into the text area.

4. **Upload Excel File:** Click "Browse files" to upload your Excel file.

5. **View and Download Results:** The generated reviews will be displayed. Click the "Download Final Data" button to download the results as an Excel file.

```

   
