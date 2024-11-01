import tkinter as tk
import random
import math

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

# Função para rotacionar um ponto em torno de um pivô
def rotate_point(x, y, angle, pivot_x, pivot_y):
    # Converter o ângulo para radianos
    radians = math.radians(angle)
    # Transladar o ponto para a origem do pivô
    translated_x = x - pivot_x
    translated_y = y - pivot_y
    # Aplicar a rotação
    rotated_x = translated_x * math.cos(radians) - translated_y * math.sin(radians)
    rotated_y = translated_x * math.sin(radians) + translated_y * math.cos(radians)
    # Transladar de volta ao ponto original
    return rotated_x + pivot_x, rotated_y + pivot_y

# Função para rotacionar o polígono
def rotate_polygon(angle, pivot_x, pivot_y):
    global polygon_points
    canvas.delete("shape")

    # Aplicar a rotação a cada ponto
    rotated_points = [rotate_point(x, y, angle, pivot_x, pivot_y) for x, y in polygon_points]

    # Desenhar o polígono rotacionado
    for i in range(len(rotated_points)):
        x0, y0 = rotated_points[i]
        x1, y1 = rotated_points[(i + 1) % len(rotated_points)]
        line_points = bresenham_line(int(x0), int(y0), int(x1), int(y1))
        for (x, y) in line_points:
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    fill="black", tags="shape")

    polygon_points = rotated_points  # Atualizar os pontos do polígono original com os novos pontos

# Função para pegar as entradas do ângulo e do ponto de pivô e aplicar a rotação
def apply_rotation():
    try:
        angle = float(entry_angle.get())
        pivot_x = int(entry_px.get())
        pivot_y = int(entry_py.get())
        if -360 <= angle <= 360:
            rotate_polygon(angle, pivot_x, pivot_y)
        else:
            print("O ângulo deve estar entre -360 e 360 graus.")
    except ValueError:
        print("Por favor, insira valores válidos para o ângulo e as coordenadas do pivô.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerar Triângulo e Rotação")

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

# Entradas para o ângulo de rotação e o ponto de pivô
label_angle = tk.Label(root, text="Ângulo de Rotação (-360 a 360):")
label_angle.pack()
entry_angle = tk.Entry(root)
entry_angle.pack()

label_px = tk.Label(root, text="Coordenada X do Pivô:")
label_px.pack()
entry_px = tk.Entry(root)
entry_px.pack()

label_py = tk.Label(root, text="Coordenada Y do Pivô:")
label_py.pack()
entry_py = tk.Entry(root)
entry_py.pack()

# Botão para aplicar a rotação
button_rotate = tk.Button(root, text="Aplicar Rotação", command=apply_rotation)
button_rotate.pack()

# Inicializa a variável para armazenar os pontos do polígono (triângulo)
polygon_points = generate_random_triangle()

root.mainloop()
