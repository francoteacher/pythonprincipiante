from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from turtle import width
root=Tk()
root.title("Aplicacion de gestion de notas")
root.geometry("1200x350")
root.config(bg="#8FE3CF")
dni=StringVar()
Nombre=StringVar()
Curso=StringVar()
notaPrimer=StringVar()
notaSegunda=StringVar()
notaTercera=StringVar()
prom=StringVar()
def conexionBBDD():
   miConexion=sqlite3.connect("escuela")
   miCursor=miConexion.cursor()
   try:
       miCursor.execute('''
       CREATE TABLE alumno (
        dni INTEGER PRIMARY KEY NOT NULL,
        NOMBRE VARCHAR(50) NOT NULL,
        CURSO VARCHAR(50) NOT NULL,
        NOTAPRIMER INT NOT NULL, 
        NOTASEGUNDA INT NOT NULL, 
        NOTATERCERA INT NOT NULL, 
        PROMEDIO INT NOT NULL)''')
       
       messagebox.showinfo("CONEXION","BASE DE DATOS CREADA EXITOSAMENTE")
   except:     
         messagebox.showinfo("CONEXION","CONEXION EXITOSA CON BASE DE DATOS")
def eliminarBBDD():
    miConexion=sqlite3.connect("escuela")
    miCursor=miConexion.cursor()
    if messagebox.askyesno(message="Los datos se perderan para siempre ¿Desea continuar?: "):
       miCursor.execute("DROP TABLE alumno")
    else:
        pass
def salirAplicación():
    valor=messagebox.askquestion("Salir","¿Estas seguro que deseas salir de la aplicacion?")     
    if valor=="yes":
        root.destroy()
def limpiarCampos():
    dni.set("")
    Nombre.set("")
    Curso.set("")      
    notaPrimer.set("")
    notaSegunda.set("")
    notaTercera.set("")
    prom.set("")
def mensaje():
    acerca="Aplicación de administracion educativa"
    messagebox.showinfo(title="INFORMACIÓN",Message=acerca)
    ###metodos
def crear():
    miConexion = sqlite3.connect("escuela")
    miCursor = miConexion.cursor()
  ##  miConexion=sqlite3.connect("base")
    ##miCursor=miConexion.cursor()
    try:
        datos=dni.get(),Nombre.get(),Curso.get(),notaPrimer.get(), notaSegunda.get(), notaTercera.get(), prom ###.get(notaPrimer+notaSegunda+notaTercera/3)
        miCursor.execute("INSERT INTO alumno VALUES(?,?,?,?,?,?,?)",(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("Advertencia","Ocurrio un error al crear (VERIFIQUE CONEXION CON BASE DE DATOS)")
        
    limpiarCampos()
    mostrar()
def mostrar():
    miConexion=sqlite3.connect("escuela")            
    miCursor=miConexion.cursor()
    registros=tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        miCursor.execute("SELECT * FROM alumno")   
        for row in miCursor:
            tree.insert("",0,text=row[0],values=(row[1],row[2],row[3],row[4],row[5],row[6]))
    except:
        pass
####tabla
tree=ttk.Treeview(height=10, columns=('#0','#1','#2','#3','#4','#5','#6'))
tree.place(x=0,y=150)
tree.column('#0',width=100)
tree.heading('#0', text="Dni",anchor=CENTER)
tree.heading('#1', text="Nombre del Alumno",anchor=CENTER)
tree.heading('#2', text="Curso",anchor=CENTER)
tree.column('#3', width=100)
tree.heading('#3', text="Nota primer etapa",anchor=CENTER)
tree.heading('#4', text="Nota segunda etapa", anchor=CENTER)
tree.heading('#5', text="Nota tercer etapa", anchor=CENTER)
tree.heading('#6', text="Nota de promedio", anchor=CENTER)

def seleccionarUsandoClick(event):
    item=tree.identify('item',event.x,event.y)
    dni.set(tree.item(item,"text"))
    Nombre.set(tree.item(item,"values")[1])
    Curso.set(tree.item(item,"values")[2])
    notaPrimer.set(tree.item(item,"values")[3])
    notaSegunda.set(tree.item(item, "values")[4])
    notaTercera.set(tree.item(item, "values")[5])
    prom.set(tree.item(item, "values")[6])
tree.bind("<Double-1>",seleccionarUsandoClick)    

def actualizar():
    miConexion=sqlite3.connect("escuela")            
    miCursor=miConexion.cursor()
    try:
        promedio=(notaPrimer.get()+notaSegunda.get()+notaTercera.get())/3
        datos=dni.get(),Nombre.get(),Curso.get(),notaPrimer.get(),notaSegunda.get(),notaTercera.get(), promedio.get(), prom
        miCursor.execute("UPDATE alumno SET dni=?, NOMBRE=?,CURSO=?,NOTA PRIMER ETAPA=?, NOTA SEGUNDA ETAPA=?, NOTA TERCER ETAPA=?, NOTA PROMEDIO=? WHERE ID="+dni.get(),(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("Advertencia","Se actualizaron los datos")
        pass
    limpiarCampos()
    mostrar()
def borrar():
     miConexion=sqlite3.connect("escuela")            
     miCursor=miConexion.cursor()
     try:
         if messagebox.askyesno(message="¿Realmente quieres eliminar el registro?", title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM alumno WHERE ID="+dni.get())
            miConexion.commit()
     except:
            messagebox.showwarning("Advertencia","OCURRIO UN ERROR A LA HORA DE TRATAR DE ELIMINAR EL REGISTRO")
     limpiarCampos()
     mostrar()

#colocamos widgets en la vista
#creamos menu
menubar=Menu(root)        
menubasedat=Menu(menubar,tearoff=0)
menubasedat.add_command(label="Crear/conectar base de dartos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicación)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu=Menu(menubar,tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)
#creamos etiquetas y cajas de texto
l1=Label(root,text="Dni")
l1.place(x=50, y=10)
e1=Entry(root,textvariable=dni, width=10, bg="yellow")
e1.place(x=100, y=10)

l2=Label(root,text="Nombre")
l2.place(x=160,y=10)
e2=Entry(root,textvariable=Nombre, width=40, bg="lightblue")
e2.place(x=210,y=10)

l3=Label(root,text="Curso")
l3.place(x=50,y=40)
e3=Entry(root,textvariable=Curso, width=10, bg="#c09bd4")
e3.place(x=100,y=40)

l4=Label(root,text="Nota primer etapa")
l4.place(x=50,y=70)
e4=Entry(root,textvariable=notaPrimer, width=10, bg="lightgreen")
e4.place(x=160,y=70)

l5=Label(root, text="Nota segunda etapa")
l5.place(x=230, y=70)
e5=Entry(root,textvariable=notaSegunda, width=10, bg="lightgreen")
e5.place(x=340, y=70)

l6=Label(root, text="Nota tercer etapa")
l6.place(x=440, y=70)
e6=Entry(root, textvariable=notaTercera, width=10, bg="lightgreen")
e6.place(x=550, y=70)

#l7=Label(root, text="Nota de Promedio")
#l7.place(x=230, y=90)
#e7=Entry(root, textvariable=prom, width=10, bg="orange")
#e7.place(x=340, y=90)



######creamos botones
b1=Button(root, text="Crear registro", command=crear)
b1.place(x=5,y=120)
b2=Button(root, text="Modificar registro", command=actualizar)
b2.place(x=150,y=120)
b3=Button(root, text="Mostrar registro", command=mostrar)
b3.place(x=310,y=120)
b4=Button(root, text="Eliminar registro" ,command=borrar)
b4.place(x=460,y=120)


root.config(menu=menubar)
root.mainloop()