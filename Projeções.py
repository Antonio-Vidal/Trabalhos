import tkinter as tk
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

# Função para projetar um ponto 3D para 2D com projeção ortogonal (de cima)
def project_orthogonal_top(points):
    return [(x, y) for x, y, z in points]  # Apenas projeta x e y

# Função para projetar um ponto 3D para 2D com projeção oblíqua (mais inclinada)
def project_oblique(points, angle=60, scale=1.5):  # Aumentamos o ângulo e o fator de escala
    angle_rad = math.radians(angle)
    return [
        (x + scale * z * math.cos(angle_rad), y + scale * z * math.sin(angle_rad)) 
        for x, y, z in points
    ]

# Função para projetar um ponto 3D para 2D com projeção em perspectiva
def project_perspective(points, d=5):
    return [(x / (z/d + 1), y / (z/d + 1)) if z/d + 1 != 0 else (x, y) for x, y, z in points]

# Função para desenhar o objeto 3D projetado em 2D e rasterizá-lo na grade
def draw_solid_3d(projection_function):
    canvas.delete("shape")  # Limpar o canvas antes de redesenhar

    if not solid_points or not solid_edges:
        return

    # Pegar a projeção 2D dos pontos
    projected_points = projection_function(solid_points)

    # Desenhar o objeto 3D original
    for edge in solid_edges:
        x0, y0, z0 = solid_points[edge[0]]
        x1, y1, z1 = solid_points[edge[1]]
        line_points_3d = bresenham_line(int(x0 * pixel_size + offset), int(-y0 * pixel_size + offset),
                                         int(x1 * pixel_size + offset), int(-y1 * pixel_size + offset))
        for (x, y) in line_points_3d:
            canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, fill="blue", tags="shape")  # Cor para o objeto 3D

    # Desenhar arestas projetadas (conectar os vértices conforme a lista de arestas)
    for edge in solid_edges:
        x0, y0 = projected_points[edge[0]]
        x1, y1 = projected_points[edge[1]]
        line_points_2d = bresenham_line(int(x0 * pixel_size + offset_2d), int(-y0 * pixel_size + offset_2d),
                                         int(x1 * pixel_size + offset_2d), int(-y1 * pixel_size + offset_2d))
        for (x, y) in line_points_2d:
            canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, fill="red", tags="shape")  # Cor para a projeção 2D

    # Desenhar linhas de projeção com cor mais fraca
    for i, (x0, y0, z0) in enumerate(solid_points):
        x1, y1 = projected_points[i]
        line_projection = bresenham_line(int(x0 * pixel_size + offset), int(-y0 * pixel_size + offset),
                                         int(x1 * pixel_size + offset_2d), int(-y1 * pixel_size + offset_2d))
        for (x, y) in line_projection:
            canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, fill="lightgreen", tags="shape")  # Cor mais fraca para a linha de projeção

# Funções para aplicar as projeções
def apply_orthogonal_projection():
    draw_solid_3d(project_orthogonal_top)

def apply_oblique_projection():
    draw_solid_3d(lambda points: project_oblique(points, angle=60, scale=1.5))  # Chama a projeção oblíqua com novos parâmetros

def apply_perspective_projection():
    draw_solid_3d(project_perspective)

# Função para adicionar um vértice
def add_vertex():
    try:
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = 5  # Adiciona um valor fixo para z
        solid_points.append((x, y, z))
        update_vertices_list()
    except ValueError:
        print("Coordenadas inválidas!")

# Função para adicionar uma aresta
def add_edge():
    try:
        v1 = int(entry_v1.get())
        v2 = int(entry_v2.get())
        if 0 <= v1 < len(solid_points) and 0 <= v2 < len(solid_points):
            solid_edges.append((v1, v2))
            update_edges_list()
        else:
            print("Índice de vértice inválido!")
    except ValueError:
        print("Índice de vértice inválido!")

# Atualiza a lista de vértices na interface
def update_vertices_list():
    listbox_vertices.delete(0, tk.END)
    for i, vertex in enumerate(solid_points):
        listbox_vertices.insert(tk.END, f"V{i}: {vertex}")

# Atualiza a lista de arestas na interface
def update_edges_list():
    listbox_edges.delete(0, tk.END)
    for i, edge in enumerate(solid_edges):
        listbox_edges.insert(tk.END, f"E{i}: {edge}")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Projeções de Sólidos 3D - Entrada de Vértices")

# Definindo o tamanho do pixel e o deslocamento
pixel_size = 10  # Diminuindo o tamanho do pixel para compactar a grade
offset = 100  # Offset para o objeto 3D
offset_2d = 250  # Offset para a projeção 2D ao lado do objeto 3D

# Aumentando o tamanho da janela para acomodar a grade
canvas_width = 400  # Ajustando a largura para caber o objeto e a projeção
canvas_height = 300  # Mantendo a altura compacta

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Função para gerar a grade no fundo
def draw_grid():
    canvas.delete("grid")  # Limpar a grade anterior
    for x in range(0, canvas_width, pixel_size):
        for y in range(0, canvas_height, pixel_size):
            canvas.create_rectangle(x, y, x + pixel_size, y + pixel_size, outline="lightgray", tags="grid")

# Desenha a grade ao iniciar
draw_grid()

# Variáveis para armazenar pontos e arestas
solid_points = []
solid_edges = []

# Campos de entrada para vértices
label_vertex = tk.Label(root, text="Adicionar Vértice (x, y):")
label_vertex.pack()

entry_x = tk.Entry(root, width=5)
entry_x.pack(side=tk.LEFT)
entry_x.insert(0, "x")

entry_y = tk.Entry(root, width=5)
entry_y.pack(side=tk.LEFT)
entry_y.insert(0, "y")

button_add_vertex = tk.Button(root, text="Adicionar Vértice", command=add_vertex)
button_add_vertex.pack(side=tk.LEFT)

# Lista de vértices
listbox_vertices = tk.Listbox(root, height=6)
listbox_vertices.pack()

# Campos de entrada para arestas
label_edge = tk.Label(root, text="Adicionar Aresta (V1, V2):")
label_edge.pack()

entry_v1 = tk.Entry(root, width=5)
entry_v1.pack(side=tk.LEFT)
entry_v1.insert(0, "V1")

entry_v2 = tk.Entry(root, width=5)
entry_v2.pack(side=tk.LEFT)
entry_v2.insert(0, "V2")

button_add_edge = tk.Button(root, text="Adicionar Aresta", command=add_edge)
button_add_edge.pack(side=tk.LEFT)

# Lista de arestas
listbox_edges = tk.Listbox(root, height=6)
listbox_edges.pack()

# Botões para escolher a projeção
button_orthogonal = tk.Button(root, text="Projeção Ortogonal", command=apply_orthogonal_projection)
button_orthogonal.pack()

button_oblique = tk.Button(root, text="Projeção Oblíqua", command=apply_oblique_projection)
button_oblique.pack()

button_perspective = tk.Button(root, text="Projeção em Perspectiva", command=apply_perspective_projection)
button_perspective.pack()

root.mainloop()
