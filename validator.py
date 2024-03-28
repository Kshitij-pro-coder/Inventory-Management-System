class Verifier:
    def __init__(self):
        self.first_8 = ["a","b","c","d","e","f","g","h"]
        self.second_4 = ["@","#","$","*"]
        self.third_4 = ["1","2","3","4"]
        self.fourth_8 = ["e","f","g","h","i","j","k","l"]
        self.fifth_8 = ["!","@","#","$","*","^","(",")"]
        self.sixth_8 = ["A","B","C","D","E","F","G","H"]

    def salt_remover(self, key):
        salt1 = "hg!@$^54$%gcf&$7fhf%$%&lsa"
        key_without_salt = key.replace(salt1, '')
        return key_without_salt

    def verification_length(self, key):
        if len(key) == 40:
            return True
        else:
            return False
    
    def verification_1(self, key):
        for char in key[:8]:
            if char not in self.first_8:
                return False
        return True
    
    def verification_2(self, key):
        for char in key[8:12]:
            if char not in self.second_4:
                return False
        return True
    
    def verification_3(self, key):
        for char in key[12:16]:
            if char not in self.third_4:
                return False
        return True
    
    def verification_4(self, key):
        for char in key[16:24]:
            if char not in self.fourth_8:
                return False
        return True
    
    def verification_5(self, key):
        for char in key[24:32]:
            if char not in self.fifth_8:
                return False
        return True
    
    def verification_6(self, key):
        for char in key[32:40]:
            if char not in self.sixth_8:
                return False
        return True     

def vldtr(user_input):
    z = 's'
    y = 'n'
    ver = Verifier()
    key = ver.salt_remover(user_input)
    if (
        ver.verification_length(key) and
        ver.verification_1(key) and
        ver.verification_2(key) and
        ver.verification_3(key) and
        ver.verification_4(key) and
        ver.verification_5(key) and
        ver.verification_6(key)
    ):
        return z
    else:
        return y

