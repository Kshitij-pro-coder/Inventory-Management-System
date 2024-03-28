import random

class Generator:
    def __init__(self):
        self.first_8 = ["a","b","c","d","e","f","g","h"]
        self.second_4 = ["@","#","$","*"]
        self.third_4 = ["1","2","3","4"]
        self.fourth_8 = ["e","f","g","h","i","j","k","l"]
        self.fifth_8 = ["!","@","#","$","*","^","(",")"]
        self.sixth_8 = ["A","B","C","D","E","F","G","H"]
    
    def generate_8(self):
        key = ""
        for _ in range(8):
            key += random.choice(self.first_8)
        for _ in range(4):
            key += random.choice(self.second_4)
        for _ in range(4):
            key += random.choice(self.third_4)
        for _ in range(8):
            key += random.choice(self.fourth_8)
        for _ in range(8):
            key += random.choice(self.fifth_8)
        for _ in range(8):
            key += random.choice(self.sixth_8)
        return key

    def add_salt(self, string, salt):
        indices = set()

        while len(indices) < 3:
            index = random.randint(0, len(string))
            indices.add(index)

        for index in sorted(indices, reverse=True):
            string = string[:index] + salt + string[index:]

        return string
   
def generate():
    gen = Generator()
    salt1 = "hg!@$^54$%gcf&$7fhf%$%&lsa"
    secret_key = gen.add_salt(gen.generate_8(), salt1)
    return secret_key
