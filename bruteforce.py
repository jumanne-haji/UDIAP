import itertools
import time

# Hii ni namba ya siri iliyofichwa (encrypted/target) tunayotaka kuipata
target_number = "7392"

def crack_password():
    print("Inaanza kutafuta namba...")
    start_time = time.time()
    
    # Kutengeneza mchanganyiko wote kuanzia tarakimu 4 (0000 hadi 9999)
    # Unaweza kupanua ukubwa mpaka tarakimu 8 kwa kuongeza wigo wa digits
    digits = "0123456789"
    
    # Jaribio la kupitia kila mchanganyiko (combination/permutation)
    for guess in itertools.product(digits, repeat=4):
        guess_str = "".join(guess)
        
        # Hapa ndipo script inapofanya correlation au kulinganisha na ile unknown number
        if guess_str == target_number:
            end_time = time.time()
            print(f"Imepatikana! Namba ni: {guess_str}")
            print(f"Imetumia sekunde: {round(end_time - start_time, 4)}")
            return guess_str

crack_password()

