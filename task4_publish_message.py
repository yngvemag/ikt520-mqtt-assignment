#!/usr/bin/env python3
"""
Task 4: Publish a message to the topic CyberSec/IKT520
"""
import time
from src.publisher import Publisher
from src.subscriber import Subscriber

def main() -> None:
    """Main function to demonstrate publishing and receiving a message."""
    print("Task 4: Publishing a message to the topic CyberSec/IKT520")
    
    # Create the subscriber and connect
    print("\n1. Setting up subscriber...")
    subscriber = Subscriber(
        client_id="subscriber-client",
        broker_host="localhost",
        broker_port=1883,
        clean_session=True
    )
    subscriber.connect()
    
    # Subscribe to the topic
    print("\n2. Subscribing to topic CyberSec/IKT520...")
    subscriber.subscribe("CyberSec/IKT520", qos=1)
    
    # Wait a moment for the subscription to be established
    time.sleep(1)
    
    # Create the publisher and connect
    print("\n3. Setting up publisher...")
    publisher = Publisher(
        client_id="publisher-client",
        broker_host="localhost",
        broker_port=1883,
        clean_session=True
    )
    publisher.connect()
    
    # Publish a message to the topic
    print("\n4. Publishing a message...")
    message = "Hello from the MQTT Python client!"
    publish_info = publisher.publish(
        topic="CyberSec/IKT520",
        payload=message,
        qos=1,
        retain=False
    )
    
    # Explanation of publish arguments
    print("\n5. Explanation of PUBLISH message arguments:")
    print("""
The publish() method arguments have the following meanings:

1. topic: The topic to which the message is published
   - Determines which subscribers will receive the message
   - Topics have a hierarchical structure using / as a separator
   - In this case: "CyberSec/IKT520"

2. payload: The actual message content to be sent
   - Can be a string, bytes, or a numeric type
   - If a string is provided, it's encoded as UTF-8 bytes

3. qos: Quality of Service level (integer: 0, 1, or 2)
   - QoS 0: At most once delivery (fire and forget)
   - QoS 1: At least once delivery (acknowledged delivery)
   - QoS 2: Exactly once delivery (assured delivery)
   - Higher QoS levels involve more handshaking and have more overhead

4. retain: Boolean flag for message retention
   - False: Normal message that is not retained
   - True: Message is stored by the broker and sent to future subscribers
   - Only one retained message is stored per topic
    """)
    
    # Wait to see if the message is received
    print("\n6. Waiting for the subscriber to receive the message...")
    time.sleep(2)
    
    # Check if the message was received
    received_messages = subscriber.get_messages_by_topic("CyberSec/IKT520")
    if received_messages:
        print("\n7. Message received by subscriber:")
        for msg in received_messages:
            print(f"  Topic: {msg['topic']}")
            print(f"  Payload: {msg['payload']}")
            print(f"  QoS: {msg['qos']}")
            print(f"  Timestamp: {msg['timestamp']}")
    else:
        print("\n7. No messages received by the subscriber.")
    
    # Disconnect the clients
    print("\n8. Disconnecting clients...")
    publisher.disconnect()
    subscriber.disconnect()

if __name__ == "__main__":
    main() 