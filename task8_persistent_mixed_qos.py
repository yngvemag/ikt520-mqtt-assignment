#!/usr/bin/env python3
"""
Task 8: Test persistent session with clean_session=FALSE, QoS 0 subscription, QoS 2 publishing
"""
import time
from src.publisher import Publisher
from src.subscriber import Subscriber

def main() -> None:
    """
    Main function to demonstrate persistent sessions with clean_session=FALSE, 
    QoS 0 subscription, and QoS 2 publishing.
    
    Steps:
    1. Create a subscriber with clean_session=FALSE
    2. Subscribe to Sensor/Temp with QoS 0
    3. Disconnect the subscriber
    4. Publish 20 messages to Sensor/Temp with QoS 2
    5. Reconnect the subscriber
    6. Observe if missed messages are delivered
    """
    print("Task 8: Testing persistent sessions with clean_session=FALSE, QoS 0 subscription, QoS 2 publishing")
    
    # Client IDs must be consistent across reconnections for persistence
    persistent_subscriber_id = "persistent-subscriber-task8"
    publisher_id = "publisher-task8"
    topic = "Sensor/Temp"
    
    # 1. Create subscriber with clean_session=FALSE
    print("\n1. Creating persistent subscriber (clean_session=FALSE)...")
    subscriber = Subscriber(
        client_id=persistent_subscriber_id,
        broker_host="localhost",
        broker_port=1883,
        clean_session=False  # Key setting for persistent sessions
    )
    
    # Connect and subscribe with QoS 0
    print("\n2. Connecting subscriber and subscribing to Sensor/Temp with QoS 0...")
    subscriber.connect()
    subscriber.subscribe(topic, qos=0)  # QoS 0 for at-most-once delivery
    
    # Wait for subscription to be established
    time.sleep(2)
    
    # 3. Disconnect the subscriber
    print("\n3. Disconnecting the subscriber...")
    subscriber.disconnect()
    
    # 4. Publish 20 messages with QoS 2 while subscriber is disconnected
    print("\n4. Creating publisher and sending 20 messages to Sensor/Temp with QoS 2...")
    publisher = Publisher(
        client_id=publisher_id,
        broker_host="localhost",
        broker_port=1883
    )
    publisher.connect()
    
    # Publish 20 messages with QoS 2
    for i in range(1, 21):
        message = f"Message {i} for persistent session QoS 0/2 test"
        publisher.publish(topic, message, qos=2)  # QoS 2 for exactly-once delivery
        print(f"  Published: {message}")
    
    publisher.disconnect()
    
    # 5. Reconnect the subscriber
    print("\n5. Reconnecting the subscriber...")
    reconnected_subscriber = Subscriber(
        client_id=persistent_subscriber_id,  # Same client ID is crucial
        broker_host="localhost",
        broker_port=1883,
        clean_session=False  # Must be False to resume the session
    )
    reconnected_subscriber.connect()
    
    # Wait to see if any messages are delivered
    print("\n6. Waiting to see if any messages are delivered...")
    time.sleep(5)
    
    # 7. Check received messages
    print("\n7. Messages received after reconnection:")
    if reconnected_subscriber.received_messages:
        print(f"  Received {len(reconnected_subscriber.received_messages)} messages:")
        for i, msg in enumerate(reconnected_subscriber.received_messages):
            print(f"  {i+1}. {msg['payload']}")
    else:
        print("  No messages received after reconnection.")
    
    # 8. Explain the observation
    print("\n8. Observation and explanation:")
    print("""
Observation: The subscriber should NOT receive any of the 20 messages sent while it was disconnected,
despite using clean_session=FALSE.

Explanation:
1. We created a persistent session with clean_session=FALSE, which:
   - Maintains client subscription information across disconnections
   - Can queue messages while the client is disconnected

2. However, a critical factor is the QoS level of the SUBSCRIPTION:
   - We subscribed with QoS 0 (at-most-once delivery)
   - QoS 0 subscriptions do not receive stored messages, even in a persistent session
   - Only QoS 1 and QoS 2 subscriptions are eligible to receive stored messages

3. The QoS level has the following implications:
   - QoS 0: No guarantee of delivery, no storage for offline clients
   - QoS 1: At-least-once delivery, messages stored for offline clients with persistent sessions
   - QoS 2: Exactly-once delivery, messages stored for offline clients with persistent sessions

4. The message persistence is determined by BOTH:
   - The client's session type (persistent or non-persistent)
   - The QoS level of the SUBSCRIPTION (not the message)

5. Even though we published with QoS 2 (highest reliability):
   - The QoS 0 subscription doesn't support storing messages for offline clients
   - The subscription QoS acts as a "maximum QoS" filter
   - Messages are "downgraded" to match the subscription QoS

This demonstrates an important concept in MQTT: message delivery guarantees are limited by 
the lowest QoS in the chain (publication QoS or subscription QoS).
    """)
    
    # Disconnect
    print("\n9. Disconnecting client...")
    reconnected_subscriber.disconnect()

if __name__ == "__main__":
    main() 