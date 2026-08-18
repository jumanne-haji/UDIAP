import hashlib

# Weka namba yako unayotaka kuificha (mfano: 12345 au namba yoyote)
namba_yetu = "12345"

# Kuigeuza iwe katika mfumo wa bytes kisha kui-hash kwa kutumia SHA-256
hashed_result = hashlib.sha256(namba_yetu.encode()).hexdigest()

print(f"Namba ya asili: {namba_yetu}")
print(f"Hali yake baada ya ku-hash (SHA-256): {hashed_result}")

