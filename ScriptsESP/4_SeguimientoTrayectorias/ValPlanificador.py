from pyRobotics import *
import matplotlib.pyplot as plt

#variables de tiempo
tf = 120 # tiempo de simulacion 
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

vMax = 0.1 #m/seg
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

sizePoints = len(pxd)

beta = np.zeros(sizePoints)

#calculo de angulo beta

for p in range(sizePoints):
    if p ==1:
        
        beta[p] = np.arctan2((pyd[p+1]-pyd[p]),(pxd[p+1]-pxd[p]))
    else:
        beta[p] = np.arctan2((pyd[p]-pyd[p-1]),(pxd[p]-pxd[p-1]))

#velocidades de referencia
uRef = np.zeros(N)# velocidad lineal m/seg
wRef = np.zeros(N) # velocidad angular rad/seg

#errores de posicion

hxe = np.zeros(N)
hye = np.zeros(N)


#bucle de evaluacion

for k in range(N):

    #algoritmo de control para un punto cercano

    minimo = 100
    for p in range(sizePoints):
        #distance euclideana
        aux = np.sqrt((pxd[p]-hx[k])**2+(pyd[p]-hy[k])**2)
        if aux < minimo:
            minimo = aux
            #posicion mas cercana
            pos = p

    #calculo de errores
    hxe[k] = pxd[pos]-hx[k]
    hye[k] = pyd[pos]-hy[k]
    #organizar los errores en un arreglo
    he = np.array([[hxe[k]],[hye[k]]])

    #Matriz jacobiana

    J = np.array([[ np.cos(phi[k]), - a*np.sin(phi[k])],
                   [ np.sin(phi[k]),  a*np.cos(phi[k])]])

    # Parametros de control
    K = np.array([[0.1,0],
                 [0,0.1]])
    #Velocidades deseadas
    pxdp = vMax*np.cos(beta[pos])
    pydp = vMax*np.sin(beta[pos])

    pdp = np.array([[pxdp],[pydp]])

    # Ley de control
    qpRef = np.linalg.pinv(J)@(pdp+K@he)

    #Aplicar ley de control

    uRef[k] = qpRef[0][0]
    wRef[k] = qpRef[1][0]

     # Integral numerica
    phi[k+1] = phi[k]+ts*wRef[k]

     # Modelo cinemático
     
    x1p = uRef[k]*np.cos(phi[k+1])
    y1p = uRef[k]*np.sin(phi[k+1])
     
     # Integral numerica
    x1[k+1] = x1[k] + ts*x1p
    y1[k+1] = y1[k] + ts*y1p
     
     # Cinematica directa   
    hx[k+1] = x1[k+1]+a*np.cos(phi[k+1]);  # Posicion inicial en el eje x en metros [m]
    hy[k+1] = y1[k+1]+a*np.sin(phi[k+1]);   # Posicion inicial en el eje y en metros [m]
     

################### SIMULACION VIRTUAL #################### 

# Cargar componentes del robot
pathStl = "stl"
color = ['blue','black','gray','gray','white','black']
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

############################## Graficas ######################


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
plt.plot(t,uRef,linewidth = 2,label='Velocidad lineal referencia')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [m/s]')
plt.grid()

plt.subplot(212)
plt.plot(t,wRef,linewidth = 2,label='Velocidad angular referencia')
plt.legend(loc='upper right')
plt.xlabel('Tiempo [s]')
plt.ylabel('Velocidad [rad/s]')
plt.grid()

plt.show()
    



    










    
    
