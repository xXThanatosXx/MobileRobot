cmake_minimum_required(VERSION 3.8)
project(difrobot_firmware)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()


# Encuentra los paquetes necesarios de Python
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

# Instalar el paquete de Python
ament_python_install_package(${PROJECT_NAME})

# Instalar scripts Python
install(PROGRAMS
  ${PROJECT_NAME}/simple_serial_transmitter.py
  ${PROJECT_NAME}/simple_serial_receiver.py
  DESTINATION lib/${PROJECT_NAME}
)


# Exportar dependencias necesarias
ament_export_dependencies(
  rclpy
  std_msgs
)

ament_package()
