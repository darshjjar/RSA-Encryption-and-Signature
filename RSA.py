import random
from sympy.ntheory import isprime 
from math import gcd
from binascii import hexlify
from ast import literal_eval

def initiate(D, E, N, Phi_N):
    choice = int(input("1: Encrypt \n2: Decrypt \n3: signature \n4: signature varification\n  "))
    if choice == 1:
        msg = input("Enter the message\n")
        E = int(input("Enter the E\n"))
        N = int(input("Enter the N\n"))
        M_divided = string_division(msg)
        M_int = string_int(M_divided)
        cypher = encode(M_int, E, N)
        print("Cypher Text: ",cypher)


    elif choice == 2:
        encrypt_msg = literal_eval(input("Enter the encrypted text\n"))
        decoded_msg = decode(encrypt_msg,D,N)
        print("Decoded message: ",decoded_msg)

    elif choice == 3:
        msg = input("Enter the name for signature\n")
        signature = sign(N, D, msg)
        print("signed cipher text: ", signature)

    else:
        encrypt_msg = literal_eval(input("Enter the cipher text for varification\n"))
        msg = input("Enter the name of the signer \n")
        E = int(input("Enter the E\n"))
        N = int(input("Enter the N\n"))
        sign_varify(encrypt_msg, E, N, msg)




def prime_random_generator(): 
    n = 10
    while not isprime(n) :
        n = random.randint(32768,65535)
    return n
 
def E_generator(phi_N):
    E = 2
    while not gcd(E,phi_N) == 1:
        E = random.randint(32768,65535)

    return E

def mod_inverse(E,phi_N):
    for i in range(1,phi_N):
        if ((E % phi_N) * (i % phi_N) % phi_N == 1):
            return i
        else:
            i = i + 1

def string_division(M):
    
    M_list = []
    n = 3
    while len(M) > 0:

        M_list.append(M[:n])
        M = M[n:]
        
       
    return M_list   

def square_and_multiply(base, power, mod):
    power_bin = bin(power)

    value = base
    for i in range(3,len(power_bin)):
        value = (value * value) % mod 
        if(power_bin[i] == '1'):
            value = value * base % mod
    
    return value


def string_int(M_list):
    for i in range(len(M_list)):
        M_list[i] = int(hexlify(bytes(M_list[i], encoding='utf8')), 16)
            
    return(M_list)



def encode(M_int, Expo , N):
    encoded = []
    

    for i in range(len(M_int)):  
        if M_int[i] > N:
            print("Message too big ")
            break     
        encoded.append(square_and_multiply(M_int[i],Expo,N))
    return encoded    



def decode(cypher,D,N):  
    decoded_msg = ''
    dcd = []
    for i in range(len(cypher)):
        cypher[i] = (square_and_multiply(cypher[i],D,N))
        
        dcd.append(bytes.fromhex(str(hex(cypher[i]))[2:]).decode('utf-8'))
        decoded_msg = decoded_msg + dcd[i]

    return decoded_msg


def sign(N, D, msg):
    M_divided = string_division(msg)
    M_int = string_int(M_divided) 
    signature = encode(M_int, D, N)
    return signature
    
    
def sign_varify(signature, D, N, msg):
    var = decode(signature, D, N)
    if msg == var:
        print("True : Signature varified successfully")
    else:
        print("False : Signature couldn't varified")



    
#p = prime_random_generator()
#q = prime_random_generator()

p = 38303
q = 61933
N = p * q   
phi_N = (p-1) * (q-1)

#E = E_generator(phi_N)

E = 51305
##calculating D = E^-1 mod phi_N

#E_inv = mod_inverse(E,phi_N)

#D = E_inv
D = 987870665

initiate(D, E, N, phi_N)






