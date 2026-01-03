# 🤝 AI Resume to Job Description Matcher

A powerful AI-powered tool designed to check how well a resume matches a specific job description. This application uses Natural Language Processing (NLP) techniques to extract key information and calculate similarity scores, helping candidates optimize their resumes for Applicant Tracking Systems (ATS).

## 🚀 Features

-   **PDF Resume Support**: Easily upload your resume in PDF format.
-   **Text Extraction**: Automatically extracts text from uploaded PDF files.
-   **Job Description Analysis**: Paste any job description to analyze.
-   **Entity Extraction**: Identifies key information (skills, qualifications, etc.) from both the resume and the job description using SpaCy.
-   **Smart Matching**: Calculates an overall match score using Sentence Transformers for semantic similarity.
-   **Detailed Breakdown**: Provides a breakdown of the match score across different aspects.
-   **Visual Feedback**: Simple and intuitive interface built with Streamlit.

## 🛠️ Technologies Used

-   **Python 3.11+**
-   **Streamlit**: For the web interface.
-   **SpaCy**: For Named Entity Recognition (NER) and text processing.
-   **Sentence-Transformers**: For semantic similarity calculation.
-   **NLTK**: For natural language processing tasks.
-   **PyPDF2**: For PDF text extraction.

## 📦 Installation

Follow these steps to set up the project locally:

1.  **Clone the Repository**
    ```bash
    git clone <repository-url>
    cd AI_RESUME_JOB_MATCHER
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Language Models**
    The application requires specific NLP models. They will be downloaded automatically on the first run, or you can manually install the SpaCy model:
    ```bash
    python -m spacy download en_core_web_sm
    ```

## 🏃 Usage

1.  **Run the Application**
    ```bash
    streamlit run app.py
    ```

2.  **Open in Browser**
    The application will automatically open in your default web browser (usually at `http://localhost:8501`).

3.  **Match Your Resume**
    -   Upload your resume PDF in the left column.
    -   Paste the job description in the right column.
    -   Click **✨ Get Match Score** to see the results!

## 📂 Project Structure

```
AI_RESUME_JOB_MATCHER/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── src/                    # Source code modules
│   ├── info_extractor.py   # Entity extraction logic
│   ├── matcher.py          # Similarity calculation logic
│   ├── pdf_parser.py       # PDF text extraction
│   ├── text_processor.py   # Text preprocessing
│   └── utils.py            # Utility functions (model loading)
├── data/                   # Data directory (resumes, etc.)
└── .gitignore             # Git ignore file
```

## ⚠️ Note

This project serves as a demonstration of NLP capabilities in resume matching. For a production-level ATS, more sophisticated Named Entity Recognition (NER) models, extensive experience parsing, and fine-tuned scoring algorithms would be required.