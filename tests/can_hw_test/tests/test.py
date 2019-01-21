#!/usr/bin/env python3

# Copyright (C) 2019 Javier FILEIV <javier.fileiv@gmail.com>
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.

# Based on Kevin Weiss <kevin.weiss@haw-hamburg.de> test files. Thank you! :)
"""
Test cases:
1)List all can interfaces on the board
2)Send random values to the board can iface using USB-CAN converter.
3receive random generated CAN values
4)Send random values and check result, reboot board, send another values an check results.
5)Receive random values and check results, reboot board, receive another random values and check results
"""

import argparse
import errno
import logging
import random
import string
import can
import random
import string
import time

from periph_can_if import PeriphCANIf

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def kwexpect(val1, val2, level="WARN"):
    """A poor mans pexpect"""
    res = level
    try:
        if isinstance(val1, str) and isinstance(val2, str):
            if val1.lower() == val2.lower():
                res = "PASS"
        elif isinstance(val1, list):
            if len(val1) == 0:
                return [res, val1, val2]
            err = False
            if len(val1) != len(val2):
                err = True
            for test_index in range(0, len(val1)):
                if val1[test_index] != val2[test_index]:
                    err = True
            if err is False:
                res = "PASS"
            else:
                return [level, val1, val2]
        elif (val1 == val2) or (val1 is val2):
            res = "PASS"
    except TypeError:
        res = 'TypeError'
    except Exception as exc:
        res = 'Unknown Error'
        logging.debug(exc)

    return [res, val1, val2]


class TestParam:
    """A poor mans way to store test params because I didn't know about dict"""
    test_num = None
    action = None
    expect_res = None


class Test:
    name = ""
    desc = ""
    notes = ""
    result = ""
    cmd_log = None
    num = 0

    def __init__(self, name, desc, cmd_list):
        self.name = name
        self.desc = desc
        self.cmd_log = cmd_list
        self.result = "PASS"

    def run_test(self, action, ex_res=None, ex_data=None,
                 res_lvl="WARN", data_lvl="WARN"):
        tp = TestParam()
        tp.test_num = self.num
        tp.action = action
        if 'data' not in action:
            tp.action['data'] = []
        tp.expect_res = list()
        if ex_res is not None:
            tp.expect_res.append(kwexpect(action['result'], ex_res, res_lvl))
            if tp.expect_res[-1][0] == "FAIL":
                self.result = tp.expect_res[-1][0]
            if tp.expect_res[-1][0] == "WARN" and self.result != "FAIL":
                self.result = tp.expect_res[-1][0]
        if ex_data is not None:

            tp.expect_res.append(kwexpect(action['data'], ex_data, data_lvl))
            if tp.expect_res[-1][0] == "FAIL":
                self.result = tp.expect_res[-1][0]
            if tp.expect_res[-1][0] == "WARN" and self.result != "FAIL":
                self.result = tp.expect_res[-1][0]
        self.num += 1
        self.cmd_log.append(tp)
        return action['data']

    def skip_test(self, skipped_fxn):
        tp = TestParam()

        tp.test_num = self.num
        self.num += 1
        tp.action = skipped_fxn
        tp.expect_res = "SKIP"
        self.cmd_log.append(tp)

    def manual_test(self, action):
        tp = TestParam()

        tp.test_num = self.num
        self.num += 1
        tp.action = action
        tp.expect_res = "PASS"
        self.cmd_log.append(tp)


def setup_test(can, linux_can_if = None):
#   do common tasks before each test
    logging.info("Reset MCU")
    can.mcu_reboot()
    if(linux_can_if is not None):
#    configure iface baudrate
        pass

def get_int_string_list(len=1):
    l = list()
    for i in range(len):
        l.append(random_with_N_digits(2))
    return l

def get_hexa_string_list(len=1):
    total_len = 2 * len
    hexa_str = ''.join(random.choice(string.hexdigits[:16]) for n in range(total_len))
    l = list()
    n = 0
    while n < total_len:
        l.append((hexa_str[n]+hexa_str[n+1]))
        n += 2
    return l
    
def send_random_msg(can_dev, linux_can_bus):
    cmd_log = list()
    t = Test('send random data test fromm device to linux PC',
             'Sends 8 random bytes (2 times) and check what we get, using the linux interface',
             cmd_log)
    
    
    '''2047 is 0x7FF (max can id number) in decimal'''
    setup_test(can_dev)

    can_if_on_board = 1
    can_id = hex(random.randrange(0, 2047, 1))
    frame_1 = get_hexa_string_list(8)
    t.run_test(can_dev.can_send(can_if_on_board, can_id, frame_1), "Success", [' '.join(frame_1)+' '])
    
    time.sleep(0.2)
    message = linux_can_bus.recv(1.0)  # Timeout in seconds.
    int_can_id = int(can_id, 16)
    print("Send ID={}, RX ID={}".format(message.arbitration_id, int_can_id))
    assert message.arbitration_id == int_can_id, 'Sent and received CID are not equal'

    sent_to_device = bytearray(bytes.fromhex(''.join(frame_1)))
    received_on_linux = message.data
    assert sent_to_device == received_on_linux, 'Sent and received frame are not equal'
    
    can_id = hex(random.randrange(0, 2047, 1))
    frame_2 = get_hexa_string_list(8)
    t.run_test(can_dev.can_send(can_if_on_board, can_id, frame_2), "Success", [' '.join(frame_2)+' '])
    
    time.sleep(0.2)
    message = linux_can_bus.recv(1.0)  # Timeout in seconds.
    int_can_id = int(can_id, 16)
    assert message.arbitration_id == int_can_id, 'Sent and received CID (2nd round) are not equal'

    sent_to_device = bytearray(bytes.fromhex(''.join(frame_2)))
    received_on_linux = message.data
    assert sent_to_device == received_on_linux, 'Sent and received 2nd frame are not equal'

    return t

def receive_random_msg(can_dev, linux_can_bus):
    cmd_log = list()
    t = Test('Receive random data test fromm linux PC to device',
             'Receives 8 random bytes (2 times) and check what we get, using the linux interface',
             cmd_log)
    
    setup_test(can_dev)

    can_if_on_board = 1
    rx_thread_nb = 0

    can_id = random.randrange(0, 2457, 1)
    frame_1 = get_int_string_list(8)
    msg = can.Message(arbitration_id=can_id,
                      data=frame_1,
                      extended_id=False)

    linux_can_bus.send(msg)
    t.run_test(can_dev.can_read_bytes(can_if_on_board, rx_thread_nb,
                                      can_id), "Success", frame_1)
    
    return t

def interfaces_list_test(can_dev):
    cmd_log = list()
    t = Test('interfaces list test',
             'Tests DUT prints a list with 3 can interfaces',
             cmd_log)
    
    setup_test(can_dev)
    
    t.run_test(can_dev.can_get_list(), "Success", [0, 1, 2])
    
    return t
    

def print_full_result(test):
    """Print full test results."""
    print('==================================================================')
    print('Name:\t\t' + test.name)
    print('Desc:\t\t' + test.desc)
    print('Result:\t\t' + test.result)
    print('Notes:\t\t' + test.notes)
    print('------------------------------------------------------------------')
    for test_param in test.cmd_log:
        print('Test Number:\t***%d***' % test_param.test_num)
        if not isinstance(test_param.action, str):
            print('Command:\t' + test_param.action['cmd'])
            if 'msg' in test_param.action:
                print('Message:\t' + test_param.action['msg'])
            if test_param.action['data'] is not None:
                print('Data:\t\t[%s]' % ', '.join(map(str,
                                                      test_param.action['data'])))
            print('Result:\t\t' + test_param.action['result'])
        else:
            print('Command:\t' + test_param.action)
        if isinstance(test_param.expect_res, str):
            print('Expect Result:\t%s' % (test_param.expect_res))
        else:
            for res in test_param.expect_res:
                print('Expect Result:\t%s (%s/%s)' % (res[0], res[1], res[2]))
        print('----------')


def print_results(test_list):
    """Print brief test results."""
    print('')
    print('==================================================================')
    for test in test_list:
        print('Name:\t\t' + test.name)
        print('Result:\t\t' + test.result + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log",
                        help='Set the log level (DEBUG, INFO, WARN)',
                        default="WARN",
                        type=str)
    parser.add_argument("--riot_port",
                        help='Port for device under test', 
                        default="/dev/ttyUSB0",
                        type=str)
    parser.add_argument("--riot_can_if",
                        help='Selected CAN interface on RIOT',
                        type=int,
                        default=1)
    parser.add_argument("--linux_can_if",
                        help='USB-CAN converter Linux Interface', 
                        default="can0",
                        type=str)

    
    args = parser.parse_args()    
    
    linux_can_bus = can.interface.Bus(channel='can0', bustype='socketcan_native', bitrate=500000)
    
    if args.log is not None:
        loglevel = args.log
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
        logging.basicConfig(level=loglevel)

    logging.debug('Choosing {} riot port, riot can interface {}, linux can ' \
    'device: {}'.format(args.riot_port,
                         args.riot_can_if, args.linux_can_if))
    can_dut = PeriphCANIf(port=args.riot_port)

    
    logging.info('Starting Test periph_can')
    test_list = list()
    test_list.append(interfaces_list_test(can_dut))
    print_full_result(test_list[-1])
    test_list.append(send_random_msg(can_dut, linux_can_bus))
    print_full_result(test_list[-1])
    test_list.append(receive_random_msg(can_dut, linux_can_bus))
    print_full_result(test_list[-1])
    
# #     test_list.append(register_read_test(bpt, uart, args.dut_uart))
# #     print_full_result(test_list[-1])
# 
    print_results(test_list)


if __name__ == "__main__":
    main()
