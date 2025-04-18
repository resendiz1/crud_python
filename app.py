from flask import Flask, render_template, request,redirect, url_for
from db import obtener_conexion
from flask import flash


app = Flask(__name__)
app.secret_key = 'clave123'



@app.route("/")
def index():
    conexion=obtener_conexion()
    cursor=conexion.cursor()
    cursor.execute("SELECT*FROM usuarios")
    usuarios= cursor.fetchall()
    conexion.close()
    return render_template("index.html", usuarios=usuarios)


@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']

        if not nombre or not correo:
            flash('Los campos son obligatorios', 'error')
            return render_template('crear.html')
        try:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre,correo))
            conexion.commit()
            conexion.close()
            flash('El usuario fue creado!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Ocurrio un error: {str(e)}', 'error')
            return render_template('crear.html')
    return render_template('crear.html')


@app.route("/editar/<int:id>", methods=['GET','POST'])
def editar(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if request.method=='POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s WHERE id = %s", (nombre, correo, id))
        conexion.commit()
        conexion.close()
        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT*FROM usuarios WHERE id= %s", (id,))
        usuario=cursor.fetchone()
        conexion.close()
        return render_template('editar.html', usuario=usuario)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id= %s", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('index'))






if __name__ == "__main__":
    app.run(debug=True)