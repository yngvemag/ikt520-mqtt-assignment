# MQTT Assignment

This repository contains a solution for the IKT520 MQTT Mandatory Assignment (MA-02), implementing various aspects of the MQTT protocol using the `paho-mqtt` library in Python.

## Prerequisites

1. Install Docker if you haven't already (<https://docs.docker.com/get-docker/>)

2. Run EMQX broker using Docker:

```bash
docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx/emqx
```

- Web interface available at: <http://localhost:18083> (default credentials admin/public)
- MQTT broker available on port 1883

## Setup Instructions

1. Install the required Python package:

```bash
pip install paho-mqtt
```

## Running the Solution

The solution is implemented in a single Python script that handles all the required tasks:

```bash
python ma-02-solution.py
```

This will execute all tasks sequentially, demonstrating MQTT protocol features through a series of experiments.

## Solution Overview

The solution implements the following MQTT tasks:

1. **Client Creation** - Creating publisher and subscriber clients
2. **Publisher Connection** - Connecting to broker and examining CONNACK response
3. **Subscriber Connection** - Connecting and subscribing to topics
4. **Message Publishing** - Publishing messages to specific topics
5. **Wildcard Subscriptions** - Testing single-level (+) and multi-level (#) wildcards
6. **Persistent Session with QoS 1** - Testing message delivery with persistent sessions
7. **Non-persistent Session with QoS 1** - Testing message delivery without session persistence
8. **Mixed QoS with Persistent Session** - Examining QoS interactions with session persistence

## Solution Files

- `ma-02-solution.py` - Main solution script implementing all tasks
- `MA-02-answer.md` - Detailed answers to all assignment questions with code examples

## Resources & References

This project utilizes the following resources:

1. **Paho MQTT Python Client Library**
   - Package: [paho-mqtt on PyPI](https://pypi.org/project/paho-mqtt/)
   - Examples: [Official Paho MQTT Python Examples](https://github.com/eclipse-paho/paho.mqtt.python/tree/master/examples)
   - Used for implementing MQTT client functionality

2. **EMQX Broker**
   - Open-source MQTT broker
   - Used as the message broker for this project
   - Runs in Docker container for easy setup and deployment

## Detailed Documentation

For detailed explanations of each task and implementation details, please refer to the [solution/README.md](./solution/README.md).
