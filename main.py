from objects.objects import ListaDoble
from ui.window import Window
from metodos.readxml import XMLReader
lector = XMLReader()
biblioteca = lector.analyze()
print(biblioteca)
#window = Window().mainloop()
