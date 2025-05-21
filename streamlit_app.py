import streamlit as st
from agenda_logic import (
    add_contact,
    list_contacts,
    search_contact_by_name,
    search_contact_by_code,
    update_contact
)
from agenda_structures import AgendaItem
import pandas as pd

# Initialize session state for update functionality
if 'contact_to_update' not in st.session_state:
    st.session_state.contact_to_update = None
if 'search_name_results' not in st.session_state:
    st.session_state.search_name_results = []
if 'search_code_result' not in st.session_state:
    st.session_state.search_code_result = None

st.title("Agenda App")

# --- Display Contacts (Main View) ---
st.header("All Contacts")
contacts = list_contacts()

if contacts:
    # Convert list of AgendaItem objects to a list of dictionaries for DataFrame
    contacts_data = [
        {
            "Code": item.codigo,
            "Name": item.nome,
            "Fixed Phone": item.fone_fixo,
            "Cell Phone": item.fone_celular,
            "Commercial Phone": item.fone_comercial
        }
        for item in contacts
    ]
    df_contacts = pd.DataFrame(contacts_data)
    st.dataframe(df_contacts.set_index("Code"))
else:
    st.write("No contacts in the agenda.")

# --- Sidebar for Actions ---

# --- Add New Contact ---
st.sidebar.header("Add New Contact")
with st.sidebar.form("add_contact_form", clear_on_submit=True):
    add_nome = st.text_input("Name*")
    add_fixo = st.text_input("Fixed Phone")
    add_celular = st.text_input("Cell Phone")
    add_comercial = st.text_input("Commercial Phone")
    add_button = st.form_submit_button("Add Contact")

if add_button:
    if add_nome: # Name is mandatory
        new_contact = add_contact(nome=add_nome, fixo=add_fixo, celular=add_celular, comercial=add_comercial)
        st.sidebar.success(f"Contact '{new_contact.nome}' added successfully with code {new_contact.codigo}!")
        st.experimental_rerun()
    else:
        st.sidebar.error("Name is a required field.")


# --- Search Contacts ---
st.sidebar.header("Search Contacts")

# By Name
search_name_query = st.sidebar.text_input("Search by Name")
if st.sidebar.button("Search Name"):
    if search_name_query:
        results = search_contact_by_name(search_name_query)
        st.session_state.search_name_results = results
        st.session_state.search_code_result = None # Clear other search
        if not results:
            st.sidebar.warning("No contacts found with that name.")
        # Rerun to display results outside the button's direct scope if needed, or display directly
        # For this setup, results will be displayed below based on session_state
    else:
        st.session_state.search_name_results = [] # Clear results if query is empty

if st.session_state.search_name_results:
    st.sidebar.subheader("Name Search Results")
    # Convert to DataFrame for better display
    search_results_data = [
        {
            "Code": item.codigo, "Name": item.nome, "Fixed": item.fone_fixo, 
            "Cell": item.fone_celular, "Commercial": item.fone_comercial
        } for item in st.session_state.search_name_results
    ]
    df_search_results = pd.DataFrame(search_results_data)
    st.sidebar.dataframe(df_search_results)


# By Code
search_code_query = st.sidebar.number_input("Search by Code", min_value=1, value=None, format="%d", step=1)
if st.sidebar.button("Search Code"):
    if search_code_query is not None:
        result = search_contact_by_code(int(search_code_query))
        st.session_state.search_code_result = result
        st.session_state.search_name_results = [] # Clear other search
        if result is None:
            st.sidebar.warning("No contact found with that code.")
    else:
        st.session_state.search_code_result = None # Clear result if query is empty

if st.session_state.search_code_result:
    st.sidebar.subheader("Code Search Result")
    item = st.session_state.search_code_result
    st.sidebar.json({ # Displaying as JSON for quick view
        "Code": item.codigo, "Name": item.nome, "Fixed Phone": item.fone_fixo,
        "Cell Phone": item.fone_celular, "Commercial Phone": item.fone_comercial
    })


# --- Update Contact ---
st.sidebar.header("Update Contact")
update_code_input = st.sidebar.number_input("Enter Code of Contact to Update", min_value=1, value=None, format="%d", key="update_code_input_key", step=1)

if st.sidebar.button("Fetch Contact for Update"):
    if update_code_input is not None:
        contact_to_edit = search_contact_by_code(int(update_code_input))
        if contact_to_edit:
            st.session_state.contact_to_update = contact_to_edit
            st.experimental_rerun() # Rerun to show the update form
        else:
            st.sidebar.error("Contact code not found.")
            st.session_state.contact_to_update = None # Clear if not found
    else:
        st.sidebar.warning("Please enter a code to fetch.")
        st.session_state.contact_to_update = None


if st.session_state.contact_to_update:
    contact = st.session_state.contact_to_update
    st.sidebar.subheader(f"Editing Contact: {contact.nome} (Code: {contact.codigo})")
    with st.sidebar.form("update_contact_form"):
        update_nome = st.text_input("New Name (leave blank to keep current)", value=contact.nome)
        update_fixo = st.text_input("New Fixed Phone (leave blank to keep current)", value=contact.fone_fixo)
        update_celular = st.text_input("New Cell Phone (leave blank to keep current)", value=contact.fone_celular)
        update_comercial = st.text_input("New Commercial Phone (leave blank to keep current)", value=contact.fone_comercial)
        update_button = st.form_submit_button("Save Updates")

        if update_button:
            # Use new values if provided, else use original from session state for empty strings
            # The logic in update_contact already handles empty strings by keeping old values,
            # but for clarity and directness:
            final_nome = update_nome if update_nome else contact.nome
            final_fixo = update_fixo # Pass empty strings as is, logic handles it.
            final_celular = update_celular
            final_comercial = update_comercial

            updated_item = update_contact(
                code=contact.codigo,
                nome=final_nome, # Must not be empty
                fixo=final_fixo,
                celular=final_celular,
                comercial=final_comercial
            )
            if updated_item:
                st.sidebar.success(f"Contact {updated_item.nome} updated successfully!")
                st.session_state.contact_to_update = None # Clear state
                st.experimental_rerun()
            else:
                # This case should ideally not happen if code was valid, but good for robustness
                st.sidebar.error("Failed to update contact. Please ensure code is valid.")
                st.session_state.contact_to_update = None # Clear state
                st.experimental_rerun()
else:
    # This is to ensure that if a user clears the update_code_input field after fetching a contact,
    # the update form disappears.
    if update_code_input is None and st.session_state.contact_to_update is not None:
         st.session_state.contact_to_update = None
         st.experimental_rerun()
