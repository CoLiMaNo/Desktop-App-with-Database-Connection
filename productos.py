from tkinter import *
from tkinter import ttk
import tkinter as tk
import sqlite3
from clientes import Clientes

class Productos:
    # Ruta de la base de datos
    db = "database/productos.db"

    # Inicialización de la aplicación
    def __init__(self, master):
        self.master = master
        master.title("App Gestor de Recambios")
        master.resizable(1, 1)
        master.wm_iconbitmap('recursos/icon.ico')  # icono ventana

        # Creacion del contenedor Frame principal
        frame = LabelFrame(self.master, text="Registrar un nuevo Recambio", labelanchor="n")
        frame.grid(row=0, column=0, columnspan=3, pady=5)  # empieza en la columna 0 y la fila 0, ocupando 3 columnas

        # Label Nombre
        self.etiqueta_nombre = Label(frame, text="Nombre: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_nombre.grid(row=1, column=0)  # Posicionamiento a traves de grid

        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.nombre.focus()  # Para que el foco del raton vaya a este Entry al inicio
        self.nombre.grid(row=1, column=1)

        # Label Categoria
        self.etiqueta_categoria = Label(frame, text="Categoria: ")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_categoria.grid(row=2, column=0)  # Posicionamiento a traves de grid

        # Entry Categoria (caja de texto que recibira la categoria)
        self.categoria = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.categoria.grid(row=2, column=1)


        # Label Precio
        self.etiqueta_precio = Label(frame, text="Precio:")  # Etiqueta de texto ubicada en el frame
        self.etiqueta_precio.grid(row=3, column=0)  # Posicionamiento a traves de grid

        # Entry Precio
        self.precio = Entry(frame)  # Caja de texto (input de texto) ubicada en el frame
        self.precio.grid(row=3, column=1)

        # Boton Añadir Producto
        style2 = ttk.Style()
        # boton actualizar pantalla
        style2.configure("Guardar producto.TButton",
                         foreground="green")  # Ajusta los colores
        self.boton_aniadir = ttk.Button(frame, text="Guardar", command=self.add_producto,
                                        style="Guardar producto.TButton")
        self.boton_aniadir.grid(row=4 , columnspan=2, sticky=W + E)

        # Mensaje informativo para el usuario
        self.mensaje = Label(text="", fg="red")
        self.mensaje.grid(row=4, column=0, columnspan=2, sticky=W + E)

        # Creacion del contenedor Frame2 area clientes
        frame2 = LabelFrame(self.master, text="Area clientes       ", labelanchor="w")
        frame2.grid(row=5, column=0, columnspan=4, pady=10)

        # Boton abrir ventana clientes
        style2.configure("Entrar.TButton",
                         foreground="blue")  # Ajusta los colores
        self.boton_ventana_clientes = ttk.Button(frame2, text="Entrar", command=self.abrir_clientes,
                                                 style="Entrar.TButton")
        self.boton_ventana_clientes.grid(row=1, columnspan=3, sticky=W + E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Se modifica la fuente de la tabla
        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 13, 'bold'))  # Se modifica la fuente de las cabeceras
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla_productos = ttk.Treeview(height=20, columns=('Nombre', 'Categoria', 'Precio'),
                                            style="mystyle.Treeview")
        self.tabla_productos.grid(row=6, column=0, columnspan=2)

        # Configura el ancho de cada columna individualmente
        self.tabla_productos.column('#0', width=550, anchor=tk.W)
        self.tabla_productos.column('#1', width=250, anchor=tk.W)
        self.tabla_productos.column('#2', width=100, anchor=tk.W)

        # Configura la última columna para ocultarla
        self.tabla_productos.column('#3', width=0, stretch=tk.NO)

        # Configuración de encabezados
        self.tabla_productos.heading('#0', text='Nombre', anchor=CENTER)  # Encabezado 0
        self.tabla_productos.heading('#1', text='Categoria', anchor=CENTER)  # Encabezado 1
        self.tabla_productos.heading('#2', text='Precio', anchor=CENTER)  # Encabezado 2


        # Botones de editar y eliminar
        style2.configure("Eliminar.TButton",
                         foreground="red")  # Ajusta los colores
        boton_eliminar = ttk.Button(text="ELIMINAR", command=self.del_producto,
                                    style="Eliminar.TButton")
        boton_eliminar.grid(row=7, column=0, sticky=W + E)

        style2.configure("Editar.TButton",
                         foreground="blue")  # Ajusta los colores
        boton_editar = ttk.Button(text="EDITAR", command=self.edit_producto,
                                  style="Editar.TButton")
        boton_editar.grid(row=7, column=1, sticky=W + E)

        # Llamada al metodo get_productos() para obtener el listado de productos al inicio de la app
        self.get_productos()

    # Método para realizar consultas a la base de datos
    def db_consulta(self, consulta, parametros = ()):
        with sqlite3.connect(self.db) as con: # Iniciamos una conexion con la base de datos (alias con)
            cursor = con.cursor()  # Generamos un cursor de la conexion para poder operar en la base de datos
            resultado = cursor.execute(consulta, parametros)  # Preparar la consulta SQL (con parametros si los hay)
            con.commit()  # Ejecutar la consulta SQL preparada anteriormente
            return resultado  # Retornar el resultado de la consulta SQL

    # Método para obtener y mostrar recambios en la tabla
    def get_productos(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla_productos.get_children() # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla_productos.delete(fila)

        # Consulta SQL
        query = 'SELECT * FROM producto ORDER BY nombre DESC' # muestra todo de la tabla producto por nombre
                                                              # de forma descendente
        registros = self.db_consulta(query)  # Se hace la llamada al metodo db_consultas

        # Escribir los datos en pantalla
        for fila in registros:
            print(fila)
            self.tabla_productos.insert('', 0, text=fila[1],  values=(fila[2], fila[3])) # invocamos al objeto tabla (self.tabla)
                    # con el metodo insert, en el primer parametro ('') no ponemos nada es un identificador

    def validacion_nombre(self):
        return len(self.nombre.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_precio(self):
        return len(self.precio.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_categoria(self):
        return len(self.categoria.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    # Método para agregar nuevo recambio
    def add_producto(self):
        if self.validacion_nombre() and self.validacion_categoria() and self.validacion_precio():
            query = "INSERT INTO producto VALUES(NULL, ?, ?, ?)"
            parametros = (self.nombre.get(), self.categoria.get(), self.precio.get())
            self.db_consulta(query, parametros)
            print("Datos guardados")
            self.mensaje["text"] = "recambio {} añadido con exito".format(self.nombre.get())
            self.nombre.delete(0, END)
            self.categoria.delete(0, END)
            self.precio.delete(0, END)
            # print(self.nombre.get())
            # print(self.precio.get())
        elif self.validacion_nombre() and self.validacion_precio() == False:
            print("El precio es obligatorio")
            self.mensaje["text"] = "El precio es obligatorio"
        elif self.validacion_nombre() == False and self.validacion_precio():
            print("El nombre es obligatorio")
            self.mensaje["text"] = "El nombre es obligatorio"

        elif self.validacion_nombre() and self.validacion_categoria() == False:
            print("La categoria es obligatorio")
            self.mensaje["text"] = "La categoria es obligatorio"

        else:
            print("El nombre la categoria y el precio son obligatorios")
            self.mensaje["text"] = "El nombre, la categoria y el precio son obligatorio"
        self.get_productos()

    # Método para eliminar un recambio
    def del_producto(self):
        print("Eliminar recmbio")
        #print(self.tabla.item(self.tabla.selection()))
        #print(self.tabla.item(self.tabla.selection())["text"])

        self.mensaje["text"] =""
        nombre = self.tabla_productos.item(self.tabla_productos.selection())["text"]
        query = "DELETE FROM producto WHERE nombre = ?"
        self.db_consulta(query, (nombre,))
        self.mensaje["text"] = "Recambio {} eliminado con exito".format(nombre)
        self.get_productos()

    # Método para editar un recambio
    def edit_producto(self):
        print("Editar Recambio")
        self.mensaje["text"] =""

        old_nombre = self.tabla_productos.item(self.tabla_productos.selection())["text"]
        old_categoria = self.tabla_productos.item(self.tabla_productos.selection())["values"][0]
        old_precio = self.tabla_productos.item(self.tabla_productos.selection())["values"][1]

        # Ventana nueva (editar producto)
        self.ventana_editar = Toplevel() # Crear una ventana por delante de la principal
        self.ventana_editar.title("Editar Recambios") # Titulo de la ventana
        self.ventana_editar.resizable(1,1) # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_editar.wm_iconbitmap('recursos/icon.ico') # Icono de la ventana


        titulo = Label(self.ventana_editar, text="Edicion de Recambios", font=("Calibri", 30, "bold"))
        titulo.grid(row=0, column=0)

        # Creacion del contenedor Frame de la ventana de Editar Producto
        frame_ep = LabelFrame(self.ventana_editar, text= "Editar el siguiente Recambio")#frame_ep: Frame Editar Producto
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Nombre antiguo
        self.etiqueta_nombre_antiguo = Label(frame_ep, text="Nombre antiguo: ", font=("Calibri", 13)) # Etiqueta
                                                                                        # de texto ubicada en el frame
        self.etiqueta_nombre_antiguo.grid(row=2, column=0) # Posicionamiento a traves de grid

        # Entry Nombre antiguo (texto que no se podra modificar)
        self.input_nombre_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_nombre),
                                          state="readonly", font=("Calibri", 13))
        self.input_nombre_antiguo.grid(row=2, column=1)

        # Label Nombre nuevo
        self.etiqueta_nombre_nuevo = Label(frame_ep, text="Nombre nuevo: ", font=("Calibri", 13))
        self.etiqueta_nombre_nuevo.grid(row=3, column=0)

        # Entry Nombre nuevo (texto que si se podra modificar)
        self.input_nombre_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_nombre_nuevo.grid(row=3, column=1)
        self.input_nombre_nuevo.focus()  # Para que el foco del raton vaya a este Entry al inicio

        # Label Categoria antiguo
        self.etiqueta_categoria_antiguo = Label(frame_ep, text="Categoria antiguo: ", font=("Calibri", 13))  # Etiqueta
        # de texto ubicada en el frame
        self.etiqueta_categoria_antiguo.grid(row=4, column=0)  # Posicionamiento a traves de grid

        # Entry Categoria antiguo (texto que no se podra modificar)
        self.input_categoria_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_categoria),
                                          state="readonly", font=("Calibri", 13))
        self.input_categoria_antiguo.grid(row=4, column=1)

        # Label Categoria nuevo
        self.etiqueta_categoria_nuevo = Label(frame_ep, text="Categoria nuevo: ", font=("Calibri", 13))
        self.etiqueta_categoria_nuevo.grid(row=5, column=0)

        # Entry Categoria nuevo (texto que si se podra modificar)
        self.input_categoria_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_categoria_nuevo.grid(row=5, column=1)

        # Label precio antiguo
        self.etiqueta_precio_antiguo = Label(frame_ep, text="Precio antiguo: ", font=("Calibri", 13)) # Etiqueta de
                                                                                        # texto ubicada en el frame
        self.etiqueta_precio_antiguo.grid(row=6, column=0) # Posicionamiento a traves de grid

        # Entry Precio antiguo (texto que no se podra modificar)
        self.input_precio_antiguo = Entry(frame_ep, textvariable=StringVar(self.ventana_editar, value=old_precio),
                                          state="readonly", font=("Calibri", 13))
        self.input_precio_antiguo.grid(row=6, column=1)

        # Label Precio nuevo
        self.etiqueta_precio_nuevo = Label(frame_ep, text="Precio nuevo: ", font=("Calibri", 13))
        self.etiqueta_precio_nuevo.grid(row=7, column=0)

        # Entry Precio nuevo (texto que si se podra modificar)
        self.input_precio_nuevo = Entry(frame_ep, font=("Calibri", 13))
        self.input_precio_nuevo.grid(row=7, column=1)

        # Boton Actualizar Recambio
        self.boton_actualizar = ttk.Button(frame_ep, text="Actualizar Recambio", command=lambda: self.actualizar_productos(self.input_nombre_nuevo.get(),
                                                                                    self.input_nombre_antiguo.get(),
                                                                                    self.input_categoria_nuevo.get(),
                                                                                    self.input_categoria_antiguo.get(),
                                                                                    self.input_precio_nuevo.get(),
                                                                                    self.input_precio_antiguo.get()))

        self.boton_actualizar.grid(row=7, column=2, sticky=W+E)

    # Método para guardar información modificada
    def actualizar_productos(self, nombre_nuevo, nombre_antiguo, categoria_nuevo, categoria_antiguo, precio_nuevo, precio_antiguo ):
        query = "UPDATE producto SET nombre = ?, categoria = ?, precio = ? WHERE nombre = ? AND categoria = ? AND precio = ?" #Creación de la consulta SQL
        parametros = (nombre_nuevo, categoria_nuevo,precio_nuevo, nombre_antiguo, categoria_antiguo, precio_antiguo) #Creación de parámetros
        self.db_consulta(query, parametros) # Ejecución de la consulta a través de self.db_consulta
        self.ventana_editar.destroy() # Cierre de la ventana de edición
        self.mensaje["text"] = "El recambio {} ha sido actualizado con exito".format(nombre_antiguo) #Actualización del mensaje
        self.get_productos() #Recarga de la lista de productos

    # abre app gestor de clientes
    def abrir_clientes(self):
        ventana_clientes = Tk()
        app_clientes = Clientes(ventana_clientes)
        #self.master.withdraw()  # oculta la ventana gestor de productos


# Código principal
if __name__ == "__main__":
    root = Tk()
    app_productos = Productos(root)
    root.mainloop()
