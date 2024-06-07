import streamlit as st

class Book:
    """
    A class used to represent a Book with a hierarchical structure.

    Attributes
    ----------
    structure : dict
        A dictionary representing the hierarchical structure of the book
    contents : dict
        A dictionary holding the content for each section title
    placeholders : dict
        A dictionary holding the Streamlit placeholders for each section title

    Methods
    -------
    flatten_structure(structure)
        Flattens a nested dictionary structure into a list of keys
    update_content(title, new_content)
        Updates the content for a given title with new content
    display_content(title)
        Displays the content of a given title using Streamlit
    display_structure(structure=None, level=1)
        Recursively displays the structure and content of the book using Streamlit
    display_toc(structure, columns, level=1, col_index=0)
        Displays the table of contents for the book using Streamlit columns
    get_markdown_content(structure=None, level=1)
        Returns the entire content of the book in Markdown format
    """

    def __init__(self, structure):
        """
        Constructs all the necessary attributes for the Book object.

        Parameters
        ----------
        structure : dict
            A dictionary representing the hierarchical structure of the book
        """
        self.structure = structure
        self.contents = {title: "" for title in self.flatten_structure(structure)}
        self.placeholders = {title: st.empty() for title in self.flatten_structure(structure)}

        st.markdown("## Working...")
        toc_columns = st.columns(4)
        self.display_toc(self.structure, toc_columns)
        st.markdown("---")

    def flatten_structure(self, structure):
        """
        Flattens a nested dictionary structure into a list of keys.

        Parameters
        ----------
        structure : dict
            A dictionary representing the hierarchical structure of the book

        Returns
        -------
        list
            A list of keys representing all the section titles in the structure
        """
        sections = []
        for title, content in structure.items():
            sections.append(title)
            if isinstance(content, dict):
                sections.extend(self.flatten_structure(content))
        return sections

    def update_content(self, title, new_content):
        """
        Updates the content for a given title with new content.

        Parameters
        ----------
        title : str
            The title of the section to update
        new_content : str
            The new content to add to the section

        Raises
        ------
        TypeError
            If the title is not a valid string or if new_content is not a string
        """
        try:
            self.contents[title] += new_content
            self.display_content(title)
        except TypeError as e:
            pass

    def display_content(self, title):
        """
        Displays the content of a given title using Streamlit.

        Parameters
        ----------
        title : str
            The title of the section to display
        """
        if self.contents[title].strip():
            self.placeholders[title].markdown(f"## {title}\n{self.contents[title]}")

    def display_structure(self, structure=None, level=1):
        """
        Recursively displays the structure and content of the book using Streamlit.

        Parameters
        ----------
        structure : dict, optional
            A dictionary representing the hierarchical structure of the book (default is None)
        level : int, optional
            The current level of depth in the structure (default is 1)
        """
        if structure is None:
            structure = self.structure

        for title, content in structure.items():
            if self.contents[title].strip():  # Only display title if there is content
                st.markdown(f"{'#' * level} {title}")
                self.placeholders[title].markdown(self.contents[title])
            if isinstance(content, dict):
                self.display_structure(content, level + 1)

    def display_toc(self, structure, columns, level=1, col_index=0):
        """
        Displays the table of contents for the book using Streamlit columns.

        Parameters
        ----------
        structure : dict
            A dictionary representing the hierarchical structure of the book
        columns : list
            A list of Streamlit columns for displaying the table of contents
        level : int, optional
            The current level of depth in the structure (default is 1)
        col_index : int, optional
            The current column index for the table of contents (default is 0)

        Returns
        -------
        int
            The updated column index after processing the structure
        """
        for title, content in structure.items():
            with columns[col_index % len(columns)]:
                st.markdown(f"{' ' * (level - 1) * 2}- {title}")
            col_index += 1
            if isinstance(content, dict):
                col_index = self.display_toc(content, columns, level + 1, col_index)
        return col_index

    def get_markdown_content(self, structure=None, level=1):
        """
        Returns the entire content of the book in Markdown format.

        Parameters
        ----------
        structure : dict, optional
            A dictionary representing the hierarchical structure of the book (default is None)
        level : int, optional
            The current level of depth in the structure (default is 1)

        Returns
        -------
        str
            The Markdown formatted string of the book content
        """
        if structure is None:
            structure = self.structure

        markdown_content = ""
        for title, content in structure.items():
            if self.contents[title].strip():  # Only include title if there is content
                markdown_content += f"{'#' * level} {title}\n{self.contents[title]}\n\n"
            if isinstance(content, dict):
                markdown_content += self.get_markdown_content(content, level + 1)
        return markdown_content
