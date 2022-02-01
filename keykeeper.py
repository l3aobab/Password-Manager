import mysql.connector
import os
from prettytable import PrettyTable
import getpass

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

clearConsole()

print()
print("Bienvenido a Key Keeper, tu gestor de contraseñas")
print("Para continuar, introce los siguientes datos:")
name=input("Nombre de usuario: ")
pswd=getpass.getpass("Contraseña: ")
bbdd=input("Nombre de la base de datos: ")

ddbb=mysql.connector.connect(host="localhost",user=name,passwd=pswd)
dbcursor=ddbb.cursor()
clearConsole()

#elegir una accion en el menu
def showOpcion():
	op=None
	try:
		op=int(input("Selecciona una opcion: "))
	except ValueError:
		clearConsole()
		print('Error, debes seleccionar un numero del 1 al 6 para seleccionar una opcion')
	return op

		##################
		# COMRPOBACIONES #
		##################

def comprobacionShow():
	print("""
Desea obtener otra contraseña?
	1.Si
	2.No
		""")
	op=None
	try:
		op=int(input("Selecciona una opcion: "))
	except ValueError:
		clearConsole()
		print('Error, selecciona uno de los valores para poder continuar')
		comprobacionShow()
	if op==1:
		clearConsole()
		showOne()
	else:
		clearConsole()
		pass
	return op

def comprobacionUpdate():
	print("""
Desea actualizar otra contraseña?
	1.Si
	2.No
		""")
	op=None
	try:
		op=int(input("Selecciona una opcion: "))
	except ValueError:
		clearConsole()
		print('Error, selecciona uno de los valores para poder continuar')
		comprobacionShow()
	if op==1:
		clearConsole()
		updateOne()
	else:
		clearConsole()
		pass
	return op

def comprobacionDelete1():
	print("""
Por favor, confirme si desea continuar.
1.Si
2.No
		""")
	op=None
	try:
		op=int(input("Selecciona una opcion: "))
	except ValueError:
		clearConsole()
		print('Error, selecciona uno de los valores para poder continuar')
		comprobacionDelete1()
	return op

def comprobacionDelete2():	
	print("""
Desea eliminar otra contraseña?
	1.Si
	2.No
		""")
	op2=None
	try:
		op2=int(input("Selecciona una opcion: "))
	except ValueError:
		clearConsole()
		print('Error, selecciona uno de los valores para poder continuar')
		comprobacionShow()
	if op2==1:
		clearConsole()
		deletePass()
	else:
		clearConsole()
		pass
	return op2

def comprobacionUpdate():
	print("""
Desea añadir otra contraseña?
	1.Si
	2.No
		""")
	op=None
	try:
		op=int(input("Selecciona una opcion: "))
	except ValueError:
		clearConsole()
		print('Error, selecciona uno de los valores para poder continuar')
		comprobacionShow()
	if op==1:
		clearConsole()
		addOne()
	else:
		clearConsole()
		pass
	return op
if ddbb:
	createDB="CREATE DATABASE IF NOT EXISTS "+bbdd
	dbcursor.execute(createDB)

	useDB="USE "+bbdd
	dbcursor.execute(useDB)

	#se crean las tablas master y gestor si no existen
	createMP="CREATE TABLE IF NOT EXISTS master (masted_id int PRIMARY KEY AUTO_INCREMENT,pass_master varchar(256))"
	dbcursor.execute(createMP)

	createT="CREATE TABLE IF NOT EXISTS gestor (user_id int PRIMARY KEY AUTO_INCREMENT,sitio varchar(50) NOT NULL,usuario varchar(50),contraseña varchar(256) NOT NULL,email varchar(100))"
	dbcursor.execute(createT)
	
	######################
	# CONTRASEÑA MAESTRA #
	######################

#def checkMaster():
#	check="SELECT pass_master FROM master"
#	dbcursor.execute(check)
#	mas=dbcursor.fetchall()
#	if (mas==None):
#		newM=input("Indica la nueva contraseña maestra: ")
#		insertM="INSERT INTO master (pass_master) values (%s)"
#		dbcursor.execute(insertM,(newM, ))
#		ddbb.commit()
#		clearConsole()
#		print("Se ha creado la nueva contraseña maestra!")
#	else:
#		writeMaster()
#	return mas

#def writeMaster():
#	master=input("Indica la contraseña maestra: ")
#	cm=checkMaster()
#	if master==cm:
#		pass
#	else:
#		writeMaster()
#
#	while not (master==cm):
#		
#	return master

	#mostrar todas las contraseñas
	def showAll():
		showGestor="SELECT * FROM gestor"
		dbcursor.execute(showGestor)
		showGestorResultado=dbcursor.fetchall()
		for fila in showGestorResultado:
			print(fila)
		return showGestorResultado

	#mostrar una linea en concreto
	def showOne():
		app=input("Indica una aplicación: ")
		usr=input("Indica el nombre de usuario: ")
		showGestorOne=("SELECT * FROM gestor WHERE sitio=%s and usuario=%s")
		dbcursor.execute(showGestorOne,(app, usr, ))
		sgor=dbcursor.fetchall()
		for fila in sgor:
			print(fila)
		comprobacionShow()
		return sgor

	#actualizar una contraseña
	def updateOne():
		app=input("Indica una aplicación: ")
		usr=input("Indica el nombre de usuario: ")
		psw=getpass.getpass("Introduce la nueva contraseña: ")
		psw2=getpass.getpass("Confirma la nueva contraseña: ")
		if psw==psw2:
			showUpdate="UPDATE gestor SET contraseña=%s WHERE sitio=%s and usuario=%s"
			dbcursor.execute(showUpdate,(psw, app, usr, ))
			sur=dbcursor.fetchall()
			ddbb.commit()
			clearConsole()
			print("Se ha actualizado tu contraseña!")
		else:
			clearConsole()
			print("Se ha producido un error, por favor, vuelva a intentarlo")
			updateOne()
		comprobacionUpdate()
		return sur

	#borrar todos los datos de un determinado sitio
	def deletePass():
		app=input("Indica una aplicación: ")
		usr=input("Indica el nombre de usuario: ")
		doDelete="DELETE FROM gestor WHERE sitio=%s and usuario=%s"
		op1=comprobacionDelete1()
		if op1==1:
			dbcursor.execute(doDelete,(app, usr, ))
			doDeleteRes=dbcursor.fetchall()
			ddbb.commit()
			clearConsole()
			print("Se ha eliminado la contraseña seleccionada!")
			comprobacionDelete2()
		else:
			clearConsole()
			pass		
		return doDeleteRes

	#añadir una nueva contraseña
	def addOne():
		app=input("Indica una aplicación: ")
		usr=input("Indica el nombre de usuario: ")
		psw=getpass.getpass("Introduce la nueva contraseña: ")
		psw2=getpass.getpass("Confirma la nueva contraseña: ")
		eml=input("Indica el correo electronico: ")
		if psw==psw2:
			insertT="INSERT INTO gestor (sitio,usuario,contraseña,email) VALUES (%s,%s,%s,%s)"
			dbcursor.execute(insertT,(app, usr, psw, eml, ))
			addOneRes=dbcursor.fetchall()
			ddbb.commit()
			clearConsole()
			print("Se ha añadido una nueva contraseña!")
		else:
			clearConsole()
			print("Se ha producido un error, por favor, vuelva a intentarlo")
			addOne()
		comprobacionUpdate()
		return addOneRes

	salir=False
	opcion=0

	while not salir:
		print("""
----------------------------------------------------------------------------------------

Bienvendio, """+ name +""", a tu gestor de contraseñas.
Para continuar, por favor, selecciona una de las siguientes opciones:

1)Mostrar todas las contraseñas
2)Mostrar una contraseña en concreto
3)Actualizar una contraseña
4)Eliminar una contraseña
5)Añadir una nueva contraseña
6)Salir

----------------------------------------------------------------------------------------
			""")

		opcion=showOpcion()

		if opcion==1:
			clearConsole()
			showAll()
		elif opcion==2:
			clearConsole()
			showOne()
		elif opcion==3:
			clearConsole()
			updateOne()
		elif opcion==4:
			clearConsole()
			deletePass()
		elif opcion==5:
			clearConsole()
			addOne()
		elif opcion==6:
			clearConsole()
			salir=True
