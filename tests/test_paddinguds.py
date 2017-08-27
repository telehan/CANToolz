import time
import unittest

from cantoolz.engine import CANSploit


class PaddingUds(unittest.TestCase):

    def tearDown(self):
        self.CANEngine.stop_loop()
        self.CANEngine = None
        print("stopped")

    def test_replay_padding(self):
        self.CANEngine = CANSploit()
        self.CANEngine.load_config("tests/configurations/test_8.py")
        self.CANEngine.start_loop()
        time.sleep(1)
        self.CANEngine.call_module(1, "s")
        time.sleep(2)
        index = 3
        ret = self.CANEngine.call_module(index, "p")
        print(ret)
        _bodyList = self.CANEngine._enabledList[index][1]._bodyList
        self.assertTrue(len(_bodyList) == 20, "Should be 20 groups of packets")
        self.assertTrue(1790 in _bodyList, "1790 should be there")
        self.assertTrue(1791 in _bodyList, "1791 should be there")
        self.assertTrue(1792 in _bodyList, "1792 should be there")
        self.assertTrue((8, bytes.fromhex("02010d4141414141"), "USBTin", False) in _bodyList[1792], "020902 as packet should be there")
        self.assertTrue((8, bytes.fromhex("062f030703000041"), "USBTin", False) in _bodyList[1792],
                        "062f0307030000 as packet should be there")
        self.assertTrue((8, bytes.fromhex("0209024141414141"), "USBTin", False) in _bodyList[1792], "020901 as packet should be there")
        self.assertTrue((8, bytes.fromhex("02010d4141414141"), "USBTin", False) in _bodyList[1790], "02010d as packet should be there")
        self.assertFalse((8, bytes.fromhex("0209044141414141"), "USBTin", False) in _bodyList[1791],
                         "020904 as packet should not be there")

        self.CANEngine.call_module(2, "r")
        time.sleep(2)
        ret = self.CANEngine.call_module(3, "p")
        print(ret)
        _bodyList = self.CANEngine._enabledList[index][1]._bodyList
        ret = self.CANEngine.call_module(3, "a")
        print(ret)
        self.assertTrue(1 == _bodyList[1800][(
            8,
            bytes.fromhex("1014490201314731"),
            "USBTin",
            False
        )], "Should be 1 packed replayed")

        self.assertTrue(0 <= ret.find("ASCII: .1G1ZT53826F109149"), "TEXT should be found in response")
        self.assertTrue(0 <= ret.find("Response: 00"), "TEXT should be found in response")
        self.assertTrue(0 <= ret.find("ASCII: I..1G1ZT53826F109149"), "TEXT should be found in response")
        self.assertTrue(0 <= ret.find("DATA: 4902013147315a54353338323646313039313439"), "TEXT should be found in response")
        self.assertTrue(0 <= ret.find("ID: 0x701 Service: 0x2f Sub: 0x3 (Input Output Control By Identifier)"), "Text should be found in response")
        self.assertTrue(0 <= ret.find("ID: 0x6ff Service: 0x1 Sub: 0xd (Req Current Powertrain)"), "Text should be found in response")