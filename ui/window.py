from tkinter.constants import END, CENTER, VERTICAL
from metodos.readxml import XMLReader
from objects.objects import Cancion, EntryPlaceholder, ListaCircular, ListaDoble
from tkinter import PhotoImage, Tk, Button, Frame, Label, ttk
import tkinter.font as TFont

class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        #1366
        x_ = self.winfo_screenwidth()//2-1360//2
        y_ = self.winfo_screenheight()//2-700//2
        #self.resizable(0,0)
        self.geometry("1360x700+{}+{}".format(x_,y_))
        self.title("IPC2 Media Player")
        self.library = None
        self.songslist = ListaDoble()
        self.playList = ListaCircular()
        self.actualPlaylist = None
        self.initComponent()
    def initComponent(self):
        self.fondo = Frame(self, background = "#082032")
        self.fondo.place(x = 0, y = 0, width = 1360, height = 700)
        #BOTONES
        self.btnCargarXML = Button(self.fondo, text = "Cargar Archivo XML...", command = self.cargarXML)
        self.btnReportes = Button(self.fondo, text = "Reportes")
        self.btnPlay = Button(self.fondo, text = "Play", command = self.play)
        self.btnPause = Button(self.fondo, text = "Pause")
        self.btnStop = Button(self.fondo, text = "Stop")
        self.btnSiguiente = Button(self.fondo,  text = "Next", command = self.aNext)
        self.btnAnterior = Button(self.fondo, text = "Back", command = self.aBack)
        self.btnAddToList = Button(self.fondo, text = "Add To List →", command = self.addToList)
        self.btnSaveList = Button(self.fondo, text = "Save List")
        #LABELS
        fontStyle = TFont.Font(family="Lucida Grande", size=13)
        self.labelCancion = Label(self.fondo, text = "Canción: ", font = fontStyle, bg = "black", fg = "white", anchor = "w")
        self.labelAlbum = Label(self.fondo, text = "Album: ", font = fontStyle, bg = "black", fg = "white", anchor = "w")
        self.labelArtista = Label(self.fondo, text = "Artista: ", font = fontStyle, bg = "black", fg = "white", anchor = "w")
        #FOTO
        self.foto = Frame(self.fondo)
        #Arbol
        columns = ("cancion", "album", "artista")
        self.tabla = ttk.Treeview(self.fondo, columns = columns, show = "headings")
        self.tabla.heading('cancion',text = "Canción")
        self.tabla.heading('album', text = "Album")
        self.tabla.heading('artista', text = "Artista")
        self.tabla.column('cancion', width = 150)
        self.tabla.column('album', width = 150)
        self.tabla.column('artista', width = 150)
        scrollbar = ttk.Scrollbar(self.fondo, orient = VERTICAL, command = self.tabla.yview)
        self.tabla.configure(yscrollcommand = scrollbar.set)
        scrollbar.place(x= 860, y = 20, width = 20, height = 585)
        #PlayList
        self.entryPlaylist = EntryPlaceholder("Nombre de Playlist", self.fondo, color = "#333")
        self.entryPlaylist.config(justify = CENTER)
        columns2 = ("lista")
        self.tablePlaylist = ttk.Treeview(self.fondo, columns =  columns2, show = "headings")
        texto = self.entryPlaylist.get()
        self.tablePlaylist.heading("lista", text = texto)
        scrollbar2 = ttk.Scrollbar(self.fondo, orient = VERTICAL, command = self.tablePlaylist.yview)
        self.tablePlaylist.configure(yscrollcommand = scrollbar2.set)
        scrollbar2.place(x = 1320, y = 50, width = 20, height = 555)
        #### UBICANDO ELEMENTOS ###
        self.btnCargarXML.place(x = 20, y = 20, width = 135, height = 25)
        self.btnReportes.place(x = 170, y = 20, width = 85, height = 25)
        self.foto.place(x = 40, y = 70, width = 360, height = 350)
        self.btnPlay.place(x = 40, y = 440, width = 60, height = 25)
        self.btnPause.place(x = 115, y = 440, width = 60, height = 25)
        self.btnStop.place(x = 190, y = 440, width = 60, height = 25)
        self.btnAnterior.place(x = 265, y = 440, width = 60, height = 25)
        self.btnSiguiente.place(x = 340, y = 440, width = 60, height = 25)
        self.labelCancion.place(x = 40, y = 480, height = 35, width = 360)
        self.labelAlbum.place(x = 40, y = 525, height = 35, width = 360)
        self.labelArtista.place(x = 40, y = 570, height = 35, width = 360)
        self.tabla.place(x = 410, y = 20, width = 450, height = 585)
        self.btnAddToList.place(x = 900, y = 100, width = 100)
        self.btnSaveList.place(x = 900, y = 150, width = 100)
        self.entryPlaylist.place(x = 1020, y = 20, width = 300, height = 30)
        self.tablePlaylist.place(x = 1020, y = 50, width = 300, height = 555)
    def cargarXML(self):
        lector = XMLReader()
        self.library = lector.analyze()
        self.songslist = self.library.toList()
        for i in range(self.songslist.lenght):
            var = self.songslist.getById(i)
            row = ("{}".format(var.nombre), "{}".format(var.album), "{}".format(var.artista))
            self.tabla.insert('', END, values = row, iid = i)
        child_id = self.tabla.get_children()[0]
        self.tabla.focus(child_id)
        self.tabla.selection_set(child_id)
    def addToList(self):
        self.tablePlaylist.heading("lista", text = self.entryPlaylist.get())
        if self.songslist.lenght > 0:
            song = self.songslist.getById(int(self.tabla.focus()))
            self.playList.append(song)
            row = ("{}".format(song.nombre), "{}".format(song.album), "{}".format(song.artista))
            self.tablePlaylist.insert('', END, values = row)
    def play(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.playList.head
            self.setInfo(self.actualPlaylist.value.nombre, self.actualPlaylist.value.album, self.actualPlaylist.value.artista)
            self.setPhoto(self.actualPlaylist)
    def aNext(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.next(self.actualPlaylist)
    def aBack(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.back(self.actualPlaylist)
    def next(self, nodo):
        aux = nodo.siguiente
        self.setInfo(aux.value.nombre, aux.value.album, aux.value.artista)
        self.setPhoto(aux)
        return aux
    def back(self, nodo):
        aux = nodo.anterior
        self.setInfo(aux.value.nombre, aux.value.album, aux.value.artista)
        self.setPhoto(aux)
        return aux
    def setPhoto(self, nodo):
        self.imageAlb = PhotoImage(file = nodo.value.imagen)
        self.lbl = Label(self.foto, image = self.imageAlb)
        self.lbl.place(x = 0, y = 0, width = 360, height = 350)
    def setInfo(self, nombre, album, artista):
        self.labelCancion.config(text = "Canción {}".format(nombre))
        self.labelAlbum.config(text = "Album: {}".format(album))
        self.labelArtista.config(text = "Artista: {}".format(artista))

        




