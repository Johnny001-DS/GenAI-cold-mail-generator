import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    st.subheader("Your Information")
    user_name = st.text_input("Your Name", value="Prinkle Singharia")
    user_role = st.text_input("Your Role", value="ML/AI Engineer")

    st.subheader("Company Information")
    url_input = st.text_input("Enter a URL: ", value="https://careers.nike.com/software-engineer-iii/job/R-49238")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links, user_name, user_role)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


import os

if __name__ == "__main__":
    if not os.getenv('GROQ_API_KEY'):
        st.error("GROQ_API_KEY environment variable not set. Please set it in your environment or an app/.env file.")
    else:
        chain = Chain()
        portfolio = Portfolio()
        st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
        create_streamlit_app(chain, portfolio, clean_text)


