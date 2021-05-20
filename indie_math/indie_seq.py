
# Basic sequence generation using the signature function
class Seq:

    def __init__(self, val):
        self.val = []
        for each in val:
            if not isinstance(each, (int, float)):
                raise ValueError("List must contain only int and float")
            else:
                self.val.append(each)

    def __add__(self, other):
        if isinstance(other, (int, float)):
            out = Seq([self.val[0] + other] + self.val[1:])
            return out
        elif isinstance(other, Seq):
            out = []
            for n in range(max(len(self), len(other))):
                out.append(self.get(n) + other.get(n))
            return Seq(out)

    def __len__(self):
        return len(self.val)

    def __str__(self):
        out = ", ".join([str(each) for each in self.val])
        return out

    def append(self, d):
        if not isinstance(d, (int, float)):
            raise ValueError("Can only append int or float")
        self.val.append(d)

    def get(self, n):
        return self.val[n] if 0 <= n < len(self.val) else 0

    def f(self, l=15):
        out = Seq([1])
        for n in range(1, l):
            q = 0
            for k in range(1, n+1):
                q += self.get(n-k) * out.get(k-1)
            out.append(q)
        return out
