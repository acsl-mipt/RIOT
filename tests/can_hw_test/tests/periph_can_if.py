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
    from linux_can import CANSocket
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
        """Get access to the I2C bus."""
        return self.send_cmd('test_can send {} {} {}'.format(_if, cid, frame))

    def can_release(self, dev=DEFAULT_CAN_IF):
        """Release to the I2C bus."""
#         return self.send_cmd('can_release {}'.format(dev))

    def can_read_reg(self, dev=DEFAULT_CAN_IF, addr=0, reg=0,
                     flag=0):
        """Read byte from register."""
#         return self.send_cmd('can_read_reg'
#                              ' {} {} {} {}'.format(dev, addr, reg, flag))

    def can_read_regs(self, dev=DEFAULT_CAN_IF, addr=0, reg=0,
                      leng=0, flag=0):
        """Read bytes from registers."""
#         return self.send_cmd('can_read_regs'
#                              ' {} {} {} {} {}'.format(dev, addr, reg,
#                                                       leng, flag))

    def can_read_byte(self, dev=DEFAULT_CAN_IF, addr=0, flag=0):
        """Read byte from the I2C device."""
#         return self.send_cmd('can_read_byte {} {} {}'.format(dev, addr, flag))

    def can_read_bytes(self, dev=DEFAULT_CAN_IF, addr=0, leng=0,
                       flag=0):
        """Read bytes from the I2C device."""
#         return self.send_cmd('can_read_bytes'
#                              ' {} {} {} {}'.format(dev, addr, leng, flag))

    def can_write_reg(self, dev=DEFAULT_CAN_IF, addr=0, reg=0,
                      data=0, flag=0):
        """Write byte to the I2C device."""
#         if isinstance(data, list):
#             data = data[0]
#         return self.send_cmd('can_write_reg'
#                              ' {} {} {} {} {}'.format(dev, addr, reg,
#                                                       data, flag))

    def can_write_regs(self, dev=DEFAULT_CAN_IF, addr=0, reg=0,
                       data=0, flag=0):
        """Write byte to register."""
#         stri = ' '.join(str(x) for x in data)
#         return self.send_cmd('can_write_regs'
#                              ' {} {} {} {} {}'.format(dev, addr, reg, flag, stri))

    def can_write_byte(self, dev=DEFAULT_CAN_IF, addr=0, data=0,
                       flag=0):
        """Write bytes to registers."""
#         if isinstance(data, list):
#             data = data[0]
#         return self.send_cmd('can_write_byte'
#                              ' {} {} {} {}'.format(dev, addr, data, flag))

    def can_write_bytes(self, dev=DEFAULT_CAN_IF, addr=0,
                        data=0, flag=0):
        """Write bytes to registers."""
#         stri = ' '.join(str(x) for x in data)
#         return self.send_cmd('can_write_bytes'
#                              ' {} {} {} {}'.format(dev, addr, flag, stri))

    def can_get_devs(self):
        """Gets amount of supported can devices."""
        return self.send_cmd('can_get_devs')

    def can_get_list(self):
        """Get the id of the fw."""
        return self.send_cmd('test_can list')

    def get_command_list(self):
        """List of all commands."""
        cmds = list()
        cmds.append(self.can_get_devs)
        cmds.append(self.can_get_available_list)
        cmds.append(self.can_send)
        cmds.append(self.can_read_reg)
        cmds.append(self.can_read_regs)
        cmds.append(self.can_read_byte)
        cmds.append(self.can_read_bytes)
        cmds.append(self.can_write_reg)
        cmds.append(self.can_write_regs)
        cmds.append(self.can_write_byte)
        cmds.append(self.can_write_bytes)
        cmds.append(self.can_release)
        return cmds
    
    def mcu_reboot(self):
        return self.send_cmd('reboot')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interface', type=str, help='interface name (e.g. vcan0)')
    parser.add_argument('-ci', '--cob_id', type=str, help='hexadecimal COB-ID (e.g. 10a)')
    parser.add_argument('-b', '--body', type=str, nargs='?', default='',
      help='hexadecimal msg body up to 8 bytes long (e.g. 00af0142fe)')
    parser.add_argument('-eid', '--extended-id', action='store_true', default=False,
      help='use extended (29 bit) COB-ID')


    return parser.parse_args()

def main():
    """Test for CAN."""
    logging.getLogger().setLevel(logging.DEBUG)

    args = parse_args()    

    try:
        pc_can = CANSocket(interface = args.interface)
        riot_can = PeriphCANIf(port='/dev/ttyUSB0', baudrate=115200)
        
        logging.debug(riot_can.can_get_available_list())
        cmds = riot_can.get_command_list()
        logging.debug("======================================================")
        for cmd in cmds:
            cmd()
            logging.debug("--------------------------------------------------")
        logging.debug("======================================================")
    except Exception as exc:
        logging.debug(exc)


if __name__ == "__main__":
    main()
