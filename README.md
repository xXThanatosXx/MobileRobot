# MobileRobot

Bienvenido al repositorio del curso de Mobile Robot. Este curso está diseñado para estudiantes e investigadores interesados en el campo de la robótica móvil y cubre desde conceptos básicos hasta aplicaciones avanzadas de robótica móvil.

## Estructura del Repositorio

Este repositorio está organizado de la siguiente manera:

- `logos/`: Carpeta que contiene los logos relacionados con el curso.
- `código/`: Ejemplos de código fuente en Python para diferentes módulos del curso.
- `README.md`: Este archivo, que proporciona una visión general y guía sobre el repositorio.

## Cómo Usar los Logos

Para utilizar los logos en tus proyectos o documentos, simplemente navega a la carpeta `logos/`, selecciona el logo que desees y descárgalo. Por favor, asegúrate de seguir las directrices de marca y uso proporcionadas.

## Ejemplos de Código Python

A lo largo del curso, utilizaremos varios ejemplos de código Python para demostrar conceptos y técnicas en robótica móvil. Puedes encontrar estos ejemplos en la carpeta `codigo/`.

# Instalación de ROS2 Humble
El objetivo de la presente práctica es instalar y configurar el entorno de trabajo de ROS2 Humble en Ubuntu 22.04, empleando una máquina virtual con VMWorkStation Player 17.

## Recursos Adicionales

Para complementar tu aprendizaje en el curso de Mobile Robot, aquí tienes algunos enlaces a recursos externos que podrían ser de tu interés:

- [VM-Player 17.5.1](https://customerconnect.vmware.com/en/downloads/info/slug/desktop_end_user_computing/vmware_workstation_player/17_0)
- [ubuntu24.0.3](https://ubuntu.com/download/desktop)
- [Documentación Oficial de ROS2 HUMble (Robot Operating System)](https://docs.ros.org/en/humble/index.html)
- 📄 [📂](./Scripts/)Scripts de instalación de ros


### Instalación de Dependencias
Para configurar el entorno necesario para el curso en un sistema operativo Ubuntu, necesitarás instalar algunas dependencias y configurar tu entorno de desarrollo. 
Primero Descargue los archivos de instalación ros2_install.sh y install_ros_packages.sh que se encuentran en la carpeta  [📂](./Scripts/)Scripts y siga los pasos que se indican en el video.

[Ver el video tutorial](https://youtu.be/sk0WTxr-yic?si=M51wHld4yW2u4Ymt)


Abre una terminal y sigue los siguientes pasos.

Presione 
```bash
Crtl + alt + t

```
Cambiar ruta a carpeta Downloads o donde descargó los archvivos de instalación:
```bash
cd Downloads
```
Convertir archivo en ejecutable:
```bash
sudo chmod +x ros2_install.sh
```
Verificar si el archivo es ejecutable:
```bash
ls -la
```
Ejecutar instalador:
```bash
./ros2_install.sh
```
Regresar al directorio principal
```bash
cd
```
Hacer source al bashrc:
```bash
source .bashrc
```
###instalar paquetes adicionales
En nueva terminal ejecutar los siguientes comandos en el espacio de trabajo principal

Presione Crtl + alt + t
```bash
source .bashrc
```
```bash
cd ..
```
```bash
sudo apt-get update 
```
```bash
sudo apt-get install ros-$ROS_DISTRO-joint-state-publisher ros-$ROS_DISTRO-xacro ros-$ROS_DISTRO-joint-state-publisher-gui ros-$ROS_DISTRO-tf2-* ros-$ROS_DISTRO-gazebo-* ros-$ROS_DISTRO-rviz-default-plugins
```
Cambiar a directorio de descargas
```bash
cd Downloads
```
Configurar el archivo install ros packages.sh como ejecutable:
```bash
sudo chmod +x install_ros_packages.sh
```
Verificar configuración
```bash
ls -la
```
Ejecutar el script:
```bash
./install_ros_packages.sh
```
Actualizar el espacio de trabajo en la ruta (home\ros):
```bash
source .bashrc
```
instalar pip en Python:
```bash
sudo apt-get install python3-pip
```
instalar paquete transform 3d:
```bash
pip install transforms3d
```
instalar terminal:
```bash
sudo apt-get install terminator
```
Revisar la versión de Ros instalada:
```bash
rosversion -d
```

