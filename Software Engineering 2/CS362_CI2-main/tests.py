import unittest
from task import my_datetime
from task import conv_num
from task import conv_endian

if __name__ == '__main__':
    unittest.main()


class TestCase(unittest.TestCase):

    # conv_num tests
    def test_num1(self):
        self.assertEqual(conv_num(""), None)

    def test_num2(self):
        self.assertEqual(conv_num("XYZ"), None)

    def test_num3(self):
        self.assertEqual(conv_num("Numbers"), None)

    def test_num4(self):
        self.assertEqual(conv_num("397DC9"), None)

    def test_num5(self):
        self.assertEqual(conv_num("C6.D7"), None)

    def test_num6(self):
        self.assertEqual(conv_num("24.127.20.198"), None)

    def test_num7(self):
        self.assertEqual(conv_num("-401-666"), None)

    def test_num8(self):
        self.assertEqual(conv_num("471x80"), None)

    def test_num9(self):
        self.assertEqual(conv_num("0x7K"), None)

    def test_num10(self):
        self.assertEqual(conv_num("8"), 8)

    def test_num11(self):
        self.assertEqual(conv_num("34555"), 34555)

    def test_num12(self):
        self.assertEqual(conv_num("-4537"), -4537)

    def test_num13(self):
        self.assertEqual(conv_num("3.1415926535"), 3.1415926535)

    def test_num14(self):
        self.assertEqual(conv_num("-99999.99999"), -99999.99999)

    def test_num15(self):
        self.assertEqual(conv_num("99."), 99.0)

    def test_num16(self):
        self.assertEqual(conv_num(".4"), 0.4)

    def test_num17(self):
        self.assertEqual(conv_num("0x0B62"), 2914)

    def test_num18(self):
        self.assertEqual(conv_num("0x0A1F67"), 663399)

    def test_num19(self):
        self.assertEqual(conv_num("-0x01E240"), -123456)

    # conv_endian tests

    def test_num20(self):
        self.assertEqual(conv_endian(123456, 'big'), '01 E2 40')

    def test_num21(self):
        self.assertEqual(conv_endian(123456), '01 E2 40')

    def test_num22(self):
        self.assertEqual(conv_endian(-123456), '-01 E2 40')

    def test_num23(self):
        self.assertEqual(conv_endian(123456, 'little'), '40 E2 01')

    def test_num24(self):
        self.assertEqual(conv_endian(-123456, 'little'), '-40 E2 01')

    def test_num25(self):
        self.assertEqual(conv_endian(num=-123456, endian='little'), '-40 E2 01')

    def test_num26(self):
        self.assertEqual(conv_endian(num=-123456, endian='small'), None)

    # my_datetime tests

    def test_num27(self):
        self.assertEqual(my_datetime(123456789), '11-29-1973')

    def test_num28(self):
        self.assertEqual(my_datetime(9876543210), '12-22-2282')

    def test_num29(self):
        self.assertEqual(my_datetime(201653971200), '02-29-8360')

    def test_num30(self):
        self.assertEqual(my_datetime(0), '01-01-1970')

    def test_num31(self):
        self.assertEqual(my_datetime(991972599), '06-08-2001')

    def test_num32(self):
        self.assertEqual(my_datetime(6746039799), '10-10-2183')
