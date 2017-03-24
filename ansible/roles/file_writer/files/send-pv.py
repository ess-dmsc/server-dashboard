#!/opt/dm_group/python-virtualenv/bin/python

import argparse
import json
import kafka


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Send commands to kafka-to-nexus.')
    arg_parser.add_argument('broker')
    arg_parser.add_argument('topic')
    arg_parser.add_argument('source')
    arg_parser.add_argument('file')
    args = arg_parser.parse_args()

    p = kafka.KafkaProducer(bootstrap_servers=args.broker)

    cmd = {
        "cmd": "FileWriter_new",

        "broker": args.broker,

        "streams": [
            {
                "topic": args.topic,
                "source": args.source,
                "nexus_path": "/entry-01/amor/dimetix"
            }
        ],

        "nexus_structure": {
            "title": "test",
            "entry-01": {
                "NX_class": "NXentry",
                "amor": {
                    "NX_class": "NXinstrument",
                    "dimetix": {
                        "NX_class": "NXevent_data"
                    }
                }
            }
        },

        "file_attributes": {
            "file_name": args.file
        }
    }

    print("Sending command to " + args.broker + ":")
    print(cmd)

    p.send("kafka-to-nexus.command", json.dumps(cmd))
