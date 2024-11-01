import tkinter as tk

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

# Função para desenhar o polígono baseado nos pontos fornecidos
def draw_polygon():
    canvas.delete("shape")
    points = []
    try:
        # Obtendo os pontos de entrada do usuário
        point_values = entry_points.get().split(",")
        if len(point_values) < 8 or len(point_values) % 2 != 0:
            print("Por favor, insira pelo menos 4 pares de coordenadas (X, Y).")
            return

        # Converte os valores em inteiros e agrupa-os em pares (X, Y)
        for i in range(0, len(point_values), 2):
            x = int(point_values[i])
            y = int(point_values[i+1])
            points.append((x, y))

        # Desenhar as arestas do polígono
        global polygon_edges
        polygon_edges = set()  # Conjunto para armazenar os pontos das arestas

        for i in range(len(points)):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % len(points)]  # Conecta o último ao primeiro
            line_points = bresenham_line(x0, y0, x1, y1)
            for (x, y) in line_points:
                canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                        x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                        fill="black", tags="shape")
                polygon_edges.add((x, y))  # Armazena os pontos das arestas

        # Salva os pontos do polígono para usar no preenchimento
        global polygon_points
        polygon_points = points
    except ValueError:
        print("Por favor, insira valores válidos.")

# Função para realizar o preenchimento por varredura (scanline fill) sem preencher as arestas
def scanline_fill():
    if not polygon_points:
        print("Por favor, desenhe um polígono primeiro.")
        return

    # Determinando os limites do polígono
    ymin = min(p[1] for p in polygon_points)
    ymax = max(p[1] for p in polygon_points)

    # Lista de interseções por linha
    for y in range(ymin, ymax + 1):
        intersecoes = []

        # Encontrando interseções com as arestas
        for i in range(len(polygon_points)):
            x0, y0 = polygon_points[i]
            x1, y1 = polygon_points[(i + 1) % len(polygon_points)]

            if y0 > y1:  # Garantir que sempre calculamos de baixo para cima
                x0, x1 = x1, x0
                y0, y1 = y1, y0

            if y0 <= y < y1:  # Verifica se há interseção com a linha y
                x_intersecao = x0 + (y - y0) * (x1 - x0) // (y1 - y0)
                intersecoes.append(x_intersecao)

        # Ordena as interseções em ordem crescente
        intersecoes.sort()

        # Preenche as linhas entre as interseções, mas não preenche as arestas
        for i in range(0, len(intersecoes), 2):
            if i + 1 < len(intersecoes):
                x_start = intersecoes[i] + 1  # Começa um pixel após a aresta
                x_end = intersecoes[i + 1] - 1  # Termina um pixel antes da aresta
                for x in range(x_start, x_end + 1):
                    if (x, y) not in polygon_edges:  # Evitar preencher arestas
                        canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                                x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                                fill="red", tags="shape")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Preenchimento por Varredura - Apenas Interno")

# Definindo o tamanho do pixel e o deslocamento
pixel_size = 20
offset = 240  # Para centralizar a grade no canvas

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

# Campo de entrada único para os pontos
label_points = tk.Label(root, text="Pontos (X1,Y1,X2,Y2,...):")
label_points.pack()
entry_points = tk.Entry(root, width=50)
entry_points.pack()

# Botão para desenhar o polígono
button_draw_polygon = tk.Button(root, text="Gerar Polígono", command=draw_polygon)
button_draw_polygon.pack()

# Botão para preencher o polígono por varredura
button_fill_polygon = tk.Button(root, text="Preencher", command=scanline_fill)
button_fill_polygon.pack()

# Variáveis globais para armazenar os pontos do polígono e suas arestas
polygon_points = []
polygon_edges = set()

root.mainloop()
