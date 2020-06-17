from PyQt5 import QtWidgets, QtGui, QtCore
import requests
from bs4 import BeautifulSoup
import sys

captionFont = QtGui.QFont('Bebas Neue', 28)
itemFont = QtGui.QFont('Century Gothic', 14)
miniFont = QtGui.QFont('Century Gothic', 12)
xminiFont = QtGui.QFont('Century Gothic', 10)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.language_dict = {'English': 'en', 'Türkçe': 'tr', 'Français': 'fr', 'Español': 'es', 'Deutsch': 'de'}
        self.setWindowTitle("Tureng search")
        self.setGeometry(0, 0, 800, 600)
        self.setMinimumSize(750, 550)
        self.tabledata = list()
        self.center()

        # Some strings
        self.pleaseTypeSomethingText = "Please type something in search bar"
        self.errorText = "Error!"
        self.wordNotFoundText = "Word not found: "

        # Translations might not be label
        self.translationsMightNotBe = QtWidgets.QLabel("Language translations might not be 100% accurate")
        self.translationsMightNotBe.setFont(xminiFont)

        # Language Translations Layout
        self.langTranslationLayout = QtWidgets.QHBoxLayout()
        self.langTranslationLayout.addWidget(self.translationsMightNotBe)
        self.langTranslationLayout.addStretch(3)

        # Header Text
        self.header = QtWidgets.QLabel("Tureng Search")
        self.header.setFont(captionFont)
        self.header.setAlignment(QtCore.Qt.AlignCenter)

        # Translate between and app language button
        self.translateBetween = QtWidgets.QLabel("Translate Between:")
        self.translateBetween.setFont(miniFont)

        self.appLanguage = QtWidgets.QLabel("App Language")
        self.appLanguage.setFont(miniFont)

        # Label's layout
        self.labelLayout = QtWidgets.QHBoxLayout()
        self.labelLayout.addStretch()
        self.labelLayout.addWidget(self.translateBetween)
        self.labelLayout.addStretch(3)
        self.labelLayout.addWidget(self.appLanguage)
        self.labelLayout.addStretch()

        # Language Combo box
        self.langCB = QtWidgets.QComboBox()
        self.langCB.addItems(list(self.language_dict.keys()))
        self.langCB.setFont(itemFont)
        self.langCB.setMinimumWidth(140)
        self.langCB.activated.connect(self.getLanguagePairs)

        # Search Box
        self.searchBar = QtWidgets.QLineEdit()
        self.searchBar.setPlaceholderText("Search in Tureng...")
        self.searchBar.setFont(itemFont)
        self.searchBar.setMinimumWidth(350)
        self.searchBar.returnPressed.connect(self.search)

        # TranslationBox
        self.pairCBox = QtWidgets.QComboBox()
        self.pairCBox.setFont(itemFont)
        self.pairCBox.setMinimumWidth(180)

        # Search button
        self.searchButton = QtWidgets.QPushButton("Search")
        self.searchButton.setFont(itemFont)
        self.searchButton.setMinimumWidth(125)
        self.searchButton.clicked.connect(self.search)

        # Combo box and search box layouts
        self.searchHLayout = QtWidgets.QHBoxLayout()

        self.searchHLayout.addWidget(self.pairCBox)
        self.searchHLayout.addWidget(self.searchBar)
        self.searchHLayout.addWidget(self.langCB)

        # Search button layout
        self.buttonHLayout = QtWidgets.QHBoxLayout()
        self.buttonHLayout.addStretch()
        self.buttonHLayout.addWidget(self.searchButton)
        self.buttonHLayout.addStretch()

        # Result table
        self.resultTable = QtWidgets.QTableWidget()
        self.resultTable.setRowCount(0)
        self.resultTable.setColumnCount(0)
        self.resultTable.setMinimumSize(600, 300)

        # Main Layout
        self.mainVLayout = QtWidgets.QVBoxLayout()
        self.mainVLayout.addWidget(self.header)
        self.mainVLayout.addStretch()
        self.mainVLayout.addLayout(self.labelLayout)
        self.mainVLayout.addLayout(self.searchHLayout)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addStretch()
        self.mainVLayout.addWidget(self.resultTable)
        self.mainVLayout.addStretch()
        self.mainVLayout.addLayout(self.langTranslationLayout)

        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.mainHLayout.addStretch()
        self.mainHLayout.addLayout(self.mainVLayout)
        self.mainHLayout.addStretch()

        self.setLayout(self.mainHLayout)
        self.getLanguagePairs()
        self.show()

    def getLanguagePairs(self):
        lang = self.language_dict[self.langCB.currentText()]
        self.pairCBox.clear()
        my_list = list()
        if lang == 'en':
            my_list = ['Turkish - English', 'German - English', 'French - English', 'Spanish - English']
            self.header.setText("Tureng Search")
            self.appLanguage.setText("App Language")
            self.translateBetween.setText("Translate Between:")
            self.searchBar.setPlaceholderText("Search in Tureng...")
            self.pleaseTypeSomethingText = "Please type something in search bar"
            self.errorText = "Error!"
            self.wordNotFoundText = "Word not found: "
            self.searchButton.setText("Search")
        elif lang == 'tr':
            my_list = ['Türkçe - İngilizce', 'Almanca - İngilizce', 'Fransızca - İngilizce', 'İspanyolca - İngilizce']
            self.header.setText("Tureng Arama")
            self.appLanguage.setText("Uygulama Dili")
            self.translateBetween.setText("Şu diller arasında çevir:")
            self.searchBar.setPlaceholderText("Tureng'de ara...")
            self.pleaseTypeSomethingText = "Lütfen arama çubuğuna bir şeyler giriniz"
            self.errorText = "Hata!"
            self.wordNotFoundText = "Kelime bulunamadı: "
            self.searchButton.setText("Ara")
        elif lang == 'fr':
            my_list = ['Turc - Anglais', 'Allemand - Anglais', 'Français - Anglais', 'Espagnol - Anglais']
            self.header.setText("Recherche Tureng")
            self.appLanguage.setText("Langue de l'application")
            self.translateBetween.setText("Traduire Entre:")
            self.searchBar.setPlaceholderText("Rechercher à Tureng...")
            self.pleaseTypeSomethingText = "Veuillez taper quelque chose dans la barre de recherche"
            self.errorText = "Erreur!"
            self.wordNotFoundText = "Mot introuvable: "
            self.searchButton.setText("Chercher")
        elif lang == 'es':
            my_list = ['Turco - Inglés', 'Alemán - Inglés', 'Francés - Inglés', 'Español - Inglés']
            self.header.setText("Búsqueda Tureng")
            self.appLanguage.setText("Idioma de la Aplicación")
            self.translateBetween.setText("Traducir Entre:")
            self.searchBar.setPlaceholderText("Buscar en Tureng...")
            self.pleaseTypeSomethingText = "Escribe algo en la barra de búsqueda"
            self.errorText = "Error!"
            self.wordNotFoundText = "Palabra no encontrada: "
            self.searchButton.setText("Buscar")
        elif lang == 'de':
            my_list = ['Türkisch - Englisch', 'Deutsch - Englisch', 'Französisch - Englisch', 'Spanisch - Englisch']
            self.header.setText("Tureng Suche")
            self.appLanguage.setText("App-Sprache")
            self.translateBetween.setText("Übersetzen Zwischen:")
            self.searchBar.setPlaceholderText("Suche in Tureng...")
            self.pleaseTypeSomethingText = "Bitte geben Sie etwas in die Suchleiste ein"
            self.errorText = "Error!"
            self.wordNotFoundText = "Wort nicht gefunden: "
            self.searchButton.setText("Suche")

        self.pairCBox.addItems(my_list)

    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def search(self): # Search word
        language = self.language_dict[self.langCB.currentText()]
        translate_between = self.pairCBox.currentText().replace('İ', 'I').lower().replace('ç', 'c').replace('é', 'e').\
            replace('á', 'a').replace('ó', 'o').replace('ñ', 'n').replace('ö', 'o').replace(' ', '').replace('ü', 'u').\
            replace('ı', 'i')
        if translate_between == 'aleman-ingles':
            translate_between = 'germano-ingles'
        word_to_search = self.searchBar.text().lower().strip()
        if len(word_to_search.replace(' ', '')) == 0:
            QtWidgets.QMessageBox.critical(self, self.errorText, self.pleaseTypeSomethingText,  QtWidgets.QMessageBox.Ok)
            return

        link = "https://tureng.com/{}/{}/{}".format(language, translate_between, word_to_search)

        try:
            self.tabledata = self.getData(link)
            self.createTable()
        except:
            QtWidgets.QMessageBox.critical(self, self.errorText, self.wordNotFoundText + word_to_search, QtWidgets.QMessageBox.Ok)
            return
    def getData(self, url): # geting data
        r = requests.get(url)
        soup = BeautifulSoup(r.content, features='lxml')
        table = soup.find_all("table", attrs={'class': 'table table-hover table-striped searchResultsTable'})
        table = table[0]
        rows = table.find_all("tr", attrs={'class': None, 'style': None})
        tabledata = list()
        for row in enumerate(rows):
            columns = row[1].find_all(['th', 'td'])
            self.temp_col = list()
            if row[0] == 0:
                self.temp_col.append(' ')
            for col in columns:
                if col.text:
                    if col.text[-1] == '\n':
                        self.temp_col.append(col.text.split()[0])
                    else:
                        self.temp_col.append(col.text)
            tabledata.append(tuple(self.temp_col[1:]))
        return tabledata

    def createTable(self): # Creating table
        self.resultTable.setRowCount(len(self.tabledata) - 1)
        self.resultTable.setColumnCount(len(self.tabledata[0]))
        self.resultTable.setHorizontalHeaderLabels(self.tabledata[0])
        for col in range(self.resultTable.columnCount()):
            self.resultTable.setColumnWidth(col, 600//3)

        for row in range(self.resultTable.rowCount()):
            for col in range(self.resultTable.columnCount()):
                item = QtWidgets.QTableWidgetItem(self.tabledata[row + 1][col])
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.resultTable.setItem(row, col, item)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()