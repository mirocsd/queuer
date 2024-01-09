import sys
import sqlite3
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSizePolicy


class QueuerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(QueuerWindow, self).__init__()
        uic.loadUi('./myui.ui', self)

        # Add event filters
        self.editAlbum.installEventFilter(self)
        self.editBook.installEventFilter(self)
        self.editMovie.installEventFilter(self)

        # Connect the remove X buttons to their functions
        self.removeAlbumButton.clicked.connect(self.remove_album)
        self.removeBookButton.clicked.connect(self.remove_book)
        self.removeMovieButton.clicked.connect(self.remove_movie) 
        
        # Setting the size policies so the GUI dynamically resizes
        self.albumQueue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.bookQueue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.movieQueue.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.editAlbum.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.editBook.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.editMovie.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.removeAlbumButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.removeBookButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.removeMovieButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.album_ids = []
        self.book_ids = []
        self.movie_ids = []
        self.initialize_db('queuer.sqlite')
        self.load_db()


    # Initialize the SQLite db, mostly courtesy of sqlite docs
    def initialize_db(self, database_dir):
        self.con = sqlite3.connect(database_dir)
        self.cur = self.con.cursor()

        # Create tables if they don't exist
        self.cur.execute("CREATE TABLE IF NOT EXISTS albums(id INTEGER PRIMARY KEY AUTOINCREMENT, name)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY AUTOINCREMENT, name)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS movies(id INTEGER PRIMARY KEY AUTOINCREMENT, name)")

        # Commit the transaction
        self.con.commit()

    # Load the db (called when initializing application)
    def load_db(self):
        self.cur.execute("SELECT id, name FROM albums")
        for id, name in self.cur.fetchall():
            self.albumQueue.addItem(name)
            self.album_ids.append(id)
        
        self.cur.execute("SELECT id, name FROM books")
        for id, name in self.cur.fetchall():
            self.bookQueue.addItem(name)
            self.book_ids.append(id)

        self.cur.execute("SELECT id, name FROM movies")
        for id, name in self.cur.fetchall():
            self.movieQueue.addItem(name)
            self.movie_ids.append(id)

    # An 'event filter' for detecting when the enter key is pressed, so when to add to which list is known 
    def eventFilter(self, input_source, event):
        if event.type() == QtCore.QEvent.KeyPress and event.key() == QtCore.Qt.Key_Return:
            if input_source == self.editAlbum:
                self.add_album()
            elif input_source == self.editBook:
                self.add_book()
            elif input_source == self.editMovie:
                self.add_movie()
            return True
        return False

    # Functions to add X to the 'X' queue (and respective tables)
    def add_album(self):
        album_name = self.editAlbum.text() # set the album name to text in the input box
        if album_name:
            self.albumQueue.addItem(album_name)
            self.cur.execute("INSERT INTO albums (name) VALUES (?)", (album_name,))
            this_id = self.cur.lastrowid
            self.album_ids.append(this_id)
            self.con.commit()
            self.editAlbum.clear() # clear the input after adding

    def add_book(self):
        book_name = self.editBook.text()
        if book_name:
            self.bookQueue.addItem(book_name)
            self.cur.execute("INSERT INTO books (name) VALUES (?)", (book_name,))
            this_id = self.cur.lastrowid
            self.book_ids.append(this_id)
            self.con.commit()
            self.editBook.clear()

    def add_movie(self):
        movie_name = self.editMovie.text()
        if movie_name:
            self.movieQueue.addItem(movie_name)
            self.cur.execute("INSERT INTO movies (name) VALUES (?)", (movie_name,))
            this_id = self.cur.lastrowid
            self.movie_ids.append(this_id)
            self.con.commit()
            self.editMovie.clear()


    # General function to remove the first (chronologically) X added
    def remove_last(self, list_widget):
        if list_widget.count() > 0:
            list_widget.takeItem(0)
    
    # Specific functions to remove the last X added
    def remove_album(self):
        self.remove_last(self.albumQueue)

        # Remove last album from db, kinda makes having remove_last() pointless since list_widget.count() is used in a condition again
        self.cur.execute("DELETE FROM albums WHERE id = ?", (self.album_ids.pop(0),)) if self.albumQueue.count() > 0 else 0
        self.con.commit()

    def remove_book(self):
        self.remove_last(self.bookQueue)
        self.cur.execute("DELETE FROM books WHERE id = ?", (self.book_ids.pop(0),)) if self.bookQueue.count() > 0 else 0
        self.con.commit()

    def remove_movie(self):
        self.remove_last(self.movieQueue)
        self.cur.execute("DELETE FROM movies WHERE id = ?", (self.movie_ids.pop(0),)) if self.movieQueue.count() > 0 else 0
        self.con.commit()


    # Need this function to override the closeEvent method, could also just open and close db after every transaction
    def closeEvent(self, event):
        self.con.close()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QueuerWindow()
    window.show()
    sys.exit(app.exec_())
