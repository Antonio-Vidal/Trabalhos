import tkinter as tk

# Função do algoritmo de Bresenham para rasterizar a linha
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

# Função para desenhar a polilinha conectando os pontos
def draw_shapes():
    canvas.delete("shape")
    try:
        # Obtenha o conjunto de pontos da entrada e os processe
        points = []
        raw_points = entry_points.get().split(",")
        
        # Verificar se temos pelo menos 8 entradas (4 pares de coordenadas)
        if len(raw_points) < 8:
            print("Insira pelo menos 4 pontos (8 valores de coordenadas X,Y).")
            return
        
        # Transformar os valores de string para inteiros e armazenar em 'points'
        for i in range(0, len(raw_points), 2):
            x = int(raw_points[i].strip())
            y = int(raw_points[i + 1].strip())
            points.append((x, y))

        # Verifique se há pelo menos 4 pontos para desenhar a polilinha
        if len(points) >= 4:
            for i in range(len(points) - 1):
                x0, y0 = points[i]
                x1, y1 = points[i + 1]
                if (-11 < x0 < 11 and -11 < y0 < 11 and -11 < x1 < 11 and -11 < y1 < 11):
                    # Desenhar linhas entre pontos consecutivos
                    line_points = bresenham_line(x0, y0, x1, y1)
                    for (x, y) in line_points:
                        canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                                x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                                fill="black", tags="shape")
                else:
                    print("As coordenadas dos pontos devem estar no intervalo -11 < x, y < 11.")
        else:
            print("Insira pelo menos 4 pontos (8 coordenadas).")
    except ValueError:
        print("Por favor, insira pares de coordenadas X,Y válidos separados por vírgula.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Desenho de Polilinhas")

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

# Entrada de múltiplos pontos (X,Y)
label_points = tk.Label(root, text="Insira pelo menos 4 pontos (X,Y) separados por vírgula, ex: 1,2,-1,3,4,5,6,7: ")
label_points.pack()

entry_points = tk.Entry(root)
entry_points.pack()

button_draw = tk.Button(root, text="Desenhar Polilinha", command=draw_shapes)
button_draw.pack()

root.mainloop()

# Antonio Carlos Silva Vidal
# 202111140003
