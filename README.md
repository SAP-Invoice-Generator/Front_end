# Invoice Management Tool

The Invoice Management Tool is a web application designed to streamline the process of extracting essential details from invoices, providing users with comprehensive analyses and management capabilities. Leveraging advanced AI technologies and backend services, the tool facilitates efficient invoice processing, data storage, and analysis.

## Features

- **Upload**: Users can upload image or PDF files containing invoices through an intuitive interface.
- **Extraction**: The application extracts critical information from invoices, including invoice numbers, dates, total amounts, currency types, item quantities, and customer names.
- **AI Integration**: Advanced AI models process invoice content to extract meaningful information efficiently.
- **Data Storage**: Extracted invoice details are stored securely in a backend database for easy retrieval and analysis.
- **Analytics**: The tool provides month-wise and year-wise expenditure analysis for users to gain insights into their financial data.
- **Error Handling**: Specific error messages guide users in resolving issues such as duplicate invoices or invalid inputs.

## Technologies Used

- **Frontend**: Streamlit
- **Backend**: Python, Supabase (PostgreSQL)
- **AI**: Gemini API, PyPDF, Google Sheets (for certain functionalities)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/invoice-management-tool.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   
   Create a `.env` file in the root directory and add the following variables:

```plaintext
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GEMINI_KEY=your_gemini_api_key
```

Replace `your_supabase_url`, `your_supabase_key`, and `your_gemini_api_key` with your actual Supabase URL, Supabase API key, and Gemini API key, respectively.

4. Run the application:

```bash
streamlit run app.py
```

5. Access the application at `http://localhost:8501` in your web browser.

## Usage

1. Upload Invoice: Click on the upload button to select and upload image or PDF files containing invoices.
2. View Results: Once uploaded, the extracted invoice details will be displayed on the interface.
3. Analyze Data: Utilize the analytics section to view month-wise and year-wise expenditure analysis.
4. Edit and Store: Edit any extracted details if necessary and submit to store the data in the backend database.
The Invoice Management Tool is hosted at [https://sap-project-beta.streamlit.app/](https://sap-project-beta.streamlit.app/). You can access it directly in your web browser to start managing your invoices.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to contribute to the development of the Invoice Management Tool.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Note:** Replace placeholders such as `your-username` and `your_supabase_url` with your actual GitHub username and Supabase URL. Additionally, ensure that you have appropriate permissions and API keys for the services used in the application.
