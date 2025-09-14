# Intelligent Job Recommendation System

This project implements an **Intelligent Job Recommendation System** that integrates **resume parsing, NLP-based semantic matching, and skill gap visualization**. The system is designed as part of an academic thesis project at **Green University of Bangladesh**.

## 🚀 Features

* **Secure Authentication** – User registration and login system.
* **Resume Parsing** – Extracts structured information (name, email, phone, skills) from PDF resumes.
* **Job Matching Engine** – Uses **TF-IDF vectorization** and **cosine similarity** to rank job postings.
* **Skill Gap Visualization** – Highlights missing skills in candidate profiles relative to job requirements.
* **Interactive UI** – Built with **Streamlit** for fast prototyping and visualization.
* **Modular Architecture** – Each component (parsing, matching, visualization) can be developed and upgraded independently.

## 🛠️ Technologies Used

* **Python**

  * `pdfplumber` (Resume text extraction)
  * `spaCy` (NLP preprocessing, lemmatization, NER)
  * `scikit-learn` (TF-IDF, cosine similarity)
  * `matplotlib` / `plotly` (Visualization)
* **Streamlit** – For the user interface.
* **SQLite / JSON** – For storing user and job datasets.

## 📂 Project Structure

```
├── Setup/                # LaTeX setup files for thesis formatting
├── Chapters/             # Thesis chapter contents
├── figures/              # Figures used in report
├── main.tex              # Main LaTeX file for the thesis
├── src/                  # Source code for the Job Recommendation System
│   ├── auth/             # Authentication module
│   ├── parser/           # Resume parsing module
│   ├── recommender/      # Job matching engine
│   ├── visualizer/       # Skill gap visualization
│   └── app.py            # Streamlit main app
└── README.md             # Project documentation
```

## ⚙️ Installation & Usage

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mahhasan41/Job-Recommendation-System-using-Machine-Learning.git
   cd Job-Recommendation-System-using-Machine-Learning
   ```

2. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**

   ```bash
   streamlit run src/app.py
   ```

   The system will open in your browser (default: `http://localhost:8501`).

## 📊 System Workflow

1. User logs in / registers.
2. Uploads a resume (PDF).
3. Resume is parsed into structured data.
4. System computes similarity between resume and job descriptions.
5. Top job recommendations and skill gap visualizations are displayed.


## 👨‍🎓 Authors

* Md. Mahmudol Hasan
