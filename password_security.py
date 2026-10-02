import hashlib
import os
import itertools
import string
import time


# ---------------- HASHING ----------------

def generate_hashes(password):
    print("\n--- HASHES ---")
    print("MD5    :", hashlib.md5(password.encode()).hexdigest())
    print("SHA-1  :", hashlib.sha1(password.encode()).hexdigest())
    print("SHA-256:", hashlib.sha256(password.encode()).hexdigest())


# ---------------- SALTED HASHING ----------------

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)

    hashed = hashlib.sha256(
        salt + password.encode()
    ).hexdigest()

    return hashed, salt


def verify_password(password, stored_hash, salt):
    new_hash, _ = hash_password(password, salt)
    return new_hash == stored_hash


# ---------------- DICTIONARY ATTACK ----------------

def dictionary_attack(target_hash, salt, filename):

    print("\n--- DICTIONARY ATTACK ---")

    try:
        with open(filename, "r") as file:

            for password in file:
                password = password.strip()

                if verify_password(password, target_hash, salt):
                    print("[+] Password found:", password)
                    return password

        print("[-] Password not found")

    except FileNotFoundError:
        print("[-] wordlist.txt not found")


# ---------------- BRUTE FORCE ----------------

def brute_force(target_hash, salt, max_length=4):

    charset = string.ascii_lowercase + string.digits

    print("\n--- BRUTE FORCE ATTACK ---")
    print("Character set:", len(charset))
    print("Maximum length:", max_length)

    attempts = 0
    start = time.time()

    for length in range(1, max_length + 1):

        for combination in itertools.product(charset, repeat=length):

            password = ''.join(combination)
            attempts += 1

            if verify_password(password, target_hash, salt):

                elapsed = time.time() - start

                print("[+] Password found:", password)
                print("[+] Attempts:", attempts)
                print("[+] Time:", round(elapsed, 2), "seconds")

                return password

    print("[-] Password not found")
    return None


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    print("==========================================")
    print("   PASSWORD HASHING & CRACKING LAB")
    print("==========================================")

    # USER INPUT
    password = input("\nEnter a password for testing: ")

    print("\nPassword received successfully.")

    # Generate hashes
    generate_hashes(password)

    # Salted SHA-256
    stored_hash, salt = hash_password(password)

    print("\n--- SALTED SHA-256 ---")
    print("Salt :", salt.hex())
    print("Hash :", stored_hash)

    # Password verification
    print("\n--- PASSWORD VERIFICATION ---")

    entered_password = input("Enter password again to verify: ")

    if verify_password(entered_password, stored_hash, salt):
        print("[+] Password verification successful")
    else:
        print("[-] Password verification failed")

    # Dictionary attack
    dictionary_attack(
        stored_hash,
        salt,
        "wordlist.txt"
    )

    # Brute-force attack
    brute_force(
        stored_hash,
        salt,
        max_length=4
    )
