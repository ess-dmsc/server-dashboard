#!/opt/dm_group/python-virtualenv/bin/python

import argparse
import json
import kafka


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Send stop command to kafka-to-nexus.')
    arg_parser.add_argument('broker')
    args = arg_parser.parse_args()

    p = kafka.KafkaProducer(bootstrap_servers=args.broker)

    cmd = { "cmd": "FileWriter_exit" }

    print("Sending command to " + args.broker + ":")
    print(cmd)

    p.send("kafka-to-nexus.command", json.dumps(cmd))
