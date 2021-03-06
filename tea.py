# ********************************************* #
# Tiny Encryption Algorithm Implementation      #
# Ian Bolin & Trevor Loula                      #
# CS-3350 Foundations of Computer Security      #
# ********************************************* #

import sys
from tea_cbc import TEA_CBC
from tea_ctr import TEA_CTR
from tea_ecb import TEA_ECB

class Wrapper:

    @staticmethod
    def parse_input(args):
        mode = args[1][1:3]
        cipher = args[2][1:4]
        output = args[3]
        text = Wrapper.read_file(args[4])
        key = Wrapper.read_file(args[5])
        iv = Wrapper.read_file(args[6])

        keys = [x for x in Wrapper.split_string(key, 4)]
        ivs = [x for x in Wrapper.split_string(iv, 4)]

        return mode, cipher, output, text, keys, ivs

    @staticmethod
    def read_file(filepath):
        try:
            f = open(filepath, "rb")
        except FileNotFoundError as e:
            print ("File", filepath, "not found")
            exit()
        else:
            try:
                text = f.read()
                if "-H" in filepath:
                    text = Wrapper.pad_hex(text)
                    return bytes.fromhex(text.decode())
                else:
                    return Wrapper.pad_text(text)
            finally:
                f.close()

    @staticmethod
    def pad_text(text):
        while len(text) % 8 != 0:
            text += b" "

        return text

    @staticmethod
    def pad_hex(hexi):
        while len(hexi) % 8 != 0:
            hexi += b"0"

        return hexi

    @staticmethod
    def split_string(s, n):
        return [s[i:i+n] for i in range(0, len(s), n)]

    @staticmethod
    def run_tea(params):
        mode, cipher, output, text, key, iv = params

        print ("mode:", cipher)   # ECB, CBC, or CTR
        #print ("text:", text.hex()) # The Plaintext or Ciphertext
        print ("key:", key)         # Key
        print ("iv:", iv)           # Initialization Vector

        if cipher == "ECB":
            if mode == "e":
                print ("Ciphertext:", TEA_ECB.encrypt(text, key).hex())
            elif mode == "d":
                if output == "-h":
                    print ("Plaintext:", TEA_ECB.decrypt(text, key).hex())
                else:
                    print ("Plaintext:", TEA_ECB.decrypt(text, key).decode())
            else:
                print ("Invalid operation mode")
        elif cipher == "CBC":
            if mode == "e":
                print ("Ciphertext:", TEA_CBC.encrypt(text, key, iv).hex())
                f = open("test", "wb")
                f.write(TEA_CBC.encrypt(text, key, iv))
            elif mode == "d":
                if output == "-h":
                    print ("Plaintext:", TEA_CBC.decrypt(text, key, iv).hex())
                else:
                    print ("Plaintext:", TEA_CBC.decrypt(text, key, iv).decode())
            else:
                print ("Invalid operation mode")
        elif cipher == "CTR":
            if mode == "e":
                print ("Ciphertext:", TEA_CTR.encrypt(text, key, iv).hex())
            elif mode == "d":
                if output == "-h":
                    print ("Plaintext:", TEA_CTR.decrypt(text, key, iv).hex())
                else:
                    print ("Plaintext:", TEA_CTR.decrypt(text, key, iv).decode())
            else:
                print ("Invalid operation mode")
        else:
            print("Invalid Mode")
            exit()

        return

def main(args):

    # python tea.py -d -ECB -h assignment-files/Ciphertexts/mystery1_ECB-H.crypt assignment-files/teacher-H.key assignment-files/teacher-H.iv
    # python tea.py -d -ECB -s assignment-files/Ciphertexts/mystery2_ECB-S.crypt assignment-files/teacher-H.key assignment-files/teacher-H.iv
    # python tea.py -d -CBC -s assignment-files/Ciphertexts/mystery3_CBC-S.crypt assignment-files/teacher-H.key assignment-files/teacher-H.iv
    # python tea.py -d -CTR -s assignment-files/Ciphertexts/mystery4_CTR-S.crypt assignment-files/teacher-H.key assignment-files/teacher-H.iv

    if len(args) != 7:
        print("Usage: python tea.py -mode -cipher -format plaintext key initialization_vector")
        print("-mode: -e, -d")
        print("-cipher: ECB, CBC, CTR")
        print("-output: -h -s")
        print("i.e. python tea.py -e -ECB plaintext.plain key.key initialization_vector.iv")
        exit()

    Wrapper.run_tea(Wrapper.parse_input(args))

if __name__ == "__main__":
    main(sys.argv)
