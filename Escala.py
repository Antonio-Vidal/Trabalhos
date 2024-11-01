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

# Função para escalonar um ponto em relação a um ponto fixo
def scale_point(x, y, scale_x, scale_y, fixed_x, fixed_y):
    # Transladar o ponto para a origem do ponto fixo
    translated_x = x - fixed_x
    translated_y = y - fixed_y
    # Aplicar a escala
    scaled_x = translated_x * scale_x
    scaled_y = translated_y * scale_y
    # Transladar de volta ao ponto original
    return scaled_x + fixed_x, scaled_y + fixed_y

# Função para escalonar o polígono
def scale_polygon(scale_x, scale_y, fixed_x, fixed_y):
    global polygon_points
    canvas.delete("shape")

    # Aplicar a escala a cada ponto
    scaled_points = [scale_point(x, y, scale_x, scale_y, fixed_x, fixed_y) for x, y in polygon_points]

    # Desenhar o polígono escalonado
    for i in range(len(scaled_points)):
        x0, y0 = scaled_points[i]
        x1, y1 = scaled_points[(i + 1) % len(scaled_points)]
        line_points = bresenham_line(int(x0), int(y0), int(x1), int(y1))
        for (x, y) in line_points:
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    fill="black", tags="shape")

    polygon_points = scaled_points  # Atualizar os pontos do polígono original com os novos pontos

# Função para pegar as entradas do fator de escala e do ponto fixo e aplicar a escala
def apply_scaling():
    try:
        scale_x = float(entry_scale_x.get())
        scale_y = float(entry_scale_y.get())
        fixed_x = int(entry_px.get())
        fixed_y = int(entry_py.get())
        
        # Validar os fatores de escala para garantir que sejam positivos
        if scale_x <= 0 or scale_y <= 0:
            print("Os fatores de escala devem ser maiores que 0.")
            return
        
        scale_polygon(scale_x, scale_y, fixed_x, fixed_y)
    except ValueError:
        print("Por favor, insira valores válidos para os fatores de escala e as coordenadas do ponto fixo.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerar Triângulo e Escalonamento")

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

# Entradas para os fatores de escala e o ponto fixo
label_scale_x = tk.Label(root, text="Fator de Escala para X (maior que 0):")
label_scale_x.pack()
entry_scale_x = tk.Entry(root)
entry_scale_x.pack()

label_scale_y = tk.Label(root, text="Fator de Escala para Y (maior que 0):")
label_scale_y.pack()
entry_scale_y = tk.Entry(root)
entry_scale_y.pack()

label_px = tk.Label(root, text="Coordenada X do Ponto Fixo:")
label_px.pack()
entry_px = tk.Entry(root)
entry_px.pack()

label_py = tk.Label(root, text="Coordenada Y do Ponto Fixo:")
label_py.pack()
entry_py = tk.Entry(root)
entry_py.pack()

# Botão para aplicar a escala
button_scale = tk.Button(root, text="Aplicar Escalonamento", command=apply_scaling)
button_scale.pack()

# Inicializa a variável para armazenar os pontos do polígono (triângulo)
polygon_points = generate_random_triangle()

root.mainloop()

# Antonio Carlos Silva Vidal
# 202111140003