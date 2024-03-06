# Clase Turtle Sim


El objetivo de la presente práctica es conocer los conceptos básico de ROS2 Humble (paquete, nodo, topicos, info y rqt), para la simulación del comportamiento de un robot móvil

### Instalación de paquete Turtlesim



<p align="center">
  <a href="https://youtu.be/sk0WTxr-yic?si=M51wHld4yW2u4Ymt">
    <img src="./Logos/imagen1.png" height="300">
  </a>
</p>

<p align="center">
<a href="https://youtu.be/sk0WTxr-yic?si=M51wHld4yW2u4Ymt" target="_blank">**Enlace a Video de instalación - Haga clic aquí para más información**</a>.
</p>

Abre una terminal y sigue los siguientes pasos.

Presione 
```bash
Crtl + alt + t

```
```bash
sudo apt install ros-humble-turtlesim
```
Revisar si los paquetes están instalados:
```bash
ros2 pkg executables turtlesim
```
En la terminal debe aparecer los siguientes paquetes:

<p align="center">
<img src="./Logos/Turtle%20pkgs.png" height="100">
</p>

## Nodo
Los nodos son las unidades básicas de ejecución en ROS y cada uno se encarga de una tarea específica, como controlar un sensor, realizar cálculos, procesar datos, o controlar actuadores.
  
Ejecutar el simulador Turtlesim en la terminal:
```bash
ros2 run turtlesim turtlesim_node
```
Ejecutar el paquete de Teleoperación en una nueva terminal:
```bash
Presione CRTL + SHIFT + t
```

```bash
ros2 run turtlesim turtle_teleop_key
```
Debe aparaecer un ventana como se muestra a continuación:
<p align="center">
<img src="./Logos/Tortuga.png" height="300">
</p>

Emplee las teclas de flechas para desplazar  y las letras (G,B,V,C,D,E,R,T), para orientar la tortuga sobre la terminal de teleoperación.
<p align="center">
<img src="./Logos/Teleop.png" height="300">
</p>

<p align="center">
<img src="./Logos/TortugaTeleop.png" height="300">
</p>

Revisar nodos activos en ros es...
```bash
ros2 node list
```
<p align="center">
<img src="./Logos/nodelist.png" height="70">
</p>

Revisar tópicos activos
```bash
ros2 topic list
```
<p align="center">
<img src="./Logos/topiclist.png" height="100">
</p>

Revisar servicios activos en ROS:
```bash
ros2 service list
```
<p align="center">
<img src="./Logos/servicelist.png" height="300">
</p>

Revisar acciones activas en ROS:
```bash
ros2 action list
```
<p align="center">
<img src="./Logos/action.png" height="50">
</p>

```bash
ros2 action list
```
Ejecutar rqt y abrir plugins (Dynamic Reconfigure, topic monitor, Matplot):

```bash
rqt_graph
```
```bash
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=Luisa/cmd_vel
```
```bash
ros2 topic info /Luisa/cmd_vel
```
```bash
ros2 topic echo /Luisa/cmd_vel
```
```bash
rqt 
```
```bash
ros2 topic list -t
```
```bash
ros2 interface show geometry_msgs/msg/Twist
```
```bash
ros2 topic pub --rate 1 /Luisa/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0,  y: 0.0, z: 1.8}}"
```
```bash
ros2 topic type /Luisa/pose
```
```bash
ros2 interface proto turtlesim/msg/Pose
```
