#!/usr/bin/env python3
"""
Task 2: Connect the publishing client to a Broker and observe CONNACK
"""
import time
from src.publisher import Publisher

class EnhancedPublisher(Publisher):
    """Enhanced Publisher with detailed connection callback."""
    
    def _on_connect(self, client, userdata, flags, rc, properties=None) -> None:
        """
        Enhanced callback for when the client connects to the broker.
        Supports both MQTT v3.1.1 and v5.0
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            flags: Response flags sent by the broker
            rc: Connection result (0 means success) - can be int or ReasonCode
            properties: Properties from the connection response (MQTT v5.0)
        """
        print("\nCONNACK received from broker:")
        reason_code = rc.value if hasattr(rc, 'value') else rc
        print(f"  Reason Code: {reason_code} ({self._get_reason_code_meaning(reason_code)})")
        print(f"  Session Present Flag: {flags.session_present if hasattr(flags, 'session_present') else False}")
        print(f"  Properties: {properties if properties else 'None'}")
        
        if reason_code == 0:
            print("  Status: Successfully connected to the broker")
        else:
            print(f"  Status: Connection failed with code {reason_code}")
    
    def _on_disconnect(self, client, userdata, flags, rc, properties=None) -> None:
        """
        Callback for when the client disconnects from the broker.
        Supports both MQTT v3.1.1 and v5.0
        
        Args:
            client: The client instance
            userdata: User data set in Client() or userdata_set()
            flags: Response flags (for v5)
            rc: Disconnection reason code
            properties: Properties from disconnect packet (MQTT v5.0)
        """
        reason_code = rc.value if hasattr(rc, 'value') else rc
        print(f"Disconnected with reason code: {reason_code}")
    
    def _get_reason_code_meaning(self, reason_code: int) -> str:
        """
        Get the meaning of a connection reason code.
        
        Args:
            reason_code: The reason code from the CONNACK packet
            
        Returns:
            Description of the reason code
        """
        meanings = {
            0: "Success - Connection accepted",
            1: "Connection refused - unacceptable protocol version",
            2: "Connection refused - identifier rejected",
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorized"
        }
        return meanings.get(reason_code, "Unknown reason code")

def main() -> None:
    """Main function to demonstrate connecting a publisher to a broker."""
    print("Task 2: Connecting publisher to broker and observing CONNACK")
    
    # Create the enhanced publisher
    publisher = EnhancedPublisher(
        client_id="publisher-client",
        broker_host="localhost",
        broker_port=1883,
        clean_session=True
    )
    
    print("\n1. Explanation of on_connect arguments:")
    print("""
The on_connect callback function is triggered when the client receives a CONNACK message from the broker.
It has the following arguments:

1. client: The client instance that triggered the callback
   - This is a reference to the MQTT client object itself
   - Useful for performing operations within the callback

2. userdata: User data of any type that was set when creating the client instance
   - This is passed from the constructor or set with user_data_set()
   - Allows passing custom data to callbacks

3. flags: A dictionary containing response flags from the broker
   - session_present: Boolean flag indicating if the broker already has a persistent session for this client
     * True: A session was present, and subscriptions still exist from previous connections
     * False: No session was present or clean_session was set to True

4. reason_code: The connection result (integer)
   - 0: Success - connection accepted
   - 1-5: Various failure reasons (protocol version, identifier rejected, etc.)

5. properties: Protocol properties from the CONNACK packet
   - MQTT v5.0 feature, contains additional metadata about the connection
   - May be None in MQTT v3.1.1
    """)
    
    print("\n2. Connecting to broker...")
    publisher.connect()
    
    # Keep the script running for a short time to observe connection
    time.sleep(3)
    
    print("\n3. Disconnecting from broker...")
    publisher.disconnect()

if __name__ == "__main__":
    main() 
