import streamlit as st
from groq import Groq
import json
import os
from dotenv import load_dotenv

from book import Book
from utils import create_markdown_file
from generation import generate_book_structure, generate_section

# Load environment variables from a .env file
load_dotenv()

# Retrieve the Groq API key from environment variables and store it in Streamlit session state
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
st.session_state.api_key = GROQ_API_KEY
st.session_state.groq = Groq()

# Initialize session state variables if they do not exist
if 'button_disabled' not in st.session_state:
    st.session_state.button_disabled = False

if 'button_text' not in st.session_state:
    st.session_state.button_text = "Generate Book"

# Display the application header
st.write("""
# 📖Solo Author Publication House
""")

from PIL import Image

# Load and display the logo image
image = Image.open('logo/logo.png')
st.image(image, caption='Solo Author Inc.')


def disable():
    """
    Disables the generate button by setting the session state variable.
    """
    st.session_state.button_disabled = True


def enable():
    """
    Enables the generate button by setting the session state variable.
    """
    st.session_state.button_disabled = False


def empty_st():
    """
    Clears all elements from the Streamlit interface.
    """
    st.empty()


# Custom CSS for a professional look and button alignment
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #F8F8F8;
        }
        .main {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .logo {
            max-width: 200px;
        }
        .stDownloadButton>button {
            background-color: #ADD8E6;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .stDownloadButton>button:hover {
            background-color: #87CEEB;
        }
        .download-button-container {
            display: flex;
            justify-content: flex-end;
        }
        .stTextInput>div>div>input {
            border: 2px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
        }
        .stDownloadButton>button {
            background-color: #008CBA;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .stDownloadButton>button:hover {
            background-color: #007bb5;
        }
        .title {
            text-align: center;
            font-size: 2em;
            margin-bottom: 20px;
        }
        .error {
            color: red;
        }
        .button-container {
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        .download-button-container {
            display: flex;
            justify-content: flex-end;
        }
    </style>
""", unsafe_allow_html=True)

try:
    with st.form("groqform"):
        # Input field for book topic
        topic_text = st.text_input("Generate Your Idea Into Book", "")

        # Generate button
        submitted = st.form_submit_button(st.session_state.button_text, on_click=disable,
                                          disabled=st.session_state.button_disabled)

        if submitted:
            # Validate the length of the book topic
            if len(topic_text) < 15:
                raise ValueError("Book topic must be at least 15 characters long")

            st.session_state.button_disabled = True

            # Check if the Groq API key is available
            if not GROQ_API_KEY:
                st.session_state.groq = Groq(api_key=groq_input_key)

            # Generate book structure
            book_structure = generate_book_structure(topic_text)

            try:
                book_structure_json = json.loads(book_structure)
                book = Book(book_structure_json)

                if 'book' not in st.session_state:
                    st.session_state.book = book

                # Print the book structure to the terminal
                print(json.dumps(book_structure_json, indent=2))

                # Display the book structure in the Streamlit interface
                st.session_state.book.display_structure()


                def stream_section_content(sections):
                    """
                    Streams and updates the content for each section of the book.

                    Parameters:
                    -----------
                    sections : dict
                        The hierarchical structure of the book with section titles and content.
                    """
                    for title, content in sections.items():
                        if isinstance(content, str):
                            content_stream = generate_section(title + ": " + content)
                            for chunk in content_stream:
                                st.session_state.book.update_content(title, chunk)
                        elif isinstance(content, dict):
                            stream_section_content(content)


                stream_section_content(book_structure_json)

            except json.JSONDecodeError:
                st.error("Failed to decode the book structure. Please try again.")

            enable()

    # Download button for the generated book
    if st.button('Download Your Book'):
        if "book" in st.session_state:
            markdown_file = create_markdown_file(st.session_state.book.get_markdown_content())
            st.download_button(
                label='Confirm Download',
                data=markdown_file,
                file_name='generated_book.txt',
                mime='text/plain',
            )
        else:
            raise ValueError("Your Download will be available once you generate Book.")

except Exception as e:
    st.session_state.button_disabled = False
    st.error(e)

    if st.button("Clear"):
        st.rerun()
