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

# Função para gerar um polígono aleatório
def generate_random_polygon():
    canvas.delete("shape")
    global polygon_points  # Use a variável global para armazenar os pontos do polígono
    num_points = random.randint(4, 8)  # Gera entre 4 e 8 pontos
    polygon_points = []

    for _ in range(num_points):
        x = random.randint(-11, 11)
        y = random.randint(-11, 11)
        polygon_points.append((x, y))

    # Desenhar o polígono
    for i in range(len(polygon_points)):
        x0, y0 = polygon_points[i]
        x1, y1 = polygon_points[(i + 1) % len(polygon_points)]  # Conecta ao primeiro ponto
        line_points = bresenham_line(x0, y0, x1, y1)
        for (x, y) in line_points:
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    fill="black", tags="shape")

# Função para implementar o Algoritmo de Sutherland-Hodgman
def sutherland_hodgman(subject_polygon, clip_polygon):
    def inside(p):
        return (clip_edge[0] * p[0] + clip_edge[1] * p[1] + clip_edge[2] > 0)

    def compute_intersection(p1, p2):
        # Calcular interseção entre a linha de clipping e a linha do polígono
        xdiff = (p2[0] - p1[0], clip_edge[0])
        ydiff = (p2[1] - p1[1], clip_edge[1])
        def det(p, q):
            return p[0] * q[1] - p[1] * q[0]
        return (det(p1, p2) * det(ydiff, (clip_edge[0], clip_edge[1])) / det(xdiff, ydiff), 
                det(p1, p2) * det(xdiff, (clip_edge[0], clip_edge[1])) / det(xdiff, ydiff))

    output_polygon = subject_polygon
    for clip_edge in clip_polygon:
        input_polygon = output_polygon
        output_polygon = []
        for i in range(len(input_polygon)):
            current_vertex = input_polygon[i]
            previous_vertex = input_polygon[i - 1]
            if inside(current_vertex):
                if not inside(previous_vertex):
                    output_polygon.append(compute_intersection(previous_vertex, current_vertex))
                output_polygon.append(current_vertex)
            elif inside(previous_vertex):
                output_polygon.append(compute_intersection(previous_vertex, current_vertex))
    return output_polygon

# Função para preencher a área de recorte na nova janela
def fill_polygon(crop_canvas, polygon):
    if not polygon:
        return

    # Determinar os limites do canvas
    x_min = min(p[0] for p in polygon)
    x_max = max(p[0] for p in polygon)
    y_min = min(p[1] for p in polygon)
    y_max = max(p[1] for p in polygon)

    for y in range(y_min, y_max + 1):
        intersections = []
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            if (p1[1] <= y < p2[1]) or (p2[1] <= y < p1[1]):
                # Calcular a interseção
                slope = (p2[0] - p1[0]) / (p2[1] - p1[1]) if p2[1] != p1[1] else 0
                x_intersect = p1[0] + slope * (y - p1[1])
                intersections.append(x_intersect)

        intersections.sort()
        for j in range(0, len(intersections), 2):
            x_start = max(int(intersections[j]), -11)
            x_end = min(int(intersections[j + 1]), 11)
            for x in range(x_start, x_end + 1):
                crop_canvas.create_rectangle((x - x_min) * pixel_size, (max_y - y) * pixel_size,
                                             (x - x_min + 1) * pixel_size, (max_y - y + 1) * pixel_size,
                                             fill="blue")

# Função para mostrar a área de recorte em uma nova janela
def crop_area():
    try:
        x0 = int(entry_x0.get())
        y0 = int(entry_y0.get())
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())

        # Define os limites da janela
        x_min = min(x0, x1)
        x_max = max(x0, x1)
        y_min = min(y0, y1)
        y_max = max(y0, y1)

        # Criar nova janela para mostrar a área de recorte
        crop_window = tk.Toplevel(root)
        crop_window.title("Área de Recorte")

        # Definindo o tamanho do pixel e o deslocamento para a nova janela
        crop_pixel_size = pixel_size
        crop_offset = crop_pixel_size * 2  # Para centralizar a grade

        # Dimensões da nova janela
        crop_canvas_width = (x_max - x_min + 1) * crop_pixel_size
        crop_canvas_height = (y_max - y_min + 1) * crop_pixel_size

        crop_canvas = tk.Canvas(crop_window, width=crop_canvas_width, height=crop_canvas_height, bg="white")
        crop_canvas.pack()

        # Desenhar nova grade na janela de recorte
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                crop_canvas.create_rectangle((x - x_min) * crop_pixel_size, (y_max - y) * crop_pixel_size,
                                             (x - x_min + 1) * crop_pixel_size, (y_max - y + 1) * crop_pixel_size,
                                             outline="lightgray")

        # Desenhar o polígono na nova janela
        for i in range(len(polygon_points)):
            x0, y0 = polygon_points[i]
            x1, y1 = polygon_points[(i + 1) % len(polygon_points)]  # Conecta ao primeiro ponto
            line_points = bresenham_line(x0, y0, x1, y1)
            for (x, y) in line_points:
                if x_min <= x <= x_max and y_min <= y <= y_max:  # Verifica se está dentro da área de recorte
                    crop_canvas.create_rectangle((x - x_min) * crop_pixel_size, (y_max - y) * crop_pixel_size,
                                                 (x - x_min + 1) * crop_pixel_size, (y_max - y + 1) * crop_pixel_size,
                                                 fill="black")

        # Criar o polígono de recorte
        clip_polygon = [(x_min, y_min), (x_max, y_min), (x_max, y_max), (x_min, y_max)]
        clipped_polygon = sutherland_hodgman(polygon_points, clip_polygon)

        # Preencher a área recortada
        fill_polygon(crop_canvas, clipped_polygon)

    except ValueError:
        print("Por favor, insira valores válidos.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerar Polígono e Recortar")

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
    canvas.delete("grid")  # Limpa a grade anterior
    for x in range(-11, 12):
        for y in range(-11, 12):
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    outline="lightgray", tags="grid")

# Desenha a grade ao iniciar
draw_grid()

# Botão para gerar um polígono aleatório
button_generate_polygon = tk.Button(root, text="Gerar Polígono", command=generate_random_polygon)
button_generate_polygon.pack()

# Entradas para a janela de recorte
label_x0 = tk.Label(root, text="X0:")
label_x0.pack()
entry_x0 = tk.Entry(root)
entry_x0.pack()

label_y0 = tk.Label(root, text="Y0:")
label_y0.pack()
entry_y0 = tk.Entry(root)
entry_y0.pack()

label_x1 = tk.Label(root, text="X1:")
label_x1.pack()
entry_x1 = tk.Entry(root)
entry_x1.pack()

label_y1 = tk.Label(root, text="Y1:")
label_y1.pack()
entry_y1 = tk.Entry(root)
entry_y1.pack()

# Botão para recortar a área
button_crop_area = tk.Button(root, text="Recortar", command=crop_area)
button_crop_area.pack()

# Inicializa a variável para armazenar os pontos do polígono
polygon_points = []

root.mainloop()
