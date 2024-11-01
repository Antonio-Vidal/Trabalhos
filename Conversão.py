import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import numpy as np
from scipy.ndimage import uniform_filter

# Variáveis globais para armazenar a imagem original e a atual
original_image = None
current_image = None

# Funções de conversão de imagem
def load_image():
    global original_image, current_image
    try:
        original_image = Image.open('imagem.jpg')  # Carregar a imagem
        current_image = original_image.copy()
        display_image(current_image)
    except FileNotFoundError:
        print("Imagem não encontrada. Certifique-se de que 'imagem.jpg' está na pasta atual.")

def convert_rgb_to_grayscale():
    global current_image
    if original_image:
        current_image = original_image.convert('L')  # Conversão para tons de cinza
        display_image(current_image)

def convert_grayscale_to_binary():
    global current_image
    if current_image:
        if current_image.mode == 'L':
            current_image = current_image.point(lambda x: 255 if x > 128 else 0, '1')  # Binário
            display_image(current_image)

# Filtros
def apply_mean_filter():
    global current_image
    if current_image:
        # Aplicar filtro de média usando scipy
        image_array = np.array(current_image)
        filtered_array = uniform_filter(image_array, size=3)  # Filtro de média 3x3
        current_image = Image.fromarray(np.uint8(filtered_array))
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

def display_image(img):
    img_tk = ImageTk.PhotoImage(img)
    label_image.config(image=img_tk)
    label_image.image = img_tk  # Manter referência da imagem
    print(f"Modo da Imagem Atual: {img.mode}")  # Adiciona uma impressão do modo da imagem

# Configuração da interface gráfica
root = tk.Tk()
root.title("Conversão e Filtragem de Imagens")

# Configura o layout
frame = tk.Frame(root)
frame.pack(side=tk.LEFT)

# Botões para conversão de imagem
button_load = tk.Button(frame, text="Carregar Imagem", command=load_image)
button_load.pack()

button_rgb_to_gray = tk.Button(frame, text="RGB para Tons de Cinza", command=convert_rgb_to_grayscale)
button_rgb_to_gray.pack()

button_gray_to_binary = tk.Button(frame, text="Tons de Cinza para Binário", command=convert_grayscale_to_binary)
button_gray_to_binary.pack()

# Botões para filtragem
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
