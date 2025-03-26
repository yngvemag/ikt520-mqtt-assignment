# MQTT Assignment Solution

This is a comprehensive solution for the IKT520 MQTT Mandatory Assignment (MA-02). The solution implements several instances of the MQTT protocol using the `paho-mqtt` library in Python.

## Setup Instructions

### Environment Setup

1. Create and activate a conda environment:

```bash
conda env create -f environment.yml
conda activate ikt520-mqtt-assignment
```

2. Ensure you have an MQTT broker running:
   - The solution is configured to use an EMQX broker running locally on port 1883
   - Web interface is available on port 18083

### Running the Solution

You can run all tasks sequentially:

```bash
python run_all_tasks.py
```

Or run a specific task:

```bash
python run_all_tasks.py 1  # Run task 1 only
```

Alternatively, you can run individual task scripts directly:

```bash
python task1_create_clients.py
```

## Solution Structure

The solution is organized as follows:

- `src/` - Core MQTT client classes
  - `mqtt_client.py` - Base MQTT client with common functionality
  - `publisher.py` - Publisher client implementation
  - `subscriber.py` - Subscriber client implementation
- Task implementations
  - `task1_create_clients.py` - Create publisher and subscriber clients
  - `task2_connect_publisher.py` - Connect publisher to broker
  - `task3_connect_subscriber.py` - Connect subscriber and make subscription
  - `task4_publish_message.py` - Publish a message to a topic
  - `task5_wildcard_subscriptions.py` - Test wildcard subscriptions
  - `task6_persistent_session_qos1.py` - Test persistent sessions with QoS 1
  - `task7_non_persistent_session.py` - Test non-persistent sessions
  - `task8_persistent_mixed_qos.py` - Test persistent sessions with mixed QoS
- `run_all_tasks.py` - Script to run all tasks sequentially
- `environment.yml` - Conda environment definition

## Answers to Assignment Questions

### 1. Use the `paho-mqtt` library and create two clients (publisher and a subscriber)

In this implementation, we created a base `MQTTClient` class in `src/mqtt_client.py` and then extended it to create specialized `Publisher` and `Subscriber` classes.

The meanings of the arguments used when creating clients are:

1. **client_id**: A unique identifier for the client
   - Used by the broker to identify each client connection
   - Associates persistent sessions with clients (when clean_session=False)
   - The broker enforces uniqueness; no two active connections can have the same ID

2. **broker_host**: The hostname or IP address of the MQTT broker
   - Specifies where the MQTT server is running (localhost in our case)

3. **broker_port**: The port number for the MQTT broker
   - Standard unencrypted MQTT uses port 1883
   - MQTT over TLS/SSL typically uses port 8883

4. **clean_session**: Determines if the broker should remove client information on disconnect
   - True: The broker discards subscription information and queued messages
   - False: The broker keeps subscription information and queues messages when offline

5. **keep_alive**: The maximum time interval (in seconds) between messages
   - The client ensures at least one message travels in either direction within each keep_alive period
   - If no application message is being exchanged, the client sends PINGREQ packets
   - If the broker doesn't receive any message within 1.5 times the keep_alive time, it assumes the connection is broken

### 2. Connect the publishing client to a Broker

We implemented a detailed `on_connect` callback in `task2_connect_publisher.py` to observe the CONNACK reply from the broker.

The arguments to the `on_connect` function have the following meanings:

1. **client**: The client instance that triggered the callback
   - Reference to the MQTT client object itself
   - Useful for performing operations within the callback

2. **userdata**: User data set when creating the client instance
   - Passed from the constructor or user_data_set()
   - Allows passing custom data to callbacks

3. **flags**: Dictionary containing response flags from the broker
   - session_present: Boolean flag indicating if a persistent session exists
     - True: A session was present, subscriptions still exist
     - False: No session was present or clean_session was True

4. **reason_code**: The connection result (integer)
   - 0: Success - connection accepted
   - 1-5: Various failure reasons (protocol version, identifier rejected, etc.)

5. **properties**: Protocol properties from the CONNACK packet
   - MQTT v5.0 feature containing metadata about the connection
   - May be None in MQTT v3.1.1

### 3. Connect the subscribing client to the Broker

We implemented a detailed `on_subscribe` callback in `task3_connect_subscriber.py` to observe the SUBACK reply from the broker when subscribing to the topic `CyberSec/IKT520`.

The arguments to the `on_subscribe` function have the following meanings:

1. **client**: The client instance that triggered the callback
   - Reference to the MQTT client object itself

2. **userdata**: User data set when creating the client instance
   - Passed from the constructor or user_data_set()

3. **mid**: Message ID for the subscribe request
   - Matches the message ID from the original subscribe() call
   - Useful for tracking which subscription this acknowledgment is for

4. **reason_codes**: List of integers giving the granted QoS or failure code
   - One reason code for each topic filter in the original subscribe request
   - Values 0-2 represent success with the granted QoS level
   - Values >= 128 represent failure codes

5. **properties**: Protocol properties from the SUBACK packet
   - MQTT v5.0 feature with additional metadata
   - May be None in MQTT v3.1.1

### 4. Publish a message to the topic `CyberSec/IKT520`

In `task4_publish_message.py`, we published a message to the topic `CyberSec/IKT520` and verified it was received by the subscriber.

The publish method arguments have the following meanings:

1. **topic**: The topic to which the message is published
   - Determines which subscribers will receive the message
   - Topics have a hierarchical structure using / as a separator

2. **payload**: The actual message content to be sent
   - Can be a string, bytes, or numeric type
   - If a string is provided, it's encoded as UTF-8 bytes

3. **qos**: Quality of Service level (0, 1, or 2)
   - QoS 0: At most once delivery (fire and forget)
   - QoS 1: At least once delivery (acknowledged delivery)
   - QoS 2: Exactly once delivery (assured delivery)
   - Higher QoS levels involve more handshaking and overhead

4. **retain**: Boolean flag for message retention
   - False: Normal message that is not retained
   - True: Message is stored by the broker and sent to future subscribers
   - Only one retained message is stored per topic

Our tests confirmed that the published message was successfully received by the subscribing client.

### 5. Make two subscriptions with wildcards

In `task5_wildcard_subscriptions.py`, we implemented and tested two types of wildcard subscriptions:

1. **Single-level wildcard (+)**: We subscribed to `Sensors/+/Temperature`
   - Represents a single level in the topic hierarchy
   - Matches exactly one topic level at the position of the wildcard
   - Example matches:
     - "Sensors/Living/Temperature"
     - "Sensors/Kitchen/Temperature"
   - Non-matches:
     - "Sensors/Bathroom/Humidity" (different final level)
     - "Sensors/Garden/Light/Level" (more levels)
     - "Weather/Outside/Temperature" (different first level)

2. **Multi-level wildcard (#)**: We subscribed to `Sensors/#`
   - Represents multiple levels in the topic hierarchy
   - Must be the last character in the topic filter
   - Matches any number of levels in the topic (including zero)
   - Example matches:
     - "Sensors/Living/Temperature"
     - "Sensors/Kitchen/Temperature"
     - "Sensors/Bathroom/Humidity"
     - "Sensors/Garden/Light/Level"
   - Non-matches:
     - "Weather/Outside/Temperature" (different first level)

Our testing showed that the single-level wildcard subscriber received only messages that matched its pattern (exactly one level between "Sensors" and "Temperature"), while the multi-level wildcard subscriber received all messages with the "Sensors" prefix, regardless of subsequent levels.

### 6. Create a client with clean_session=FALSE and QoS 1

In `task6_persistent_session_qos1.py`, we tested a persistent session with clean_session=FALSE and QoS 1:

**Observation**: The subscriber received all 20 messages after reconnection.

**Explanation**:
1. When a client connects with clean_session=FALSE, the broker creates a persistent session.
2. The session stores:
   - Client subscriptions
   - Messages with QoS > 0 that arrive when the client is disconnected
3. When we subscribed with QoS 1, the broker guaranteed at-least-once delivery.
4. While disconnected, the broker queued the 20 QoS 1 messages for our client.
5. Upon reconnection with the same client ID and clean_session=FALSE:
   - The broker recognized the returning client
   - The existing session was resumed
   - Stored subscriptions were still active
   - Queued messages were delivered to the client

This behavior demonstrates the reliability features of MQTT:
- Persistent sessions maintain client state across disconnections
- QoS 1 ensures messages are delivered even when clients are temporarily offline
- Client IDs must remain consistent to identify the same client across connections

### 7. Create a client with clean_session=TRUE and QoS 1

In `task7_non_persistent_session.py`, we tested a non-persistent session with clean_session=TRUE and QoS 1:

**Observation**: The subscriber did NOT receive any of the 20 messages sent while it was disconnected.

**Explanation**:
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

The difference between this and Task 6 illustrates the impact of the clean_session flag:
- With clean_session=TRUE: Client state is transient, lasting only for the current connection
- With clean_session=FALSE: Client state persists across disconnections, allowing message queuing

### 8. Create a client with clean_session=FALSE, QoS 0 subscription, and QoS 2 publishing

In `task8_persistent_mixed_qos.py`, we tested a persistent session with clean_session=FALSE, QoS 0 subscription, and QoS 2 publishing:

**Observation**: The subscriber did NOT receive any of the 20 messages sent while it was disconnected, despite using clean_session=FALSE.

**Explanation**:
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
   - Messages are effectively "downgraded" to match the subscription QoS

This demonstrates an important concept in MQTT: message delivery guarantees are limited by the lowest QoS in the chain (publication QoS or subscription QoS).

## Conclusion

This solution demonstrates various aspects of the MQTT protocol, focusing on:

1. Client creation and connection
2. Message publishing and subscription
3. Topic wildcards
4. Session persistence
5. Quality of Service levels and their implications

The code is modular, well-documented, and provides extensive explanations of the observed behaviors, making it a comprehensive reference for understanding MQTT functionality. 