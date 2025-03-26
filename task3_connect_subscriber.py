#!/usr/bin/env python3
"""
Task 3: Connect the subscribing client to the Broker and make a subscription
"""
import time
from src.subscriber import Subscriber

class EnhancedSubscriber(Subscriber):
    """Enhanced Subscriber with detailed subscription callback."""
    
    def _on_subscribe(self, client, userdata, mid, reason_codes, properties) -> None:
        """
        Enhanced callback for when the client subscribes to a topic.
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            mid: Message ID for the subscription request
            reason_codes: List of reason codes for each topic filter
            properties: Properties from the SUBACK packet
        """
        print("\nSUBACK received from broker:")
        print(f"  Message ID: {mid}")
        
        for i, code in enumerate(reason_codes):
            topic = list(self.subscriptions.keys())[i] if i < len(self.subscriptions) else f"Unknown topic {i}"
            qos = code if code < 128 else None
            print(f"  Topic {i+1}: {topic}")
            print(f"    Reason Code: {code} ({self._get_reason_code_meaning(code)})")
            print(f"    Granted QoS: {qos}")
        
        print(f"  Properties: {properties if properties else 'None'}")
    
    def _get_reason_code_meaning(self, reason_code) -> str:
        """
        Get the meaning of a subscription reason code.
        
        Args:
            reason_code: The reason code from the SUBACK packet
            
        Returns:
            Description of the reason code
        """
        # Ensure we get an integer value from the reason code
        if hasattr(reason_code, "value"):
            code_value = reason_code.value
        elif hasattr(reason_code, "__int__"):
            code_value = int(reason_code)
        else:
            code_value = reason_code
        
        meanings = {
            0: "Success - Maximum QoS 0",
            1: "Success - Maximum QoS 1",
            2: "Success - Maximum QoS 2",
            128: "Failure - Unspecified error",
            131: "Failure - Implementation specific error",
            135: "Failure - Not authorized",
            143: "Failure - Topic filter invalid",
            145: "Failure - Packet identifier in use",
            151: "Failure - Quota exceeded",
            158: "Failure - Shared subscriptions not supported",
            161: "Failure - Subscription identifiers not supported",
            162: "Failure - Wildcard subscriptions not supported"
        }
        return meanings.get(code_value, f"Unknown reason code: {code_value}")

def main() -> None:
    """Main function to demonstrate connecting a subscriber and making a subscription."""
    print("Task 3: Connecting subscriber to broker and making a subscription")
    
    # Create the enhanced subscriber
    subscriber = EnhancedSubscriber(
        client_id="subscriber-client",
        broker_host="localhost",
        broker_port=1883,
        clean_session=True
    )
    
    print("\n1. Connecting to broker...")
    subscriber.connect()
    
    print("\n2. Explanation of the on_subscribe function:")
    print("""
The on_subscribe callback function is triggered when the client receives a SUBACK message from the broker.
It has the following arguments:

1. client: The client instance that triggered the callback
   - This is a reference to the MQTT client object itself

2. userdata: User data of any type that was set when creating the client instance
   - This is passed from the constructor or user_data_set()

3. mid: Message ID for the subscribe request
   - Matches the message ID returned from the original subscribe() call
   - Useful for tracking which subscription request this acknowledgment corresponds to

4. reason_codes: List of integers giving the granted QoS or failure code for each subscription
   - One reason code for each topic filter in the original subscribe request
   - Values 0-2 represent success with the granted QoS level
   - Values >= 128 represent failure codes

5. properties: Protocol properties from the SUBACK packet (MQTT v5.0 feature)
   - Contains additional metadata about the subscription acknowledgment
   - May be None in MQTT v3.1.1
    """)
    
    print("\n3. Subscribing to topic CyberSec/IKT520 with QoS 1...")
    subscriber.subscribe("CyberSec/IKT520", qos=1)
    
    # Keep the connection open for a short time to observe subscription
    print("\n4. Keeping connection open for 5 seconds...")
    time.sleep(5)
    
    print("\n5. Disconnecting from broker...")
    subscriber.disconnect()

if __name__ == "__main__":
    main() 