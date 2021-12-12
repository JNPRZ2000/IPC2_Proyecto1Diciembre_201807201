from tkinter import messagebox
class Nodo:
    def __init__(self, value, id):
        self.value = value
        self.id = id
        self.siguiente = None
        self.anterior = None
    def __str__(self) -> str:
        return str(self.value)
class ListaDoble:
    def __init__(self):
        self.lenght = 0
        self.cabeza = None
        self.cola = None
    def append(self, value):
        nuevo = Nodo(value, self.lenght)
        if self.cabeza == None:
            self.cabeza = nuevo
            self.cola = self.cabeza
        else:
            actual = self.cola
            nuevo.anterior = actual
            self.cola = nuevo
            actual.siguiente = self.cola
        self.lenght += 1
    def getById(self, id):
        if self.cabeza == None:
            return "No hay cabeza"
        else:
            if id < 0 or id >= self.lenght:
                return "Fuera de rango"
            else:
                actual = self.cabeza
                while actual.id != id:
                    actual = actual.siguiente
                return actual
    '''def contains(self, value):
        if self.cabeza == None:
            return False
        else:
            actual = self.cabeza
            while actual != None:
                if actual.value == value:
                    break
                else:
                    actual = actual.siguiente
            if actual != None:
                return actual.id
            else:
                return None'''
    def contains(self, nombre):
        if self.cabeza == None:
            return False
        else:
            actual = self.cabeza
            while actual != None:
                if actual.value.nombre == nombre:
                    break
                else:
                    actual = actual.siguiente
            if actual != None:
                return actual.id
            else:
                return None
    def travel(self):
        actual = self.cabeza
        while actual:
            actual = actual.siguiente
            return actual

    def __str__(self):
        if self.cabeza == None:
            return "[]"
        else:
            string = "["
            actual = self.cabeza
            while actual != None:
                if actual.siguiente == None:
                    string += "{}]".format(actual)
                else:
                    string += "{},".format(actual)
                actual = actual.siguiente
            return string

class Cancion:
    def __init__(self, nombre, album, artista, ruta, imagen):
        self.nombre = nombre
        self.album = album
        self.artista = artista
        self.ruta = ruta
        self.imagen = imagen
    def __str__(self):
        return "Canción: {}".format(self.nombre)
class Album:
    def __init__(self, nombre, imagen):
        self.nombre = nombre
        self.imagen = imagen
        self.listaCanciones = ListaDoble()
    def agregarCancion(self, nombre, ruta, imagen):
        if self.listaCanciones.containsC(nombre):
            messagebox.showwarning(message="Ya existe una canción con el nombre:\n{}\nAsí que no se ha agregado".format(nombre))
        else:
            self.listaCanciones.append(Cancion(nombre,ruta,imagen))
class Artista:
    def __init__(self, nombre):
        self.nombre = nombre
        self.listaAlbumes = ListaDoble()
    def agregarAlbum(self, nombre, imagen):
        if self.listaAlbumes.contains(nombre) == True:
            messagebox.showwarning(message="Ya existe una album con el nombre:\n{}\nAsí que no se ha agregado".format(nombre))
        else:
            self.listaAlbumes.append(Album(nombre, imagen))
class Library:
    def __init__(self):
        self.listaArtistas = ListaDoble()
    def addSong(self, song):
        new = song
        nombre = new.nombre
        album = new.album
        artista = new.artista
        imagen = new.imagen
        contains = self.listaArtistas.contains(artista)
        if contains != None:
            artist = self.listaArtistas.getById(contains)
            contains = artist.listaAlbumes.contains(album)
            if contains != None:
                album_ = artist.listaAlbumes.getById(contains)
                contains = album_.listaCanciones.contains(nombre)
                if contains != None:
                    print("Cancion en biblioteca.. Posición: {}".format(contains))
                else:
                    album.listaCanciones.append(new)
            else:
                artist.listaAlbumes.append(Album(album, imagen).listaCanciones.append(new))

        else:
            self.listaArtistas.append(Artista(artista).listaAlbumes.append(Album(album, imagen).listaCanciones.append(new)))
        



        
        