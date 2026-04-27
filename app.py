import streamlit as st
import os

# --- CLASS DEFINITION ---
class Book:
    def __init__(self, title, genre):
        self.__title = title
        self.__genre = genre

    def get_title(self):
        return self.__title

    def get_genre(self):
        return self.__genre

    def display_order(self, index):
        return f"{index}. 📖 **Title:** {self.__title} | **Category:** {self.__genre}"

# --- DATA PERSISTENCE LAYER ---
FILE_NAME = "book_inventory.txt"

def save_rental(book_obj):
    """Appends a single book rental to the text file."""
    with open(FILE_NAME, "a") as f:
        f.write(f"{book_obj.get_title()},{book_obj.get_genre()}\n")

def load_all_rentals():
    """Reads the file and returns a list of Book objects."""
    rentals = []
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as f:
            for line in f:
                # Clean and split each line into Title and Genre
                parts = line.strip().split(",")
                if len(parts) == 2:
                    # Re-instantiate the Book object for the UI
                    rentals.append(Book(parts[0], parts[1]))
    return rentals

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("System Menu")
page = st.sidebar.radio("Navigate to:", ["Add Rental", "View History"])

# --- PAGE: ADD RENTAL ---
if page == "Add Rental":
    st.title("📚 Add New Rental")
    
    with st.form("input_form", clear_on_submit=True):
        title = st.text_input("Enter Book Title")
        genre = st.selectbox("Select Genre", ["Fiction", "Non-Fiction", "Sci-Fi", "Fantasy", "Mystery", "History"])
        submitted = st.form_submit_button("Log Rental")
        
    if submitted:
        if title.strip():
            new_book = Book(title, genre)
            save_rental(new_book)
            st.success(f"Successfully logged: {title}")
        else:
            st.error("Title cannot be blank.")

# --- PAGE: VIEW HISTORY ---
elif page == "View History":
    st.title("📜 Rental History")
    
    # 1. Load data from file
    all_books = load_all_rentals()
    
    # 2. Search/Filter Section
    search_query = st.text_input("🔍 Search by title...", "").lower()
    
    # 3. Filtering Logic
    # We create a new list containing only books that match the search query
    filtered_books = [
        book for book in all_books 
        if search_query in book.get_title().lower()
    ]

    # 4. Display Results
    if not all_books:
        st.info("The inventory is currently empty.")
    elif not filtered_books:
        st.warning(f"No titles found matching '{search_query}'.")
    else:
        st.write(f"Showing **{len(filtered_books)}** of {len(all_books)} records")
        st.divider()
        
        for i, book in enumerate(filtered_books, 1):
            st.write(book.display_order(i))