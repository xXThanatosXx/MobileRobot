
# Configuración de Arduino con ROS2 en Docker sobre Windows y WSL2

Esta guía te llevará a través de los pasos necesarios para configurar y ejecutar un contenedor Docker con **ROS2** en **Windows** utilizando **WSL2** y conectarlo a un **Arduino** a través de USB.

## 1. Instalar Docker Desktop con soporte para WSL2

- Instalar wsl
```bash
wsl --install -d Ubuntu
```
Acualizar:
```bash
wsl --update
```
Apagar:
```bash
wsl --shutdown
```
Listar Wsl:
```bash
wsl --list --verbose
```
Ejecutar WSL:
```bash
wsl -d Ubuntu
```


1. **Descargar e instalar Docker Desktop**:
   - Ve a la [página oficial de Docker](https://www.docker.com/products/docker-desktop) y descarga Docker Desktop.
   - Durante la instalación, selecciona la opción de usar **WSL 2** como backend.

2. **Configurar WSL2**:
   - Docker Desktop usa **WSL2** para ejecutar contenedores en Windows. Si aún no tienes WSL2 configurado, asegúrate de instalarlo siguiendo [esta guía](https://docs.microsoft.com/en-us/windows/wsl/install).

   - identificar puerto USB:
   Identificar puertos
   ```bash
   mode
   ```

   - Verifica que WSL2 está instalado con:
     ```bash
     wsl --list --verbose
     ```

## 2. Instalar y configurar `usbipd` para acceder a dispositivos USB

1. **Instalar `usbipd`**:
   - Abre **PowerShell** como administrador y ejecuta:
     ```bash
     winget install --interactive --exact dorssel.usbipd-win
     ```

2. **Verificar dispositivos USB conectados**:
   - Conecta tu **Arduino** a un puerto USB y verifica los dispositivos con:
     ```bash
     usbipd list
     ```

3. **Adjuntar el dispositivo USB a WSL2**:
   - Adjunta el Arduino a WSL2 con:
     ```bash
     usbipd attach --busid 1-2 --wsl
     ```

4. **Verificar el dispositivo en WSL**:
   - Verifica que el dispositivo esté disponible:
     ```bash
     ls /dev/ttyACM0
     ```
5. **Desactivar puerto**
   ```bash
     usbipd detach --busid <BUSID> 
   ```



## 3. Ejecutar el contenedor Docker con acceso al dispositivo USB

1. **Iniciar el contenedor Docker**:
   ```bash
   docker run --name ros-humble-usb --gpus all --cpus="6" --memory="8g" -it --device=/dev/ttyACM0 \
       --env=DISPLAY=host.docker.internal:0 --volume="c:/mnt/c" \
       --volume="c:/users/unimar/documents/docker/Shared_Folder:/mnt/shared_folder" \
       --restart=no --runtime=runc --network=host -t ros2-humble-usb:latest
   ```

2. **Verificar el acceso al puerto USB**:
   ```bash
   ls /dev/ttyACM0
   ```

## 5. Configurar ROS2 y ejecutar nodos que interactúen con el Arduino

1. **Dar permisos al puerto serie**:
   ```bash
   sudo chmod 666 /dev/ttyACM0
   ```
   ```bash
   sudo usermod -aG dialout $USER
   ```
   

2. **Ejecutar tu nodo ROS2**:
   ```bash
   ros2 run difrobot_firmware simple_serial_transmitter.py --ros-args -p port:=/dev/ttyACM0
   ```

## 6. Solución de problemas comunes

- Si no puedes acceder al puerto USB, asegúrate de que está adjunto con `usbipd`.
- Si ves errores de permisos, verifica que el usuario tiene permisos para acceder al puerto serie con `chmod 666 /dev/ttyACM0`.

---

¡Listo! Siguiendo estos pasos deberías poder configurar y ejecutar un contenedor Docker con ROS2 y comunicarte con tu Arduino a través del puerto USB.


https://learn.microsoft.com/en-us/windows/wsl/connect-usb