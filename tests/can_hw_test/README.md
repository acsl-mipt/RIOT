How To Run
==========
Test only available for Linux and some STM32 devices. Check Makefile for boards with CAN device.

Prerequsites
============
CAN-USB converter like this one. [PEAK == CAN FD](https://www.peak-system.com/PCAN-USB-FD.365.0.html?&L=1).

### Example Test With STM32F413ZH
1. Configure the CAN-USB to get a can interface working, for this use Google my friend!
2. Flash this conn_can_hw_test FW on your DUT
3. Connect DUT can port to your USB-CAN converter. Respect CANH, CANL and ground connections.
4. 
5. Run the test.py from the conn_can/tests directory (with options)</br>
`python test.py` for basic tests with autoconnect</br>
`python3 test.py` for python 3</br>
`python test.py --log=DEBUG` to see all debug messages</br>
`python test.py --dut_port="/dev/ttyACM0"` to specify the port</br>
`python test.py --log=DEBUG --dut_port="/dev/ttyACM0" --dut_baud=9600 --bpt_port="/dev/ttyACM1" > nucleo-f401_test.txt` for all the fix'ns</br>

Flags
==========
--log=DEBUG -> allows for debug output</br>
--dut_port -> the port name of the DUT</br>
--dut_baud -> the baud rate of the DUT</br>
--bpt_port -> the port name of the BPT

Notes
==========
- If no serial connection to the BPT the test should still be able to run, it just will not be able to reset.
- Connect the SDA, SCL and if possible the DUT reset pin.
- Autoconnect *may* work if no ports are specified.
- Default baud rate is 115200
