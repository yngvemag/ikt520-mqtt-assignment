#!/usr/bin/env python3
"""
Task 1: Create two MQTT clients (publisher and subscriber)
"""
import time
from src.publisher import Publisher
from src.subscriber import Subscriber

def main() -> None:
    """Main function to demonstrate creating MQTT clients."""
    # Create a publisher client
    print("Task 1: Creating MQTT clients (publisher and subscriber)")
    print("\n1. Creating publisher client")
    publisher = Publisher(
        client_id="publisher-client",
        broker_host="localhost",
        broker_port=1883,
        clean_session=True
    )
    
    # Create a subscriber client
    print("\n2. Creating subscriber client")
    subscriber = Subscriber(
        client_id="subscriber-client",
        broker_host="localhost",
        broker_port=1883,
        clean_session=True
    )
    
    # Print client configuration
    print("\nPublisher Configuration:")
    print(f"  Client ID: {publisher.client_id}")
    print(f"  Broker Host: {publisher.broker_host}")
    print(f"  Broker Port: {publisher.broker_port}")
    print(f"  Clean Session: {publisher.clean_session}")
    print(f"  Keep Alive: {publisher.keep_alive}")
    
    print("\nSubscriber Configuration:")
    print(f"  Client ID: {subscriber.client_id}")
    print(f"  Broker Host: {subscriber.broker_host}")
    print(f"  Broker Port: {subscriber.broker_port}")
    print(f"  Clean Session: {subscriber.clean_session}")
    print(f"  Keep Alive: {subscriber.keep_alive}")
    
    print("\n3. Discussion of Client Arguments:")
    print("""
Arguments used when creating MQTT clients:
    
1. client_id: A unique identifier for the client. This is used by the broker to:
   - Identify each client connection
   - Associate persistent sessions with clients (when clean_session=False)
   - The broker enforces uniqueness, so no two active connections can have the same ID
    
2. broker_host: The hostname or IP address of the MQTT broker to connect to
   - This is where the MQTT server is running (localhost in our case)
    
3. broker_port: The port number for the MQTT broker 
   - Standard unencrypted MQTT uses port 1883
   - MQTT over TLS/SSL typically uses port 8883
    
4. clean_session: Determines if the broker should remove all information about this client when it disconnects
   - True: The broker discards any subscription information and queued messages
   - False: The broker keeps subscription information and queues messages when the client is offline
    
5. keep_alive: The maximum time interval (in seconds) between messages sent or received
   - The client will ensure that at least one message travels in either direction within each keep_alive period
   - If no application message is being exchanged, the client sends PINGREQ packets
   - If the broker doesn't receive any message from the client within 1.5 times the keep_alive time, 
     it assumes the connection is broken and closes it
    """)

if __name__ == "__main__":
    main() 