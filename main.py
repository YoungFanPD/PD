from flask import Flask, redirect, url_for, render_template as rt, request, flash
from peewee import *

db = SqliteDatabase("Contact.db")


class Contacto(Model):
    nombre = CharField()
    telefono = CharField()
    email = CharField()

    class Meta:
        database = db


def crearConexion():
    db.connect()
    db.create_tables([Contacto])


def particionar_lista(lista, n):
    return [lista[i * n:i * n + n] for i in range(n)]


app = Flask(__name__)
app
app.config['MYSQL_USER'] = 'user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'Contactos'
mysql_db = MySQL(app)

app.secret_key = 'mysecretkey'  # funciona para usar mensajes flash


@app.route('/')
def index():
    contactos = Contacto.select()
    tope = len(contactos) / 4
    len(contactos) // 4
    print()
    nueva_lista = particionar_lista(contactos, round(tope))
    print(len(contactos))
    print(len(contactos) // 4)
    print(len(nueva_lista))
    for contact in nueva_lista[1]:
        print(contact.nombre)
    # cur=mysql_db.connection.cursor() #genera la conexion
    # cur.execute('select* from Contacto') #ejecuta un querty
    # data = cur.fetchall()#regresa los datos de la tabla
    return rt('index.html', contacts=nueva_lista)


@app.route('/add', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        crearConexion()
        contacto = Contacto(nombre=fullname, telefono=phone, email=email)
        contacto.save()
        flash('REGISTRO EXITOSO')
        # cur = mysql_db.connection.cursor()
        # cur.execute("insert into contacts (fullname, phone, email) values(%s,$s,$s)",(fullname,phone,email))
        # mysql_db.connection.commit()
    return redirect(url_for('index'))


@app.route('/edit/<string:id>')
def edit_contact(id):
    contacto = Contacto.get_by_id(id)
    return rt('edit.html', contact=contacto)


@app.route('/update/<string:id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        contacto = Contacto.get_by_id(id)
        contacto.nombre = fullname = request.form['fullname']
        contacto.telefono = phone = request.form['phone']
        contacto.email = email = request.form['email']
        contacto.save()
        flash("Contacto Modificado")
    return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    query = Contacto.delete().where(Contacto.id == id)
    query.execute()
    flash('CONTACTO ELIMINADO')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
