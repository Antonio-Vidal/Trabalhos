import tkinter as tk

def draw_ellipse(x_center, y_center, rx, ry):
    points = []
    x = 0
    y = ry

    # Inicializando parâmetros de decisão
    rx2 = rx * rx
    ry2 = ry * ry
    tworx2 = 2 * rx2
    twory2 = 2 * ry2
    px = 0
    py = tworx2 * y

    # Região 1
    p = round(ry2 - (rx2 * ry) + (0.25 * rx2))
    while px < py:
        points.append((x_center + x, y_center + y))
        points.append((x_center - x, y_center + y))
        points.append((x_center + x, y_center - y))
        points.append((x_center - x, y_center - y))
        x += 1
        px += twory2
        if p < 0:
            p += ry2 + px
        else:
            y -= 1
            py -= tworx2
            p += ry2 + px - py

    # Região 2
    p = round(ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2)
    while y >= 0:
        points.append((x_center + x, y_center + y))
        points.append((x_center - x, y_center + y))
        points.append((x_center + x, y_center - y))
        points.append((x_center - x, y_center - y))
        y -= 1
        py -= tworx2
        if p > 0:
            p += rx2 - py
        else:
            x += 1
            px += twory2
            p += rx2 - py + px

    return points

def draw_shapes():
    canvas.delete("shape")
    try:
        x_center = int(entry_x_center.get())
        y_center = int(entry_y_center.get())
        rx = int(entry_rx.get())
        ry = int(entry_ry.get())

        if -11 < x_center < 11 and -11 < y_center < 11:
            # Desenha elipse
            if rx > 0 and ry > 0:
                ellipse_points = draw_ellipse(x_center, y_center, rx, ry)
                for (x, y) in ellipse_points:
                    canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                            x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                            fill="black", tags="shape")
        else:
            print("As coordenadas do centro devem estar no intervalo -11 < x < 11 e -11 < y < 11.")
    except ValueError:
        print("Por favor, insira valores inteiros válidos.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Desenho de Elipses")

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

# Entradas para o centro e raios
label_x_center = tk.Label(root, text="Centro X:")
label_x_center.pack()
entry_x_center = tk.Entry(root)
entry_x_center.pack()

label_y_center = tk.Label(root, text="Centro Y:")
label_y_center.pack()
entry_y_center = tk.Entry(root)
entry_y_center.pack()

label_rx = tk.Label(root, text="Raio Horizontal (rx):")
label_rx.pack()
entry_rx = tk.Entry(root)
entry_rx.pack()

label_ry = tk.Label(root, text="Raio Vertical (ry):")
label_ry.pack()
entry_ry = tk.Entry(root)
entry_ry.pack()

button_draw = tk.Button(root, text="Desenhar Elipse", command=draw_shapes)
button_draw.pack()

root.mainloop()
