import streamlit as st
import os
import pandas as pd  # Added for Linda's structured view

# Import your classes from the separate blueprints file
from blueprints import Book, DigitalBook

# --- DATA PERSISTENCE LAYER ---
# Fixed Simon's bug by using a pipe '|' instead of a comma ','
FILE_NAME = "book_inventory.txt"
DELIMITER = "|"

def save_rental(book_obj):
    """System Resilience: Using try/except to protect file writes."""
    try:
        with open(FILE_NAME, "a") as f:
            # Saving with pipe to allow commas in titles
            f.write(f"{book_obj.get_title()}{DELIMITER}{book_obj.get_genre()}\n")
    except Exception as e:
        st.error(f"Error saving data: {e}")

def load_all_rentals():
    """System Resilience: Using try/except to protect file reads."""
    rentals = []
    try:
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as f:
                for line in f:
                    parts = line.strip().split(DELIMITER)
                    if len(parts) == 2:
                        # Uses the Book class imported from blueprints.py
                        rentals.append(Book(parts[0], parts[1]))
    except Exception as e:
        st.error(f"Error loading data: {e}")
    return rentals

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("System Menu")
page = st.sidebar.radio("Navigate to:", ["Add Rental", "View History"])

# --- PAGE: ADD RENTAL ---
if page == "Add Rental":
    st.title("📚 Add New Rental")
    
    # Fixed Dan's bug: clear_on_submit=True ensures the form resets
    with st.form("input_form", clear_on_submit=True):
        st.info("Fill out the details below. The form will reset after a successful log.")
        title = st.text_input("Enter Book Title").strip() # Simon's fix: .strip() handles whitespace
        genre = st.selectbox("Select Genre", ["Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Mystery", "History"])
        submitted = st.form_submit_button("Log Rental")
        
    if submitted:
        if title: 
            # Creating a new Book object from blueprints
            new_book = Book(title, genre)
            save_rental(new_book)
            st.success(f"Successfully logged: {title}")
        else:
            st.error("Submission failed: Please enter a valid book title.")

# --- PAGE: VIEW HISTORY ---
elif page == "View History":
    st.title("📜 Rental History")
    
    all_books = load_all_rentals()
    
    # Librarian Linda & Low-Vision Leo Fix: Using a Dataframe
    if not all_books:
        st.info("The inventory is currently empty.")
    else:
        # Convert objects to a list of dictionaries for Pandas using display_info() from blueprints
        data_list = [b.display_info() for b in all_books]
        df = pd.DataFrame(data_list)

        # Search Bar
        search_query = st.text_input("🔍 Search by title...", "").lower()
        
        # Filtering logic
        filtered_df = df[df['Title'].str.lower().str.contains(search_query)]

        if filtered_df.empty:
            st.warning(f"No titles found matching '{search_query}'.")
        else:
            # Linda's Sort: Allow user to sort by clicking column headers
            st.write(f"Showing **{len(filtered_df)}** of {len(all_books)} records")
            
            # This renders a clean, accessible, and sortable table
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)