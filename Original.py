import tkinter as tk
from tkinter import ttk, messagebox

def tabla_verdad(variable):
    combinaciones = 2 ** variable
    columnas = [[] for _ in range(variable)]

    for i in range(combinaciones):
        fila = []
        valor = i
        for _ in range(variable):
            fila.append(valor % 2)  
            valor //= 2  
        
        fila.reverse()  
        
        for j in range(variable):
            columnas[j].append(fila[j])
    
    return columnas



# Función simplificada para mostrar la tabla de verdad
def mostrar_tabla():
    try:
        variables = int(entrada_variables.get())
        
        if 2 <= variables <= 4:
            columnas = tabla_verdad(variables)
            
            
            for widget in tabla_frame.winfo_children():
                widget.destroy()

            
            encabezado = ['x', 'y', 'z', 'w'][:variables] + ['f']
            for i, titulo in enumerate(encabezado):
                tk.Label(tabla_frame, text=titulo, font=("Arial", 12, "bold")).grid(row=0, column=i, padx=10, pady=10)

            global comboboxes
            comboboxes = []

            
            for i in range(2**variables):
                for j in range(variables):
                    tk.Label(tabla_frame, text=columnas[j][i], font=("Arial", 12)).grid(row=i+1, column=j, padx=10, pady=10)
                
                combobox = ttk.Combobox(tabla_frame, values=["0", "1"], width=3)
                combobox.set("1")
                combobox.grid(row=i+1, column=variables, padx=10, pady=10)
                comboboxes.append(combobox)
            
        else:
            messagebox.showerror("Error", "El número de variables debe estar entre 2 y 4.")
    except ValueError:
        messagebox.showerror("Error", "Ingrese un número válido de variables.")


def obtener_valores_tabla():
    valores = [combobox.get() for combobox in comboboxes]
    return valores

def agrupaciones(valores, filas, columnas):
    agrupaciones_horizontal = []
    agrupaciones_vertical = []
    agrupaciones_4 = []
    agrupaciones_8 = []
    agrupadas_4 = set()  
    agrupadas_8 = set()
    
    
    for i in range(filas - 1):
        for j in range(columnas - 1):
            idx = i * columnas + j
            if (valores[idx] == '1' and valores[idx + 1] == '1' and
                valores[idx + columnas] == '1' and valores[idx + columnas + 1] == '1'):
                agrupaciones_4.append([(i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1)])                
                agrupadas_4.update([(i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1)])
    

    for i in range(filas - 1):
        for j in range(columnas - 3):  
            idx = i * columnas + j
            if (valores[idx] == '1' and valores[idx + 1] == '1' and valores[idx + 2] == '1' and valores[idx + 3] == '1' and
                valores[idx + columnas] == '1' and valores[idx + columnas + 1] == '1' and valores[idx + columnas + 2] == '1' and valores[idx + columnas + 3] == '1'):
                agrupaciones_8.append([(i, j), (i, j + 1), (i, j + 2), (i, j + 3), 
                                    (i + 1, j), (i + 1, j + 1), (i + 1, j + 2), (i + 1, j + 3)])
                agrupadas_8.update([(i, j), (i, j + 1), (i, j + 2), (i, j + 3),
                                    (i + 1, j), (i + 1, j + 1), (i + 1, j + 2), (i + 1, j + 3)])
    
    for i in range(filas - 3):
        for j in range(columnas - 1): 
            idx = i * columnas + j
            if (valores[idx] == '1' and valores[idx + columnas] == '1' and valores[idx + 2 * columnas] == '1' and valores[idx + 3 * columnas] == '1' and
                valores[idx + 1] == '1' and valores[idx + columnas + 1] == '1' and valores[idx + 2 * columnas + 1] == '1' and valores[idx + 3 * columnas + 1] == '1'):
                agrupaciones_8.append([(i, j), (i + 1, j), (i + 2, j), (i + 3, j),
                                    (i, j + 1), (i + 1, j + 1), (i + 2, j + 1), (i + 3, j + 1)])
                agrupadas_8.update([(i, j), (i + 1, j), (i + 2, j), (i + 3, j),
                                    (i, j + 1), (i + 1, j + 1), (i + 2, j + 1), (i + 3, j + 1)])


    for i in range(filas):
        for j in range(columnas):
            idx = i * columnas + j
            
            if j + 1 < columnas and valores[idx] == '1' and valores[idx + 1] == '1':
                if (i, j) not in agrupadas_4 and (i, j + 1) not in agrupadas_4 and (i, j) not in agrupadas_8 and (i, j + 1) not in agrupadas_8:  
                    agrupaciones_horizontal.append([(i, j), (i, j + 1)])
            
            if i + 1 < filas and valores[idx] == '1' and valores[idx + columnas] == '1':
                if (i, j) not in agrupadas_4 and (i + 1, j) not in agrupadas_4 and (i, j) not in agrupadas_8 and (i + 1, j) not in agrupadas_8:  
                    agrupaciones_vertical.append([(i, j), (i + 1, j)])

    return agrupaciones_horizontal, agrupaciones_vertical, agrupaciones_4, agrupaciones_8


def dibujar_mapa_karnaugh(valores):

    funcion_simplificada = ""
    num_valores = len(valores)
    if num_valores == 4: 
        filas, columnas = 2, 2
        etiquetas_vertical = ['x\'', 'x']
        etiquetas_horizontal = ['y\'', 'y']
        valores = [valores[0], valores[1], valores[2], valores[3]]


        if valores[0] == '1' and valores[1] == '1'  and valores[2] == '1' and valores[3] == '1':
            funcion_simplificada= "F(X,Y): (1)"
        elif valores[0] == '1' and valores[1] == '1'  and valores[2] == '1':
            funcion_simplificada= "F(X,Y): (x' V y')"
        elif valores[1] == '1' and valores[2] == '1'  and valores[3] == '1':
            funcion_simplificada= "F(X,Y): (x V y)"
        elif valores[3] == '1' and valores[0] == '1'  and valores[1] == '1':
            funcion_simplificada= "F(X,Y): (x' V y)"
        elif valores[0] == '1' and valores[2] == '1'  and valores[3] == '1':
            funcion_simplificada= "F(X,Y): (x V y')"
        else:
            
            if valores[0] == '1' and valores[1] == '1':
                funcion_simplificada = "F(X,Y): x'"
                x_prim = True
            if valores[2] == '1' and valores[3] == '1':
                funcion_simplificada = "F(X,Y): x"
            if valores[0] == '1' and valores[2] == '1':
                funcion_simplificada = "F(X,Y): y'"
                y_prim = True        
            if valores[1] == '1' and valores[3] == '1':
                funcion_simplificada = "F(X,Y): y"
            
    elif num_valores == 8:
        x_=False
        y_=False
        z_=False
        x_prim= False
        y_prim= False
        z_prim=False 
        filas, columnas = 2, 4
        etiquetas_vertical = ['x\'', 'x']
        etiquetas_horizontal = ['y\'z\'', 'y\'z', 'yz', 'yz\'']
        valores = [valores[0], valores[1], valores[3], valores[2],  
                    valores[4], valores[5], valores[7], valores[6]]
        if valores[0] == '1' and valores[1] == '1'  and valores[2] == '1' and valores[3] == '1' and valores[4] == '1' and valores[5] == '1'  and valores[6] == '1' and valores[7] == '1':
            funcion_simplificada= "F(X,Y,Z): (1)"
        else:
            if valores[0] == '1' and valores[1] == '1' and valores[2] == '1' and valores[3] == '1':
                funcion_simplificada = "F(X,Y,Z): x'"
                x_prim= True
            if valores[4] == '1' and valores[5] == '1' and valores[6] == '1' and valores[7] == '1':
                funcion_simplificada = "F(X,Y,Z): x"
                x_= True
            if valores[0] == '1' and valores[1] == '1' and valores[4] == '1' and valores[5] == '1':
                funcion_simplificada = "F(X,Y,Z): y'"
                y_prim= True
            if valores[2] == '1' and valores[3] == '1' and valores[6] == '1' and valores[7] == '1':
                funcion_simplificada = "F(X,Y,Z): y"
                y_= True
            if valores[0] == '1' and valores[3] == '1' and valores[4] == '1' and valores[7] == '1':
                funcion_simplificada = "F(X,Y,Z): z'"
                z_prim= True 
            if valores[1] == '1' and valores[2] == '1' and valores[5] == '1' and valores[6] == '1':
                funcion_simplificada = "F(X,Y,Z): z"
                z_= True

            if valores[0] == '1' and valores[4] == '1'  and valores[5] == '1' and valores[7] == '1' and valores[6]:
                funcion_simplificada= "F(X,Y,Z): x V (y' Ʌ z')"
            if valores[1] == '1' and valores[4] == '1'  and valores[5] == '1' and valores[7] == '1' and valores[6]:
                funcion_simplificada= "F(X,Y,Z): x V (y' Ʌ z)"            
            if valores[3] == '1' and valores[4] == '1'  and valores[5] == '1' and valores[7] == '1' and valores[6]:
                funcion_simplificada= "F(X,Y,Z): x V (y Ʌ z)"
            if valores[2] == '1' and valores[4] == '1'  and valores[5] == '1' and valores[7] == '1' and valores[6]:
                funcion_simplificada= "F(X,Y,Z): x V (y Ʌ z')"

            
            if y_prim == True and x_ == True:
                funcion_simplificada= "F(X,Y,Z): (y' V x)"
            if y_prim == True and x_prim == True:
                funcion_simplificada= "F(X,Y,Z): (y' V x')"            
            if y_prim == True and z_ == True:
                funcion_simplificada= "F(X,Y,Z): (y' V z)"
            if y_prim == True and z_prim == True:
                funcion_simplificada= "F(X,Y,Z): (y' V z')"
            if y_ == True and x_ == True:
                funcion_simplificada= "F(X,Y,Z): (y V x)"
            if y_ == True and x_prim == True:
                funcion_simplificada= "F(X,Y,Z): (y V x')"            
            if y_ == True and z_ == True:
                funcion_simplificada= "F(X,Y,Z): (y V z)"
            if y_ == True and z_prim == True:
                funcion_simplificada= "F(X,Y,Z): (y V z')"
            if x_ == True and z_ == True:
                funcion_simplificada= "F(X,Y,Z): (x V z)"
            if x_ == True and z_prim == True:
                funcion_simplificada= "F(X,Y,Z): (x V z')"
            if x_prim == True and z_prim == True:
                funcion_simplificada= "F(X,Y,Z): (x' V z')"
            if x_prim == True and z_ == True:
                funcion_simplificada= "F(X,Y,Z): (x' V z)"

            



    elif num_valores == 16:
        x_=False
        y_=False
        z_=False
        w_=False
        x_prim= False
        y_prim= False
        z_prim=False
        w_prim=False 
        filas, columnas = 4, 4
        etiquetas_vertical = ['x\'y\'', 'x\'y', 'xy', 'xy\'']
        etiquetas_horizontal = ['z\'w\'', 'z\'w', 'zw', 'zw\'']
        valores = [valores[0], valores[1], valores[3], valores[2],  
                    valores[4], valores[5], valores[7], valores[6],
                    valores[12], valores[13], valores[15], valores[14],
                    valores[8], valores[9], valores[11], valores[10]]
        if valores[0] == '1' and valores[1] == '1'  and valores[2] == '1' and valores[3] == '1' and valores[4] == '1' and valores[5] == '1'  and valores[6] == '1' and valores[7] == '1' and valores[8] == '1' and valores[9] == '1'  and valores[10] == '1' and valores[11] == '1' and valores[12] == '1' and valores[13] == '1'  and valores[14] == '1' and valores[15] == '1':
            funcion_simplificada= "F(X,Y,Z,W): (1)"
        else:
            if valores[0] == '1' and valores[1] == '1'  and valores[2] == '1' and valores[3] == '1' and valores[4] == '1' and valores[5] == '1'  and valores[6] == '1' and valores[7] == '1':
                funcion_simplificada ="F(X,Y,Z,W): x'"
                x_prim = True
            if valores[8] == '1' and valores[9] == '1'  and valores[10] == '1' and valores[11] == '1' and valores[12] == '1' and valores[13] == '1'  and valores[14] == '1' and valores[15] == '1':
                funcion_simplificada ="F(X,Y,Z,W): x"
                x_= True
            if valores[0] == '1' and valores[1] == '1'  and valores[2] == '1' and valores[3] == '1' and valores[11] == '1' and valores[10] == '1'  and valores[9] == '1' and valores[8] == '1':
                funcion_simplificada ="F(X,Y,Z,W): y'"
                y_prim = True
            if valores[4] == '1' and valores[5] == '1'  and valores[6] == '1' and valores[7] == '1' and valores[15] == '1' and valores[14] == '1'  and valores[13] == '1' and valores[12] == '1':
                funcion_simplificada ="F(X,Y,Z,W): y"
                y_ = True
            if valores[0] == '1' and valores[1] == '1'  and valores[4] == '1' and valores[5] == '1' and valores[8] == '1' and valores[9] == '1'  and valores[12] == '1' and valores[13] == '1':
                funcion_simplificada ="F(X,Y,Z,W): z'"
                z_prim = True
            if valores[2] == '1' and valores[3] == '1'  and valores[6] == '1' and valores[7] == '1' and valores[10] == '1' and valores[11] == '1'  and valores[14] == '1' and valores[15] == '1':
                funcion_simplificada ="F(X,Y,Z,W): z "
                z_ = True
            if valores[0] == '1' and valores[4] == '1'  and valores[12] == '1' and valores[8] == '1' and valores[2] == '1' and valores[6] == '1'  and valores[14] == '1' and valores[10] == '1':
                funcion_simplificada ="F(X,Y,Z,W): w'"
                w_prim=True
            if valores[1] == '1' and valores[3] == '1'  and valores[5] == '1' and valores[7] == '1' and valores[13] == '1' and valores[15] == '1'  and valores[9] == '1' and valores[11] == '1':
                funcion_simplificada ="F(X,Y,Z,W): w"
                w_=True

            if x_prim == True and y_prim == True:
                funcion_simplificada ="F(X,Y,Z,W): (x' V y')"
            if x_prim == True and y_ == True:
                funcion_simplificada ="F(X,Y,Z,W): (x' V y)"
            if x_prim == True and z_prim == True:
                funcion_simplificada ="F(X,Y,Z,W): (x' V z')"
            if x_prim == True and z_ == True:
                funcion_simplificada ="F(X,Y,Z,W): (x' V z)"
            if x_prim == True and w_prim == True:
                funcion_simplificada ="F(X,Y,Z,W): (x' V w')"
            if x_prim == True and w_ == True:
                funcion_simplificada ="F(X,Y,Z,W): (x' V w)"
            if y_prim == True and z_prim == True:
                funcion_simplificada ="F(X,Y,Z,W): (y' V z')"
            if y_prim == True and z_ == True:
                funcion_simplificada ="F(X,Y,Z,W): (y' V z)"
            if y_prim == True and w_prim == True:
                funcion_simplificada ="F(X,Y,Z,W): (y' V w')"
            if y_prim == True and w_ == True:
                funcion_simplificada ="F(X,Y,Z,W): (y' V w)"
            if z_prim == True and w_prim == True:
                funcion_simplificada ="F(X,Y,Z,W): (z' V w')"
            if z_prim == True and w_ == True:
                funcion_simplificada ="F(X,Y,Z,W): (z' V w)"
            if x_ == True and y_prim == True:
                funcion_simplificada="F(X,Y,Z,W):(x V y') "
            if x_ == True and z_prim == True:
                funcion_simplificada="F(X,Y,Z,W): (x V z')"
            if x_ == True and w_prim == True:
                funcion_simplificada="F(X,Y,Z,W): (x V w')"
            if x_ == True and y_ == True:
                funcion_simplificada="F(X,Y,Z,W):(x V y) "
            if x_ == True and z_ == True:
                funcion_simplificada="F(X,Y,Z,W): (x V z)"
            if x_ == True and w_ == True:
                funcion_simplificada="F(X,Y,Z,W): (x V w)"   
            if y_ == True and z_prim == True:
                funcion_simplificada="F(X,Y,Z,W): (y V z')"
            if y_ == True and w_prim == True:
                funcion_simplificada="F(X,Y,Z,W): (y V w')"
            if z_ == True and w_prim == True:
                funcion_simplificada="F(X,Y,Z,W): (z V w')"







    canvas.delete("all")

    cell_width = 60
    cell_height = 60

    agrupaciones_horizontal, agrupaciones_vertical, agrupaciones_4, agrupaciones_8 = agrupaciones(valores, filas, columnas)

    for i in range(filas):
        for j in range(columnas):
            x1 = j * cell_width + 50  
            y1 = i * cell_height + 50
            x2 = x1 + cell_width
            y2 = y1 + cell_height
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)
            idx = i * columnas + j
            if idx < num_valores and valores[idx] == '1':
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text="1", font=("Arial", 12), fill="red")

    for grupo in agrupaciones_horizontal:
        x1 = min(grupo[0][1], grupo[1][1]) * cell_width + 60
        y1 = min(grupo[0][0], grupo[1][0]) * cell_height + 60
        x2 = (max(grupo[0][1], grupo[1][1]) + 1) * cell_width + 40
        y2 = (max(grupo[0][0], grupo[1][0]) + 1) * cell_height + 40
        canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)

    for grupo in agrupaciones_vertical:
        x1 = min(grupo[0][1], grupo[1][1]) * cell_width + 55
        y1 = min(grupo[0][0], grupo[1][0]) * cell_height + 55
        x2 = (max(grupo[0][1], grupo[1][1]) + 1) * cell_width + 45
        y2 = (max(grupo[0][0], grupo[1][0]) + 1) * cell_height + 45
        canvas.create_rectangle(x1, y1, x2, y2, outline="green", width=2)

    for grupo in agrupaciones_4:
        x1 = min(grupo[0][1], grupo[1][1], grupo[2][1], grupo[3][1]) * cell_width + 60
        y1 = min(grupo[0][0], grupo[1][0], grupo[2][0], grupo[3][0]) * cell_height + 60
        x2 = (max(grupo[0][1], grupo[1][1], grupo[2][1], grupo[3][1]) + 1) * cell_width + 40
        y2 = (max(grupo[0][0], grupo[1][0], grupo[2][0], grupo[3][0]) + 1) * cell_height + 40
        canvas.create_rectangle(x1, y1, x2, y2, outline="orange", width=2)

    for grupo in agrupaciones_8:
        x1 = min(grupo[0][1], grupo[1][1], grupo[2][1], grupo[3][1], 
                 grupo[4][1], grupo[5][1], grupo[6][1], grupo[7][1]) * cell_width + 60
        y1 = min(grupo[0][0], grupo[1][0], grupo[2][0], grupo[3][0], 
                 grupo[4][0], grupo[5][0], grupo[6][0], grupo[7][0]) * cell_height + 60
        x2 = (max(grupo[0][1], grupo[1][1], grupo[2][1], grupo[3][1], 
                  grupo[4][1], grupo[5][1], grupo[6][1], grupo[7][1]) + 1) * cell_width + 40
        y2 = (max(grupo[0][0], grupo[1][0], grupo[2][0], grupo[3][0], 
                  grupo[4][0], grupo[5][0], grupo[6][0], grupo[7][0]) + 1) * cell_height + 40
        canvas.create_rectangle(x1, y1, x2, y2, outline="purple", width=2)

    for i in range(filas):
        y = i * cell_height + 100
        canvas.create_text(30, y, text=etiquetas_vertical[i], font=("Arial", 12, "bold"))

    for j in range(columnas):
        x = j * cell_width + 100
        canvas.create_text(x, 30, text=etiquetas_horizontal[j], font=("Arial", 12, "bold"))

    label_funcion_simplificada.config(text=funcion_simplificada)



def calcular_mapa():
    valores = obtener_valores_tabla()
    dibujar_mapa_karnaugh(valores)


root = tk.Tk()
root.title("Tabla de Verdad y Mapa de Karnaugh")
notebook=ttk.Notebook()

tabla_frame = tk.Frame(root)
tabla_frame.grid(row=0, column=0, padx=10, pady=10)


canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.grid(row=0, column=1, padx=10, pady=10)


label_funcion_simplificada = tk.Label(root, text="Funcion simplificada aparecerá aquí", font=("Arial", 12), fg="blue")
label_funcion_simplificada.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Número de variables (2-4):").grid(row=1, column=0, padx=10, pady=5)

entrada_variables = tk.Entry(root)
entrada_variables.grid(row=2, column=0, padx=10, pady=5)

btn_mostrar_tabla = tk.Button(root, text="Mostrar Tabla", command=mostrar_tabla)
btn_mostrar_tabla.grid(row=3, column=0, padx=10, pady=5)

btn_calcular = tk.Button(root, text="Calcular Mapa", command=calcular_mapa)
btn_calcular.grid(row=4, column=0, padx=10, pady=5)


root.mainloop()