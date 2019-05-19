from flask import Flask, render_template
from flask import request, Response
from dbUtil import dbUtil
from datetime import datetime
import datetime
import sqlite3
import sqlite3 as sql
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import io
import random


#instantiate bd interation object
database = "C:\\sqlite\dataloggertest.db"
dbinst = dbUtil()

app = Flask(__name__)


@app.route('/')
def index():
	#return '<h1>You got to the APP.... </h1>'
	return render_template('home.html')

@app.route('/list')              #method to display a table with whole database
def list():
   con = sql.connect(database)
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("SELECT * FROM logger")
   rows = cur.fetchall();
   for row in rows:
   	print(row)
   return render_template("list.html",rows = rows)

@app.route('/chartTest')         #generates test chart image
def chartTest():
	print("in chartTest")
	fig = create_figure()
	print("back in chartTest")
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')

@app.route('/dispChart')         #displays page with test chart image
def dispChartTest():
	print("in DispChart")
	return render_template('dispChart.html')

@app.route('/dispTeaChart')      #displays page with tea consumption chart
def dispTeaChart():
	return render_template('dispTeaChart.html')

@app.route('/testChart')
def listCol():
	print("in testChart")
	xyTestChart = XYTestChart()
	print("back in testChart")
	fig = create_figure_var(xyTestChart[0], xyTestChart[1])
	#fig.savefig("C:/Users/Dylan/flaskproject/static/images/temp.png")
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')
	
def XYTestChart():
	print("in XYTestChart")
	connection = dbinst.connect_to_db(database)
	cur = connection.cursor()
	cur.execute("SELECT time_data, weight_data FROM logger WHERE type_date = 'Test Food'")
	rows = cur.fetchall()
	
	dateList = []
	weightList = []
	index = 0

	print("Number of rows %2d" %(len(rows)))
	

	for row in rows:
		tempstr1 = str(rows[index][0])
		tempstr2 = tempstr1[0:28]
		dateList.append([datetime.datetime.strptime(tempstr2, '%Y-%m-%d %H:%M:%S.%f')])
		#print("Date is %s" %(dateList[index]))

		tempInt = int((rows[index][1]))
		weightList.append(tempInt)
		#print("Weight is %s" %(weightList[index]))

		index += 1
	XYList = [dateList, weightList]
	return XYList

def create_figure_var(x, y):
	print("in create_figure_var")
	fig = Figure()
	fig.subplots_adjust(bottom=0.2)
	axis = fig.add_subplot(1,1,1)
	#axis2 = fig.add_subplot(1,1,1)
	xs = x
	ys = y
	axis.set_xlabel('Time of Day')
	axis.set_ylabel('Weight (g)')
	axis.tick_params(axis = 'x', rotation = 45)
	axis.grid()
	axis.xaxis.set_major_locator(plt.MaxNLocator(10))
	axis.yaxis.set_major_locator(plt.MaxNLocator(10))
	#axis.xaxis.set_major_locator(mdates.DateFormatter("%M"))
	axis.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
	#axis.xaxis.set_minor_formatter(mdates.DateFormatter("%M:%S"))

	#axis.plot(xs, ys)
	print("axis of type ")
	print(type(axis))
	print("fig of type ")
	print(type(fig))


	axis.plot(xs, ys, 'o', color='black')
	axis.plot(xs, ys, color='green')


	return fig

def create_figure():
	#fig = Figure()
	#axis = fig.add_subplot(1,1,1)
	#xs = range(100)
	#ys = [random.randint(1,50) for x in xs]
	#axis.set_xlabel('x')
	#axis.set_ylabel('y')
	#fig.ylabel('y')
	#axis.plot(xs, ys)

	fig = plt.figure()
	print("createed new fig with plt.figure()")
	ax = fig.add_subplot(111)
	print("added subplot")
	ax.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
	print("created plot")
	ax.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
	print("created scatter")
	ax.set_xlim(0.5, 4.5)

	print("in create_figure")
	plt.close()   #attempt to fix server locking up
	print("after plt.close")
	plt.clf()
	print("after plt.clf")
	plt.cla()
	print("after plt.cla")

	return fig

@app.route('/postjson', methods = ['POST'])
def postJsonHandler():
	print (request.is_json)
	content = request.get_json()


	#For testing
	#print (content)
	#print ()
	#print (content['device'])
	#print (content['value'])
	#print (content['timestamp'])

	#get content ready for sending to db
	timestamp = datetime.datetime.now()
	print(timestamp)
	weight = float((content['weight']))
	foodtype = (content['foodtype'])

	print("gets json ok")
	connection = dbinst.connect_to_db(database)
	print("connected to db ok")

	if (dbinst.checkData(timestamp, weight, foodtype)):
		try:
			print("passed data check")
			log = (timestamp, weight, foodtype)
			print("log is equal to")
			print(log)
			with connection:
				loggerid = dbinst.create_entry(connection, log)
				print(loggerid)
				print("Data logged")
				dbinst.select_all_logs(connection)	
		except Exception as e:
			print("Data not logged, some Error occured")
			print(e)


	return 'JSON posted'

if __name__ == '__main__':
	app.run(debug=1, host='0.0.0.0', port= 8090)
