import math
import random

def is_prime(number):  #Pirminis skaičius
    if number < 2:  # jei skaičius mažesnis nei 2
        return False  # jeigu sk < 2, tai tai nėra pirminis skaičius
    for i in range(2, number // 2 + 1):  #daliklius nuo 2 iki number // 2 + 1
        if number % i == 0:  # Jei sk dalijasi be liekanos i, tai jis nėra pirminis
            return False
    return True  # nėra daliklių = pirminis


def mod_inverse(e, phi):
    for d in range(3, phi):  # Einame per galimus d reikšmes
        if (d * e) % phi == 1:  # Patikriname, ar d yra atvirkštinis po moduliu e
            return d
    raise ValueError("Modular inverse does not exist")

def write_to_file(filename, data):  # funkcija irasyti duomenis i faila
    with open(filename, "w") as file:  # open
        file.write(data)  # write

def read_from_file(filename):  # Funkcija skaito duomenis iš failo
    with open(filename, "r") as file:  # Atidarome failą skaitymui
        return file.read()
def euklido_algoritmas(a, b):
    while b != 0:
        a, b = b, a % b
    return a

action = input("Choose action (1 - encryption, 2 - decryption): ")

if action == "1":  # 1
    while True: # Begalinis ciklas, skirtas įvesti pirminį skaičių p
        p = int(input("Enter prime number p: "))
        if is_prime(p):
            break
        else:
            print("This is not a prime number. Please try again.")

    while True:
        q = int(input("Enter prime number q: "))
        if is_prime(q):
            break
        else:
            print("This is not a prime number. Please try again.")

    n = p * q
    phi_n = (p - 1) * (q - 1)  # for n

    e = random.randint(3, phi_n - 1)  # Generuojamas atsitiktinis e iš intervalo [3, phi_n - 1]
    while euklido_algoritmas(e, phi_n) != 1:  # Tikrinama, ar e ir phi_n yra tarpusavyje pirminiai
        e = random.randint(3, phi_n - 1)  # Jei ne, generuojamas naujas atsitiktinis e

    d = mod_inverse(e, phi_n) #d, kuris yra atvirkštinis e mod phi_n

    print("Public key:", e)  #  e
    print("Private key:", d)  #  d
    print("n:", n)  #  n
    print("Phi(n):", phi_n)  # Φ[n]
    print("p:", p)  # 1 p
    print("q:", q)  # 2 q

    message = input("Enter message to encrypt: ")  # kazkoks zodis

    message_encoded = [ord(ch) for ch in message]  # paverčia pranešimą į skaitinį formatą, naudodama ASCII kodavimą
    ciphertext = [pow(ch, e, n) for ch in message_encoded]  # šifruoja pranešimą naudojant RSA algoritmą

    write_to_file("public_key.txt", f"{e} {n}")  # publik key and n write to the file
    write_to_file("encrypted_text.txt", " ".join(map(str, ciphertext)))  # text

    print("Cipher text saved in 'encrypted_text.txt'.")  # good

elif action == "2":  # 2
    def find_factors(n):  # Funkcija skirta rasti skaičiaus n daliklius
        for i in range(2, int(n ** 0.5) + 1):  # Einame per skaičius nuo 2 iki n kvadratinio šaknies
            if n % i == 0:  # Tikriname, ar n dalijasi be liekanos iš šio skaičiaus
                return i, n // i  # Jei taip, grąžiname daliklio porą (i, n // i)
        return None, None  # Jei daliklis nerastas, grąžiname None, None

    n = int(input("Enter number n: "))  #  n

    p, q = find_factors(n)  # find p,q

    def phi(n, p, q):  # Apskaičiuojame Eulerio funkciją φ(n)
        return (p - 1) * (q - 1)  # Grąžiname Eulerio funkcijos reikšmę

    phi_n = phi(n, p, q)  # Apskaičiuojame Eulerio funkciją φ(n) naudojant skaičius p ir q

    e = int(input("Enter public key (e): "))  # pub

    d = mod_inverse(e, phi_n)  # private

    print("Private key (d):", d)  # rodo d

    ciphertext_data = read_from_file("encrypted_text.txt")  # check text
    ciphertext_parts = ciphertext_data.split()  # by part
    ciphertext = [int(ch) for ch in ciphertext_parts]  # paverčia kiekvieną užšifruoto teksto fragmentą iš teksto į sveikąjį skaičių.

    decrypted_message_encoded = [pow(ch, d, n) for ch in ciphertext]  # decrypt
    decrypted_message = "".join(chr(ch) for ch in decrypted_message_encoded)  # užšifruotas tekstas paverčia į simbolius.

    print("Decrypted message:", decrypted_message)

else:
    print("Invalid action choice.")
