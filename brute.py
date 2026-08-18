import hashlib
import itertools

# Hii ndiyo hash iliyofichwa (kwa mfano SHA-256 ya namba fulani)
target_hash = "2517852c01d0d15b026639c096e289bf50d32f520970335e76a6e5452f1e42c2"

def crack_hash():
    digits = "0123456789"
    # Kutoka tarakimu 4 hadi 8 (hapa mfano nimeweka 4 kwa uchache)
    for length in range(4, 9):
        print(f"Inajaribu urefu wa tarakimu {length}...")
        for guess in itertools.product(digits, repeat=length):
            guess_str = "".join(guess)
            
            # Ku-hash hiyo namba inayojaribiwa
            guess_hash = hashlib.sha256(guess_str.encode()).hexdigest()
            
            # Kulinganisha hash iliyopatikana na ile ya siri
            if guess_hash == target_hash:
                print(f"Imepatikana! Namba halisi ni: {guess_str}")
                return guess_str

crack_hash()

