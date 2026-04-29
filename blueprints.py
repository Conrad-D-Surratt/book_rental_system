# Parent class to handle basic book data
class Book:
    def __init__(self, title, genre):
        self.__title = title
        self.__genre = genre

    def get_title(self):
        return self.__title

    def get_genre(self):
        return self.__genre

    def display_info(self):
        return {"Title": self.__title, "Genre": self.__genre}

# Child class
class DigitalBook(Book):
    def __init__(self, title, genre, file_size):
        # Use super() to initialize the title and genre from the parent class
        super().__init__(title, genre)
        # Unique attribute for the digital version
        self.file_size = file_size 

    def display_details(self):
        # Returns a formatted string
        return f"{self.get_title()} (Digital - {self.file_size}MB)"