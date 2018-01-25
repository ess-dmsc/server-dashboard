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
        "file_attributes": {
            "file_name": args.filename
        },
        "nexus_structure": {
            "attributes": {
                "title": "test"
            },
            "children": [{
                "type": "group",
                "name": "entry-01",
                "attributes": {
                    "NX_class": "NXentry"
                },
                "children": [{
                    "type": "group",
                    "name": "amor",
                    "attributes": {
                        "NX_class": "NXinstrument"
                    },
                    "children": [{
                        "type": "group",
                        "name": "events",
                        "attributes": {
                            "NX_class": "NXevent_data"
                        },
                        "children": [{
                            "type": "stream",
                            "stream": {
                                "topic": "C-SPEC_detector",
                                "source": "c_spec_data",
                                "writer_module": "ev42",
                                "type": "uint32",
                            }
                        }]
                    }, {
                        "type": "group",
                        "name": "dimetix",
                        "attributes": {
                            "NX_class": "NXevent_data"
                        },
                        "children": [{
                            "type": "stream",
                            "stream": {
                                "topic": "amor_sim",
                                "source": "SQ:AMOR:DIMETIX:DIST",
                                "writer_module": "f142",
                                "type": "double",
                            }
                        }]
                    }]
                }]
            }]
        }
    }

    print("Sending command to " + args.broker + ":")
    print(cmd)

    json_cmd = bytes(json.dumps(cmd), 'ascii')
    future = p.send("kafka-to-nexus.command", json_cmd)
    future.get(timeout=1)  # Wait for message to be sent or timeout.
