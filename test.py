

class first():

    def __init__(self, name):
        self.name = name


    def name(self):
        return self.name



class second():

    def __init__(self, sirname):
        self.sirname = sirname


    def kat(self):
        obj1 = first('reference')
        ans2 = obj1.name
        return ans2


obj2 = second('adad')
ans = obj2.kat
