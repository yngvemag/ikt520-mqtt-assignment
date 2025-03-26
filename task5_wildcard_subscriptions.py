#!/usr/bin/env python3
"""
Task 5: Make two subscriptions with wildcards and test their operation
"""
import time
from src.publisher import Publisher
from src.subscriber import Subscriber

def main() -> None:
    """Main function to demonstrate wildcard subscriptions."""
    print("Task 5: Testing wildcard subscriptions")
    
    # Create the subscribers
    print("\n1. Setting up subscribers...")
    
    # Subscriber with single-level wildcard
    single_level_subscriber = Subscriber(
        client_id="single-level-wildcard-client",
        broker_host="localhost",
        broker_port=1883
    )
    single_level_subscriber.connect()
    
    # Subscriber with multi-level wildcard
    multi_level_subscriber = Subscriber(
        client_id="multi-level-wildcard-client",
        broker_host="localhost",
        broker_port=1883
    )
    multi_level_subscriber.connect()
    
    # Create the publisher
    publisher = Publisher(
        client_id="publisher-client",
        broker_host="localhost",
        broker_port=1883
    )
    publisher.connect()
    
    # Subscribe using wildcards
    print("\n2. Setting up subscriptions with wildcards...")
    
    # Single-level wildcard (+)
    single_level_topic = "Sensors/+/Temperature"
    print(f"  Subscribing to single-level wildcard topic: {single_level_topic}")
    single_level_subscriber.subscribe(single_level_topic, qos=1)
    
    # Multi-level wildcard (#)
    multi_level_topic = "Sensors/#"
    print(f"  Subscribing to multi-level wildcard topic: {multi_level_topic}")
    multi_level_subscriber.subscribe(multi_level_topic, qos=1)
    
    # Wait for subscriptions to be established
    time.sleep(2)
    
    # Publish messages to various topics
    print("\n3. Publishing messages to various topics...")
    test_topics = [
        "Sensors/Living/Temperature",   # Should match both subscriptions
        "Sensors/Kitchen/Temperature",  # Should match both subscriptions
        "Sensors/Bathroom/Humidity",    # Should match only multi-level wildcard
        "Sensors/Garden/Light/Level",   # Should match only multi-level wildcard
        "Weather/Outside/Temperature"   # Should match neither subscription
    ]
    
    for topic in test_topics:
        payload = f"Value for {topic}"
        publisher.publish(topic, payload, qos=1)
        print(f"  Published to {topic}: {payload}")
    
    # Wait for all messages to be delivered
    print("\n4. Waiting for message delivery...")
    time.sleep(3)
    
    # Show received messages for single-level wildcard subscriber
    print("\n5. Messages received by single-level wildcard subscriber (+):")
    if single_level_subscriber.received_messages:
        for msg in single_level_subscriber.received_messages:
            print(f"  Topic: {msg['topic']}")
            print(f"  Payload: {msg['payload']}")
            print(f"  QoS: {msg['qos']}")
            print()
    else:
        print("  No messages received.")
    
    # Show received messages for multi-level wildcard subscriber
    print("\n6. Messages received by multi-level wildcard subscriber (#):")
    if multi_level_subscriber.received_messages:
        for msg in multi_level_subscriber.received_messages:
            print(f"  Topic: {msg['topic']}")
            print(f"  Payload: {msg['payload']}")
            print(f"  QoS: {msg['qos']}")
            print()
    else:
        print("  No messages received.")
    
    # Explanation of wildcard behavior
    print("\n7. Explanation of wildcard behavior:")
    print("""
MQTT supports two types of wildcards for topic subscriptions:

1. Single-level wildcard (+):
   - Represents a single level in the topic hierarchy
   - Matches exactly one topic level at the position of the wildcard
   - Examples:
     * "Sensors/+/Temperature" matches:
       - "Sensors/Living/Temperature"
       - "Sensors/Kitchen/Temperature"
     * But does NOT match:
       - "Sensors/Bathroom/Humidity" (different final level)
       - "Sensors/Garden/Light/Level" (more levels)
       - "Weather/Outside/Temperature" (different first level)

2. Multi-level wildcard (#):
   - Represents multiple levels in the topic hierarchy
   - Must be the last character in the topic filter
   - Matches any number of levels in the topic (including zero)
   - Examples:
     * "Sensors/#" matches:
       - "Sensors/Living/Temperature"
       - "Sensors/Kitchen/Temperature"
       - "Sensors/Bathroom/Humidity"
       - "Sensors/Garden/Light/Level"
     * But does NOT match:
       - "Weather/Outside/Temperature" (different first level)

Wildcards provide a powerful way to subscribe to multiple related topics with a single subscription,
allowing clients to receive messages from a range of topics that match a specific pattern.
    """)
    
    # Disconnect all clients
    print("\n8. Disconnecting clients...")
    publisher.disconnect()
    single_level_subscriber.disconnect()
    multi_level_subscriber.disconnect()

if __name__ == "__main__":
    main() 