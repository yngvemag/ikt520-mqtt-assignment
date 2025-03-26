from typing import Optional, List, Dict, Any, Tuple
import time
from .mqtt_client import MQTTClient

class Subscriber(MQTTClient):
    """MQTT Subscriber client."""
    
    def __init__(
        self, 
        client_id: str,
        broker_host: str = "localhost", 
        broker_port: int = 1883,
        clean_session: bool = True,
        keep_alive: int = 60
    ) -> None:
        """
        Initialize a new Subscriber client.
        
        Args:
            client_id: Unique identifier for this client
            broker_host: MQTT broker hostname or IP address
            broker_port: MQTT broker port
            clean_session: Whether to start a clean session
            keep_alive: Keep alive interval in seconds
        """
        super().__init__(client_id, broker_host, broker_port, clean_session, keep_alive)
        self.subscriptions = {}
    
    def subscribe(self, topic: str, qos: int = 0) -> int:
        """
        Subscribe to a topic.
        
        Args:
            topic: Topic to subscribe to
            qos: Quality of Service level (0, 1, or 2)
            
        Returns:
            Message ID for the subscription request
        """
        print(f"Subscribing to topic {topic} with QoS {qos}")
        result, mid = self.client.subscribe(topic, qos)
        
        if result == 0:
            self.subscriptions[topic] = {
                'qos': qos,
                'mid': mid,
                'timestamp': time.time()
            }
        else:
            print(f"Failed to subscribe to {topic}, result code: {result}")
        
        return mid
    
    def subscribe_multiple(self, topics: List[Tuple[str, int]]) -> int:
        """
        Subscribe to multiple topics.
        
        Args:
            topics: List of tuples containing (topic, qos)
            
        Returns:
            Message ID for the subscription request
        """
        print(f"Subscribing to multiple topics: {topics}")
        result, mid = self.client.subscribe(topics)
        
        if result == 0:
            for topic, qos in topics:
                self.subscriptions[topic] = {
                    'qos': qos,
                    'mid': mid,
                    'timestamp': time.time()
                }
        else:
            print(f"Failed to subscribe to topics, result code: {result}")
        
        return mid
    
    def unsubscribe(self, topic: str) -> int:
        """
        Unsubscribe from a topic.
        
        Args:
            topic: Topic to unsubscribe from
            
        Returns:
            Message ID for the unsubscribe request
        """
        print(f"Unsubscribing from topic {topic}")
        result, mid = self.client.unsubscribe(topic)
        
        if result == 0 and topic in self.subscriptions:
            del self.subscriptions[topic]
        
        return mid
    
    def get_messages_by_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Get all messages received for a specific topic.
        
        Args:
            topic: Topic to get messages for
            
        Returns:
            List of message dictionaries
        """
        return [msg for msg in self.received_messages if msg['topic'] == topic]
    
    def wait_for_messages(self, topic: str = None, count: int = 1, timeout: float = 10.0) -> List[Dict[str, Any]]:
        """
        Wait for a specific number of messages to be received.
        
        Args:
            topic: Topic to wait for messages on (None for any topic)
            count: Number of messages to wait for
            timeout: Maximum time to wait in seconds
            
        Returns:
            List of received messages
        """
        start_time = time.time()
        current_count = len(self.get_messages_by_topic(topic)) if topic else len(self.received_messages)
        target_count = current_count + count
        
        while current_count < target_count:
            if time.time() - start_time > timeout:
                print(f"Timeout waiting for messages. Got {current_count}/{target_count}")
                break
            
            time.sleep(0.1)
            current_count = len(self.get_messages_by_topic(topic)) if topic else len(self.received_messages)
        
        if topic:
            return self.get_messages_by_topic(topic)[-count:] if current_count >= target_count else []
        else:
            return self.received_messages[-count:] if current_count >= target_count else [] 