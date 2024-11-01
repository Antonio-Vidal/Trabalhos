import tkinter as tk
from PIL import Image, ImageTk, ImageFilter

# Variáveis globais para armazenar a imagem original e a atual
original_image = None
current_image = None

# Funções de carregamento e conversão de imagem
def load_image():
    global original_image, current_image
    try:
        original_image = Image.open('imagem.bmp')  # Carregar a imagem BMP
        current_image = original_image.copy()
        display_image(current_image)
    except FileNotFoundError:
        print("Imagem não encontrada. Certifique-se de que 'imagem.bmp' está na pasta atual.")

def display_image(img):
    img_tk = ImageTk.PhotoImage(img)
    label_image.config(image=img_tk)
    label_image.image = img_tk  # Manter referência da imagem
    print(f"Modo da Imagem Atual: {img.mode}")  # Adiciona uma impressão do modo da imagem

# Funções de remoção de ruído
def apply_mean_filter():
    global current_image
    if current_image:
        # Aplicar filtro de média usando Pillow
        current_image = current_image.filter(ImageFilter.BoxBlur(radius=1))  # Filtro de média (blur)
        display_image(current_image)

def apply_median_filter():
    global current_image
    if current_image:
        current_image = current_image.filter(ImageFilter.MedianFilter(size=3))  # Filtro mediano
        display_image(current_image)

def apply_gaussian_filter():
    global current_image
    if current_image:
        current_image = current_image.filter(ImageFilter.GaussianBlur(radius=2))  # Filtro Gaussiano
        display_image(current_image)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Remoção de Ruído em Imagens BMP")

# Configura o layout
frame = tk.Frame(root)
frame.pack(side=tk.LEFT)

# Botões para carregamento de imagem
button_load = tk.Button(frame, text="Carregar Imagem", command=load_image)
button_load.pack()

# Botões para remoção de ruído
button_mean_filter = tk.Button(frame, text="Filtro de Média", command=apply_mean_filter)
button_mean_filter.pack()

button_median_filter = tk.Button(frame, text="Filtro Mediano", command=apply_median_filter)
button_median_filter.pack()

button_gaussian_filter = tk.Button(frame, text="Filtro Gaussiano", command=apply_gaussian_filter)
button_gaussian_filter.pack()

# Label para exibir a imagem
label_image = tk.Label(root)
label_image.pack()

# Inicia a aplicação
root.mainloop()

# Antonio Carlos Silva Vidal
# 202111140003
