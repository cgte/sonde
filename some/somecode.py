def somecodefunction(a):
    return a


class SomecodeClass:
    def __init__(self, b):
        self.b = b
        self.ncalls = 0

    def someclasmethod(self, c):
        self.ncalls += 1
        return c * 2
