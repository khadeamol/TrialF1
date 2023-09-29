class tryClass():
    # def __init__(self):
    #     self.v = "v"

    def funcOne(self, val1):
        # print("Entered function",val1)
        self.var = val1
        return self.var

a = tryClass()
print("printed here",a.funcOne(1))