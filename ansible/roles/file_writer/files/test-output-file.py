#!/opt/dm_group/python-virtualenv/bin/python

"""A sample output NeXus file check.

Return codes:
0 -- success
1 -- differences found
2 -- error
"""

import argparse
import sys
import h5py


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('filename')
    args = arg_parser.parse_args()

    try:
        f = h5py.File(args.filename, mode='r')
    except:
        print('ERROR: exception reading file ' + args.filename)
        sys.exit(2)

    dimetix_values = f['entry-01/amor/dimetix/value'][0:3]
    if not (dimetix_values == [0, 1, 2]).all():
        print('ERROR: dimetix values differ from expected')
        print('  Values in file: ' + str(dimetix_values))
        sys.exit(1)

    detector_ids = f['entry-01/amor/events/detector_id'][0:3]
    if not (detector_ids == [387, 2102, 2036]).all():
        print('ERROR: detector_id values differ from expected')
        print('  Values in file: ' + str(detector_ids))
        sys.exit(1)

    print('Expected output found in files.')
    sys.exit(0)
