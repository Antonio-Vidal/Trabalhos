import tkinter as tk
import random

# Função para desenhar uma linha usando o algoritmo de Bresenham
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return points

# Função para gerar um triângulo aleatório (3 lados)
def generate_random_triangle():
    canvas.delete("shape")
    global polygon_points  # Usar a variável global para armazenar os pontos do triângulo
    polygon_points = []

    for _ in range(3):  # Gerar 3 pontos para formar um triângulo
        x = random.randint(-11, 11)
        y = random.randint(-11, 11)
        polygon_points.append((x, y))

    # Desenhar o triângulo
    for i in range(len(polygon_points)):
        x0, y0 = polygon_points[i]
        x1, y1 = polygon_points[(i + 1) % len(polygon_points)]  # Conectar o último ponto ao primeiro
        line_points = bresenham_line(x0, y0, x1, y1)
        for (x, y) in line_points:
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    fill="black", tags="shape")

    return polygon_points

# Função para realizar a translação
def translate_polygon(dx, dy):
    global polygon_points
    canvas.delete("shape")

    # Aplicar translação a cada ponto
    translated_points = [(x + dx, y + dy) for x, y in polygon_points]

    # Desenhar o polígono transladado
    for i in range(len(translated_points)):
        x0, y0 = translated_points[i]
        x1, y1 = translated_points[(i + 1) % len(translated_points)]
        line_points = bresenham_line(x0, y0, x1, y1)
        for (x, y) in line_points:
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    fill="black", tags="shape")

    polygon_points = translated_points  # Atualizar os pontos do polígono original com os novos pontos

# Função para pegar as coordenadas de translação da interface e aplicá-las
def apply_translation():
    try:
        dx = int(entry_dx.get())
        dy = int(entry_dy.get())
        translate_polygon(dx, dy)
    except ValueError:
        print("Por favor, insira valores válidos para dx e dy.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerar Triângulo e Translação")

# Definindo o tamanho do pixel e o deslocamento
pixel_size = 20
offset = 240  # Para centralizar a grade

# Aumentando o tamanho da janela para acomodar a grade
canvas_width = 23 * pixel_size  # 23 quadrados (de -11 a 11)
canvas_height = 23 * pixel_size  # 23 quadrados (de -11 a 11)

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Função para desenhar a grade
def draw_grid():
    canvas.delete("grid")  # Limpar a grade anterior
    for x in range(-11, 12):
        for y in range(-11, 12):
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    outline="lightgray", tags="grid")

# Desenha a grade ao iniciar
draw_grid()

# Botão para gerar um triângulo aleatório
button_generate_triangle = tk.Button(root, text="Gerar Triângulo", command=lambda: generate_random_triangle())
button_generate_triangle.pack()

# Entradas para coordenadas de translação
label_dx = tk.Label(root, text="Deslocamento em X (dx):")
label_dx.pack()
entry_dx = tk.Entry(root)
entry_dx.pack()

label_dy = tk.Label(root, text="Deslocamento em Y (dy):")
label_dy.pack()
entry_dy = tk.Entry(root)
entry_dy.pack()

# Botão para aplicar a translação
button_translate = tk.Button(root, text="Aplicar Translação", command=apply_translation)
button_translate.pack()

# Inicializa a variável para armazenar os pontos do polígono (triângulo)
polygon_points = generate_random_triangle()

root.mainloop()
