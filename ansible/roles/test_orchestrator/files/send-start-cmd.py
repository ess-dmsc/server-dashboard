import argparse
import json
import kafka


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Send commands to kafka-to-nexus.')
    arg_parser.add_argument('broker')
    arg_parser.add_argument('filename')
    args = arg_parser.parse_args()

    p = kafka.KafkaProducer(bootstrap_servers=args.broker)

    cmd = {
        "cmd": "FileWriter_new",
        "broker": args.broker,
        "job_id": "integration-test",
        "streams": [
            {
                "topic": "C-SPEC_detector",
                "source": "c_spec_data",
                "nexus_path": "/entry-01/amor/events"
            },
            {
                "topic": "amor_sim",
                "source": "SQ:AMOR:DIMETIX:DIST",
                "nexus_path": "/entry-01/amor/dimetix"
            }
        ],

        "nexus_structure": {
            "title": "test",
            "entry-01": {
                "NX_class": "NXentry",
                "amor": {
                    "NX_class": "NXinstrument",
                    "events": {
                        "NX_class": "NXevent_data"
                    },
                    "dimetix": {
                        "NX_class": "NXevent_data"
                    }
                }
            }
        },

        "file_attributes": {
            "file_name": args.filename
        }
    }

    print("Sending command to " + args.broker + ":")
    print(cmd)

    json_cmd = bytes(json.dumps(cmd), 'ascii')
    future = p.send("kafka-to-nexus.command", json_cmd)
    future.get(timeout=1)  # Wait for message to be sent or timeout.
