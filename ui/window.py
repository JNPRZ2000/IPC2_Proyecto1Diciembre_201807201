import os
from tkinter.constants import END, CENTER, VERTICAL
from metodos.readxml import XMLReader
from objects.objects import EntryPlaceholder, ListaCircular, ListaDoble
from tkinter import Image, Tk, Button, Frame, Label, ttk, messagebox
import tkinter.font as TFont
from PIL import Image
from PIL import ImageTk
from thread.thread import TPlay

class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        x_ = self.winfo_screenwidth()//2-1360//2
        y_ = self.winfo_screenheight()//2-700//2
        self.resizable(0,0)
        self.geometry("1360x700+{}+{}".format(x_,y_))
        self.title("NOZC Media Player")
        self.library = None
        self.songslist = ListaDoble()
        self.playList = ListaCircular()
        self.actualPlaylist = None
        self.threadPlay = None
        self.listaPlayList = ListaDoble()
        self.initComponent()
    def initComponent(self):
        self.fondo = Frame(self, background = "#082032")
        self.fondo.place(x = 0, y = 0, width = 1360, height = 700)
        #BOTONES
        self.btnCargarXML = Button(self.fondo, text = "Cargar Archivo XML...", command = self.cargarXML)
        self.btnReportes = Button(self.fondo, text = "Reportes", command = self.reportes)
        self.btnPlay = Button(self.fondo, text = "Play", command = self.play)
        self.btnPause = Button(self.fondo, text = "Pause", command = self.pause)
        self.btnStop = Button(self.fondo, text = "Stop", command = self.stop)
        self.btnSiguiente = Button(self.fondo,  text = "Next", command = self.aNext)
        self.btnAnterior = Button(self.fondo, text = "Back", command = self.aBack)
        self.btnAddToList = Button(self.fondo, text = "Add To List →", command = self.addToList)
        self.btnSaveList = Button(self.fondo, text = "Save List", command = self.saveList)
        self.btnRandom = Button(self.fondo, text = "Random", bg = "#333", fg = "white")
        self.btnDelete = Button(self.fondo, text = "Clear List", command = self.addPlayList)
        self.btnExportList = Button(self.fondo, text = "Exportar Listas", command = self.exportarListas)
        #LABELS
        fontStyle = TFont.Font(family="Lucida Grande", size=13)
        self.labelCancion = Label(self.fondo, text = "Canción: ", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        self.labelAlbum = Label(self.fondo, text = "Album: ", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        self.labelArtista = Label(self.fondo, text = "Artista: ", font = fontStyle, bg = "#082032", fg = "white", anchor = "w")
        #FOTO
        self.foto = Frame(self.fondo)
        #Arbol
        self.addArbol()
        #PlayList
        self.addPlayList()
        #COMBOBOX
        self.cbbArtistas = ttk.Combobox(self.fondo, state = "readonly")
        self.cbbAlbumbes = ttk.Combobox(self.fondo, state = "readonly")
        self.cbbListas = ttk.Combobox(self.fondo, state = "readonly")
        self.cbbArtistas.bind("<<ComboboxSelected>>", self.change_artist)
        self.cbbAlbumbes.bind("<<ComboboxSelected>>", self.change_album)
        self.cbbArtistas.place(x = 890, y = 20, width = 120)
        self.cbbAlbumbes.place(x = 890, y = 60, width = 120)
        self.cbbListas.place(x = 890, y = 100, width = 120)
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
        self.btnAddToList.place(x = 900, y = 150, width = 100)
        self.btnSaveList.place(x = 900, y = 200, width = 100)
        self.btnRandom.place(x = 900, y = 250, width = 100) 
        self.btnDelete.place(x = 900, y = 300, width = 100)
        self.btnExportList.place(x = 900, y = 350, width = 100) 
    def addArbol(self):
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
        self.tabla.place(x = 410, y = 20, width = 450, height = 585)
    def addPlayList(self):
        self.entryPlaylist = EntryPlaceholder("Nombre de Playlist", self.fondo, color = "#333")
        self.entryPlaylist.config(justify = CENTER)
        columns2 = ("lista")
        self.tablePlaylist = ttk.Treeview(self.fondo, columns =  columns2, show = "headings")
        texto = self.entryPlaylist.get()
        self.tablePlaylist.heading("lista", text = texto)
        scrollbar2 = ttk.Scrollbar(self.fondo, orient = VERTICAL, command = self.tablePlaylist.yview)
        self.tablePlaylist.configure(yscrollcommand = scrollbar2.set)
        scrollbar2.place(x = 1320, y = 50, width = 20, height = 555)
        self.entryPlaylist.place(x = 1020, y = 20, width = 300, height = 30)
        self.tablePlaylist.place(x = 1020, y = 50, width = 300, height = 555)
        self.playList = ListaCircular()
    def cargarXML(self):
        lector = XMLReader()
        self.library = lector.analyze()
        self.songslist = self.library.toList()
        self.setArtistas()
    def setArtistas(self):
        Artistas = self.library.getArtistas()
        self.cbbArtistas["values"] = Artistas
        self.cbbArtistas.current(0)
        self.change_artist(None)
    def change_artist(self, event):
        self.setAlbumes()
    def setAlbumes(self):
        artista = self.cbbArtistas.current()
        artista = self.library.listaArtistas.getById(artista)
        self.cbbAlbumbes["values"] = artista.getAlbumes()
        self.cbbAlbumbes.current(0)
        self.setCanciones()
    def change_album(self, event):
        self.setCanciones()
    def setCanciones(self):
        self.addArbol()
        self.songslist = self.library.listaArtistas.getById(
            self.cbbArtistas.current()).listaAlbumes.getById(
                self.cbbAlbumbes.current()).getCanciones()
        for i in range(self.songslist.length):
            song = self.songslist.getById(i)
            row = ("{}".format(song.nombre),"{}".format(song.album),"{}".format(song.artista))
            self.tabla.insert('', END, values = row, iid = i)
        child_id = self.tabla.get_children()[0]
        self.tabla.focus(child_id)
        self.tabla.selection_set(child_id)     
    def addToList(self):
        self.tablePlaylist.heading("lista", text = self.entryPlaylist.get())
        if self.songslist.length > 0:
            song = self.songslist.getById(int(self.tabla.focus()))
            self.playList.append(song)
            row = ("{}".format(song.nombre), "{}".format(song.album), "{}".format(song.artista))
            self.tablePlaylist.insert('', END, values = row, iid = self.playList.length-1)
    def play(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.playList.head
            self.setInfo(self.actualPlaylist.value.nombre, self.actualPlaylist.value.album, self.actualPlaylist.value.artista)
            self.setPhoto(self.actualPlaylist)
            self.reproducir(self.actualPlaylist.value)
        elif self.songslist.length > 0 and self.playList.length == 0:
            for i in range(self.songslist.length):
                song = self.songslist.getById(i)
                self.playList.append(song)
                row = ("{}".format(song.nombre), "{}".format(song.album), "{}".format(song.artista))
                self.tablePlaylist.insert('', END, values = row, iid = i)
                self.play()    
    def aNext(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.next(self.actualPlaylist)
            self.tablePlaylist.focus(self.actualPlaylist.id)
            self.tablePlaylist.selection_set(self.actualPlaylist.id)
            self.reproducir(self.actualPlaylist.value)
    def aBack(self):
        if self.playList.length > 0:
            self.actualPlaylist = self.back(self.actualPlaylist)
            self.tablePlaylist.focus(self.actualPlaylist.id)
            self.tablePlaylist.selection_set(self.actualPlaylist.id)
            self.reproducir(self.actualPlaylist.value)
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
        try:
            self.img1 = Image.open(nodo.value.imagen)
            self.img1 = self.img1.resize((360,350), Image.ANTIALIAS)
            self.photoImg1 = ImageTk.PhotoImage(self.img1)
            self.lbl = Label(self.foto, image = self.photoImg1)
            self.lbl.place(x = 0,y = 0, width = 360, height = 350)
        except FileNotFoundError:
            print(FileNotFoundError)
    def setInfo(self, nombre, album, artista):
        self.labelCancion.config(text = "Canción {}".format(nombre))
        self.labelAlbum.config(text = "Album: {}".format(album))
        self.labelArtista.config(text = "Artista: {}".format(artista))
    def reproducir(self, cancion):
        if self.threadPlay != None:
            self.threadPlay.raise_exception()
            self.threadPlay.join()
        self.threadPlay = TPlay(cancion.ruta)
        self.threadPlay.start()
    def pause(self):
        if self.threadPlay != None:
            if self.threadPlay.estado != "p":
                self.threadPlay.estado = "p"
            else:
                self.threadPlay.estado = "r"
    def stop(self):
        if self.threadPlay != None:
            self.threadPlay.estado = "e"
    def reportes(self):
        if self.library != None:
            self.library.report()
            if self.listaPlayList.length > 0:
                string = """
digraph G{
    edge [weigth = 1000];
    subgraph listas{
        rankdir = LR;\n"""
                string2 = ""
                for i in range(self.listaPlayList.length):
                    lista = self.listaPlayList.getById(i)
                    string += '\t\t"{}"[color = beige style = "filled"];\n'.format(lista.nombre)
                    string2 +="\tsubgraph lista{}{}\n".format(i,"{")
                    string2 += "\t\trank = same;\n"
                    for j in range(lista.length):
                        cancion = lista.getById(j)
                        string2 += '\t\t"{}"[color = coral style = "filled"]\n'.format(cancion.nombre)
                    string2 += "\t}\n"
                string += '\t}\n'
                string += string2
                for i in range(self.listaPlayList.length):
                    lista = self.listaPlayList.getById(i)
                    if i+1 == self.listaPlayList.length:
                        string += '"{}"->"NoneL->"\n'.format(lista.nombre)
                    else:
                        siguiente = self.listaPlayList.getById(i+1)
                        string += '"{}"->"{}"\n'.format(lista.nombre, siguiente.nombre)
                    for j in range(lista.length):
                        cancion = lista.getById(j)
                        if j == 0:
                            string += '"{}"->"{}"'.format(lista.nombre, cancion.nombre)
                        if j+1 == lista.length:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(0).nombre)
                        else:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(j+1).nombre)
                for i in range(self.listaPlayList.length-1,-1,-1):
                    lista = self.listaPlayList.getById(i)
                    if i-1 == -1:
                        string += '"{}"->"<-NoneL"\n'.format(lista.nombre)
                    else:
                        siguiente = self.listaPlayList.getById(i-1)
                        string += '"{}"->"{}"\n'.format(lista.nombre, siguiente.nombre)
                    for j in range(lista.length-1,-1,-1):
                        cancion = lista.getById(j)
                        if j-1 == -1:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(lista.length-1).nombre)
                        else:
                            string += '"{}"->"{}"\n'.format(cancion.nombre, lista.getById(j-1).nombre)
                string += '}'
                file = open("grafo_circular.dot", "w")
                file.write(string)
                file.close()
                os.system('dot -Tpng grafo_circular.dot -o grafo_circular.png')
            else:
                messagebox.showerror(message = "No se han creado listas de reproducción", title = "Error")
        else:
            messagebox.showerror(message = "No se ha cargado ninguna biblioteca", title = "Error")
    def saveList(self):
        self.playList.nombre = self.entryPlaylist.get()
        aux = self.playList
        self.playList = None
        contenedor = self.listaPlayList.contains(aux.nombre)
        print("Contenedor: {}".format(contenedor))
        if contenedor == None:
            self.listaPlayList.append(aux)
            valores = []
            for i in range(self.listaPlayList.length):
                valores.append(self.listaPlayList.getById(i).nombre)
                self.cbbListas["values"] = valores
        else:
            messagebox.showwarning(title = "Alerta!!!", message = "Ya existe una lista de reproducción con este nombre")
        self.addPlayList()
    def exportarListas(self):
        if self.listaPlayList.length > 0:
            xml = '<?xml version = "1.0" encoding="UTF-8"?>\n'
            xml += '<ListasReproduccion>\n'
            for i in range(self.listaPlayList.length):
                lista = self.listaPlayList.getById(i)
                xml += '\t<Lista nombre = "{}">\n'.format(lista.nombre)
                for j in range(lista.length):
                    cancion = lista.getById(j)
                    xml += '\t\t<cancion nombre = "{}"\n'.format(cancion.nombre)
                    xml += '\t\t\t<artista>{}</artista>\n'.format(cancion.artista)
                    xml += '\t\t\t<album>{}</album>\n'.format(cancion.album)
                    xml += '\t\t\t<vecesReproducida>{}</vecesReproducida>\n'.format(0)
                    xml += '\t\t\t<imagen>{}</imagen>\n'.format(cancion.imagen)
                    xml += '\t\t\t<ruta>{}</ruta>\n'.format(cancion.ruta)
                    xml += '\t\t</cancion>\n'
                xml += '\t</Lista>\n'
            xml += '</ListasReproduccion>\n'
            file = open("Listas_de_reproducción.xml", "w")
            file.write(xml)
            file.close()