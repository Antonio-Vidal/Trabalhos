import tkinter as tk

# Função para calcular os pontos da curva de Bézier de grau 2
def bezier_curve(p0, p1, p2, steps=100):
    points = []
    for t in range(steps + 1):
        t /= steps
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        points.append((round(x), round(y)))  # Arredondar para usar o algoritmo de rasterização
    return points

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

# Função para desenhar a curva de Bézier
def draw_shapes():
    canvas.delete("shape")
    try:
        x0, y0 = int(entry_x0.get()), int(entry_y0.get())
        x1, y1 = int(entry_x1.get()), int(entry_y1.get())
        cx, cy = int(entry_cx.get()), int(entry_cy.get())

        if -11 < x0 < 11 and -11 < y0 < 11 and -11 < x1 < 11 and -11 < y1 < 11 and -11 < cx < 11 and -11 < cy < 11:
            # Desenha a curva de Bézier
            bezier_points = bezier_curve((x0, y0), (cx, cy), (x1, y1))
            for i in range(len(bezier_points) - 1):
                line_points = bresenham_line(bezier_points[i][0], bezier_points[i][1],
                                             bezier_points[i + 1][0], bezier_points[i + 1][1])
                for (x, y) in line_points:
                    canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                            x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                            fill="black", tags="shape")
        else:
            print("As coordenadas dos pontos devem estar no intervalo -11 < x, y < 11.")
    except ValueError:
        print("Por favor, insira valores inteiros válidos.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Desenho de Curvas de Bézier de Grau 2")

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

# Função auxiliar para criar entradas lado a lado
def create_entry_pair(label_text1, entry1, label_text2, entry2):
    frame = tk.Frame(root)
    frame.pack()
    
    label1 = tk.Label(frame, text=label_text1)
    label1.pack(side=tk.LEFT)
    entry1.pack(side=tk.LEFT)

    label2 = tk.Label(frame, text=label_text2)
    label2.pack(side=tk.LEFT)
    entry2.pack(side=tk.LEFT)

# Entradas para os pontos de controle da curva de Bézier (organizados em pares)
entry_x0 = tk.Entry(root)
entry_y0 = tk.Entry(root)
create_entry_pair("Ponto Inicial X0:", entry_x0, "Y0:", entry_y0)

entry_x1 = tk.Entry(root)
entry_y1 = tk.Entry(root)
create_entry_pair("Ponto Final X1:", entry_x1, "Y1:", entry_y1)

entry_cx = tk.Entry(root)
entry_cy = tk.Entry(root)
create_entry_pair("Ponto de Controle CX:", entry_cx, "CY:", entry_cy)

button_draw = tk.Button(root, text="Desenhar Curva de Bézier", command=draw_shapes)
button_draw.pack()

root.mainloop()

# Antonio Carlos Silva Vidal
# 202111140003
