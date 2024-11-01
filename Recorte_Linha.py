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

# Função para gerar uma linha aleatória
def generate_random_line():
    canvas.delete("shape")
    x0 = random.randint(-11, 11)
    y0 = random.randint(-11, 11)
    x1 = random.randint(-11, 11)
    y1 = random.randint(-11, 11)

    # Armazena os pontos da linha
    global random_line_points
    random_line_points = (x0, y0, x1, y1)

    line_points = bresenham_line(x0, y0, x1, y1)
    for (x, y) in line_points:
        canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                fill="black", tags="shape")

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
        crop_offset = crop_pixel_size * 2  # Para centralizar a grade no canvas

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

        # Desenhar a linha original na nova janela
        original_line_points = bresenham_line(random_line_points[0], random_line_points[1], random_line_points[2], random_line_points[3])
        for (x, y) in original_line_points:
            if x_min <= x <= x_max and y_min <= y <= y_max:
                crop_canvas.create_rectangle((x - x_min) * crop_pixel_size, (y_max - y) * crop_pixel_size,
                                             (x - x_min + 1) * crop_pixel_size, (y_max - y + 1) * crop_pixel_size,
                                             fill="black")

        # Preencher a área dentro da janela de recorte
        for x in range(x_min, x_max + 1):
            for y in range(y_min, y_max + 1):
                # Preencher com lightblue
                crop_canvas.create_rectangle((x - x_min) * crop_pixel_size, (y_max - y) * crop_pixel_size,
                                             (x - x_min + 1) * crop_pixel_size, (y_max - y + 1) * crop_pixel_size,
                                             fill="lightblue")

                # Desenhar a parte da linha que está dentro da janela de recorte
                if (x, y) in original_line_points:
                    crop_canvas.create_rectangle((x - x_min) * crop_pixel_size, (y_max - y) * crop_pixel_size,
                                                 (x - x_min + 1) * crop_pixel_size, (y_max - y + 1) * crop_pixel_size,
                                                 fill="red")

    except ValueError:
        print("Por favor, insira valores válidos.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Gerar Linha e Recortar")

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

# Botão para gerar uma linha aleatória
button_generate_line = tk.Button(root, text="Gerar Linha", command=generate_random_line)
button_generate_line.pack()

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

root.mainloop()
