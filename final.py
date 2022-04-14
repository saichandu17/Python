from tkinter import * 
from tkinter import ttk
from tkinter import messagebox
from warnings import showwarning
from webbrowser import get
import numpy as np
from turtle import *

r = Tk()
r.geometry("500x600+500+50")
r.title('Pantograph Input Interface')
masslist=[]
springstiffnesslist=[]
dampinglist=[]
pantsim=[]
chad=[]
M=[]
K=[]
degfdm=[]
alpbet=[]


def drawfunc(m,k,c):
	print(degfdm[0].get())
	display=Tk()
	display.geometry("800x800+500+50")
	canvas=Canvas(master=display, width=600, height=400)
	canvas.pack()
	draw=RawTurtle(canvas)
	#draw.setup(startx=0,starty=0)
	draw.penup()
	draw.goto(0,0)
	draw.right(90)
	draw.forward(170)
	draw.left(90)
	draw.backward(50)
	draw.pendown()
	draw.forward(100)
	x=draw.xcor()
	y=draw.ycor()

	draw.penup()
	draw.goto(x-80,y+30)
	draw.pendown()
	x=draw.xcor()
	y=draw.ycor()
	orx=x+50
	ory=y-30
	sprx=x+10
	spry=y-30
	draw.penup()
	draw.goto(sprx,spry)
	draw.pendown()
	for i in range(int(degfdm[0].get())):
#springdiagram
		draw.left(90)
		draw.forward(10)
		sprx=draw.xcor()
		spry=draw.ycor()
		draw.setpos(sprx-5,spry+2)
		draw.setpos(sprx+10,spry+4)
		draw.setpos(sprx-10,spry+6)
		draw.setpos(sprx+10,spry+8)
		draw.setpos(sprx,spry+10)
		draw.forward(10)
		sprx=draw.xcor()
		spry=draw.ycor()+30
		draw.right(90)
		draw.penup()
		draw.goto(x,y)
		draw.pendown()
#massdiagram
		draw.forward(60)
		draw.left(90)
		draw.forward(30)
		draw.left(90)
		draw.forward(60)
		draw.left(90)
		draw.forward(30)
		draw.penup()
		draw.goto(x,y+60)
		draw.pendown()
		draw.left(90)
		x=draw.xcor()
		y=draw.ycor()
		draw.penup()
		draw.goto(sprx,spry)
		draw.pendown()

	draw.penup()
	draw.goto(orx,ory)
	draw.left(90)
	draw.pendown()
	for i in range(int(degfdm[0].get())):
		draw.forward(10)
		ory=draw.ycor()
		draw.penup()
		draw.goto(orx-5,ory+5)
		draw.pendown()
		draw.right(180)
		draw.forward(5)
		draw.left(90)
		draw.forward(10)
		draw.left(90)
		draw.forward(5)
		draw.left(90)
		draw.penup()
		draw.forward(2)
		draw.pendown()
		draw.forward(6)
		draw.penup()
		draw.backward(3)
		draw.right(90)
		draw.pendown()
		draw.forward(15)
		draw.penup()
		ory=draw.ycor()
		draw.goto(orx,ory+30)
		draw.pendown()
	#draw.hide()
	'''t.setpos(10,-10)
	t.setpos(0,0)
	t.setpos(10,10)
	t.setpos(0,20)
	t.setpos(10,30)
	t.setpos(0,40)
	t.setpos(10,50)'''
	tree=ttk.Treeview(display, column=("Mass(kg)","Spring Stiffness(N/m)","damping values(Ns/m)"),show='headings', height=int(degfdm[0].get()))
	tree.column("# 1", anchor=CENTER)
	tree.heading("# 1", text="Mass(kg)")
	tree.column("# 2", anchor=CENTER)
	tree.heading("# 2", text="Spring Stiffness(N/m)")
	tree.column("# 3", anchor=CENTER)
	tree.heading("# 3", text="damping values(Ns/m)")

	# Insert the data in Treeview widget
	for z in range(int(degfdm[0].get())):
		tree.insert('', 'end', text="1", values=(str(m[z]),str(k[z]),str(c[z])))
	tree.pack()
	dis = Label(display,text ="Values in table represented in bottom -> top hierarchy of pantograph")
	dis.pack()

def matrixgen():

	m=[]
	k=[]
	c=[]
	
	for i in masslist:
		x=float(i.get())
		m.append(x)

	for i in springstiffnesslist:
		x=float(i.get())
		k.append(x)

	for i in dampinglist:
		x=float(i.get())
		c.append(x)	
	print(m)
	print(k)
	print(c)		
	'''eng=matlab.engine.start_matlab()
	n=eng.cell2mat(m)
	M=eng.diag(n)
	print(M)
	K=eng.zeros(eng.size(M))
	print(K)'''
	'''m_con=[]
	x=[]
	for i in range(0,len(k)-1):
		x.append(k[i])
		x.append(k[i+1])
		m_con.append(x)
		x=[]
	print(m_con)
	k_con=[]
	x.append(m[0])
	k_con.append(x)
	x=[]
	for i in range(0,len(m)-1):
		x.append(m[i])
		x.append(m[i+1])
		k_con.append(x)
		x=[]
	x.append(m[len(m)-1])
	k_con.append(x)
	x=[]
	print(k_con)
	m_con=[[1],[1,2],[2,3]]
	k_con=[[1,2],[2,3],[3]]
	eng.workspace['k_con']=k_con
	eng.workspace['m_con']=m_con
	#eng.print(m_con)
	#eng.print(k_con)
	eng.workspace['K']=K
	eng.workspace['k']=k
	eng.workspace['i']=0
	eng.workspace['j']=0
	eng.workspace['m']=m
	for i in range(0,len(m)):
		eng.workspace['i']=i+1
		K[i][i]=eng.eval('sum(k(m_con{i}(:)))')
		for j in range(0,len(k)):
			eng.workspace['j']=j+1
			if eng.eval('sum(k_con{j}==i)') != 0:
				for m in range(0,len(j)):
					eng.workspace['m']=m+1
					if i != eng.eval('k_con{j}(m)'):
						K[i][eng.eval('k_con{j}(m)')]=eng.eval('-k(j)')'''
	m_con=[]
	k_con=[]
	ls=[]
	ls.append(0)
	m_con.append(ls)
	ls=[]
	for i in range(len(m)-1):
		ls.append(i)
		ls.append(i+1)
		m_con.append(ls)
		ls=[]
	for i in range(len(k)-1):
		ls.append(i)
		ls.append(i+1)
		k_con.append(ls)
		ls=[]
	ls.append((len(k)-1))
	k_con.append(ls)
	ls=[]
	print(m_con)
	print(k_con)




	#m_con=[[0],[0,1],[1,2]]
	#k_con=[[0,1],[1,2],[2]]
	M=np.diag(m)
	K=np.zeros([len(m),len(m)])
	print(M)
	print(K)
	summ=0
	for i in range(len(m)):
		#K[i,i]=np.sum(k[m_con[i]])
		for j in m_con[i]:
			summ+=k[j]
		K[i,i]=summ
		summ=0
		for j in range(len(k)):
			if (i in k_con[j]) != 0:
				for z in range(0,len(k_con[j])):
					if i != k_con[j][z]:
						K[i,k_con[j][z]]=-k[j]
	print(K)
	alp=int(alpbet[0].get())
	bet=int(alpbet[1].get())
	add1=np.multiply(alp,K)
	add2=np.multiply(bet,M)
	D=np.add(add1,add2)
	print(D)
	drawfunc(m,k,c)



def check():
	stat = Tk()	
	r.destroy()


	stat.geometry("500x600+500+50")
	stat.title('Pantograph Simulation input interface ')
	lop = Label(stat,text = "Pantograph Static input parameters")
	lop.pack()

	t1=Label(stat,text="Enter the number of pantographs")
	t1.pack()
	t11=Entry(stat)
	t11.pack()

	t2=Label(stat,text="Enter the distance between pantographs")
	t2.pack()
	t21=Entry(stat)
	t21.pack()

	t3=Label(stat,text="Enter the alpha value")
	t3.pack()
	t31=Entry(stat)
	t31.pack()

	t4=Label(stat,text="Enter the beta value")
	t4.pack()
	t41=Entry(stat)
	t41.pack()
	alpbet.append(t31)
	alpbet.append(t41)
	button1 = Button(stat, text='Submit', width=25, command=matrixgen)
	button1.pack()


	stat.mainloop()
	
	

def lumped():
	button2.destroy()
	button3.destroy()
	button4.destroy()
	chad=Tk()
	chad.geometry("500x600+500+50")
	chad.title('Pantograph Input Interface')
	l = Label(chad,text = "Pantograph Static input parameters")
	l.pack()

	deg=Label(chad,text="Enter the degrees of freedom",)
	deg.pack()
	deg1=Entry(chad)
	degfdm.append(deg1)
	deg1.pack()
	
	

	def inputval():
		
		#r.destroy()
		pantsim=Tk()
		pantsim.title("Pantograph input interface")
		pantsim.geometry("500x600+500+50")
		mainframe=Frame(pantsim)
		mainframe.pack(fill=BOTH, expand=1)
	
		canvas=Canvas(mainframe)
		canvas.pack(side=LEFT, fill=BOTH, expand=1)
	
		scroll=ttk.Scrollbar(mainframe,orient=VERTICAL,command=canvas.yview)
		scroll.pack(side=RIGHT, fill=Y)
	
		canvas.configure(yscrollcommand=scroll.set)
		canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))
	
		newframe=Frame(canvas)
		canvas.create_window(0,0, window=newframe, anchor="nw")
		if deg1.get()=="":
			messagebox.showwarning("No Value Entered")
		else:	
	
			for i in range(int(float(deg1.get()))):
			
				m1=Label(newframe,text=f"Enter the m{i+1} in kg")
				m1.pack()
				m11=Entry(newframe)
				masslist.append(m11)
				m11.pack()
				
				
				k1=Label(newframe,text=f"Enter the k{i+1} in N/m")
				k1.pack()
				k11=Entry(newframe)
				springstiffnesslist.append(k11)
				k11.pack()
			
		
				c1=Label(newframe,text=f"Enter the c{i+1} in Ns/m")
				c1.pack()
				c11=Entry(newframe)
				dampinglist.append(c11)
				c11.pack()
			
		#scroll.config(command=pantsim.yview)
	
		button1= Button(newframe, text='Submit', width=25, command=check)
		button1.pack()

		
		pantsim.mainloop()
		
	button1= Button(chad, text='Submit', width=25, command=inputval)
	button1.pack()
	

	chad.mainloop()
mylabel2 = Label(r,text ="Select the mass model")
mylabel2.pack()

button4 = Button(r,text='Multi-body mass model',width=25)
button4.pack()

button3 = Button(r,text=' Single rod connect model',width=25)
button3.pack()

button2 = Button(r,text='Lumped mass model',width=25,command=lumped)
button2.pack()
r.mainloop()