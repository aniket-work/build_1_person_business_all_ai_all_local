🏢 Build a 1-Person Business Using AI, All Locally 🏢

In this project, we'll build a one-person business using AI agents, all running locally. Get ready for an exciting journey!

**Prerequisites:**

* Python installed on your system.
* A basic understanding of virtual environments and command-line tools.

**Steps:**

1. **Virtual Environment Setup:**

   - Create a dedicated virtual environment for our project:
   
     ```bash
     python -m venv build_1_person_business_all_ai_all_local 
     ```

   - Activate the environment:
   
     * Windows:
        ```bash
        build_1_person_business_all_ai_all_local\Scripts\activate
        ```
     * Unix/macOS:
        ```bash
        source build_1_person_business_all_ai_all_local/bin/activate
        ```

2. **Install Project Dependencies:**

   - Grab the necessary packages with the help of `pip`:
   
     ```bash
     pip install -r requirements.txt
     ```

3. **Setup Groq key:**

   - get your groq key from https://console.groq.com/keys
   - set your key in .env file as : GROQ_API_KEY=<YOUR_KEY>
    ```
   
4. Run 
```python
(build_1_person_business_all_ai_all_local) ~\PycharmProjects\build_1_person_business_all_ai_all_local>python -m streamlit run main.py
```


