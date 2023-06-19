# Los animatronicos

En este documento se describe como se debe de ejecutar los diferentes procesos para poder emplear el robot de este proyecto:


////////////////////////////////////////////////////////////
-------------------------PAGINA WEB-------------------------
////////////////////////////////////////////////////////////

-BRIDGE: ros2 launch rosbridge_server rosbridge_websocket_launch.xml
-HTTP: python3 -m http.server 8000 #dentro de la carpeta de rosweb

////////////////////////////////////////////////////////////
-------------------------GENERAL----------------------------
////////////////////////////////////////////////////////////

-POSICION ROBOT GAZEBO: ros2 topic pub -1 /initialpose geometry_msgs/msg/PoseWithCovarianceStamped "{header: {stamp: {sec: 0}, frame_id: 'map'}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {w: 0.0}}}}"

-SERVICIO: ros2 launch proy_fnaf_my_service movement_server_launch.launch.py #en caso de utilizar los servicios

-RVIZ: ros2 launch proy_fnaf_my_nav2_system my_tb3_sim_nav2.launch.py
-MAPA: ros2 service call /map_server/load_map nav2_msgs/srv/LoadMap "{map_url: $HOME/turtlebot3_ws/src/proy_fnaf/proy_fnaf_my_nav2_system/config/my_map.yaml}"

////////////////////////////////////////////////////////////
---------------------ROBOT VIRTUAL--------------------------
////////////////////////////////////////////////////////////

-GAZEBO: ros2 launch proy_fnaf_my_world turtlebot3_my_world.launch.py

-DETECCION COLORES: ros2 run capture_image capture_image 

////////////////////////////////////////////////////////////
-----------------------ROBOT REAL---------------------------
////////////////////////////////////////////////////////////

TP-LINK_6CAE		password: 41422915

ssh ubuntu@192.168.0.64 #conectarse con el robot source install/setup.bash
password: turtlebot

#comandos para hacer cosas con el robot 

ros2 launch turtlebot3_bringup robot.launch.py #hacer dentro del ssh #es para empezar la conexion
ros2 run nav2_map_server map_saver_cli -f ~/nombre #para guardar un entorno escaneado

PUBLICAR IMAGENES: ros2 run image_tools cam2image --ros-args -p burger_mode:=false -p frequency

