import tkinter as tk

def draw_circle(x_center, y_center, radius):
    points = []
    x = radius
    y = 0
    p = 1 - radius  # Ponto inicial

    while x >= y:
        points.append((x_center + x, y_center + y))
        points.append((x_center + y, y_center + x))
        points.append((x_center - y, y_center + x))
        points.append((x_center - x, y_center + y))
        points.append((x_center - x, y_center - y))
        points.append((x_center - y, y_center - x))
        points.append((x_center + y, y_center - x))
        points.append((x_center + x, y_center - y))
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1

    # Adicionando pontos do raio
    points.append((x_center + radius, y_center))  # Ponto do raio no eixo X
    points.append((x_center, y_center + radius))  # Ponto do raio no eixo Y
    points.append((x_center - radius, y_center))  # Ponto do raio no eixo X negativo
    points.append((x_center, y_center - radius))  # Ponto do raio no eixo Y negativo

    return points

def draw_shapes():
    canvas.delete("shape")
    try:
        x_center = int(entry_x_center.get())
        y_center = int(entry_y_center.get())
        radius = int(entry_radius.get())

        if -11 < x_center < 11 and -11 < y_center < 11:
            # Desenha círculo
            if radius > 0:
                circle_points = draw_circle(x_center, y_center, radius)
                for (x, y) in circle_points:
                    canvas.create_rectangle(x * pixel_size + offset, -y * pixel_size + offset,
                                            x * pixel_size + pixel_size + offset, -y * pixel_size + pixel_size + offset,
                                            fill="black", tags="shape")
        else:
            print("As coordenadas do centro devem estar no intervalo -11 < x < 11 e -11 < y < 11.")
    except ValueError:
        print("Por favor, insira valores inteiros válidos.")

# Configuração da interface gráfica
root = tk.Tk()
root.title("Desenho de Círculos")

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

# Entradas para o centro e raio
label_x_center = tk.Label(root, text="Centro X:")
label_x_center.pack()
entry_x_center = tk.Entry(root)
entry_x_center.pack()

label_y_center = tk.Label(root, text="Centro Y:")
label_y_center.pack()
entry_y_center = tk.Entry(root)
entry_y_center.pack()

label_radius = tk.Label(root, text="Raio (Círculo):")
label_radius.pack()
entry_radius = tk.Entry(root)
entry_radius.pack()

button_draw = tk.Button(root, text="Desenhar Círculo", command=draw_shapes)
button_draw.pack()

root.mainloop()
