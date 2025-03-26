from typing import Optional, Any, Dict
import time
from .mqtt_client import MQTTClient

class Publisher(MQTTClient):
    """MQTT Publisher client."""
    
    def __init__(
        self, 
        client_id: str,
        broker_host: str = "localhost", 
        broker_port: int = 1883,
        clean_session: bool = True,
        keep_alive: int = 60
    ) -> None:
        """
        Initialize a new Publisher client.
        
        Args:
            client_id: Unique identifier for this client
            broker_host: MQTT broker hostname or IP address
            broker_port: MQTT broker port
            clean_session: Whether to start a clean session
            keep_alive: Keep alive interval in seconds
        """
        super().__init__(client_id, broker_host, broker_port, clean_session, keep_alive)
        self.published_messages = []
    
    def publish(
        self, 
        topic: str, 
        payload: str,
        qos: int = 0,
        retain: bool = False,
        wait_for_publish: bool = False
    ) -> Dict[str, Any]:
        """
        Publish a message to a topic.
        
        Args:
            topic: Topic to publish to
            payload: Message payload
            qos: Quality of Service level (0, 1, or 2)
            retain: Whether to retain the message
            wait_for_publish: Whether to wait for the publish to complete
            
        Returns:
            Dictionary with information about the published message
        """
        print(f"Publishing message to topic {topic}: {payload} (QoS: {qos}, Retain: {retain})")
        
        # Publish the message
        info = self.client.publish(topic, payload, qos=qos, retain=retain)
        
        if wait_for_publish:
            info.wait_for_publish()
        
        # Store information about this publication
        message_info = {
            'topic': topic,
            'payload': payload,
            'qos': qos,
            'retain': retain,
            'message_id': info.mid,
            'timestamp': time.time()
        }
        
        self.published_messages.append(message_info)
        return message_info
    
    def publish_multiple(
        self, 
        topic: str, 
        payloads: list,
        qos: int = 0,
        retain: bool = False,
        wait_for_publish: bool = False
    ) -> list:
        """
        Publish multiple messages to a topic.
        
        Args:
            topic: Topic to publish to
            payloads: List of message payloads
            qos: Quality of Service level (0, 1, or 2)
            retain: Whether to retain the messages
            wait_for_publish: Whether to wait for each publish to complete
            
        Returns:
            List of dictionaries with information about the published messages
        """
        results = []
        for i, payload in enumerate(payloads):
            message_info = self.publish(
                topic, 
                payload, 
                qos=qos, 
                retain=retain, 
                wait_for_publish=wait_for_publish
            )
            results.append(message_info)
            
            # Short delay between messages to avoid flooding the broker
            if i < len(payloads) - 1:
                time.sleep(0.01)
                
        return results 