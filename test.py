from base64 import b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import scrypt
from Cryptodome.Util.Padding import unpad

def decrypt_string(encrypted_text, password):
    try:
        # Decode base64
        data = b64decode(encrypted_text)
        
        # Extract salt
        salt = data[8:16]  # Skip 'Salted__' prefix
        
        # Generate key and IV using scrypt
        key_iv = scrypt(password.encode(), salt, key_len=48, N=16384, r=8, p=1)
        key = key_iv[:32]
        iv = key_iv[32:48]  # Ensure 16-byte IV
        
        # Create cipher
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt
        decrypted = cipher.decrypt(data[16:])  # Skip salt prefix
        
        # Remove padding
        decrypted = unpad(decrypted, AES.block_size)
        
        # Try different encodings
        try:
            return decrypted.decode('utf-8')
        except:
            return decrypted.decode('latin-1')
            
    except Exception as e:
        return f"Decryption failed: {str(e)}"

# Test it
encrypted = "U2FsdGVkX19lvNMu2hvHum4H/gZzIRHReModkeyK5Jo="
password = "gmonad"

result = decrypt_string(encrypted, password)
print(f"Decrypted result: {result}")