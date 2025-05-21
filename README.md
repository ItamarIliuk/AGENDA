# Streamlit Agenda Application

This is a simple agenda (contact book) application with a web interface built using Streamlit.
The backend logic is written in Python and interacts with a binary data file (`agenda.dat`) for persistence.

## Features

- Add new contacts (Name, Fixed Phone, Cell Phone, Commercial Phone)
- List all saved contacts
- Search for contacts by name (substring, case-insensitive)
- Search for contacts by their unique code
- Update existing contact information

## Project Structure

- `streamlit_app.py`: The main Streamlit application file.
- `agenda_logic.py`: Contains the business logic for managing contacts.
- `agenda_data_handler.py`: Handles reading from and writing to the `agenda.dat` file.
- `agenda_structures.py`: Defines the `AgendaItem` data structure.
- `agenda.dat`: Binary file where contact data is stored (automatically created).
- `agenda.c`: Original C code for the command-line agenda (not used by the Streamlit app).
- `.gitignore`: Specifies intentionally untracked files by Git.
- `README.md`: This file.

## Setup and Running

1.  **Prerequisites:**
    - Python 3.7+
    - pip (Python package installer)

2.  **Clone the repository (if you haven't already):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

3.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

4.  **Install dependencies:**
    The application requires Streamlit and Pandas.
    ```bash
    pip install streamlit pandas
    ```

5.  **Run the Streamlit application:**
    ```bash
    streamlit run streamlit_app.py
    ```
    This will typically open the application in your default web browser.

## How it Works

The application re-implements the core functionality of the original C-based agenda program in Python.
- Contact data is stored in `agenda.dat`. The first 4 bytes of this file store an integer representing the last used contact code (sequence number). Subsequent data consists of fixed-size records for each contact.
- The `agenda_data_handler.py` module uses Python's `struct` module to pack and unpack data to/from the binary file, matching the structure defined in the original C program.
- `agenda_logic.py` provides functions to add, list, search, and update contacts.
- `streamlit_app.py` uses these functions to create an interactive web interface.
