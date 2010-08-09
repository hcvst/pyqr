# Copyright Hans Christian v. Stockhausen, 2010 

import matrix, ffield, Image

# Encoding mode, error correction and masking constants
QR_MODE_NUM, QR_MODE_AN, QR_MODE_8, QR_MODE_KANJI = 0, 1, 2, 3
QR_ECLEVEL_L, QR_ECLEVEL_M, QR_ECLEVEL_Q, QR_ECLEVEL_H = 0, 1, 2, 3
QR_MASK_0, QR_MASK_1, QR_MASK_2, QR_MASK_3 = 0, 1, 2, 3
QR_MASK_4, QR_MASK_5, QR_MASK_6, QR_MASK_7 = 4, 5, 6, 7

# Encoding defaults
default_micro = False           # Standard QR Codes 
default_version = 2             # Version 2 with 25x25 modules
default_mode = QR_MODE_8        # See table_alnum below
default_eclevel = QR_ECLEVEL_L  # Medium ec level

# Encoding table for alphanumeric mode (QR_MODE_NUM) Index corresponds
# to encoded value, i.e. 'A' encoded is 10 and 'Z' 35.
table_alnum = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '$', '%', '*',
               '+', '-', '.', '/', ':']

# Table for alignment pattern positions. For example a Version 2 QRCode
# uses row/col-positions 6 and 18. All possible combinations to place the
# pattern are (6,6), (6,18), (18,6) and (18,18). However all positions
# except for (18,18) are covered partially by one of the three finder patterns 
# so only (18,18) is used. 
table_align = [
    None, # version 0 does not exist
    None, # no alignment pattern for Version 1
    [6,18],
    [6,22],
    [6,26],
    [6,30],
    [6,34],
    [6,22,38], # FIXME and all versions below
    [6,24],
    [6,26],
    [6,28], # Version 10
    [6,30],
    [6,32],
    [6,34],
    [6,26],
    [6,26],
    [6,26],
    [6,30],
    [6,30],
    [6,30],
    [6,34], # Version 20
    [6,28],
    [6,26],
    [6,30],
    [6,28],
    [6,32],
    [6,30],
    [6,34],
    [6,26],
    [6,30],
    [6,26], # Version 30
    [6,30],
    [6,34],
    [6,30],
    [6,34],
    [6,30],
    [6,24],
    [6,28],
    [6,32],
    [6,26],
    [6,30]  # version 40 
    ]

# Generator polynomials for Reed Solomon error correction by number
# of error correction codewords.
# FIXME - try to generate this table
table_generator = {
    2:[],
    5:[],
    6:[],
    7:[],
    8:[],
    10:[216,194,159,111,199,94,95,113,157,193],
    13:[],
    14:[],
    15:[29,196,111,163,112,74,10,105,105,139,132,151,32,134,26],
    16:[],
    17:[119,66,83,120,119,22,197,83,249,41,143,134,85,53,125,99,79],
    18:[],
    20:[]
    }

# Lookup table for symbol traits. The lookup key is the tuple (Microcode?, Version, EC Level).
# For example (False, 2, QR_ECLEVEL_L) represents QRCode (i.e. not Microcode) Version 2 using
# error correction level L. Entries take the form of (b, c, k) where b is the number of error
# correction blocks, c the total number of codewords per block and k the number of data 
# codewords per block... (FIXME is this correct?????)

table_traits = {
    #MICROCODES
    (True, 1, None):(1, 5, 3),
    (True, 2, QR_ECLEVEL_L):(1, 10, 5),
    (True, 2, QR_ECLEVEL_M):(1, 10, 4),
    (True, 3, QR_ECLEVEL_L):(1, 17, 11),
    (True, 3, QR_ECLEVEL_M):(1, 17, 9),
    (True, 4, QR_ECLEVEL_L):(1, 24, 16),
    (True, 4, QR_ECLEVEL_M):(1, 24, 14),
    (True, 4, QR_ECLEVEL_Q):(1, 24, 10),
    #QRCODES
    (False, 1, QR_ECLEVEL_L):(1, 26, 19),
    (False, 1, QR_ECLEVEL_M):(1, 26, 16),
    (False, 1, QR_ECLEVEL_Q):(1, 26, 13),
    (False, 1, QR_ECLEVEL_H):(1, 26, 9),
    (False, 2, QR_ECLEVEL_L):(1, 44, 34),
    (False, 2, QR_ECLEVEL_M):(1, 44, 28),
    (False, 2, QR_ECLEVEL_Q):(1, 44, 22),
    (False, 2, QR_ECLEVEL_H):(1, 44, 16),
    (False, 3, QR_ECLEVEL_L):(1, 70, 55),
    (False, 3, QR_ECLEVEL_M):(1, 70, 44),
    (False, 3, QR_ECLEVEL_Q):(2, 35, 17), #FIXME cannot deal with blocksize >1 yet
    (False, 3, QR_ECLEVEL_H):(2, 35, 13)
    #FIXME ...
    }

# Lookup table for format information
# Key (Mask, EC Level) maps to (QR-Format, Micro-Format)
table_format = { 
    #FIXME populate entire table
    (QR_ECLEVEL_L, QR_MASK_0):(0x0, 0x0), # Data bits 01000 (01 EC_L, 000 Mask)
    (QR_ECLEVEL_L, QR_MASK_1):(0x0, 0x0), 
    (QR_ECLEVEL_L, QR_MASK_2):(0x0, 0x0), 
    (QR_ECLEVEL_L, QR_MASK_3):(0x789D, 0x68CA), 
    (QR_ECLEVEL_L, QR_MASK_4):(0x0, 0x0),
    (QR_ECLEVEL_L, QR_MASK_5):(0x0, 0x0),
    (QR_ECLEVEL_L, QR_MASK_6):(0x0, 0x0),
    (QR_ECLEVEL_L, QR_MASK_7):(0x0, 0x0),
    
    (QR_ECLEVEL_M, QR_MASK_0):(0x0, 0x0), # 00000
    (QR_ECLEVEL_M, QR_MASK_1):(0x0, 0x0),
    (QR_ECLEVEL_M, QR_MASK_2):(0x0, 0x0),
    (QR_ECLEVEL_M, QR_MASK_3):(0x5B4B, 0x4B1C),
    (QR_ECLEVEL_M, QR_MASK_4):(0x0, 0x0),
    (QR_ECLEVEL_M, QR_MASK_5):(0x0, 0x0),
    (QR_ECLEVEL_M, QR_MASK_6):(0x0, 0x0),
    (QR_ECLEVEL_M, QR_MASK_7):(0x0, 0x0),
    
    (QR_ECLEVEL_Q, QR_MASK_0):(0x0, 0x0), # 11000
    (QR_ECLEVEL_Q, QR_MASK_1):(0x0, 0x0),
    (QR_ECLEVEL_Q, QR_MASK_2):(0x0, 0x0),
    (QR_ECLEVEL_Q, QR_MASK_3):(0x0, 0x0),
    (QR_ECLEVEL_Q, QR_MASK_4):(0x0, 0x0),
    (QR_ECLEVEL_Q, QR_MASK_5):(0x0, 0x0),
    (QR_ECLEVEL_Q, QR_MASK_6):(0x0, 0x0),
    (QR_ECLEVEL_Q, QR_MASK_7):(0x0, 0x0),
    
    (QR_ECLEVEL_H, QR_MASK_0):(0x0, 0x0), # 10000
    (QR_ECLEVEL_H, QR_MASK_1):(0x0, 0x0),
    (QR_ECLEVEL_H, QR_MASK_2):(0x0, 0x0),
    (QR_ECLEVEL_H, QR_MASK_3):(0x19D0, 0x0987),
    (QR_ECLEVEL_H, QR_MASK_4):(0x0, 0x0),
    (QR_ECLEVEL_H, QR_MASK_5):(0x0, 0x0),
    (QR_ECLEVEL_H, QR_MASK_6):(0x0, 0x0),
    (QR_ECLEVEL_H, QR_MASK_7):(0x0, 0x0),
    }

class QRError(Exception):
    pass

class QRCode(object):

    def __init__(self, 
                 microcode = default_micro,
                 version = default_version,
                 mode = default_mode,
                 eclevel = default_eclevel):

        if version < 1 or version > 40 or (version > 4 and microcode):
            raise QRError(
                'Invalid version. Version limited to 1..4 for '  
                'Microcodes and 1..40 for regular QR Codes.')

        if mode not in [QR_MODE_NUM, QR_MODE_AN,
                        QR_MODE_8, QR_MODE_KANJI]:
            raise QRError('Mode unknown.')

        if eclevel not in [QR_ECLEVEL_L, QR_ECLEVEL_M, 
                           QR_ECLEVEL_Q, QR_ECLEVEL_H]: 
            raise QRError('Error correction level unknown.')

        self.version = version        
        self.microcode = microcode        
        self.mode = mode
        self.eclevel = eclevel
        base_size, size_increment = (11, 2) if self.microcode else (21, 4)
        self.size = base_size + size_increment * (version - 1)
        self.blocks, \
        self.codewords, \
        self.datawords = table_traits[(self.microcode, self.version, self.eclevel)]
        self.matrix = None


    def encode(self, s):
        data = self.encode_string(s)
        m = matrix.Matrix(self.size, self.size, 8)
        self.plot_function_pattern(m)
        format_qr, format_micro = table_format[(self.eclevel, QR_MASK_3)]
        self.plot_format_information(m, bitlist(format_qr, 15))
        self.plot_data(m, int_to_bitlist(data), mask=lambda i,j: (i+j) % 3 == 0)
        self.matrix = m
        

            
        
    def encode_string(self, s):
        if self.mode == QR_MODE_NUM:
            raise NotImplementedError
        elif self.mode == QR_MODE_AN:
            codewords = self.encode_AN(s)
        elif self.mode == QR_MODE_8:
            codewords = self.encode_8(s)
        elif self.mode == QR_MODE_KANJI:
            raise NotImplementedError
        # add more than padding
        codewords += [236, 17] * self.codewords #magic padding sequence
        # and cut to size
        codewords = codewords[:self.datawords]
        return codewords + self.get_ecc(codewords) # FIXME

    def encode_AN(self, s):
        data = list(s.upper())
        bits = [0,0,1,0] #4bit
        l = len(data)
        bits += bitlist(l, 9) #FIXME 9 not always the case?
        oddbit = None if l % 2 == 0 else data.pop()
        for i in range(0,len(data),2):
            v = table_alnum.index(data[i])*45
            v += table_alnum.index(data[i+1])
            bits += bitlist(v, 11)
        if oddbit:
            v = table_alnum.index(oddbit)
            bits += bitlist(v, 6)
        bits += [0,0,0,0] #FIXME only add terminator if required?
        return bit_to_intlist(bits)
    
    def encode_8(self, s):
        bits = [0,1,0,0]
        bits += bitlist(len(s), 8)
        for c in s:
            bits += bitlist(ord(c),8)
        bits += [0,0,0,0] #FIXME only add terminator if required?
        return bit_to_intlist(bits)
        
    def get_ecc(self, codewords):
        "as described in BBC whitepaper..."
        generator = table_generator[self.codewords - self.datawords]
        F = ffield.FField(8)
        acc = [0] * (len(codewords) + len(generator))
        p = 0
        for c in codewords:
            acc[p] = F.Add(acc[p], c)
            q = 1
            for g in generator:
                acc[p+q] = F.Add(acc[p+q], F.Multiply(acc[p], g))
                q += 1
            p += 1
        return acc[len(codewords):]

    def plot_function_pattern(self, m):
        #plot alingnment pattern
        p_align = [[1,1,1,1,1],
                   [1,0,0,0,1],
                   [1,0,1,0,1],
                   [1,0,0,0,1],
                   [1,1,1,1,1]]
        # find center coordinates
        cc = table_align[self.version]
        if cc:
            positions = [(i,j) for i in cc for j in cc]
            for i, j in positions:
                #avoid finder patterns
                if i == 6:
                    if j == 6 or j > self.size - 8: continue
                elif j == 6 and i > self.size - 8: continue
                m.plot(i-2, j-2, p_align)
        
        
        #plot timing pattern
        m.plot(6,0, [[1,0]*self.size])
        m.plot(0,6, [[1],[0]]*self.size)
        #plot finder pattern
        p_finder = [[0,0,0,0,0,0,0,0,0],
                    [0,1,1,1,1,1,1,1,0],
                    [0,1,0,0,0,0,0,1,0],
                    [0,1,0,1,1,1,0,1,0],
                    [0,1,0,1,1,1,0,1,0],
                    [0,1,0,1,1,1,0,1,0],
                    [0,1,0,0,0,0,0,1,0],
                    [0,1,1,1,1,1,1,1,0],
                    [0,0,0,0,0,0,0,0,0]]
        m.plot(-1, -1, p_finder)
        m.plot(-1, self.size-8, p_finder)
        m.plot(self.size-8, -1, p_finder)
        
        
    def plot_format_information(self, m, f):
        #plot format info around finders
        s = self.size
        
        m[8,0] = m[s-1,8] = f[0]
        m[8,1] = m[s-2,8] = f[1]
        m[8,2] = m[s-3,8] = f[2]
        m[8,3] = m[s-4,8] = f[3]
        m[8,4] = m[s-5,8] = f[4]
        m[8,5] = m[s-6,8] = f[5]
        m[8,7] = m[s-7,8] = f[6]
        m[8,8] = m[8,s-8] = f[7]
        m[7,8] = m[8,s-7] = f[8]
        m[5,8] = m[8,s-6] = f[9]
        m[4,8] = m[8,s-5] = f[10]
        m[3,8] = m[8,s-4] = f[11]
        m[2,8] = m[8,s-3] = f[12]
        m[1,8] = m[8,s-2] = f[13]
        m[0,8] = m[8,s-1] = f[14]
        
        m[s-8,8] = 1 #FIX
        
    def plot_data(self, m, data, mask):
        data.reverse() # cheaper to pop of the end
        def walk_symbol():
            s = self.size
            i = j = s -1
            direction = -1
            right = True
            is_free = lambda i,j: i < s and j < s and m[i,j] == 8 #FIXME
            while True:
                yield i, j
                if right:
                    if is_free(i, j-1):
                        j -= 1
                        right = False
                    elif is_free(i+direction, j):
                        i += direction
                else:
                    if is_free(i+direction, j+1):
                        j += 1
                        i += direction
                        right = True
                    elif is_free(i+direction, j):
                        i += direction
                    elif is_free(i+direction*2, j+1): #TIMING PATTERN
                        j += 1
                        i += direction*2
                        right = True                    
                    elif is_free(i+direction*6, j+1): # ALIGNMENT PATTERN
                        j += 1
                        i += direction*6
                        right = True
                    elif is_free(i, j-1):
                        j -= 1
                        direction *= -1
                        right = True   
                    elif is_free(i, j-2):
                        j -= 2
                        direction *= -1
                        right = True
                    elif is_free(i-8, 8): # jump above bottom right format info
                        i -= 8
                        j = 8
                        direction *= -1
                        right = True
                    else: break
                                 
        for i, j in walk_symbol():
            try:
                d = data.pop()
            except IndexError: #end of data
                d = 0
            if mask(i,j):
                m[i,j] = 0 if d else 1
            else:
                m[i,j] = d    
    
    def to_string(self, on='X', off=' '):
        l = [on if x==1 else off for x in self.matrix.to_list()]
        s = ''
        for i in range(0, len(l), self.size):
            s += ''.join(l[i:i+self.size])
            s += '\n'
        return s

    def to_image(self, module_width=6, on=0x008000, off=0xffffff):
        s = self.size
        img = Image.new('RGB', (s, s), off)
        img.putdata([on if x==1 else off for x in self.matrix.to_list()])
        return img.resize((module_width*s, module_width*s))

        
# helper

def bitlist(i, l):
    """
    Returns a list of length l representing the bit sequence of i.
    For example: bitlist(2,5) returns [0,0,0,1,0]
    """
    b = bin(i)[2:] #cut off initial '0b'
    d = l - len(b)
    if d < 0:
        raise Exception("Integer does not fit into bitlist.")
    else:
        return [int(i) for i in list('0'*d+b)]

def bit_to_intlist(b):
    d = len(b) % 8
    if d: b += [0] * (8 - d) # pad list 
    intlist = []
    for i in range(0, len(b), 8):
        v  = b[i] << 7
        v += b[i+1] << 6
        v += b[i+2] << 5
        v += b[i+3] << 4
        v += b[i+4] << 3
        v += b[i+5] << 2
        v += b[i+6] << 1
        v += b[i+7] 
        intlist.append(v)
    return intlist

def int_to_bitlist(intlist):
    b = []
    for i in intlist:
        b += bitlist(i, 8)
    return b


