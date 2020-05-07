def somefunction(a):
    return a


class SomeClass:
    def __init__(self, b):
        self.b = b
        self.ncalls = 0

    def method(self, c):
        self.ncalls += 1
        return c * 2
