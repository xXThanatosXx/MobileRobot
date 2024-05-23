from pyRobotics import *
import matplotlib.pyplot as plt

#variables de tiempo
tf = 60 # tiempo de simulacion 
ts = 0.1 # tiempo de muestreo

t = np.arange(0,tf+ts,ts)# vector tiempo

N = len(t)# numero de muestras

#Datos del robot
a = 0.07 # distancia desde el centro del eje de las ruedas al punto de control


#condiciones iniciales
x1 = np.zeros(N+1)
y1 = np.zeros(N+1)
phi = np.zeros(N+1)

hx = np.zeros(N+1)
hy = np.zeros(N+1)

x1[0] = -2
y1[0] = 0
#orientacion inicial
phi[0] = 0*(np.pi/180)

#Cinematica directa

#posicion inicial en eje x y en metros [m]
hx[0] = x1[0]+a*np.cos(phi[0]);
hy[0] = y1[0]+a*np.sin(phi[0]);

#planeador de terayectorias

vMax = 0.15
div = 250
#camino a seguir

px = []
py = []

pointX = [-2,-1,1,2,2.1,1,-1,-2,-2]
pointY = [0.5,1,1,0.5,-0.5,-1,-1,-0.5,0.5]

for p in range(len(pointX)-1):
    px.append(np.linspace(pointX[p],pointX[p+1],div))
    py.append(np.linspace(pointY[p],pointY[p+1],div))

pxd = np.hstack(px)
pyd = np.hstack(py)


fig = plt.figure()
plt.plot(pxd,pyd,'b',linewidth = 2,label = 'camino deseado')
plt.legend(loc = 'upper right')
plt.xlabel('X[m]')
plt.ylabel('y[m]')
plt.grid()
plt.show()
