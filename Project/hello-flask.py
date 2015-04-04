from flask import  Flask, jsonify, render_template, request
import datetime
import time
import math
import MySQLdb
app = Flask(__name__)

#from ucasts import ID12LA
#reader = ID12LA()

db = MySQLdb.connect(host="104.131.49.32", # your host, usually localhost
                     user="dp3", # your username
                      passwd="dp3", # your password
                      db="theNetwork") # name of the data base

#ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=1)

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

import serial
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=0.5)
def getrfid():
	string = ser.read(12)
	if len(string) != 0:
		return string
		

class eachLink:
	id = ''
	fName = ''
	lName = ''
	angle = 0
	cos = 0
	sin = 0
	color = ''

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('main.html', **templateData)

@app.route("/admin")
def admin():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
   return render_template('admin.html', **templateData)


@app.route('/load_rfid')
def add_numbers():
	print 'test'
	ser.flushInput()

	rfid = None
	for x in range(0, 10):
      		#rfid = reader.get_last_scan()
		rfid = getrfid()
		print rfid
		if rfid != None:
			return jsonify(result=rfid)
		time.sleep(0.1)
      	print 'test2'
        return jsonify(result=0)
    


@app.route("/user/<pin>")
def readPin(pin):
	cur.execute("SELECT * FROM theNetwork.Links WHERE userRFID='"+pin+"'")
	row = cur.fetchone()

	linked = [0] * 4
	n_linked = 0
	for i in range (0, 4):
		print row[i+1]
		print "abs"
		if row[i+1] != "0":
			n_linked += 1
			linked[i] = row[i+1]
		
			
    	
	#linked = row[16].split(';')
	#n_linked = len(linked)
	list = []
	for i in range (0, n_linked):
		cur.execute("SELECT * FROM theNetwork.UserData WHERE userRFID='"+linked[i]+"'")
		link = cur.fetchone()
		e_link = eachLink()
		e_link.id = link[0]
		e_link.fName = link[1]
		e_link.lName = link[2]
		e_link.angle = 360/n_linked*i
		e_link.sin = math.sin(math.radians(e_link.angle))
		e_link.cos = math.cos(math.radians(e_link.angle))
		e_link.color = link[17]
		list.append(e_link)
	print list

	cur.execute("SELECT * FROM theNetwork.UserData WHERE userRFID='"+pin+"'")
	row = cur.fetchone()

 
   	templateData = {
		'logged_number': pin,
      		'f_name' : row[1],
		'l_name' : row[2],
		'html' : list,
		'm_color' : row[17]
      	}
	

  	return render_template('pin.html', **templateData)

@app.route("/user/<pin>/map/<user>")
def map(pin, user):
	templateData = {
      		'logged_number': pin,
		'view_number' : user
	}
	return render_template('map.html', **templateData)

@app.route("/user/<pin>/info/<user>")
def info(pin, user):

	cur.execute("SELECT * FROM theNetwork.UserData WHERE userRFID='"+user+"'")
	row = cur.fetchone()
	templateData = {
		'name' : str(row[1]) + ' ' + str(row[2]),
		'gender' : str(row[14]),
		'age' : str(row[4]),
		'date_of_birth' : str(row[5]),
		'nationality' : str(row[6]),
		't_address' : str(row[7]) + ', ' + str(row[8]) + ', ' + str(row[9]),
		'p_address' : str(row[10]) + ', ' + str(row[11]) + ', ' + str(row[12]),
      		'checked_in_time': str(row[15]),
		'checked_in_location': 'Somerville House',
		'logged_number': pin,
		'view_number' : user
	}
	return render_template('info.html', **templateData)

@app.route("/admin/edit/<user>")
def edit(user):

	cur.execute("SELECT * FROM theNetwork.UserData WHERE userRFID='"+user+"'")
	row = cur.fetchone()
	templateData = {
		'name' : str(row[1]) + ' ' + str(row[2]),
		'gender' : str(row[14]),
		'age' : str(row[4]),
		'date_of_birth' : str(row[5]),
		'nationality' : str(row[6]),
		't_address' : str(row[7]) + ', ' + str(row[8]) + ', ' + str(row[9]),
		'p_address' : str(row[10]) + ', ' + str(row[11]) + ', ' + str(row[12]),
      		'checked_in_time': str(row[15]),
		'checked_in_location': '',
		'logged_number': user,
		'view_number' : user
	}
	return render_template('edit.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)