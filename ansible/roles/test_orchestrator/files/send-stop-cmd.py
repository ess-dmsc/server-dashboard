import argparse
import json
import kafka


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Send stop command to kafka-to-nexus.')
    arg_parser.add_argument('broker')
    args = arg_parser.parse_args()

    p = kafka.KafkaProducer(bootstrap_servers=args.broker)

    cmd = {
        "cmd": "FileWriter_exit"
    }

    print("Sending command to " + args.broker + ":")
    print(cmd)

    json_cmd = bytes(json.dumps(cmd), 'ascii')
    future = p.send("kafka-to-nexus.command", json_cmd)
    future.get(timeout=1)  # Wait for message to be sent or timeout.
