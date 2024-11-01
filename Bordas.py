import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np

# Variáveis globais para armazenar a imagem original e a atual
original_image = None
current_image = None

# Função para carregar a imagem JPG
def load_image():
    global original_image, current_image
    try:
        # Carregar a imagem usando OpenCV (JPG)
        original_image = cv2.imread('imagem.jpg', cv2.IMREAD_GRAYSCALE)  # Imagem carregada em escala de cinza
        current_image = original_image.copy()
        display_image(current_image)
    except FileNotFoundError:
        print("Imagem não encontrada. Certifique-se de que 'imagem.jpg' está na pasta atual.")

# Função para exibir a imagem na interface
def display_image(img):
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
    label_image.config(image=img_tk)
    label_image.image = img_tk  # Manter referência da imagem

# Funções de detecção de borda
def apply_sobel():
    global current_image
    if current_image is not None:
        # Aplicar Sobel
        sobelx = cv2.Sobel(current_image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(current_image, cv2.CV_64F, 0, 1, ksize=3)
        sobel_combined = cv2.magnitude(sobelx, sobely)
        sobel_combined = np.uint8(sobel_combined)
        display_image(sobel_combined)

def apply_prewitt():
    global current_image
    if current_image is not None:
        # Prewitt utiliza convolução direta, definida manualmente
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
        
        # Aplicar filtros Prewitt em X e Y
        prewittx = cv2.filter2D(current_image, cv2.CV_64F, kernelx)
        prewitty = cv2.filter2D(current_image, cv2.CV_64F, kernely)
        
        # Calcular a magnitude da borda
        prewitt_combined = np.sqrt(prewittx**2 + prewitty**2)
        prewitt_combined = np.uint8(prewitt_combined)
        display_image(prewitt_combined)

def apply_canny():
    global current_image
    if current_image is not None:
        # Aplicar Canny
        canny_edges = cv2.Canny(current_image, 100, 200)
        display_image(canny_edges)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Detecção de Bordas - Sobel, Prewitt, Canny")

# Configura o layout
frame = tk.Frame(root)
frame.pack(side=tk.LEFT)

# Botão para carregar a imagem
button_load = tk.Button(frame, text="Carregar Imagem", command=load_image)
button_load.pack()

# Botões para aplicar filtros de borda
button_sobel = tk.Button(frame, text="Bordas Sobel", command=apply_sobel)
button_sobel.pack()

button_prewitt = tk.Button(frame, text="Bordas Prewitt", command=apply_prewitt)
button_prewitt.pack()

button_canny = tk.Button(frame, text="Bordas Canny", command=apply_canny)
button_canny.pack()

# Label para exibir a imagem
label_image = tk.Label(root)
label_image.pack()

# Inicia a aplicação
root.mainloop()

# Antonio Carlos Silva Vidal
# 202111140003
