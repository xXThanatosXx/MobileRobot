from pyRobotics import *
import time
from pyArduino import *
import matplotlib.pyplot as plt

#################### TIEMPO ###################

tf = 120 # tiempo de simulacion
ts = 0.1 #  tiempo de muestreo
t = np.arange(0,tf+ts,ts) # vector tiempo

N = len(t) # cantidad de muestras

################### PARAMETROS ROBOT ###################
a = 0.1 # Distancia desde el centro del eje de las ruedas al punto de control

################### CONDICIONES INICIALES ###################

# Asignar memoria 
x1 = np.zeros(N+1) 
y1 = np.zeros(N+1)
phi = np.zeros(N+1)

hx = np.zeros(N+1) 
hy = np.zeros(N+1)

x1[0] = -2
y1[0] = 0
phi[0] = 0*(np.pi/180) # Orientacion inicial en radianes [rad]

# Cinematica directa

hx[0] = x1[0]+a*np.cos(phi[0]);  # Posicion inicial en el eje x en metros [m]
hy[0] = y1[0]+a*np.sin(phi[0]);  # Posicion inicial en el eje y en metros [m]

################### CAMINO DESEADO ####################
vMax = 0.1
div = 350
px = []
py = []


# Camino de n lineas

pointX = [-2,-1,1,2,2.1,1,-1,-2,-2]
pointY = [0.5,1,1,0.5,-0.5,-1,-1,-0.5,0.5]

for p in range(len(pointX)-1):
     px.append(np.linspace(pointX[p],pointX[p+1],div))
     py.append(np.linspace(pointY[p],pointY[p+1],div))

pxd = np.hstack(px)
pyd = np.hstack(py)

sizePoints = len(pxd) # cantidad de puntos

betad = np.zeros(sizePoints)

# Calculo del angulo beta
for p in range(sizePoints):
     if p==1:
          betad[p]=np.arctan2(pyd[p+1]-pyd[p],pxd[p+1]-pxd[p]);
     else:
          betad[p]=np.arctan2(pyd[p]-pyd[p-1],pxd[p]-pxd[p-1]);


################### VELOCIDADES DE REFERENCIA #################### 

uRef = np.zeros(N)  # Velocidad lineal en metros/segundos [m/s]
wRef = np.zeros(N) # Velocidad angular en radianes/segundos [rad/s]

################### VELOCIDADES MEDIDAS #################### 

uMeas = np.zeros(N)  # Velocidad lineal en metros/segundos [m/s]
wMeas = np.zeros(N)  # Velocidad angular en radianes/segundos [rad/s]

################## COMUNICACION SERIAL #########################
port = 'COM8'
baudRate = 115200 # Baudios
arduino = serialArduino(port,baudRate,2)
arduino.readSerialStart()

################### ERRORES ####################
hxe = np.zeros(N) 
hye = np.zeros(N)

################### BUCLE ####################  
for k in range(N):
     start_time = time.time() # Tiempo actual

     #################### CONTROL #####################

     # Punto mas cercano
     minimo=100
     for p in range(sizePoints):
          aux=np.sqrt((pxd[p]-hx[k])**2+(pyd[p]-hy[k])**2)
          if aux<minimo:
               minimo=aux
               pos=p
               
     # Errores
     hxe[k] = pxd[pos] - hx[k]
     hye[k] = pyd[pos] - hy[k]

     he = np.array([[hxe[k] ],[hye[k] ]])

     # Matriz Jacobiana
     J = np.array([[ np.cos(phi[k]), - a*np.sin(phi[k])],
                   [ np.sin(phi[k]),  a*np.cos(phi[k])]])

     # Parametros de control
     K = np.array([[ 0.1, 0],
                   [ 0,  0.1]])

     # Velocidad deseada
     pxdp = vMax*np.cos(betad[pos]);
     pydp = vMax*np.sin(betad[pos]);
        
     pdp = np.array([[pxdp], [pydp]])
     
     # Ley de control 
     qpRef = np.linalg.pinv(J)@(pdp+K@he)

     #################### APLICAR ACCIONES DE CONTROL #####################

     uRef[k] = qpRef[0][0]
     wRef[k] = qpRef[1][0]

     arduino.sendData([uRef[k],wRef[k]])

     uMeas[k] = arduino.rawData[0]
     wMeas[k] = arduino.rawData[1]
     
     # Integral numerica
     phi[k+1] = phi[k]+ts*wMeas[k]

    # Modelo cinemático
     
     x1p = uMeas[k]*np.cos(phi[k+1])
     y1p = uMeas[k]*np.sin(phi[k+1])
     
     # Integral numerica
     x1[k+1] = x1[k] + ts*x1p
     y1[k+1] = y1[k] + ts*y1p
     
     # Cinematica directa   
     hx[k+1] = x1[k+1]+a*np.cos(phi[k+1]);  # Posicion inicial en el eje x en metros [m]
     hy[k+1] = y1[k+1]+a*np.sin(phi[k+1]);   # Posicion inicial en el eje y en metros [m]

     elapsed_time = time.time() - start_time # Tiempo transcurrido
     
     time.sleep(ts-elapsed_time) # Esperar hasta completar el tiempo de muestreo
     
################## COMUNICACION SERIAL #########################

arduino.sendData([0,0]) # Detener robot     
arduino.close() # Cerrar puerto serial        

################### SIMULACION VIRTUAL #################### 

# Cargar componentes del robot
pathStl = "stl"
color = ['yellow','black','gray','gray','white','blue']
uniciclo = robotics(pathStl,color) # Instanciar objeto robotics (carpeta que almacena los .stl, color de los componentes del robot)

# Configurar escena
xmin = -3
xmax = 3
ymin = -3
ymax = 3
zmin = 0
zmax = 2
bounds = [xmin, xmax, ymin, ymax, zmin, zmax]
uniciclo.configureScene(bounds) # Configrar escena (limites)

# Mostrar graficas 
uniciclo.plotDesiredTrajectory(pxd,pyd) # Graficar Trayectoria deseada
uniciclo.initTrajectory(hx,hy) # Graficar Trayectoria realizada por el robot

# Mostrar robots
escala = 5
uniciclo.initRobot(x1,y1,phi,escala) # Mostrar robot

 # Iniciar simulacion          
uniciclo.startSimulation(10,ts) # Iniciar simulacion en el entorno virtual


# Errores
fig = plt.figure()
plt.plot(t,hxe,'b',linewidth = 2, label='hxe')
plt.plot(t,hye,'r',linewidth = 2,  label='hye')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Error [m]')
plt.grid()

# Acciones de control
fig = plt.figure()
plt.subplot(211)
plt.plot(t,uMeas,linewidth = 2,label='Velocidad lineal medida')     
plt.plot(t,uRef,linewidth = 2,label='Velocidad lineal referencia')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.grid()

plt.subplot(212)
plt.plot(t,wMeas,linewidth = 2,label='Velocidad angular medida')     
plt.plot(t,wRef,linewidth = 2,label='Velocidad angular referencia')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [rad/s]')
plt.grid()

plt.show()




