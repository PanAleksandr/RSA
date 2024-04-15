import math
import random

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("Обратный модуль не существует")

# Функция генерации простого числа
def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

# Функция для записи в файл
def write_to_file(filename, data):
    with open(filename, "w") as file:
        file.write(data)

# Функция для чтения из файла
def read_from_file(filename):
    with open(filename, "r") as file:
        return file.read()

action = input("Выберите действие (1 - шифрование, 2 - расшифровка): ")

if action == "1":
    # Ввод простого числа p
    while True:
        p = int(input("Введите простое число p: "))
        if is_prime(p):
            break
        else:
            print("Это не простое число. Попробуйте еще раз.")

    # Ввод простого числа q
    while True:
        q = int(input("Введите простое число q: "))
        if is_prime(q):
            break
        else:
            print("Это не простое число. Попробуйте еще раз.")

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Выбор публичного ключа e
    e = random.randint(3, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)

    # Вычисление приватного ключа d
    d = mod_inverse(e, phi_n)

    print("Открытый ключ:", e)
    print("Закрытый ключ:", d)
    print("n:", n)
    print("Фи(n):", phi_n)
    print("p:", p)
    print("q:", q)

    # Шифрование сообщения
    message = input("Введите сообщение для шифрования: ")

    message_encoded = [ord(ch) for ch in message]
    ciphertext = [pow(ch, e, n) for ch in message_encoded]

    # Сохранение открытого ключа в файл
    write_to_file("public_key.txt", f"{e} {n}")


    # Сохранение зашифрованного текста в файл
    write_to_file("encrypted_text.txt", " ".join(map(str, ciphertext)))

    print("Шифротекст сохранен в файле 'encrypted_text.txt'.")

elif action == "2":
    def find_factors(n):
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return i, n // i
        return None, None


    # Įvedimas n iš konsolės
    n = int(input("Įveskite skaičių n: "))

    # Surasti pirminius faktorius
    p, q = find_factors(n)
    print("Pirmas pirminis faktorius:", p)
    print("Antras pirminis faktorius:", q)


    def phi(n, p, q):
        return (p - 1) * (q - 1)


    # Naudodami gautus pirminius faktorius p ir q, suskaičiuokite Φ(n)
    phi_n = phi(n, p, q)
    print("Φ(n):", phi_n)



    def mod_inverse(e, phi):
        for d in range(3, phi):
            if (d * e) % phi == 1:
                return d
        raise ValueError("Modulinis atvirkštinis neegzistuoja")


    # Įvedimas viešo rakto e
    e = int(input("Įveskite viešą raktą (e): "))

    # Skaičiuojame φ(n)
    phi_n = phi(n, p, q)

    # Skaičiuojame privataus rakto d
    d = mod_inverse(e, phi_n)

    print("Privatus raktas (d):", d)

    # Чтение зашифрованного текста из файла
    ciphertext_data = read_from_file("encrypted_text.txt")
    ciphertext_parts = ciphertext_data.split()
    ciphertext = [int(ch) for ch in ciphertext_parts]

    decrypted_message_encoded = [pow(ch, d, n) for ch in ciphertext]
    decrypted_message = "".join(chr(ch) for ch in decrypted_message_encoded)

    print("Расшифрованное сообщение:", decrypted_message)

else:
    print("Неверный выбор действия.")
