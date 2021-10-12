from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request


app = Flask(__name__)

from usuarios import usuarios
from productos import productos
from proveedores import proveedores

@app.route('/', methods=['GET', 'POST'])
def sesion():
    return render_template("sesion.html")



#------------------------------------------------------------------------------------------------------------

# Agregar un usuario

@app.route('/Dashboard/UsuarioSuper', methods=['POST'])
def add_usuarios():
    usuario = request.json
    usuarios.append(usuario)
    return jsonify( {"message": "Usuario {} agregado.".format(usuario["nombre"]), "Usuarios": usuarios} )


# Buscar todos los usuarios

@app.route('/Dashboard/UsuarioSuper')
@app.route('/Dashboard/UsuarioAdmin')
def get_usuarios():
    return jsonify( {"Usuarios": usuarios} )

# Buscar un usuario en especifico

@app.route('/Dashboard/UsuarioSuper/<nom_usuario>')
@app.route('/Dashboard/UsuarioAdmin/<nom_usuario>')
def get_usuario(nom_usuario):
    lista_usuarios = [ usuario for usuario in usuarios if usuario["nombre"] == nom_usuario ]
    if len(lista_usuarios) > 0:
        return jsonify( {"Usuario": lista_usuarios[0]} )
    else:
        return jsonify( {"message": "Usuario no encontrado."} )

# Editar un usuario

@app.route('/Dashboard/UsuarioSuper/<nom_usuario>', methods=['PUT'])
@app.route('/Dashboard/UsuarioAdmin/<nom_usuario>', methods=['PUT'])
def update_usuario(nom_usuario):
    lista_usuarios = [ usuario for usuario in usuarios if usuario["nombre"] == nom_usuario ]
    if len(lista_usuarios) > 0:
        usuario = lista_usuarios[0]
        usuario["nombre"] = request.json['nombre']
        usuario["contraseña"] = request.json['contraseña']
        usuario["Rol"] = request.json['Rol']
        return jsonify( {"message": "Usuario {} actualizado.".format(nom_usuario), "Usuarios": usuarios}  )    
    return jsonify( {"message": "Usuario {} no encontrado.".format(nom_usuario), "Usuarios": usuarios} )

# Eliminar un usuario

@app.route('/Dashboard/UsuarioSuper/<nom_usuario>', methods=['DELETE'])
@app.route('/Dashboard/UsuarioAdmin/<nom_usuario>', methods=['DELETE'])
def delete_usuario(nom_usuario):
    lista_usuarios = [ usuario for usuario in usuarios if usuario["nombre"] == nom_usuario ]
    if len(lista_usuarios) > 0:
        usuarios.remove( lista_usuarios[0] )
        return jsonify( {"message": "Usuario {} eliminado.".format(nom_usuario), "Usuarios": usuarios} )
    return jsonify( {"message": "Usuarios {} no encontrado.".format(nom_usuario), "Usuarios": usuarios})

#--------------------------------------------------------------------------------------------------------------------------


# Agregar un producto

@app.route('/Dashboard/ProductoAdmin', methods=['POST'])
def add_productos():
    producto = request.json
    productos.append(producto)
    return jsonify( {"message": "Producto {} agregado.".format(producto["nombre"]), "Productos": productos} )


# Buscar todos los productos


@app.route('/Dashboard/ProductoAdmin')
@app.route('/Dashboard/ProductoUsuario')
def get_productos():
    return jsonify( {"Productos": productos} )

  
# Buscar un producto en especifico

@app.route('/Dashboard/ProductoAdmin/<nom_producto>')
@app.route('/Dashboard/ProductoUsuario/<nom_producto>')
def get_producto(nom_producto):
    lista_productos = [ producto for producto in productos if producto["nombre"] == nom_producto ]
    if len(lista_productos) > 0:
        return jsonify( {"Producto": lista_productos[0]} )
    else:
        return jsonify( {"message": "Producto no encontrado."} )



# Editar un producto

@app.route('/Dashboard/ProductoAdmin/<nom_producto>', methods=['PUT'])
def update_producto(nom_producto):
    lista_productos = [ producto for producto in productos if producto["nombre"] == nom_producto ]
    if len(lista_productos) > 0:
        producto = lista_productos[0]
        producto["codigo"] = request.json['codigo']
        producto["nombre"] = request.json['nombre']
        producto["descripcion"] = request.json['descripcion']
        producto["cantidad min req"] = request.json['cantidad min req']
        producto["stock"] = request.json['stock']
        producto["proveedor"] = request.json['proveedor']
        return jsonify( {"message": "Producto {} actualizado.".format(nom_producto), "Productos": productos}  )    
    return jsonify( {"message": "Producto {} no encontrado.".format(nom_producto), "Productos": productos} )

# Eliminar un producto

@app.route('/Dashboard/ProductoAdmin/<nom_producto>', methods=['DELETE'])
def delete_producto(nom_producto):
    lista_productos = [ producto for producto in productos if producto["nombre"] == nom_producto ]
    if len(lista_productos) > 0:
        productos.remove( lista_productos[0] )
        return jsonify( {"message": "Producto {} eliminado.".format(nom_producto), "Productos": productos} )
    return jsonify( {"message": "Producto {} no encontrado.".format(nom_producto), "Productos": productos})




# Buscar productos cantidad minima requerida

@app.route('/Dashboard/ProductoUsuario/cantidad')
def get_cant():
    lista_productos = [ producto for producto in productos if producto["stock"] < producto["cantidad min req"] ]
    if len(lista_productos) > 0:
        return jsonify( {"Productos ": lista_productos} )
    else:
        return jsonify( {"message": "El inventario esta completo."} )



#--------------------------------------------------------------------------------------------------------------------------   

# Buscar todos los proveedores

@app.route('/Dashboard/ProveedorAdmin')
@app.route('/Dashboard/ProveedorEmpleado')
def get_proveedores():
    return jsonify( {"proveedores": proveedores} )
    
# Agregar un proveedores

@app.route('/Dashboard/ProveedorAdmin', methods=['POST'])
def add_proveedores():
    proveedor = request.json
    proveedores.append(proveedor)
    return jsonify( {"message": "Proveedor {} agregado.".format(proveedor["nombre"]), "Proveedores": proveedores} )




# Buscar un Proveedor en especifico

@app.route('/Dashboard/ProveedorAdmin/<nom_proveedor>')
@app.route('/Dashboard/ProveedorEmpleado/<nom_proveedor>')
def get_proveedor(nom_proveedor):
    lista_proveedores = [ proveedor for proveedor in proveedores if proveedor["nombre"] == nom_proveedor ]
    if len(lista_proveedores) > 0:
        return jsonify( {"Proveedor": lista_proveedores[0]} )
    else:
        return jsonify( {"message": "proveedor no encontrado."} )

# Editar un proveedor

@app.route('/Dashboard/ProveedorAdmin/<nom_proveedor>', methods=['PUT'])
#@app.route('/Dashboard/ProveedorEmpleado/<nom_proveedor>', methods=['PUT']) SOlO EDITA EL ADMINISTRADOR
def update_proveedores(nom_proveedor):
    lista_proveedores = [ proveedor for proveedor in proveedores if proveedor["nombre"] == nom_proveedor ]
    if len(lista_proveedores) > 0:
        proveedor = lista_proveedores[0]
        proveedor["nombre"] = request.json['nombre']
        proveedor["telefono"] = request.json['telefono']
        proveedor["direccion"] = request.json['direccion']
        
        return jsonify( {"message": "Proveedor {} actualizado.".format(nom_proveedor), "Proveedores": proveedores}  )    
    return jsonify( {"message": "Proveedor {} no encontrado.".format(nom_proveedor), "Proveedores": proveedores})    

#Eliminar proveedor

@app.route('/Dashboard/ProveedorAdmin/<nom_proveedor>', methods=['DELETE']) 
def delete_proveedores(nom_proveedor):
    lista_proveedores = [ proveedor for proveedor in proveedores if proveedor["nombre"] == nom_proveedor ]
    if len(lista_proveedores) > 0:
        proveedores.remove( lista_proveedores[0] )
        return jsonify( {"message": "Proveedor {} eliminado.".format(nom_proveedor), "Proveedores": proveedores})
    return jsonify( {"message": "Proveedor {} no encontrado.".format(nom_proveedor), "Proveedores": proveedores})



#--------------------------------------------------------------------------------------------------------------------------


#Decoradores de los archivos HTML

"""

@app.route('/', methods=['GET', 'POST'])
def sesion():
    return render_template("sesion.html")



@app.route('/Dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("Dashboard.html")    

@app.route('/Dashboard/UsuarioSuper', methods=['GET', 'POST'])
def usuario_uper():
    return render_template("UsuarioSuper.html")

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


@app.route('/Dashboard/UsuarioSuper/editarUsuario', methods=['GET', 'POST'])
@app.route('/Dashboard/UsuarioAdmin/editarUsuario', methods=['GET', 'POST'])
def editar_usuario():
    return render_template("editarUsuario.html")  


@app.route('/Dashboard/ProductoUsuario/editarProducto', methods=['GET', 'POST'])
@app.route('/Dashboard/ProductoAdmin/editarProducto', methods=['GET', 'POST'])
def editar_producto():
    return render_template("editarProducto.html")  


@app.route('/Dashboard/ProveedorUsuario/editarProveedor', methods=['GET', 'POST'])
@app.route('/Dashboard/ProveedorAdmin/editarProveedor', methods=['GET', 'POST'])
def editar_proveedor():
    return render_template("editarProveedor.html")    

"""


if __name__ == "__main__":
    print("Entró en el IF.")
    app.run(debug=True, port=5000)           


    