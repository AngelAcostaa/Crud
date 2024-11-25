from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import pymysql.cursors




   


app=Flask(__name__)

def connect_to_db():
   return pymysql.connect(
      host='localhost',
      user='root',
      password='',
      database='tienda',
      cursorclass=pymysql.cursors.DictCursor,
      ssl_disabled=True
   )
   


@app.route('/')
def inde():
    return render_template ('index.html')






@app.route('/formular', methods=["GET", "POST"])
def formular():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM fabricante")
        fabricantes = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener fabricantes: {e}")
        return redirect(url_for('inde'))



    if request.method=="POST":
    
     nombre=request.form['nombre']
     id_fabricante=request.form['id_fabricante']
     precio=request.form['precio']


     try:
            conn= connect_to_db()
            cur = conn.cursor()
            cur.execute('INSERT INTO producto (nombre, precio, id_fabricante) VALUES ( %s, %s, %s)',
                     (nombre, precio, id_fabricante))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('inde'))
     except Exception:
         return redirect (url_for('inde'))
    return render_template('formulario.html', fabricantes=fabricantes)


@app.route('/formular2', methods=["GET", "POST"])
def formular2():
   if request.method=="POST":
     Nombre=request.form['Nombre']
    


     try:
            conn= connect_to_db()
            cur = conn.cursor()
            cur.execute('INSERT INTO fabricante (nombre) VALUES (%s)',
                     (Nombre))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('inde'))
     except Exception:
         return redirect (url_for('inde'))
   return render_template('formulario2.html')



@app.route('/reportt')
def reportt():
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM fabricante")
        fabricantes = cur.fetchall()
        cur.close()
        conn.close()
    except Exception as e:
        flash(f"Error al obtener fabricantes: {e}")
        return redirect(url_for('inde'))  

    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM producto")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('reporte.html', productos=data, fabricantes=fabricantes)
    except Exception:
        return render_template('reporte.html', productos=[])
    

@app.route('/reportt2')
def reportt2():
    try:
        conn = connect_to_db()
        cur = conn.cursor() 
        cur.execute("SELECT * FROM fabricante")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('reporte2.html', fabricantes=data)
    except Exception:
        return render_template('reporte2.html', fabricantes=[])

@app.route('/delete/<string:id>')
def delete(id):
    conn= connect_to_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM fabricante WHERE id=%s', id)               
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('reportt2'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    if request.method=="POST":
    
     Nombre=request.form['Nombre']
    


     try:
            conn= connect_to_db()
            cur = conn.cursor()
            cur.execute('UPDATE fabricante SET Nombre=%s WHERE id=%s',
                     (Nombre, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('reportt2'))
     except Exception:
         return redirect (url_for('inde'))
    return render_template('formulario2.html')
 


@app.route('/delete2/<string:id>')
def delete2(id):
    conn= connect_to_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM producto WHERE id=%s', id)              
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('reportt'))

@app.route('/edit2/<string:id>', methods=['POST'])
def edit2(id):
    

    if request.method=="POST":
     nombre=request.form['nombre']
     id_fabricante=request.form['id_fabricante']
     precio=request.form['precio']

     try:
            conn= connect_to_db()
            cur = conn.cursor()
            cur.execute('UPDATE producto SET nombre=%s, id_fabricante=%s, precio=%s WHERE id=%s',
                     (nombre, id_fabricante, precio, id))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('reportt'))
     except Exception:
         return redirect (url_for('inde'))
    return render_template('formulario2.html')
        
      


if __name__=='__main__':
     app.run(debug=True)
  


    