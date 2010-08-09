import unittest

import matrix, qrcode

class MatrixTest(unittest.TestCase):
    
    def setUp(self):
        self.m1 = matrix.Matrix(10, 10)
        self.m2 = matrix.Matrix(10, 5, initial=42)
        self.m3 = matrix.Matrix(1, 10, initial=69)
        self.m4 = matrix.Matrix(15, 1, initial=23)
        
    def testCreate(self):
        self.assertEqual(self.m1[0,0], None)
        self.assertEqual(self.m2[9,4], 42)
        
    def testSet(self):
        self.assertEqual(self.m1[1,0], None)
        self.assertEqual(self.m1[2,0], None)
        self.assertEqual(self.m1[1,1], None)
        self.m1[1,0] = 1
        self.assertEqual(self.m1[1,0], 1)
        self.assertEqual(self.m1[2,0], None)
        self.assertEqual(self.m1[1,1], None)
        
    def testGetRow(self):
        self.assertEqual(self.m3.get_row(0), [69] * 10)
        self.assertEqual(self.m1.get_row(8), [None] * 10)
                
    def testGetCol(self):
        self.assertEqual(self.m4.get_col(0), [23] * 15)
        self.assertEqual(self.m1.get_col(8), [None] * 10)

        
class QRCodeTest(unittest.TestCase):
      
    def testSymbolSize(self):
        self.assertEqual(25, qrcode.QRCode().size)
        self.assertEqual(21, qrcode.QRCode(version=1).size)
        self.assertEqual(13, qrcode.QRCode(microcode=True).size)
        self.assertEqual(15, qrcode.QRCode(microcode=True, version=3).size)
        
    def testInvalidVersion(self):
        self.assertRaises(qrcode.QRError, qrcode.QRCode, version=0)
        self.assertRaises(qrcode.QRError, qrcode.QRCode, version=5, microcode=True)
        self.assertRaises(qrcode.QRError, qrcode.QRCode, version=41)
        
    def testBitlist(self):
        self.assertEqual([0,0,0,1,0], qrcode.bitlist(2, 5))
        
    def testBitToIntlist(self):
        self.assertEqual([0,255], 
                         qrcode.bit_to_intlist(
                             [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]))
        
    def testIntToBitlist(self):
        self.assertEqual([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                         qrcode.int_to_bitlist([128,1]))
        
    def testEncode(self):
        #qrcode.QRCode(version=1).encode('HTTP://QR-CODE.CO.PA')
        qrcode.QRCode().encode('HTTP://QR-CODE.CO.ZA/0123456789/0123456789/0123')
if __name__ == '__main__':
    unittest.main()