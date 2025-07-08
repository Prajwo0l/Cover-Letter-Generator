# 🖍️ AI Cover Letter Generator

This is a Streamlit web application that generates personalized cover letters using a fine-tuned language model. It was fine-tuned on June 6 using relevant job application data and provides multiple formatting styles to suit different professional needs.

---

## 📌 Features

- ✍️ Automatically generates personalized cover letters based on job details, experience, and skills.
- 🎨 Multiple formatting options: Minimal, Formal, and Modern.
- 🧠 Uses a fine-tuned transformer-based language model.
- ⚙️ Runs on GPU (if available) or CPU.
- 💻 Built with Python, Streamlit, PyTorch, and Hugging Face Transformers.

---

## 📂 Project Structure

├── app.py # Main Streamlit app
├── fine_tuned_model/ # Locally saved fine-tuned model
├── june6.ipynb # Notebook used for fine-tuning (summary and training)
└── requirements.txt # List of required dependencies


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/cover-letter-generator.git
cd cover-letter-generator
```


### 2. Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```


### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Add Fine-Tuned Model
   
Make sure your fine-tuned Hugging Face model (from june6.ipynb) is saved in a folder named:

```bash
fine_tuned_model/
```

### 5. Run the Application

```bash
streamlit run app.py
```

 ## 🧠 How It Works
-The app collects user data like name, skills, and job title.
-A custom prompt is created using this information.
-The prompt is sent to a fine-tuned transformer model that generates a full cover letter.
-The result is formatted into three professional templates.
-The user can view, edit, and copy the generated letter from the app.

 ## 👤 Author
Prajwol Lamichhane
📧 lamichhane.prajwool@gmail.com
🔗 GitHub

