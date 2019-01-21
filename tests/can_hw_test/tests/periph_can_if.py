# Copyright (C) 2018 Kevin Weiss <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the GNU Lesser
# General Public License v2.1. See the file LICENSE in the top level
# directory for more details.


"""@package PyToAPI
This module handles parsing of information from RIOT periph_can test.
"""
import logging
import unittest
import argparse

try:
    import socket, sys
    from riot_pal import DutShell
except ImportError as e:
    raise ImportError(e)

# 2019-01-11 08:16:41,510 - INFO # test_can list
# 2019-01-11 08:16:41,512 - INFO # test_can send ifnum can_id [B1 [B2 [B3 [B4 [B5 [B6 [B7 [B8]]]]]]]]
# 2019-01-11 08:16:41,515 - INFO # test_can recv ifnum user_id timeout can_id1 [can_id2..can_id16]
# 2019-01-11 08:16:41,516 - INFO # test_can close user_id
# 2019-01-11 08:16:41,518 - INFO # test_can bind_isotp ifnum user_id source_id dest_id
# 2019-01-11 08:16:41,520 - INFO # test_can send_isotp user_id [B1 [.. [ Bn ]]]
# 2019-01-11 08:16:41,522 - INFO # test_can recv_isotp user_id timeout
# 2019-01-11 08:16:41,523 - INFO # test_can close_isotp user_id
# 2019-01-11 08:16:41,524 - INFO # test_can get_filter ifnum
# 2019-01-11 08:16:41,525 - INFO # test_can set_bitrate ifnum bitrate [sample_point]
# 2019-01-11 08:16:41,525 - INFO # test_can get_bitrate ifnum
# 2019-01-11 08:16:41,526 - INFO # test_can get_counter ifnum
# 2019-01-11 08:16:41,526 - INFO # test_can power_up ifnum
# 2019-01-11 08:16:41,527 - INFO # test_can power_down ifnum

class PeriphCANIf(DutShell):
    """Interface to the a node with can firmware."""
    FW_ID = 'periph_can'
    DEFAULT_CAN_IF = 0
    DEFAULT_CAN_CID = 100
    DEFAULT_CAN_FRAME = [0x00, 0x01, 0x02, 0x35, 0x55, 0x22]


    def can_send(self, _if=DEFAULT_CAN_IF, cid=DEFAULT_CAN_CID, frame=DEFAULT_CAN_FRAME):
        cmd_to_send = 'test_can send {} {} {}'.format(_if, cid, ' '.join(frame))
        print(cmd_to_send)
        return self.send_cmd(cmd_to_send)

    def can_read_bytes(self, dev=DEFAULT_CAN_IF, rx_thread_nb=0, can_id=0):
        cmd_to_send = 'test_can recv {} {} {} {}'.format(dev, rx_thread_nb, 10000000, str(hex(can_id)))
        print(cmd_to_send)
        return self.send_cmd(cmd_to_send)

    def can_get_list(self):
        cmd_to_send = 'test_can list'
        return self.send_cmd(cmd_to_send)

    
    def mcu_reboot(self):
        return self.send_cmd('reboot')

# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-i', '--interface', type=str, help='interface name (e.g. vcan0)')
#     parser.add_argument('-ci', '--cob_id', type=str, help='hexadecimal COB-ID (e.g. 10a)')
#     parser.add_argument('-b', '--body', type=str, nargs='?', default='',
#       help='hexadecimal msg body up to 8 bytes long (e.g. 00af0142fe)')
#     parser.add_argument('-eid', '--extended-id', action='store_true', default=False,
#       help='use extended (29 bit) COB-ID')
# 
# 
#     return parser.parse_args()
# 
# def main():
#     """Test for CAN."""
#     logging.getLogger().setLevel(logging.DEBUG)
# 
#     args = parse_args()    
# 
#     try:
#         pc_can = CANSocket(interface = args.interface)
#         riot_can = PeriphCANIf(port='/dev/ttyUSB0', baudrate=115200)
#         
#         logging.debug(riot_can.can_get_available_list())
#         cmds = riot_can.get_command_list()
#         logging.debug("======================================================")
#         for cmd in cmds:
#             cmd()
#             logging.debug("--------------------------------------------------")
#         logging.debug("======================================================")
#     except Exception as exc:
#         logging.debug(exc)
# 
# 
# if __name__ == "__main__":
#     main()
