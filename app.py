import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from datetime import datetime


# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = os.path.abspath("./fine_tuned_model")

@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(model_path, local_files_only=True).to(device)
    return tokenizer, model

tokenizer, model = load_model()

# ------------------------
# Streamlit UI
# ------------------------
st.set_page_config(page_title="Cover Letter Generator", layout="centered")
st.title("🖍️ AI Cover Letter Generator")

# Sidebar
st.sidebar.title("⚙️ Settings")
template_choice = st.sidebar.selectbox("Select Template Style", ["Minimal", "Formal", "Modern"])

st.sidebar.markdown(f"**Device:** {'GPU - ' + torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
st.sidebar.markdown(f"**Model Path:** `{model_path}`")

with st.form("cover_letter_form"):
    st.subheader("Your Information")
    applicant_name = st.text_input("Full Name", "Priya Verma")
    address = st.text_input("Address", "123 Street Name, City, State ZIP")
    phone = st.text_input("Phone Number", "+1 234 567 8900")
    email = st.text_input("Email", "priya@example.com")
    
    st.subheader("Job Details")
    job_title = st.text_input("Job Title", "Data Analyst")
    company = st.text_input("Hiring Company", "Google")
    recruiter = st.text_input("Hiring Manager or Recruiter Name", "Hiring Manager")
    company_address = st.text_input("Company Address", "1600 Amphitheatre Parkway, Mountain View, CA 94043")

    experience = st.text_area("Work Experience", "Business Intelligence Intern working on SQL and Tableau...")
    skills = st.text_area("Skills", "Python, Excel, Power BI")

    submitted = st.form_submit_button("Generate Cover Letter")

# ------------------------
# Formatting Templates
# ------------------------
def apply_template(style, letter_body):
    if style == "Minimal":
        return f"""
{applicant_name.upper()}
{address} | {phone} | {email}

{today_str}

{recruiter}  
{company}  
{company_address}  

{letter_body}


"""
    elif style == "Formal":
        address_parts = address.split(',')
        city = address_parts[1].strip() if len(address_parts) > 1 else ''
        state_zip = address_parts[2].strip() if len(address_parts) > 2 else ''

        return f"""
{applicant_name.upper()}{" " * 40}{city}, {state_zip}  
{" " * 45}{phone} | {email}  
{"-" * 60}

{today_str}

{recruiter}  
{company}  
{company_address}  

{letter_body}


"""
    elif style == "Modern":
        return f"""
{applicant_name.upper()}
{job_title.upper()}

{address} | {phone} | {email}
______________________________________________________

{today_str}

{recruiter}  
{company}  
{company_address}  

Dear {recruiter.split()[0] if recruiter else 'Hiring Manager'},

{letter_body}



"""
    else:
        return letter_body


# ------------------------
# Cover Letter Generation
# ------------------------
if submitted:
    today_str = datetime.today().strftime("%d %B %Y")
    with st.spinner("Generating your cover letter..."):
        prompt = (
            f"Job Title: {job_title}\n"
            f"Hiring Company: {company}\n"
            f"Applicant Name: {applicant_name}\n"
            f"Working Experience: {experience}\n"
            f"Skillsets: {skills}\n"
            f"Cover Letter:\n"
        )

        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            output = model.generate(
                **inputs,
                max_new_tokens=400,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                pad_token_id=tokenizer.eos_token_id
            )

        generated = tokenizer.decode(output[0], skip_special_tokens=True)
        if "Cover Letter:" in generated:
            letter_body = generated.split("Cover Letter:")[-1].strip()
        else:
            letter_body = generated.strip()

        # Show all styles as editable tabs
        st.success("✅ Here's your formatted cover letter in all styles:")
        for style in ["Minimal", "Formal", "Modern"]:
            with st.expander(f"{style} Template"):
                formatted_letter = apply_template(style, letter_body)
                st.text_area("Cover Letter", value=formatted_letter, height=500, key=f"editable_{style}")