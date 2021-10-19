
class aaa:
    def __init__(self,age) -> None:
        self.age = age
    def __gt__(self,other):
        return self.age > other.age

a = aaa(15)
b = aaa(16)

print(a>5)