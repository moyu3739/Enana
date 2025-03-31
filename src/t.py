

class A:
    name = "class A"

    def __init__(self, x: int, name: str):
        self.x = x
        self.name = "instance A"



class B(A):
    name = "class B"

    def __init__(self, x: int):
        super().__init__(x, "class B")

    @classmethod
    def GetName(cls):
        return cls.name


b = B(114)
print(b.x, b.GetName())
