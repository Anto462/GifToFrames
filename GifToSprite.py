import tkinter as tk #UI
from tkinter import ttk #UI
from PIL import Image, ImageTk #IMG
from PIL import Image, ImageSequence #ANALIZAR FRAMES
from tkinter import filedialog,simpledialog as simpledialog #UI EXP ARCHHIVOS
import os #SISTEMA OPERATIVO
import sys #SISTEMA



def resource_path(relative_path): #Siempre que se consulta a la ruta relativa es porque se esta consultando a la ruta donde esta actualmente el programa
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path) #Se hace return con la ruta actual donde esta ejecutandose el programa


def unpack_gif(src):
    image = Image.open(src) #se tomael gif que se pasa por parametro a la func
    frames = [] #lista frames
    disposal = [] #dumb

    for gifFrame in ImageSequence.Iterator(image): #Iterador de frames del gif
        disposal_method = gifFrame.disposal_method #bumb de frames
        disposal.append(disposal_method)
        frames.append(gifFrame.convert('RGBA')) #se guarda el frame convertido en RGBA (debe permitir transparencia)

    output = [] #resultado
    lastFrame = None
    for i, loadedFrame in enumerate(frames): #Carga y enumerado de los frames
        if disposal[i] == 2 and lastFrame is not None: #frame en dumb
            lastFrame.paste(loadedFrame, mask=loadedFrame) 
            output.append(lastFrame.copy().convert('P')) #resultado de el ultimo frame
        else:  # Tratar cualquier otro método como 'Do Not Dispose'
            output.append(loadedFrame.convert('P'))

        lastFrame = loadedFrame

    return output #Se regresa el listado


def save_all_frames(file): #Salvar frames
    "Saves all the frames of the gif as numbered png files"
    if not file:
        print("No file selected")
        return

    base_name = simpledialog.askstring("Input", "Nombre a guardar los frames:", parent=root) #Se solicita el nombre bajo el que se guardan los frames
    if not base_name:
        print("No se brindo nombre de frame")
        return

    folder_selected = filedialog.askdirectory() #Ubicacion de guardado de los frames
    if not folder_selected:
        print("No se eligio el folder objetivo")
        return

    im = unpack_gif(file[0]) #Gif base para ser separado en frames
    for n, i in enumerate(im): #Se hace un ciclo para enumerar los frames
        frame_file = f"{base_name}_{n:02d}.png" #Nombre elegido y numero de frame
        frame_path = os.path.join(folder_selected, frame_file) #Join de ruta con el nombre final del frame

        # Convertir a RGBA y cambiar tamaño
        resized_frame = i.convert('RGBA').resize((1280, 720), Image.LANCZOS) #Importante mantener en RGBA y LANCZOS

        # Guardar frame con transparencia
        resized_frame.save(frame_path, "PNG") #Se guarda el frame tras se reajustado
        print(f"Frame guardado en: {frame_path}")

    print("Proceso completado, Frames salvados")

# root.withdraw()
#UI
def getfile(): #Obtencion de img para UI
    global filename
    try:
        filename = filedialog.askopenfilenames(
            parent=root,
            initialdir=".",
            initialfile='tmp',
            filetypes=[("GIF", "*.gif"),
                    ("All files", "*")]
            )
        print(filename)
        img = Image.open(resource_path(filename[0]))
        img = img.resize((150, 150))
        img = ImageTk.PhotoImage(img)
        getfile.image = img
        label["image"] = img
        button2.pack()
    except:
        pass

filename = ""
root = tk.Tk()
root.title("Extractor de frames")

# Estilo para la barra de progreso, no utilizado 
style = ttk.Style(root)
style.theme_use('clam')
style.configure("TProgressbar", foreground='green', background='green')

img2 = tk.PhotoImage(file=resource_path("gif_split.png"))
label1 = tk.Label(master=root,
    image=img2)
label1.pack(padx=10, pady=10)
button = tk.Button(
    master=root,
    bg="cornflowerblue",
    text="Seleccion de GIF",
    command=getfile)
button.pack()
#Se muestra tras elegir el gif como vista previa

img3 = ImageTk.PhotoImage(file=resource_path("Shikiup.png"))
label = tk.Label(master=root,
    image=img3,
    )
label.pack()
button2 = tk.Button(
    master=root,
    bg="cornflowerblue",
    text="Pasar a frames .PNG",
    command=lambda: save_all_frames(filename))
# button2.pack()

root.mainloop()
# save_all_frames(filename)
#Se salvan los frames pero manteniendo el programa abierto