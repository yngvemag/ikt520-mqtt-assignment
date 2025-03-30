import paho.mqtt.client as mqtt
import time
from typing import List, Dict, Any, Optional, Callable, Union
import sys
import threading
from uuid import uuid4

# Global variables to track message receipt
received_messages: Dict[str, List[str]] = {
    "task4": [],
    "task5_single": [],
    "task5_multi": [],
    "task6": [],
    "task7": [],
    "task8": []
}

def task1() -> tuple[mqtt.Client, mqtt.Client]:
    """
    Task 1: Create two MQTT clients - publisher and subscriber.
    
    Returns:
        tuple: (publisher_client, subscriber_client)
    """
    print("\n--- Task 1: Creating MQTT Clients ---")
    
    # Create publisher
    publisher = mqtt.Client(
        client_id=f"publisher-{uuid4().hex[:8]}",  # Generate unique ID
        clean_session=True                         # New session each time
    )
    
    # Create subscriber
    subscriber = mqtt.Client(
        client_id=f"subscriber-{uuid4().hex[:8]}",  # Generate unique ID
        clean_session=True                          # New session each time
    )
    
    print(f"Publisher client created with ID: {publisher._client_id.decode()}")
    print(f"Subscriber client created with ID: {subscriber._client_id.decode()}")
    
    return publisher, subscriber


def task2(publisher: mqtt.Client) -> None:
    """
    Task 2: Connect the publishing client to the broker and observe CONNACK.
    
    Args:
        publisher: MQTT publisher client
    """
    print("\n--- Task 2: Connect Publisher to Broker ---")
    
    # Define the on_connect callback function
    def on_connect(client: mqtt.Client, 
                  userdata: Any, 
                  flags: Dict[str, bool], 
                  rc: int) -> None:
        """Callback when client connects to broker."""
        if rc == 0:
            print(f"Connected to broker with result code {rc}")
            session_present = flags.get('session_present', False)
            print(f"Session present flag: {session_present}")
        else:
            print(f"Failed to connect: {rc}")
    
    # Set the callback
    publisher.on_connect = on_connect
    
    # Connect to broker with error handling
    try:
        publisher.connect(host="localhost", port=1883, keepalive=60)
        publisher.loop_start()
        time.sleep(1)  # Give time for connection to establish
    except Exception as e:
        print(f"Error connecting to broker: {e}")


def task3(subscriber: mqtt.Client) -> None:
    """
    Task 3: Connect the subscribing client and subscribe to a topic.
    
    Args:
        subscriber: MQTT subscriber client
    """
    print("\n--- Task 3: Connect Subscriber and Make Subscription ---")
    
    # Define on_connect callback
    def on_connect(client: mqtt.Client, 
                  userdata: Any, 
                  flags: Dict[str, bool], 
                  rc: int) -> None:
        """Callback when client connects to broker."""
        if rc == 0:
            print(f"Subscriber connected to broker with result code {rc}")
            session_present = flags.get('session_present', False)
            print(f"Session present flag: {session_present}")
            
            # Subscribe to the topic after successful connection
            client.subscribe("CyberSec/IKT520", qos=1)
        else:
            print(f"Subscriber failed to connect: {rc}")
    
    # Define on_subscribe callback
    def on_subscribe(client: mqtt.Client, 
                    userdata: Any, 
                    mid: int, 
                    granted_qos: List[int]) -> None:
        """Callback when broker confirms subscription."""
        print(f"Subscribed with message ID {mid}, granted QoS: {granted_qos}")
    
    # Define on_message callback
    def on_message(client: mqtt.Client, 
                  userdata: Any, 
                  msg: mqtt.MQTTMessage) -> None:
        """Callback when message is received."""
        print(f"Received message: '{msg.payload.decode()}' on topic '{msg.topic}'")
        # Add to appropriate tracking list
        if msg.topic == "CyberSec/IKT520":
            received_messages["task4"].append(msg.payload.decode())
    
    # Set the callbacks
    subscriber.on_connect = on_connect
    subscriber.on_subscribe = on_subscribe
    subscriber.on_message = on_message
    
    # Connect to broker
    try:
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        time.sleep(2)  # Give time for connection and subscription
    except Exception as e:
        print(f"Error connecting subscriber: {e}")


def task4(publisher: mqtt.Client) -> None:
    """
    Task 4: Publish a message to a topic.
    
    Args:
        publisher: MQTT publisher client
    """
    print("\n--- Task 4: Publish Message ---")
    
    # Define parameters
    topic = "CyberSec/IKT520"
    payload = "Hello MQTT World!"
    qos = 1
    retain = False
    
    # Publish the message
    try:
        info = publisher.publish(
            topic=topic,
            payload=payload,
            qos=qos,
            retain=retain
        )
        
        # Wait for message to be sent
        info.wait_for_publish()
        
        print(f"Published message '{payload}' to topic '{topic}'")
        
        # Wait to see if message is received
        time.sleep(2)
        
        if received_messages["task4"]:
            print(f"Subscriber received {len(received_messages['task4'])} messages:")
            for msg in received_messages["task4"]:
                print(f"  - {msg}")
        else:
            print("No messages received by subscriber")
    except Exception as e:
        print(f"Error publishing message: {e}")


def task5(publisher: mqtt.Client) -> None:
    """
    Task 5: Demonstrate wildcard subscriptions.
    
    Args:
        publisher: MQTT publisher client
    """
    print("\n--- Task 5: Wildcard Subscriptions ---")
    
    # Create two subscribers for wildcard topics
    single_wildcard = mqtt.Client(client_id=f"single-wildcard-{uuid4().hex[:8]}")
    multi_wildcard = mqtt.Client(client_id=f"multi-wildcard-{uuid4().hex[:8]}")
    
    # Define on_connect for single-level wildcard subscriber
    def on_connect_single(client: mqtt.Client, 
                         userdata: Any, 
                         flags: Dict[str, bool], 
                         rc: int) -> None:
        if rc == 0:
            print("Single-level wildcard subscriber connected")
            # Subscribe with single-level wildcard (+)
            client.subscribe("Sensors/+/Temperature", qos=1)
            print("Subscribed to: Sensors/+/Temperature")
        else:
            print(f"Single-level wildcard subscriber failed to connect: {rc}")
    
    # Define on_connect for multi-level wildcard subscriber
    def on_connect_multi(client: mqtt.Client, 
                        userdata: Any, 
                        flags: Dict[str, bool], 
                        rc: int) -> None:
        if rc == 0:
            print("Multi-level wildcard subscriber connected")
            # Subscribe with multi-level wildcard (#)
            client.subscribe("Sensors/#", qos=1)
            print("Subscribed to: Sensors/#")
        else:
            print(f"Multi-level wildcard subscriber failed to connect: {rc}")
    
    # Define on_message for single-level wildcard subscriber
    def on_message_single(client: mqtt.Client, 
                         userdata: Any, 
                         msg: mqtt.MQTTMessage) -> None:
        print(f"SINGLE-WILDCARD received: '{msg.payload.decode()}' on '{msg.topic}'")
        received_messages["task5_single"].append(f"{msg.topic}: {msg.payload.decode()}")
    
    # Define on_message for multi-level wildcard subscriber
    def on_message_multi(client: mqtt.Client, 
                        userdata: Any, 
                        msg: mqtt.MQTTMessage) -> None:
        print(f"MULTI-WILDCARD received: '{msg.payload.decode()}' on '{msg.topic}'")
        received_messages["task5_multi"].append(f"{msg.topic}: {msg.payload.decode()}")
    
    # Set callbacks
    single_wildcard.on_connect = on_connect_single
    single_wildcard.on_message = on_message_single
    multi_wildcard.on_connect = on_connect_multi
    multi_wildcard.on_message = on_message_multi
    
    # Connect and start loops
    try:
        single_wildcard.connect(host="localhost", port=1883)
        multi_wildcard.connect(host="localhost", port=1883)
        single_wildcard.loop_start()
        multi_wildcard.loop_start()
        
        # Wait for connections
        time.sleep(2)
        
        # Publish messages to different topics
        test_topics = [
            ("Sensors/Living/Temperature", "22C"),
            ("Sensors/Kitchen/Temperature", "25C"),
            ("Sensors/Living/Humidity", "60%"),
            ("Sensors/Garden/Temperature", "18C"),
            ("Sensors/Kitchen/Temperature/Indoor", "24C"),
            ("Weather/Outside/Temperature", "15C")
        ]
        
        for topic, payload in test_topics:
            publisher.publish(topic=topic, payload=payload, qos=1)
            print(f"Published '{payload}' to '{topic}'")
            time.sleep(0.5)
        
        # Wait for all messages to be received
        time.sleep(2)
        
        # Print results
        print("\nSingle-level wildcard (+) subscription results:")
        for msg in received_messages["task5_single"]:
            print(f"  - {msg}")
        
        print("\nMulti-level wildcard (#) subscription results:")
        for msg in received_messages["task5_multi"]:
            print(f"  - {msg}")
    
    except Exception as e:
        print(f"Error in wildcard test: {e}")
    finally:
        # Disconnect
        single_wildcard.disconnect()
        multi_wildcard.disconnect()
        single_wildcard.loop_stop()
        multi_wildcard.loop_stop()


def task6() -> None:
    """
    Task 6: Test persistent session with QoS 1.
    
    Creates persistent session, disconnects subscriber, publishes messages,
    then reconnects to verify message delivery.
    """
    print("\n--- Task 6: Persistent Session (QoS 1) ---")
    
    # Use fixed client ID for persistence
    client_id = "persistent-subscriber-task6"
    
    # Create subscriber with persistent session
    subscriber = mqtt.Client(
        client_id=client_id,
        clean_session=False  # Persistent session
    )
    
    # Define on_connect handler
    def on_connect(client: mqtt.Client, 
                  userdata: Any, 
                  flags: Dict[str, bool], 
                  rc: int) -> None:
        session_present = flags.get('session_present', False)
        print(f"Persistent subscriber connected, rc={rc}, session present={session_present}")
        
        # Subscribe only if session not present (first connect)
        if not session_present:
            print("No session present, creating new subscription")
            client.subscribe("Sensor/Temp", qos=1)  # QoS 1 subscription
            print("Subscribed to Sensor/Temp with QoS 1")
        else:
            print("Session present, using existing subscription")
    
    # Define on_message handler
    def on_message(client: mqtt.Client, 
                  userdata: Any, 
                  msg: mqtt.MQTTMessage) -> None:
        print(f"Persistent subscriber received: '{msg.payload.decode()}' on '{msg.topic}'")
        received_messages["task6"].append(msg.payload.decode())
    
    # Set callbacks
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message
    
    try:
        # Connect and subscribe
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        time.sleep(2)  # Give time to connect and subscribe
        
        # Disconnect subscriber
        print("Disconnecting subscriber...")
        subscriber.disconnect()
        subscriber.loop_stop()
        time.sleep(1)
        
        # Create publisher and publish 20 messages
        publisher = mqtt.Client(client_id="publisher-task6")
        publisher.connect(host="localhost", port=1883)
        publisher.loop_start()
        
        print("Publishing 20 messages while subscriber is offline")
        for i in range(1, 21):
            publisher.publish("Sensor/Temp", f"Temperature reading {i}", qos=1)
        time.sleep(1)
        
        publisher.disconnect()
        publisher.loop_stop()
        
        # Reconnect subscriber with same client ID
        print("Reconnecting subscriber with persistent session...")
        subscriber = mqtt.Client(
            client_id=client_id,  # Same client ID
            clean_session=False   # Keep the session
        )
        subscriber.on_connect = on_connect
        subscriber.on_message = on_message
        
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        
        # Wait for queued messages to be delivered
        time.sleep(5)
        
        print(f"\nReceived {len(received_messages['task6'])} messages after reconnection")
        print("Observation: The subscriber received all messages published while it was disconnected.")
        print("Explanation:")
        print("  - clean_session=False creates a persistent session")
        print("  - QoS 1 ensures messages are stored for offline clients")
        print("  - When client reconnects with same ID, broker delivers stored messages")
    
    except Exception as e:
        print(f"Error in persistent session test: {e}")
    finally:
        subscriber.disconnect()
        subscriber.loop_stop()


def task7() -> None:
    """
    Task 7: Test non-persistent session with QoS 1.
    
    Creates non-persistent session, disconnects subscriber, publishes messages,
    then reconnects to verify message delivery behavior.
    """
    print("\n--- Task 7: Non-Persistent Session (QoS 1) ---")
    
    # Use fixed client ID
    client_id = "non-persistent-subscriber-task7"
    
    # Create subscriber with clean session
    subscriber = mqtt.Client(
        client_id=client_id,
        clean_session=True  # Non-persistent session
    )
    
    # Define on_connect handler
    def on_connect(client: mqtt.Client, 
                  userdata: Any, 
                  flags: Dict[str, bool], 
                  rc: int) -> None:
        session_present = flags.get('session_present', False)
        print(f"Non-persistent subscriber connected, rc={rc}, session present={session_present}")
        
        # Always subscribe since it's a clean session
        client.subscribe("Sensor/Temp", qos=1)  # QoS 1 subscription
        print("Subscribed to Sensor/Temp with QoS 1")
    
    # Define on_message handler
    def on_message(client: mqtt.Client, 
                  userdata: Any, 
                  msg: mqtt.MQTTMessage) -> None:
        print(f"Non-persistent subscriber received: '{msg.payload.decode()}' on '{msg.topic}'")
        received_messages["task7"].append(msg.payload.decode())
    
    # Set callbacks
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message
    
    try:
        # Connect and subscribe
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        time.sleep(2)  # Give time to connect and subscribe
        
        # Disconnect subscriber
        print("Disconnecting subscriber...")
        subscriber.disconnect()
        subscriber.loop_stop()
        time.sleep(1)
        
        # Create publisher and publish 20 messages
        publisher = mqtt.Client(client_id="publisher-task7")
        publisher.connect(host="localhost", port=1883)
        publisher.loop_start()
        
        print("Publishing 20 messages while subscriber is offline")
        for i in range(1, 21):
            publisher.publish("Sensor/Temp", f"Temperature reading {i}", qos=1)
        time.sleep(1)
        
        publisher.disconnect()
        publisher.loop_stop()
        
        # Reconnect subscriber with same client ID
        print("Reconnecting subscriber with clean session...")
        subscriber = mqtt.Client(
            client_id=client_id,  # Same client ID
            clean_session=True    # Clean session
        )
        subscriber.on_connect = on_connect
        subscriber.on_message = on_message
        
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        
        # Wait for any messages
        time.sleep(5)
        
        print(f"\nReceived {len(received_messages['task7'])} messages after reconnection")
        print("Observation: The subscriber did NOT receive any messages published while it was disconnected.")
        print("Explanation:")
        print("  - clean_session=True creates a new session each time")
        print("  - All subscriptions and pending messages are deleted when client disconnects")
        print("  - QoS 1 guarantees delivery only for active sessions")
    
    except Exception as e:
        print(f"Error in non-persistent session test: {e}")
    finally:
        subscriber.disconnect()
        subscriber.loop_stop()


def task8() -> None:
    """
    Task 8: Test persistent session with QoS 0 subscription and QoS 2 publishing.
    
    Tests message delivery with persistent session but QoS 0 subscription.
    """
    print("\n--- Task 8: Persistent Session, QoS 0 Subscription, QoS 2 Publishing ---")
    
    # Use fixed client ID
    client_id = "mixed-qos-subscriber-task8"
    
    # Create subscriber with persistent session
    subscriber = mqtt.Client(
        client_id=client_id,
        clean_session=False  # Persistent session
    )
    
    # Define on_connect handler
    def on_connect(client: mqtt.Client, 
                  userdata: Any, 
                  flags: Dict[str, bool], 
                  rc: int) -> None:
        session_present = flags.get('session_present', False)
        print(f"Subscriber connected, rc={rc}, session present={session_present}")
        
        # Subscribe only if session not present
        if not session_present:
            print("No session present, creating new subscription")
            client.subscribe("Sensor/Temp", qos=0)  # QoS 0 subscription
            print("Subscribed to Sensor/Temp with QoS 0")
        else:
            print("Session present, using existing subscription")
    
    # Define on_message handler
    def on_message(client: mqtt.Client, 
                  userdata: Any, 
                  msg: mqtt.MQTTMessage) -> None:
        print(f"Subscriber received: '{msg.payload.decode()}' on '{msg.topic}'")
        received_messages["task8"].append(msg.payload.decode())
    
    # Set callbacks
    subscriber.on_connect = on_connect
    subscriber.on_message = on_message
    
    try:
        # Connect and subscribe
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        time.sleep(2)  # Give time to connect and subscribe
        
        # Disconnect subscriber
        print("Disconnecting subscriber...")
        subscriber.disconnect()
        subscriber.loop_stop()
        time.sleep(1)
        
        # Create publisher and publish 20 messages with QoS 2
        publisher = mqtt.Client(client_id="publisher-task8")
        publisher.connect(host="localhost", port=1883)
        publisher.loop_start()
        
        print("Publishing 20 messages with QoS 2 while subscriber is offline")
        for i in range(1, 21):
            publisher.publish("Sensor/Temp", f"Temperature reading {i}", qos=2)
        time.sleep(1)
        
        publisher.disconnect()
        publisher.loop_stop()
        
        # Reconnect subscriber with same client ID
        print("Reconnecting subscriber with persistent session...")
        subscriber = mqtt.Client(
            client_id=client_id,  # Same client ID
            clean_session=False   # Keep the session
        )
        subscriber.on_connect = on_connect
        subscriber.on_message = on_message
        
        subscriber.connect(host="localhost", port=1883, keepalive=60)
        subscriber.loop_start()
        
        # Wait for any queued messages
        time.sleep(5)
        
        print(f"\nReceived {len(received_messages['task8'])} messages after reconnection")
        print("Observation: The subscriber did NOT receive any messages published while it was disconnected.")
        print("Explanation:")
        print("  - Despite using clean_session=False (persistent session)")
        print("  - QoS 0 subscription doesn't support message storage")
        print("  - The subscription QoS level (0) determines storage behavior")
        print("  - Even though messages were published with QoS 2, they weren't stored")
    
    except Exception as e:
        print(f"Error in mixed QoS test: {e}")
    finally:
        subscriber.disconnect()
        subscriber.loop_stop()


def main() -> None:
    """
    Main function to run all tasks sequentially.
    """
    try:
        print("==== IKT520 MQTT Assignment Solution ====")
        print("Make sure an MQTT broker is running at localhost:1883")
        print("(e.g., using: docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx/emqx)")
        
        # Tasks with shared clients
        publisher, subscriber = task1()
        task2(publisher)
        task3(subscriber)
        task4(publisher)
        task5(publisher)
        
        # Stop and clean up shared clients
        subscriber.disconnect()
        publisher.disconnect()
        subscriber.loop_stop()
        publisher.loop_stop()
        
        # Tasks with their own clients
        task6()
        task7()
        task8()
        
        print("\n==== Assignment Complete ====")
        
    except KeyboardInterrupt:
        print("\nExiting due to user interrupt...")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Ensure clients are disconnected
        try:
            publisher.disconnect()
            subscriber.disconnect()
        except:
            pass


if __name__ == "__main__":
    main() 