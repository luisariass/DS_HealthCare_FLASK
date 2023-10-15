from flask import Flask, request, render_template, url_for, redirect
from logic.model import db, Appointment
from datetime import datetime  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# CRUD operations
# Create
# Read
# Update
# Delete
@app.route('/test', methods=['POST']) 
def schedule_appointment():
    name = request.form.get('name')
    email = request.form.get('email')
    date_str = request.form.get('date')
    time_str = request.form.get('time')
    
    date1 = datetime.strptime(date_str, '%Y-%m-%d').date()
    time1 = datetime.strptime(time_str, '%H:%M').time()
    
    appointment = Appointment(name=name, email=email, date=date1, time=time1)
    db.session.add(appointment) # agregar 
    db.session.commit()
    
    return redirect(url_for("view_appointments"))


@app.route('/delete/<int:id>', methods=['GET']) 
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    
    if appointment:
        db.session.delete(appointment) # eliminar
        db.session.commit()
        return render_template('delete_succes.html', appointment=appointment)

@app.route('/')
def home():
    return render_template ('home.html')

@app.route('/login')
def login():
    return render_template ('login.html')

@app.route('/agendamiento')
def agenda():
    return render_template ('agendamiento.html')

@app.route('/lista_citas')
def view_appointments():
    appointments = Appointment.query.all()
    return render_template('lista_citas.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)