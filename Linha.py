import tkinter as tk

def bresenham(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    sx = 1 if dx > 0 else -1
    sy = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        err = dx / 2.0
        while x1 != x2:
            points.append((x1, y1))
            err -= dy
            if err < 0:
                y1 += sy
                err += dx
            x1 += sx
        points.append((x2, y2))
    else:
        err = dy / 2.0
        while y1 != y2:
            points.append((x1, y1))
            err -= dx
            if err < 0:
                x1 += sx
                err += dy
            y1 += sy
        points.append((x2, y2))
    
    return points

def draw_grid():
    # Desenha a grade de pixels
    canvas.delete("grid")  # Limpa a grade anterior
    for x in range(-11, 12):
        for y in range(-11, 12):
            canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                    x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                    outline="lightgray", tags="grid")

def draw_line():
    canvas.delete("line")
    try:
        x1 = int(entry_x1.get())
        y1 = int(entry_y1.get())
        x2 = int(entry_x2.get())
        y2 = int(entry_y2.get())

        if -11 < x1 < 11 and -11 < y1 < 11 and -11 < x2 < 11 and -11 < y2 < 11:
            points = bresenham(x1, y1, x2, y2)
            for (x, y) in points:
                # Ajusta as coordenadas para a grade de pixels
                canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                        x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                        fill="black", tags="line")
        else:
            print("As coordenadas devem estar no intervalo -11 < x < 11 e -11 < y < 11.")
    except ValueError:
        print("Por favor, insira valores inteiros válidos.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Desenho de Linha com Algoritmo de Bresenham")

# Definindo o tamanho do pixel e o deslocamento
pixel_size = 20
offset = 240  # Para centralizar a grade no canvas

# Aumentando o tamanho da janela para acomodar a grade
canvas_width = 23 * pixel_size  # 23 quadrados (de -11 a 11)
canvas_height = 23 * pixel_size  # 23 quadrados (de -11 a 11)

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Desenha a grade ao iniciar
draw_grid()

label_x1 = tk.Label(root, text="x1:")
label_x1.pack()
entry_x1 = tk.Entry(root)
entry_x1.pack()

label_y1 = tk.Label(root, text="y1:")
label_y1.pack()
entry_y1 = tk.Entry(root)
entry_y1.pack()

label_x2 = tk.Label(root, text="x2:")
label_x2.pack()
entry_x2 = tk.Entry(root)
entry_x2.pack()

label_y2 = tk.Label(root, text="y2:")
label_y2.pack()
entry_y2 = tk.Entry(root)
entry_y2.pack()

button_draw = tk.Button(root, text="Desenhar Linha", command=draw_line)
button_draw.pack()

root.mainloop()
