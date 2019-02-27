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
    from riot_pal import DutShell
except ImportError as e:
    raise ImportError(e)

class PeriphCANIf(DutShell):
    """Interface to the a node with can firmware."""
    FW_ID = 'periph_can'
    DEFAULT_CAN_IF = 0
    DEFAULT_CAN_CID = 100

    def can_send(self, _if=DEFAULT_CAN_IF, cid=DEFAULT_CAN_CID, frame=DEFAULT_CAN_FRAME):
        cmd_to_send = 'test_can send {} {} {}'.format(_if, cid, ' '.join(frame))
        return self.send_cmd(cmd_to_send)

    def can_read_bytes(self, dev=DEFAULT_CAN_IF, rx_thread_nb=0, can_id=0):
        cmd_to_send = 'test_can recv {} {} {} {}'.format(dev, rx_thread_nb, 10000000, str(hex(can_id)))
        return self.send_cmd(cmd_to_send)

    def can_get_list(self):
        cmd_to_send = 'test_can list'
        return self.send_cmd(cmd_to_send)

    def can_only_get_output(self, send_cmd):
        response = self._read()
        cmd_info = {'cmd': send_cmd, 'data': None}
        while response != '':
            if self.COMMAND in response:
                cmd_info['msg'] = response.replace(self.COMMAND, '')
                cmd_info['cmd'] = cmd_info['msg'].replace('\n', '')

            if self.SUCCESS in response:
                clean_msg = response.replace(self.SUCCESS, '')
                cmd_info['msg'] = clean_msg.replace('\n', '')
                cmd_info['result'] = self.RESULT_SUCCESS
                cmd_info['data'] = self._try_parse_data(cmd_info['msg'])
                break

            if self.ERROR in response:
                clean_msg = response.replace(self.ERROR, '')
                cmd_info['msg'] = clean_msg.replace('\n', '')
                cmd_info['result'] = self.RESULT_ERROR
                break
            response = self._read()

        if response == '':
            cmd_info['result'] = self.RESULT_TIMEOUT
            logging.debug(self.RESULT_TIMEOUT)
        return cmd_info

    def mcu_reboot(self):
        return self.send_cmd('reboot')