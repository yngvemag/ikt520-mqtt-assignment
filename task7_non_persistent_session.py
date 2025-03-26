#!/usr/bin/env python3
"""
Task 7: Test non-persistent session with clean_session=TRUE and QoS 1
"""
import time
from src.publisher import Publisher
from src.subscriber import Subscriber

def main() -> None:
    """
    Main function to demonstrate non-persistent sessions with clean_session=TRUE and QoS 1.
    
    Steps:
    1. Create a subscriber with clean_session=TRUE
    2. Subscribe to Sensor/Temp with QoS 1
    3. Disconnect the subscriber
    4. Publish 20 messages to Sensor/Temp with QoS 1
    5. Reconnect the subscriber
    6. Observe if missed messages are delivered
    """
    print("Task 7: Testing non-persistent sessions with clean_session=TRUE and QoS 1")
    
    # Client IDs
    subscriber_id = "non-persistent-subscriber-task7"
    publisher_id = "publisher-task7"
    topic = "Sensor/Temp"
    
    # 1. Create subscriber with clean_session=TRUE
    print("\n1. Creating non-persistent subscriber (clean_session=TRUE)...")
    subscriber = Subscriber(
        client_id=subscriber_id,
        broker_host="localhost",
        broker_port=1883,
        clean_session=True  # Key setting for non-persistent sessions
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
        message = f"Message {i} for non-persistent session test"
        publisher.publish(topic, message, qos=1)
        print(f"  Published: {message}")
    
    publisher.disconnect()
    
    # 5. Reconnect the subscriber
    print("\n5. Reconnecting the subscriber (should NOT receive missed messages)...")
    reconnected_subscriber = Subscriber(
        client_id=subscriber_id,  # Same client ID, but doesn't matter with clean_session=TRUE
        broker_host="localhost",
        broker_port=1883,
        clean_session=True  # True means start fresh session
    )
    reconnected_subscriber.connect()
    
    # Re-subscribe to the topic
    print("\n6. Re-subscribing to the topic...")
    reconnected_subscriber.subscribe(topic, qos=1)
    
    # Wait to see if any messages are delivered
    print("\n7. Waiting to see if any messages are delivered...")
    time.sleep(5)  
    
    # 8. Check received messages
    print("\n8. Messages received after reconnection:")
    if reconnected_subscriber.received_messages:
        print(f"  Received {len(reconnected_subscriber.received_messages)} messages:")
        for i, msg in enumerate(reconnected_subscriber.received_messages):
            print(f"  {i+1}. {msg['payload']}")
    else:
        print("  No messages received after reconnection.")
    
    # 9. Explain the observation
    print("\n9. Observation and explanation:")
    print("""
Observation: The subscriber should NOT receive any of the 20 messages sent while it was disconnected.

Explanation:
1. When a client connects with clean_session=TRUE, the broker creates a new, non-persistent session.
2. When the client disconnects:
   - The broker removes all subscription information for this client
   - The broker does not queue messages for this client while it's offline
   - All session state is discarded

3. When the client reconnects with clean_session=TRUE:
   - A completely new session is established
   - No previous subscriptions exist
   - No queued messages are waiting
   - The client must explicitly re-subscribe to topics of interest

4. Even though we published with QoS 1:
   - QoS only guarantees delivery for active sessions or persistent sessions
   - With clean_session=TRUE, there was no active session to deliver to
   - There was no persistent session to queue messages for

This behavior contrasts with Task 6, where we used clean_session=FALSE:
- With clean_session=TRUE: Client state is transient, lasting only for the current connection
- With clean_session=FALSE: Client state persists across disconnections, allowing message queuing
    """)
    
    # Publish a new message after resubscription
    print("\n10. Publishing a new message after resubscription...")
    publisher = Publisher(
        client_id=publisher_id,
        broker_host="localhost",
        broker_port=1883
    )
    publisher.connect()
    new_message = "New message after resubscription"
    publisher.publish(topic, new_message, qos=1)
    publisher.disconnect()
    
    # Wait for the new message
    print("\n11. Waiting for the new message...")
    time.sleep(3)
    
    # Check if new message was received
    print("\n12. Checking if new message was received:")
    if reconnected_subscriber.received_messages:
        print(f"  Received {len(reconnected_subscriber.received_messages)} messages:")
        for i, msg in enumerate(reconnected_subscriber.received_messages):
            print(f"  {i+1}. {msg['payload']}")
    else:
        print("  No messages received.")
    
    # Disconnect
    print("\n13. Disconnecting client...")
    reconnected_subscriber.disconnect()

if __name__ == "__main__":
    main() 