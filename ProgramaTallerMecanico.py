import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

#Clase conector a la base de datos 'dbtaller_mecanico'
class Conexion:
    def __init__(self):
        self.user = "root"
        self.password = ""
        self.database = "dbtaller_mecanico"
        self.host = "localhost"
        self.conn = None
    
    def open(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database
            )
            return self.conn
        except Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            return None
    
    def close(self):
        if self.conn:
            self.conn.close()

#Clase dbUsuario para manejar las operaciones CRUD
class dbUsuario:
    def __init__(self):
        self.con = Conexion()

    def save(self, user):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (usuario_id, nombre, username, password, perfil) VALUES (%s, %s, %s, %s, %s)"
            datos = (user['usuario_id'], user['nombre'], user['username'], user['password'], user['perfil'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al guardar usuario: {e}")
            finally:
                self.con.close()

    def search(self, usuario_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM usuarios WHERE usuario_id = %s"
            try:
                cursor.execute(sql, (usuario_id,))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al buscar usuario: {e}")
            finally:
                self.con.close()
        return None

    def edit(self, user):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = """UPDATE usuarios 
                     SET nombre = %s, username = %s, password = %s, perfil = %s 
                     WHERE usuario_id = %s"""
            datos = (user['nombre'], user['username'], user['password'], user['perfil'], user['usuario_id'])
            try:
                cursor.execute(sql, datos)
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario editado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al editar usuario: {e}")
            finally:
                self.con.close()

    def remove(self, usuario_id):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "DELETE FROM usuarios WHERE usuario_id = %s"
            try:
                cursor.execute(sql, (usuario_id,))
                conn.commit()
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
            except Error as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {e}")
            finally:
                self.con.close()

    def verificar_credenciales(self, username, password):
        conn = self.con.open()
        if conn:
            cursor = conn.cursor()
            sql = "SELECT * FROM usuarios WHERE username = %s AND password = %s"
            try:
                cursor.execute(sql, (username, password))
                row = cursor.fetchone()
                return row
            except Error as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {e}")
            finally:
                self.con.close()
        return None

#Clase para la ventana Login
class LoginWindow(tk.Toplevel):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.title("Login")
        self.geometry("400x300")

        ttk.Label(self, text="Username:").pack(pady=10)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Password:").pack(pady=10)
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self, text="Login", command=self.verificar_login)
        self.login_button.pack(pady=20)

    def verificar_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = dbUsuario()
        user = db.verificar_credenciales(username, password)

        if user:
            self.destroy()
            root.deiconify()
            app = Application(root)
        else:
            messagebox.showerror("Error", "Usuario y/o Contraseña incorrecto(s)")

#Clase para la ventana principal
class Application(ttk.Frame):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Taller mecánico")
        main_window.geometry("750x300")

        self.notebook = ttk.Notebook(self)
        
        pestana_clientes = ttk.Frame(self.notebook)
        pestana_clientes.grid_columnconfigure(0, weight=1)
        pestana_clientes.grid_columnconfigure(1, weight=1)

        ttk.Label(pestana_clientes, text="Ingrese ID a buscar:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.txIdBuscar = ttk.Entry(pestana_clientes, width=30)
        self.txIdBuscar.grid(row=0, column=1, padx=10, pady=10)

        self.btnBuscar = ttk.Button(pestana_clientes, text="Buscar", command=self.buscarUsuario)
        self.btnBuscar.grid(row=0, column=2, padx=10, pady=10)

        ttk.Label(pestana_clientes, text="Usuario ID:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.txId = ttk.Entry(pestana_clientes, width=30)
        self.txId.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(pestana_clientes, text="Nombre:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.txNombre = ttk.Entry(pestana_clientes, width=30)
        self.txNombre.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(pestana_clientes, text="Username:").grid(row=2, column=2, padx=10, pady=5, sticky="e")
        self.txUsername = ttk.Entry(pestana_clientes, width=30)
        self.txUsername.grid(row=2, column=3, padx=10, pady=5)

        ttk.Label(pestana_clientes, text="Password:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.txPassword = ttk.Entry(pestana_clientes, width=30)
        self.txPassword.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(pestana_clientes, text="Perfil:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.comboPerfil = ttk.Combobox(pestana_clientes, values=["Seleccione", "Admin", "Secretaria", "Mecanico"], state='readonly')
        self.comboPerfil.set("Seleccione")
        self.comboPerfil.grid(row=4, column=1, padx=10, pady=5)

        self.btnNuevo = ttk.Button(pestana_clientes, text="Nuevo", command=self.limpiarCampos)
        self.btnNuevo.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.btnGuardar = ttk.Button(pestana_clientes, text="Guardar", command=self.guardarUsuario)
        self.btnGuardar.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.btnCancelar = ttk.Button(pestana_clientes, text="Cancelar", command=self.limpiarCampos)
        self.btnCancelar.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.btnEditar = ttk.Button(pestana_clientes, text="Editar", command=self.editarUsuario)
        self.btnEditar.grid(row=5, column=3, padx=10, pady=10, sticky="w")

        self.btnEliminar = ttk.Button(pestana_clientes, text="Eliminar", command=self.eliminarUsuario)
        self.btnEliminar.grid(row=5, column=4, padx=10, pady=10, sticky="w")

        self.notebook.add(pestana_clientes, text="Usuarios")
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        self.pack()

    #Funciones para acciones de los usuarios
    def limpiarCampos(self):
        self.txId.delete(0, 'end')
        self.txNombre.delete(0, 'end')
        self.txUsername.delete(0, 'end')
        self.txPassword.delete(0, 'end')
        self.comboPerfil.set("Seleccione")

    def guardarUsuario(self):
        if self.validarCampos():
            user = {
                'usuario_id': self.txId.get(),
                'nombre': self.txNombre.get(),
                'username': self.txUsername.get(),
                'password': self.txPassword.get(),
                'perfil': self.comboPerfil.get()
            }
            db = dbUsuario()
            db.save(user)

    def buscarUsuario(self):
        usuario_id = self.txIdBuscar.get()
        if usuario_id:
            db = dbUsuario()
            user = db.search(usuario_id)
            if user:
                self.txId.delete(0, 'end')
                self.txId.insert(0, user[0])
                self.txNombre.delete(0, 'end')
                self.txNombre.insert(0, user[1])
                self.txUsername.delete(0, 'end')
                self.txUsername.insert(0, user[2])
                self.txPassword.delete(0, 'end')
                self.txPassword.insert(0, user[3])
                self.comboPerfil.set(user[4])
            else:
                messagebox.showerror("Error", "Usuario no encontrado")

    def editarUsuario(self):
        if self.validarCampos():
            user = {
                'usuario_id': self.txId.get(),
                'nombre': self.txNombre.get(),
                'username': self.txUsername.get(),
                'password': self.txPassword.get(),
                'perfil': self.comboPerfil.get()
            }
            db = dbUsuario()
            db.edit(user)

    def eliminarUsuario(self):
        usuario_id = self.txId.get()
        if usuario_id:
            db = dbUsuario()
            db.remove(usuario_id)
            self.limpiarCampos()

    def validarCampos(self):
        if not self.txId.get() or not self.txNombre.get() or not self.txUsername.get() or not self.txPassword.get() or self.comboPerfil.get() == "Seleccione":
            messagebox.showerror("Error", "Faltan Campos por llenar")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    login = LoginWindow(root)
    root.mainloop()
