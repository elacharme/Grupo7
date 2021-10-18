from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from flask import jsonify
import os
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, g



app = Flask(__name__)
app.secret_key = os.urandom(24)

#--------------------------------------------------------------------------------------------------

# Inicio de session
@app.route('/', methods=['GET', 'POST'])
def sesion():
  
    if request.method == 'POST':
        db = get_db()
        usuario = request.form['usuario']
        password = request.form['contraseña'] 

        error = None

        if not usuario:
            error = "Usuario requerido."
            flash(error)
        if not password:
            error = "Contraseña requerida"
            flash(error)

        if error is not None:
            return render_template("sesion.html")
        else:         
            user = db.execute(
                'SELECT id, usuario, contrasena, rol FROM Usuarios WHERE usuario = ?', (usuario,) 
                ).fetchone()
            print(user)
            if user is None:
                error = "Usuario no existe."
                flash(error)
            else:
                password_correcto = check_password_hash(user[2],password)
                if not password_correcto:
                    flash('Usuario y/o contraseña no son correctos.')
                    return render_template("sesion.html",)
                else:
                    session.clear()
                    session['id_usuario'] = user[0]
                    return redirect( 'Dashboard' )   

   # GET: 
    return render_template("sesion.html")
#--------------------------------------------------------------------------------------------------

# Before Request
@app.before_request
def cargar_usuario_registrado():
    print("Entró en before_request.")
    id_usuario = session.get('id_usuario')
    if id_usuario is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT id, usuario, contrasena, rol FROM Usuarios WHERE usuario = ?'
            ,
            (id_usuario,)
        ).fetchone()

#---------------------------------------------------------------------------------------------------


 # para crear usuario   

@app.route('/Dashboard/UsuarioSuper', methods=['GET', 'POST'])
def usuario_super():
    if request.method == 'POST':                  
        usuario = request.form['usuario']         
        password = request.form['password']
        rol = request.form['rol']    

        error = None
        db = get_db()

        if not usuario:
            error = "Usuario requerido."
            flash(error)
        if not password:
            error = "Contraseña requerida."
            flash(error)
        if not rol:
            error = "Rol requerido."
            flash(error)   

        user_nombre = db.execute(
            'SELECT * FROM Usuarios WHERE usuario = ? ', (usuario,) 
            ).fetchone()
        print(usuario)
        if user_nombre is not None:
            error = "Usuario ya existe."
            flash(error)   
        
        if error is not None:
            return render_template("UsuarioSuper.html")
        else:
        # Seguro:
            password_cifrado = generate_password_hash(password)
            db.execute(
                'INSERT INTO Usuarios (usuario,contrasena,rol) VALUES (?,?,?)',
                (usuario,password_cifrado,rol)
                )
                               
            db.commit()
            flash('Usuario creado') 

    return render_template("UsuarioSuper.html")

#---------------------------------------------------------------------------------------------------------
 # Consultar usuarios       

@app.route('/Dashboard/UsuarioSuper/select', methods=['GET', 'POST'])
def consulta_super():

    if request.method == 'POST':  
        usuario = request.form['usuario']

        if not usuario:
            usuarios = sql_select_usuarios()
        else: 
            db = get_db()
            usuarios = db.execute(
            'SELECT * FROM Usuarios WHERE usuario = ? ', (usuario,) 
            ).fetchall()
            if len(usuarios) < 1 :
               error = "Usuario NO existe."
               flash(error) 
            
            
  
    return render_template("UsuarioSuper.html", usuarios=usuarios)
    

@app.route('/Dashboard/UsuarioAdmin/select', methods=['GET', 'POST'])
def consulta_admin():

    if request.method == 'POST':  
        usuario = request.form['usuario']

        if not usuario:
            usuarios = sql_select_usuarios()
        else: 
            db = get_db()
            usuarios = db.execute(
            'SELECT * FROM Usuarios WHERE usuario = ? ', (usuario,) 
            ).fetchall()
            if len(usuarios) < 1:
               error = "Usuario NO existe."
               flash(error)            
            
  
    return render_template("UsuarioAdmin.html", usuarios=usuarios)    
    

#------------------------------------------------------------------------------------------------------    
# Para editar usuarios    
   
@app.route('/Dashboard/UsuarioSuper/editarUsuario/<nom_usuario>', methods=['GET', 'POST'])
@app.route('/Dashboard/UsuarioAdmin/editarUsuario/<nom_usuario>', methods=['GET', 'POST'])
def editar_usuario(nom_usuario):
    if request.method == 'POST':                  
            usuario = request.form['usuario']         
            password = request.form['password']
            rol = request.form['rol']    

            error = None
            db = get_db()

            if not usuario:
                error = "Usuario requerido."
                flash(error)
            if not password:
                error = "Contraseña requerida."
                flash(error)
            if not rol:
                error = "Rol requerido."
                flash(error)   

                  
            if error is not None:
                return render_template("editarUsuario.html")
            else:
            # Seguro:
                password_cifrado = generate_password_hash(password)
                db.execute(
                    'UPDATE Usuarios SET usuario = ?,contrasena = ?,rol = ? WHERE usuario = ?',
                    (usuario,password_cifrado,rol,usuario)
                    )
                                             
                db.commit()
                flash('Usuario Editado')
                usuarios = db.execute(
                    'SELECT * FROM Usuarios WHERE usuario = ? ', (nom_usuario,) 
                    ).fetchall()
                print(usuarios)   
                return render_template("editarUsuario.html",  usuarios = usuarios , nom_usuario=nom_usuario)
         
    else:
              
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM Usuarios WHERE usuario = ? ', (nom_usuario,) 
            ).fetchall()
        print(usuarios)   
        return render_template("editarUsuario.html",  usuarios = usuarios , nom_usuario=nom_usuario)

#----------------------------------------------------------------------------------------------------------

#Para Eliminar usuarios

@app.route('/Dashboard/UsuarioSuper/eliminarUsuario/<nom_usuario>', methods=['GET', 'POST'])
@app.route('/Dashboard/UsuarioAdmin/eliminarUsuario/<nom_usuario>', methods=['GET', 'POST'])    
def eliminar_usuario(nom_usuario):
    if request.method == 'POST':                  
            usuario = request.form['usuario']         
               

            error = None
            db = get_db()

            if not usuario:
                error = "Usuario requerido."
                flash(error)
                             
            if error is not None:
                return render_template("eliminarUsuario.html")
            else:
            
                db.execute(
                    'DELETE FROM Usuarios WHERE usuario = ?',
                    (usuario,)
                    )
                                            
                db.commit()
                flash('Usuario Eliminado')
                return render_template("eliminarMensaje.html")
            


    else:
        db = get_db()
        usuarios = db.execute(
            'SELECT * FROM Usuarios WHERE usuario = ? ', (nom_usuario,) 
            ).fetchall()
        print(usuarios)
        
        return render_template("eliminarUsuario.html",  usuarios = usuarios , nom_usuario=nom_usuario)
                 
       

#----------------------------------------------------------------------------------------


#--------------------------------------------------------------------------------------------

#Plantillas

@app.route('/Dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("Dashboard.html")    

@app.route('/Dashboard/UsuarioAdmin', methods=['GET', 'POST'])
def usuario_admin():
    return render_template("UsuarioAdmin.html")    


@app.route('/Dashboard/ProductoAdmin', methods=['GET', 'POST'])
def producto_admin():
    return render_template("ProductoAdmin.html")    

@app.route('/Dashboard/ProductoUsuario', methods=['GET', 'POST'])
def producto_usuario():
    return render_template("ProductoUsuario.html")   

@app.route('/Dashboard/ProveedorAdmin', methods=['GET', 'POST'])
def proveedor_admin():
    return render_template("ProveedorAdmin.html")    

@app.route('/Dashboard/ProveedorEmpleado', methods=['GET', 'POST'])
def proveedor_empleado():
    return render_template("ProveedorEmpleado.html")   

#-------------------------------------------------------------------------------------

@app.route('/Dashboard/ProductoUsuario/editarProducto', methods=['GET', 'POST'])
@app.route('/Dashboard/ProductoAdmin/editarProducto', methods=['GET', 'POST'])
def editar_producto():
    return render_template("editarProducto.html")  


@app.route('/Dashboard/ProveedorUsuario/editarProveedor', methods=['GET', 'POST'])
@app.route('/Dashboard/ProveedorAdmin/editarProveedor', methods=['GET', 'POST'])
def editar_proveedor():
    return render_template("editarProveedor.html")    

#------------------------------------------------------------------------------------------------------

# FUNCIONES  
def sql_select_usuarios():
    sql = "SELECT * FROM Usuarios"
    conn = get_db()
    cursoObj = conn.cursor()
    cursoObj.execute(sql)
    usuarios= cursoObj.fetchall()  # [ [47,"Monitor",368000.0,23], [99,"Mouse",25000.0,64] ]
    print(usuarios)
    return usuarios


#--------------------------------------------------------------------------------------------------


#Metodo Main
   

if __name__ == "__main__":
    print("Entró en el IF.")
    app.run(debug=True, port=5000)           


    