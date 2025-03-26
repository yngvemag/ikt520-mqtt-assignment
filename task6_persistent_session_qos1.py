#!/usr/bin/env python3
"""
Task 6: Test persistent session with clean_session=FALSE and QoS 1
"""
import time
import os
from src.publisher import Publisher
from src.subscriber import Subscriber

def main() -> None:
    """
    Main function to demonstrate persistent sessions with clean_session=FALSE and QoS 1.
    
    Steps:
    1. Create a subscriber with clean_session=FALSE
    2. Subscribe to Sensor/Temp with QoS 1
    3. Disconnect the subscriber
    4. Publish 20 messages to Sensor/Temp with QoS 1
    5. Reconnect the subscriber
    6. Observe if missed messages are delivered
    """
    print("Task 6: Testing persistent sessions with clean_session=FALSE and QoS 1")
    
    # Client IDs must be consistent across reconnections for persistence
    persistent_subscriber_id = "persistent-subscriber-task6"
    publisher_id = "publisher-task6"
    topic = "Sensor/Temp"
    
    # 1. Create subscriber with clean_session=FALSE
    print("\n1. Creating persistent subscriber (clean_session=FALSE)...")
    subscriber = Subscriber(
        client_id=persistent_subscriber_id,
        broker_host="localhost",
        broker_port=1883,
        clean_session=False  # Key setting for persistent sessions
    )
    
    # Connect and subscribe
    print("\n2. Connecting subscriber and subscribing to Sensor/Temp with QoS 1...")
    subscriber.connect()
    subscriber.subscribe(topic, qos=1)  # QoS 1 for at-least-once delivery
    
    # Wait for subscription to be established
    time.sleep(2)
    
    # 3. Disconnect the subscriber
    print("\n3. Disconnecting the subscriber...")
    subscriber.disconnect()
    
    # 4. Publish 20 messages while subscriber is disconnected
    print("\n4. Creating publisher and sending 20 messages to Sensor/Temp with QoS 1...")
    publisher = Publisher(
        client_id=publisher_id,
        broker_host="localhost",
        broker_port=1883
    )
    publisher.connect()
    
    # Publish 20 messages
    for i in range(1, 21):
        message = f"Message {i} for persistent session test"
        publisher.publish(topic, message, qos=1)
        print(f"  Published: {message}")
    
    publisher.disconnect()
    
    # 5. Reconnect the subscriber
    print("\n5. Reconnecting the subscriber (should receive missed messages)...")
    reconnected_subscriber = Subscriber(
        client_id=persistent_subscriber_id,  # Same client ID is crucial
        broker_host="localhost",
        broker_port=1883,
        clean_session=False  # Must be False to resume the session
    )
    reconnected_subscriber.connect()
    
    # Wait for missed messages to be delivered
    print("\n6. Waiting for queued messages to be delivered...")
    time.sleep(10)  # Allow time for all messages to be delivered
    
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
Observation: The subscriber should receive all 20 messages after reconnection.

Explanation:
1. When a client connects with clean_session=FALSE, the broker creates a persistent session.
2. The session stores:
   - Client subscriptions
   - Messages with QoS > 0 that arrive when the client is disconnected
3. When we subscribed with QoS 1, the broker guaranteed at-least-once delivery.
4. While disconnected, the broker queued the 20 QoS 1 messages for our client.
5. Upon reconnection with the same client ID and clean_session=FALSE:
   - The broker recognized the returning client
   - The existing session was resumed (not a new one)
   - Stored subscriptions were still active
   - Queued messages were delivered to the client
   
This behavior demonstrates the reliability features of MQTT:
- Persistent sessions maintain client state across disconnections
- QoS 1 ensures messages are delivered even when clients are temporarily offline
- Client IDs must remain consistent to identify the same client across connections
    """)
    
    # Disconnect
    print("\n9. Disconnecting client...")
    reconnected_subscriber.disconnect()

if __name__ == "__main__":
    main() 