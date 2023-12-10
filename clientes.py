import sqlite3
from tkinter import *
from tkinter import ttk
import tkinter as tk



class Clientes:
    # Ruta de la base de datos
    dbc = "database/clientes.db"

    # Inicialización de la aplicación
    def __init__(self, master):
        self.master = master
        master.title("App Gestor de Clientes")
        self.ventana_clientes = master
        self.ventana_clientes.resizable(1, 1)
        self.ventana_clientes.wm_iconbitmap('recursos/icon2.ico')

        # Mensaje para mostrar información al usuario
        self.mensaje_c = Label(self.master, text="", fg="red")

        # Creacion del contenedor Frame principal
        frame2 = LabelFrame(self.master, text="Area Clientes", labelanchor= "n")
        frame2.grid(row=0, column=0, columnspan=9, pady=20, )

        # Label Nombre
        self.etiqueta_nombre = Label(frame2, text="Nombre: ")
        self.etiqueta_nombre.grid(row=1, column=0)

        # Entry Nombre (caja de texto que recibira el nombre)
        self.nombre = Entry(frame2)
        self.nombre.focus()
        self.nombre.grid(row=1, column=1)

        # Boton Añadir Clientes
        self.boton_Buscar_cliente = ttk.Button(frame2, text="Buscar Cliente", command=self.buscar_cliente,
                                               style="Buscar cliente.TButton")
        self.boton_Buscar_cliente.grid(row=2, columnspan=2, sticky=W + E)

        # Crear la tabla de clientes
        self.tabla_clientes = ttk.Treeview(self.ventana_clientes, columns=('fecha', 'nombre', 'telefono', 'direccion',
                                                                    'marca', 'modelo', 'matricula',
                                                                    'kilometros', 'averias'))

        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 11, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])

        # Estructura de la tabla
        self.tabla_clientes.column('0', width=0, stretch=tk.NO)  # Ancho 0 y stretch=NO para ocultar la ultima columna


        # Configuración de encabezados
        self.tabla_clientes.heading('#1', text='Fecha', anchor=CENTER)
        self.tabla_clientes.heading('#2', text='Nombre', anchor=CENTER)
        self.tabla_clientes.heading('#3', text='Telefono', anchor=CENTER)
        self.tabla_clientes.heading('#4', text='Direccion', anchor=CENTER)
        self.tabla_clientes.heading('#5', text='Marca', anchor=CENTER)
        self.tabla_clientes.heading('#6', text='Modelo', anchor=CENTER)
        self.tabla_clientes.heading('#7', text='Matricula', anchor=CENTER)
        self.tabla_clientes.heading('#8', text='Kilometros', anchor=CENTER)
        self.tabla_clientes.heading('#9', text='Averia', anchor=CENTER)
        self.tabla_clientes.grid(row=3, column=0, columnspan=4)  # ajustado a 3 columnas

        # Configura el ancho de cada columna individualmente
        self.tabla_clientes.column('#0', width=0, anchor=tk.W)
        self.tabla_clientes.column('#1', width=150, anchor=tk.W)
        self.tabla_clientes.column('#2', width=300, anchor=tk.W)
        self.tabla_clientes.column('#3', width=150, anchor=tk.W)
        self.tabla_clientes.column('#4', width=350, anchor=tk.W)
        self.tabla_clientes.column('#5', width=150, anchor=tk.W)
        self.tabla_clientes.column('#6', width=150, anchor=tk.W)
        self.tabla_clientes.column('#7', width=150, anchor=tk.W)
        self.tabla_clientes.column('#8', width=150, anchor=tk.W)
        self.tabla_clientes.column('#9', width=300, anchor=tk.W)


        # Crear un Frame para contener los botones
        frame2_botones = tk.Frame(self.ventana_clientes)
        frame2_botones.grid(row=5, column=0, columnspan=4, sticky='we')

        # Botones actualizar pantalla, eliminar, nuevo y salir
        style2 = ttk.Style()
        #boton actualizar pantalla
        style2.configure("Actualizar pantalla.TButton",
                        foreground="blue")  # Ajusta los colores
        boton_ver = ttk.Button(frame2_botones, text="ACTUALIZAR PANTALLA", command=self.get_cliente,
                               style="Actualizar pantalla.TButton")
        boton_ver.grid(row=0, column=0, sticky='we')

       # Boton eliminar cliente
        style2.configure("Eliminar.TButton",
                        foreground="red")  # Ajusta los colores
        boton_eliminar = ttk.Button(frame2_botones, text="ELIMINAR", command=self.eliminar_cliente,
                                    style="Eliminar.TButton")
        boton_eliminar.grid(row=0, column=1, sticky='we')

       # Boton nuevo abre ventana emergente agregar nuevo ingreso
        style2.configure("Nuevo.TButton",
                        foreground="green")  # Ajusta los colores
        boton_ventana_cliente_nuevo = ttk.Button(frame2_botones, text="NUEVO", command=self.add_nuevo,
                                                 style="Nuevo.TButton")
        boton_ventana_cliente_nuevo.grid(row=0, column=2, sticky='we')

        # Boton salir
        style2.configure("Salir.TButton",
                        foreground="black")  # Ajusta los colores
        boton_salir = ttk.Button(frame2_botones, text="SALIR", command=self.salir,
                                  style="Salir.TButton")
        boton_salir.grid(row=0, column=3, sticky='we')

        #Llamada al metodo get_cliente() para obtener el listado de clientes al inicio de la app
        self.get_cliente()

        # Ubicacion Mensaje informativo para el usuario
        self.mensaje_c.grid(row=3, column=0, columnspan=2, sticky=W + E)

    # Método para realizar consultas a la base de datos
    def db_consulta_clientes(self, consulta, parametros=()):
        with sqlite3.connect(self.dbc) as con: # Iniciamos una conexion con la base de datos (alias con)
            cursor = con.cursor()  # Generamos un cursor de la conexion para poder operar en la base de datos
            resultado = cursor.execute(consulta, parametros)  # Preparar la consulta SQL (con parametros si los hay)
            con.commit()  # Ejecutar la consulta SQL preparada anteriormente
            return resultado  # Retornar el resultado de la consulta SQL

    # Método para obtener y mostrar clientes en la tabla
    def get_cliente(self):
        # Lo primero, al iniciar la app, vamos a limpiar la tabla por si hubiera datos residuales o antiguos
        registros_tabla = self.tabla_clientes.get_children()  # Obtener todos los datos de la tabla
        for fila in registros_tabla:
            self.tabla_clientes.delete(fila)

        # Consulta SQL
        query = 'SELECT fecha, nombre, telefono, direccion, marca, modelo, matricula, kilometros, averia FROM cliente ORDER BY nombre DESC' \
                ''
        registros = self.db_consulta_clientes(query)

        # Escribir los datos en pantalla
        for fila in registros:
            print(fila)
            self.tabla_clientes.insert('', 0, values=fila[0:9])

    # Método para buscar clientes por nombre
    def buscar_cliente(self):
        # Obtiene el nombre ingresado en la Entry de búsqueda
        nombre = self.nombre.get()

        # Limpia la tabla antes de mostrar los resultados de la búsqueda
        registros_tabla = self.tabla_clientes.get_children()
        for fila in registros_tabla:
            self.tabla_clientes.delete(fila)

        # Consulta SQL para buscar clientes por nombre (insensible a mayúsculas y minúsculas)
        query = 'SELECT fecha, nombre, telefono, direccion, marca, modelo, matricula, kilometros, averia FROM cliente WHERE LOWER(nombre) LIKE LOWER(?)'
        nombre_like = f'%{nombre}%'
        registros = self.db_consulta_clientes(query, (nombre_like,))

        # Muestra los resultados en la tabla
        for fila in registros:
            self.tabla_clientes.insert('', 0, values=fila[0:9])

        # Mensaje informativo si no hay resultados
        if not registros:
            self.mensaje_c["text"] = "No se encontraron resultados para la búsqueda: {}".format(nombre)
        else:
            self.mensaje_c["text"] = ""  # Limpia el mensaje si hay resultados

        # Limpia el contenido del Entry después de realizar la búsqueda
        self.nombre.delete(0, END)

        # Mensaje informativo para el usuario
#        self.mensaje_c.grid(row=3, column=0, columnspan=2, sticky=S)



    def validacion_fecha(self):
        return len(self.fecha.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_nombre(self):
        return len(self.nombre_ac.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_telefono(self):
        return len(self.telefono.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_direccion(self):
        return len(self.direccion.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_marca(self):
        return len(self.marca.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_modelo(self):
        return len(self.modelo.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_matricula(self):
        return len(self.matricula.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    def validacion_averia(self):
        return len(self.averia.get()) != 0  # comprueba el tamaño y si es distinto que cero devuelve un True

    # Método para agregar nuevo cliente
    def add_nuevo(self):
        print("Agregar Nuevo")
        self.mensaje_c["text"] = ""

        # Ventana nueva (agregar cliente)
        self.ventana_nuevo = Toplevel()  # Crear una ventana por delante de la principal
        self.ventana_nuevo.title("Nuevo Ingreso")  # Titulo de la ventana
        self.ventana_nuevo.resizable(1, 1)  # Activar la redimension de la ventana. Para desactivarla: (0,0)
        self.ventana_nuevo.wm_iconbitmap('recursos/icon2.ico')  # Icono de la ventana

        titulo = Label(self.ventana_nuevo, text="Nuevo Ingreso", font=("Calibri", 30, "bold"))
        titulo.grid(row=0, column=0)

        # Creacion del contenedor Frame de la ventana de Agregar Nuevo
        frame_ac = LabelFrame(self.ventana_nuevo,
                              text="Registrar Ingreso", labelanchor="n")  # frame_ac: Frame Agregar cliente
        frame_ac.grid(row=1, column=0, columnspan=20, pady=20)

        # Label Fecha input
        self.etiqueta_fecha = Label(frame_ac, text="Fecha: ", font=("Calibri", 11))
        self.etiqueta_fecha.grid(row=1, column=0)

        # Entry Fecha Input
        self.fecha = Entry(frame_ac, font=("Calibri", 11))
        self.fecha.focus()  # Para que el foco del raton vaya a este Entry al inicio
        self.fecha.grid(row=1, column=1)


         # Label Nombre input
        self.etiqueta_nombre = Label(frame_ac, text="Nombre: ", font=("Calibri", 11))
        self.etiqueta_nombre.grid(row=2, column=0)

        # Entry Nombre Input
        self.nombre_ac = Entry(frame_ac, font=("Calibri", 11))
        self.nombre_ac.grid(row=2, column=1)

        # Label Telefono input
        self.etiqueta_telefono = Label(frame_ac, text="Telefono: ", font=("Calibri", 11))
        self.etiqueta_telefono.grid(row=3, column=0)

        # Entry telefono Input
        self.telefono = Entry(frame_ac, font=("Calibri", 11))
        self.telefono.grid(row=3, column=1)

         # Label Direccion input
        self.etiqueta_direccion = Label(frame_ac, text="Direccion: ", font=("Calibri", 11))
        self.etiqueta_direccion.grid(row=4, column=0)

        # Entry Direccion Input
        self.direccion = Entry(frame_ac, font=("Calibri", 11))
        self.direccion.grid(row=4, column=1)

         # Label Marca input
        self.etiqueta_marca = Label(frame_ac, text="Marca: ", font=("Calibri", 11))
        self.etiqueta_marca.grid(row=5, column=0)

        # Entry Marca Input
        self.marca = Entry(frame_ac, font=("Calibri", 11))
        self.marca.grid(row=5, column=1)

         # Label Modelo input
        self.etiqueta_modelo = Label(frame_ac, text="Modelo: ", font=("Calibri", 11))
        self.etiqueta_modelo.grid(row=6, column=0)

        # Entry Modelo Input
        self.modelo = Entry(frame_ac, font=("Calibri", 11))
        self.modelo.grid(row=6, column=1)

         # Label Matricula input
        self.etiqueta_matricula = Label(frame_ac, text="Matricula: ", font=("Calibri", 11))
        self.etiqueta_matricula.grid(row=7, column=0)

        # Entry Modelo Input
        self.matricula = Entry(frame_ac, font=("Calibri", 11))
        self.matricula.grid(row=7, column=1)

         # Label Kilometros input
        self.etiqueta_kilometros = Label(frame_ac, text="Kilometros: ", font=("Calibri", 11))
        self.etiqueta_kilometros.grid(row=8, column=0)

        # Entry Kilometros Input
        self.kilometros = Entry(frame_ac, font=("Calibri", 11))
        self.kilometros.grid(row=8, column=1)

         # Label Averia input
        self.etiqueta_averia = Label(frame_ac, text="Avería: ", font=("Calibri", 11))
        self.etiqueta_averia.grid(row=9, column=0)

        # Entry Averia Input
        self.averia = Entry(frame_ac, font=("Calibri", 11))
        self.averia.grid(row=9, column=1)

        # Boton guardar nuevo
        self.boton_guardar_cliente = ttk.Button(frame_ac, text="Guardar", command=self.guardar_cliente)
        self.boton_guardar_cliente.grid(row=10, column=1, sticky='we')

        # Mensaje informativo para el usuario ventana emergente
#        self.mensaje_c.config(text="", fg="red")
        self.mensaje_c.grid(row=1, column=0, columnspan=2, sticky=S)

    # Método para guardar información de nuevo cliente o ingreso al taller en la base de datos
    def guardar_cliente(self):
        if (self.validacion_fecha() and
            self.validacion_nombre() and
            self.validacion_telefono() and
            self.validacion_direccion() and
            self.validacion_marca() and
            self.validacion_modelo() and
            self.validacion_matricula() and
            self.validacion_averia()
        ):
            query = "INSERT INTO cliente (fecha, nombre, telefono, direccion, marca, modelo, matricula, kilometros, averia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            parametros = (self.fecha.get(), self.nombre_ac.get(), self.telefono.get(), self.direccion.get(),
                          self.marca.get(), self.modelo.get(), self.matricula.get(), self.kilometros.get(),
                          self.averia.get()
                          )
            self.db_consulta_clientes(query, parametros)
            print("Datos guardados")
            self.fecha.delete(0, END)
            self.nombre.delete(0, END)
            self.telefono.delete(0, END)
            self.direccion.delete(0, END)
            self.marca.delete(0, END)
            self.modelo.delete(0, END)
            self.matricula.delete(0, END)
            self.averia.delete(0, END)
            self.mensaje_c["text"] = "Ingreso añadido con éxito"
        elif self.validacion_fecha() and self.validacion_nombre() == False:
            print("El nombre es obligatorio")
            self.mensaje_c["text"] = "El nombre es obligatorio"
        elif self.validacion_fecha() == False and self.validacion_nombre():
            print("La fecha es obligatoria")
            self.mensaje_c["text"] = "La fecha es obligatorio"
        elif self.validacion_telefono() and self.validacion_direccion() == False:
            print("El telefono es obligatorio")
            self.mensaje_c["text"] = "El telefono es obligatorio"
        elif self.validacion_telefono() == False and self.validacion_direccion():
            print("La direccion es obligatoria")
            self.mensaje_c["text"] = "La direccion es obligatorio"
        elif self.validacion_marca() and self.validacion_modelo() == False:
            print("La marca es obligatoria")
            self.mensaje_c["text"] = "La marca es obligatoria"
        elif self.validacion_marca() == False and self.validacion_modelo():
            print("La marca es obligatoria")
            self.mensaje_c["text"] = "La marca es obligatoria"
        else:
            print("Todos los campos son obligatorios")
            self.mensaje_c["text"] = "Todos los campos son obligatorios"
        self.get_cliente()
        self.ventana_nuevo.destroy()
        self.ventana_nuevo = None

    # Método para eliminar cliente seleccionado
    def eliminar_cliente(self):
        print("Eliminar cliente")
        # print(self.tabla.item(self.tabla.selection()))
        # print(self.tabla.item(self.tabla.selection())["text"])
        self.mensaje_c["text"] = ""
        selected_item = self.tabla_clientes.selection()
        nombre = self.tabla_clientes.item(selected_item, 'values')[1]
        query = "DELETE FROM cliente WHERE nombre = ?"
        self.db_consulta_clientes(query, (nombre,))
        self.mensaje_c["text"] = "cliente {} eliminado con exito".format(nombre)
        self.get_cliente()
        self.mensaje_c.grid(row=1, column=0, columnspan=2, sticky=S)

    # Método para cerrar la aplicación
    def salir(self):
        self.ventana_clientes.destroy()


# Código principal
if __name__ == "__main__":
    root = Tk()
    app_clientes = Clientes(root)
    root.mainloop()
