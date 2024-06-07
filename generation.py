import streamlit as st

def generate_book_structure(prompt: str) -> str:
    """
    Generates a hierarchical JSON structure for a book based on the given subject prompt.

    This function interacts with a language model to create a comprehensive structure for a long book,
    omitting sections like the introduction and conclusion. The structure is returned in JSON format.

    Parameters:
    -----------
    prompt : str
        The subject prompt for which the book structure is to be generated.

    Returns:
    --------
    str
        A JSON-formatted string representing the hierarchical structure of the book.
    """
    completion = st.session_state.groq.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {
                "role": "system",
                "content": (
                    "Write in JSON format:\n\n"
                    "{\"Title of section goes here\":\"Description of section goes here\",\n"
                    "\"Title of section goes here\":{"
                    "\"Title of section goes here\":\"Description of section goes here\","
                    "\"Title of section goes here\":\"Description of section goes here\","
                    "\"Title of section goes here\":\"Description of section goes here\"}"
                    "}"
                )
            },
            {
                "role": "user",
                "content": (
                    "Write a comprehensive structure, omitting introduction and conclusion sections "
                    "(forward, author's note, summary), for a long (>300 page) book on the following subject:\n\n"
                    f"<subject>{prompt}</subject>"
                )
            }
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    return completion.choices[0].message.content

def generate_section(prompt: str):
    """
    Generates content for a specific section of the book based on the given prompt.

    This function interacts with a language model to create a long, comprehensive, structured chapter
    for a given section title. The content is generated as a stream of text chunks.

    Parameters:
    -----------
    prompt : str
        The section title prompt for which the chapter content is to be generated.

    Yields:
    -------
    str
        A chunk of the generated content for the section.
    """
    stream = st.session_state.groq.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert writer. Generate a long, comprehensive, structured chapter for the section provided."
            },
            {
                "role": "user",
                "content": (
                    "Generate a long, comprehensive, structured chapter for the following section:\n\n"
                    f"<section_title>{prompt}</section_title>"
                )
            }
        ],
        temperature=0.3,
        max_tokens=8000,
        top_p=1,
        stream=True,
        stop=None,
    )

    for chunk in stream:
        tokens = chunk.choices[0].delta.content
        if tokens:
            yield tokens
