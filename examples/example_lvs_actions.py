__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import lvs
import time

if __name__ == '__main__':
    lvs_instance = lvs.LVSDispatcher()
    # lvs_instance.connect('192.168.250.115', 'LVS-95XX', 'LVS-95XX', 'LVS-95XX')
    lvs_instance.connect()
    count = lvs_instance.record_count()
    print(count)
    # for i in range(count):
    #     text = lvs_instance.symbol_text(i + 1)
    #     if text is not None:
    #         print(text)
    #
    # for i in range(count):
    #     text = lvs_instance.overall_grade(i + 1)
    #     if text is not None:
    #         print(text)

    for i in range(count):
        text = lvs_instance.get_parameter(i + 1, ['Overall grade', 'Decoded text'])
        if text is not None:
            print(text)

    # records = lvs_instance.get_previous_n_records(5)
    # for record in records:
    #     print(record)

