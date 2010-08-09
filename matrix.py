# Copyright Hans Christian v. Stockhausen, 2010 

class Matrix(object):

    def __init__(self, i, j, initial=None):
        self.i = i
        self.j = j
        self.m = [[initial] * j for _ in range(i)]

    def __getitem__(self, (i,j)):
        return self.m[i][j]

    def __setitem__(self, (i,j), data):
        self.m[i][j] = data

    def to_list(self):
        return [x for row in self.m for x in row]

    def get_row(self, r):
        return self.m[r]

    def get_col(self, c):
        return [row[c] for row in self.m]
    
    def plot(self, origin_i, origin_j, pattern): #FIXME rather than patter this shoud be matrix
        for i, row in enumerate(pattern):
            i += origin_i
            if i < 0 or i >= self.i: continue
            for j, value in enumerate(row):
                j += origin_j
                if j < 0 or j >= self.j: continue
                self[i, j] = value
                
    def __repr__(self):
        s = '['
        s += ',\n'.join([str(r) for r in self.m])
        s += ']'
        return s
