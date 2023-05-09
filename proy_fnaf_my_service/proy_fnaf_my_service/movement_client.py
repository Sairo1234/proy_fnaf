#importamos el mensaje
from custom_interface.srv import MyMoveMsg
#importamos la bib ROS2 para python
import rclpy
from rclpy.node import Node
# importar Odometry desde la interface nav_msgs
from nav_msgs.msg import Odometry
# importar la librería de calidad del servicio para fijar las políticas de calidad
from rclpy.qos import ReliabilityPolicy, QoSProfile
#importamos la bib sys para poder usar los arg de entrada
import sys

#definimos la clase cliente
class ClientAsync(Node):

    def __init__(self):
        #inicializa el nodo cliente
        super().__init__('movement_client')
        #crea el objeto cliente
        self.client = self.create_client(MyMoveMsg, 'movement')
        #cada segundo revisa si el servicio esta activo
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('el servicio no esta activo, prueba de nuevo...')
        
        #crea el mensaje 
        self.req = MyMoveMsg.Request()            

        # creamos una variable para pasarle el texto para parar o seguir o girar
        self.position_x = 0.0
        self.position_y = 0.0

        self.subscriber= self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback, 
            QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)) 
        # prevent unused variable warning
        self.subscriber

    def send_request(self, parametro):
        # usa sys.argv para tener acceso a los argumentos introducidos en la
        # llamada al programa por consola
        if parametro == "nada":
            self.req.move = sys.argv[1]
        else:
            self.req.move = parametro

        #envia la peticion del servicio
        self.future = self.client.call_async(self.req)

    def listener_callback(self, msg):
        # imprime los datos leídos
        self.position_x = msg.pose.pose.position.x
        self.position_y = msg.pose.pose.position.y
        self.get_logger().info('Se está recibiendo x: "%s"' % str(msg.pose.pose.position.x))
        self.get_logger().info('Se está recibiendo y: "%s"' % str(msg.pose.pose.position.y)) 
        
        if (self.position_y > -0.01 and self.position_x < 0 and self.position_x > -0.1):
            # se le pasa a una variable de la clase
            self.get_logger().info('dentro del if')
            self.send_request("parar")

def main(args=None):
    #inicializa la comunicacion ROS2
    rclpy.init(args=args)
    #declara el constructor del objeto cliente
    client = ClientAsync()
    #ejecuta el metodo de peticion de servicio
    client.send_request("nada")

    while rclpy.ok():
        #deja el nodo abierto hasta recibir ctrl+c
        rclpy.spin(client)
        #si se ha enviado el mensaje future
        if client.future.done():
            try:
                # chequea el mensaje future
                # si se ha enviado una respuesta 
                # la recoge
                response = client.future.result()
            except Exception as e:
                client.get_logger().info('La llamada al servicio ha fallado %r' % (e,))
        else:
            client.get_logger().info('Respuesta del servicio %r' % (response.success,))
        break
    #ejecuta el metodo de peticion de servicio
    client.send_request()

    # client.destroy_node()
    # rclpy.shutdown()

if __name__=='__main__':
    main()
