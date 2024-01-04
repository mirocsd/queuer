import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QSizePolicy

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
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


    # This is an 'event filter' for detecting when the enter key is pressed,
    # so we know when to add to which list.    
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

    # Functions to add X to the 'X' queue
    def add_album(self):
        album_name = self.editAlbum.text() # set the album name to text in the input box
        if album_name:
            self.albumQueue.addItem(album_name)
            self.editAlbum.clear() # clear the input after adding

    def add_book(self):
        book_name = self.editBook.text()
        if book_name:
            self.bookQueue.addItem(book_name)
            self.editBook.clear()

    def add_movie(self):
        item_name = self.editMovie.text()
        if item_name:
            self.movieQueue.addItem(item_name)
            self.editMovie.clear()


    # Specific functions to remove the last X added
    def remove_album(self):
        self.remove_last(self.albumQueue)

    def remove_book(self):
        self.remove_last(self.bookQueue)

    def remove_movie(self):
        self.remove_last(self.movieQueue)


    # General function to remove the first (chronologically) X added
    def remove_last(self, list_widget):
        if list_widget.count() > 0:
            list_widget.takeItem(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
