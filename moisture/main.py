from flask import Flask, render_template, request, redirect, url_for, session
import serial
import time
import psycopg2


"""
Database hosted on ElephantSQL
Database Information
Table Name : moisture_level
Columns : time, moisture 
"""

#establishing the connection
conn = psycopg2.connect(database="jndfzdqr", user='jndfzdqr', password='sp5Z_RTJs-Z9mOFUWHmOXhZ1B4nE-mws', host='john.db.elephantsql.com', port= '5432')
#Creating a cursor object using the cursor() method
cursor = conn.cursor()
cursor.execute("select version()")
data = cursor.fetchone()

print("Connection established to: ",data)

lower_threshhold = 25
upper_threshhold = 75

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('Home.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

@app.route('/select')
def select():
    return render_template('select.html')

@app.route('/rice')
def rice():
    global lower_threshhold
    global upper_threshhold
    lower_threshhold = 60
    upper_threshhold = 90
    print("I am here in rice")
    return render_template('select.html')

@app.route('/tomato')
def tomato():
    global lower_threshhold
    global upper_threshhold
    lower_threshhold = 35
    upper_threshhold = 75
    return render_template('select.html')

@app.route('/wheat')
def wheat():
    global lower_threshhold
    global upper_threshhold
    lower_threshhold = 30
    upper_threshhold = 70
    return render_template('select.html')

@app.route('/aloe')
def aloe():
    global lower_threshhold
    global upper_threshhold
    lower_threshhold = 20
    upper_threshhold = 50
    return render_template('select.html')

@app.route('/default')
def default():
    global lower_threshhold
    global upper_threshhold
    lower_threshhold = 25
    upper_threshhold = 75
    return render_template('select.html')


@app.route('/check')
def check():

    arduino = serial.Serial('com4', 9600)
    print("Estabilished serial connection to Arduino")
    time.sleep(2)
    arduino_data = arduino.readline()
    decoded_values = str(arduino_data[0:len(arduino_data)].decode("utf-8"))
    print(decoded_values)
    data = int(decoded_values)
    print(data) 
    
    if(data<lower_threshhold):
        cursor.execute("INSERT INTO moisture_level(moisture) VALUES ( %s )" % (data))
        cursor.execute("commit;")
        arduino.close()
        print(lower_threshhold, upper_threshhold)
        return render_template('Check1.html', message = data)

    elif(data>=lower_threshhold and data < upper_threshhold):
        cursor.execute("INSERT INTO moisture_level(moisture) VALUES ( %s )" % (data))
        cursor.execute("commit;")   
        arduino.close()
        return render_template('Check2.html', message = data)

    else:
        cursor.execute("INSERT INTO moisture_level(moisture) VALUES ( %s )" % (data))
        cursor.execute("commit;")
        arduino.close()
        return render_template('Check3.html', message = data)
    

app.secret_key = 'super secret key'
app.run(debug=True)