This uses SSHamilton's code to send RS232 commands to program the [TestEquity 115 Temperature Chamber](https://www.testequity.com/UserFiles/documents/pdfs/115Aman.pdf).
Notes:
1. The actual chamber temperature reading is Modbus register 100 (Input 1 Value).
1. The static temperature set point is Modbus register 300 (Set Point 1).
1. The temperature set point during a profile is Modbus register 4122 (Set Point 1, Current Profile Status).
1 The decimal points are implied. For example, 1005 is actually 100.5 and -230 is -23.0.
