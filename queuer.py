import sys
from PyQt5 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('./myui.ui', self)

        self.addAlbumButton.clicked.connect(self.add_album)
        self.addBookButton.clicked.connect(self.add_book)
        self.addMovieButton.clicked.connect(self.add_movie)

        self.removeAlbumButton.clicked.connect(self.remove_album)
        self.removeBookButton.clicked.connect(self.remove_book)
        self.removeMovieButton.clicked.connect(self.remove_movie) 
        

    def add_album(self):
        album_name = self.editAlbum.text()
        if album_name:
            self.listAlbums.addItem(album_name)
            self.musicNameEdit.clear()

    def add_book(self):
        book_name = self.bookNameEdit.text()
        if book_name:
            self.listBooks.addItem(book_name)
            self.bookNameEdit.clear()

    def add_movie(self):
        item_name = self.movieNameEdit.text()
        if item_name:
            self.listMovies.addItem(item_name)
            self.movieNameEdit.clear()

    def remove_album(self):
        self.remove_selected_item(self.listAlbum)

    def remove_book(self):
        self.remove_selected_item(self.listBooks)

    def remove_movie(self):
        self.remove_selected_item(self.listMovies)

    def remove_selected_item(self, list_widget):
        selected_item = list_widget.currentRow()
        if selected_item >= 0:
            list_widget.takeItem(selected_item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
