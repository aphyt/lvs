__author__ = 'Joseph Ryan'
__license__ = "GPLv2"
__maintainer__ = "Joseph Ryan"
__email__ = "jr@aphyt.com"

import lvs

if __name__ == '__main__':
    lvs_instance = lvs.LVSDispatcher()
    lvs_instance.connect('192.168.250.115', 'LVS-95XX', 'LVS-95XX', 'LVS-95XX')
    print(lvs_instance.record_count())
