from tkinter import Tk, Button, Frame, Label
import tkinter.font as TFont
class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.update()
        x_ = self.winfo_screenwidth()//2-720//2
        y_ = self.winfo_screenheight()//2-480//2
        self.resizable(0,0)
        self.geometry("720x480+{}+{}".format(x_,y_))
        self.title("IPC2 Media Player")
        self.initComponent()
    def initComponent(self):
        self.fondo = Frame(self, background = "#082032")
        self.fondo.place(x = 0, y = 0, width = 720, height = 480)
        #BOTONES
        self.btnCargarXML = Button(self.fondo, text = "Cargar Archivo XML...")
        self.btnReportes = Button(self.fondo, text = "Reportes")
        self.btnPlay = Button(self.fondo, text = "Play")
        self.btnPause = Button(self.fondo, text = "Pause")
        self.btnStop = Button(self.fondo, text = "Stop")
        self.btnSiguiente = Button(self.fondo,  text = "Next")
        self.btnAnterior = Button(self.fondo, text = "Back")
        #LABELS
        fontStyle = TFont.Font(family="Lucida Grande", size=13)
        self.labelCancion = Label(self.fondo, text = "Canción: ", font = fontStyle, bg = "#082032", fg = "white")
        self.labelAlbum = Label(self.fondo, text = "Album: ", font = fontStyle, bg = "#082032", fg = "white")
        self.labelArtista = Label(self.fondo, text = "Artista: ", font = fontStyle, bg = "#082032", fg = "white")
        #FOTO
        self.foto = Frame(self)
        #### UBICANDO ELEMENTOS ###
        self.btnCargarXML.place(x = 20, y = 20, width = 135, height = 25)
        self.btnReportes.place(x = 170, y = 20, width = 85, height = 25)
        self.foto.place(x = 40, y = 70, width = 400, height = 350)
        self.btnPlay.place(x = 40, y = 440, width = 60, height = 25)
        self.btnPause.place(x = 115, y = 440, width = 60, height = 25)
        self.btnStop.place(x = 190, y = 440, width = 60, height = 25)
        self.btnAnterior.place(x = 265, y = 440, width = 60, height = 25)
        self.btnSiguiente.place(x = 340, y = 440, width = 60, height = 25)
        self.labelCancion.place(x = 470, y = 70, height = 35)
        self.labelAlbum.place(x = 470, y = 115, height = 35)
        self.labelArtista.place(x = 470, y = 160, height = 35)

        
        




