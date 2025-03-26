import time
from typing import Callable, Optional, Dict, Any, List
import paho.mqtt.client as mqtt

class MQTTClient:
    """Base MQTT client class with common functionality."""
    
    def __init__(
        self, 
        client_id: str,
        broker_host: str = "localhost", 
        broker_port: int = 1883,
        clean_session: bool = True,
        keep_alive: int = 60
    ) -> None:
        """
        Initialize a new MQTT client.
        
        Args:
            client_id: Unique identifier for this client
            broker_host: MQTT broker hostname or IP address
            broker_port: MQTT broker port
            clean_session: Whether to start a clean session
            keep_alive: Keep alive interval in seconds
        """
        self.client_id = client_id
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.clean_session = clean_session
        self.keep_alive = keep_alive
        
        # Initialize the MQTT client
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=client_id,
            clean_session=clean_session
        )
        
        # Set up default callbacks
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message
        self.client.on_subscribe = self._on_subscribe
        self.client.on_publish = self._on_publish
        
        # Message storage for received messages
        self.received_messages = []
    
    def connect(self) -> None:
        """Connect to the MQTT broker."""
        print(f"Connecting to broker at {self.broker_host}:{self.broker_port}...")
        self.client.connect(self.broker_host, self.broker_port, self.keep_alive)
        self.client.loop_start()
        time.sleep(1)  # Short delay to allow connection to establish
    
    def disconnect(self) -> None:
        """Disconnect from the MQTT broker."""
        print("Disconnecting from broker...")
        self.client.loop_stop()
        self.client.disconnect()
    
    def _on_connect(self, client, userdata, flags, reason_code, properties) -> None:
        """
        Callback for when the client connects to the broker.
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            flags: Response flags sent by the broker (ConnectFlags object)
            reason_code: Connection result (0 means success)
            properties: Properties from the connection response
        """
        status = "successful" if reason_code == 0 else f"failed with code {reason_code}"
        print(f"Connection {status}")
        print(f"Connection flags: {flags}")
        
        # Access session_present as an attribute, not using get()
        if hasattr(flags, 'session_present'):
            print(f"Session present: {flags.session_present}")
    
    def _on_disconnect(self, client, userdata, reason_code, properties=None, disconnect_flags=None) -> None:
        """
        Callback for when the client disconnects from the broker.
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            reason_code: Disconnection reason code
            properties: Properties from the disconnect packet
            disconnect_flags: Flags from the disconnect packet
        """
        if reason_code != 0:
            print(f"Unexpected disconnection. Reason code: {reason_code}")
        else:
            print("Disconnected from broker")
    
    def _on_message(self, client, userdata, message) -> None:
        """
        Callback for when a message is received from the broker.
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            message: The received message
        """
        payload = message.payload.decode()
        print(f"Received message on topic {message.topic}: {payload} (QoS: {message.qos})")
        self.received_messages.append({
            'topic': message.topic,
            'payload': payload,
            'qos': message.qos,
            'timestamp': time.time()
        })
    
    def _on_subscribe(self, client, userdata, mid, reason_codes, properties) -> None:
        """
        Callback for when the client subscribes to a topic.
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            mid: Message ID for the subscription request
            reason_codes: List of reason codes for each topic filter
            properties: Properties from the SUBACK packet
        """
        print(f"Subscribed with message ID {mid}")
        print(f"Reason codes: {reason_codes}")
    
    def _on_publish(self, client, userdata, mid, reason_code, properties) -> None:
        """
        Callback for when a message is published.
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            mid: Message ID for the published message
            reason_code: Publish reason code
            properties: Properties from the PUBACK packet
        """
        print(f"Message published with ID {mid}, reason code: {reason_code}") 