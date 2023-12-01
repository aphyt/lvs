__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import lvs
import time

if __name__ == '__main__':
    lvs_instance = lvs.LVSDispatcher()
    lvs_instance.connect('192.168.250.115', 'LVS-95XX', 'LVS-95XX', 'LVS-95XX')
    count = lvs_instance.record_count()
    records = lvs_instance.get_previous_n_records(5)
    for record in records:
        print(record)

    lvs_instance.upper_read_index = count
    try:
        while True:
            records = lvs_instance.read_upper_records()
            for record in records:
                print(record)
            time.sleep(1.0)
    except KeyboardInterrupt:
        pass

