# Gronsfeld_23011102043  

Lakshmi Narayanan P  
IoT-A  
23011102043  

## Overview  
This project implements a secure message transmission scheme using the Gronsfeld Cipher for encryption and decryption, along with a custom 16-bit hash function for integrity verification. The system ensures confidentiality through encryption and integrity through hashing.  

## Assumptions  
- Cipher: Gronsfeld Cipher  
- Key: Numeric (e.g., 31415), repeated cyclically  
- Alphabet: A–Z only  
- Plaintext is converted to uppercase before processing  

**Hash function:**  
H(C) = (Σ ASCII(Ci)) mod 2^16  

- Hash size: 16 bits (4 hexadecimal digits)  
- Message format: Ciphertext || Hash  

## Encryption Algorithm  
**Input:** Plaintext P, Key K  
**Output:** Ciphertext C  

1. Convert P to uppercase.  
2. Remove all characters not in A–Z.  
3. Repeat key K cyclically to match the length of P.  
4. For each character Pi in P:  
   - Convert Pi to numeric value (A=0, ..., Z=25)  
   - Take corresponding key digit Ki  
   - Compute Ci = (Pi + Ki) mod 26  
   - Convert Ci back to character  
5. Combine all Ci to form ciphertext C.  

## Hashing Algorithm  
**Input:** Ciphertext C  
**Output:** Hash H  

1. Initialize sum S = 0  
2. For each character Ci in C:  
   - Add ASCII(Ci) to S  
3. Compute H = S mod 2^16  
4. Convert H to a 4-digit hexadecimal value  

## Message Formation  
**Input:** Ciphertext C, Hash H  
**Output:** Final Message F  

1. Append hash H to ciphertext C  
2. F = C || H  
3. Transmit F  

## Hash Verification Algorithm  
**Input:** Received message F  
**Output:** Valid / Invalid  

1. Extract last 4 characters as H_received  
2. Remaining part is C_received  
3. Compute H_computed using hashing algorithm  
4. If H_computed equals H_received, message is VALID  
5. Otherwise, message is INVALID  

## Decryption Algorithm  
**Input:** Ciphertext C, Key K  
**Output:** Plaintext P  

1. Repeat key K cyclically to match the length of C  
2. For each character Ci in C:  
   - Convert Ci to numeric value (A=0, ..., Z=25)  
   - Take corresponding key digit Ki  
   - Compute Pi = (Ci - Ki + 26) mod 26  
   - Convert Pi back to character  
3. Combine all Pi to obtain plaintext P  

## Examples  

### Example 1  
**Input:**  
- Plaintext: `HELLO WORLD`  
- Key: `31415`  

**Step 1 – Normalization:**  
`HELLOWORLD`  

**Step 2 – Encryption (Gronsfeld Cipher):**  
`KFPMTAPSPH`  

**Step 3 – Hash Computation:**  
- ASCII sum = 766  
- Hash = `02fe`  

**Final Transmitted Message:**  
`KFPMTAPSPH02fe`  

**Receiver Side:**  
- Extract hash: `02fe`  
- Recompute hash → matches  
- Decrypt → `HELLOWORLD`  

---

### Example 2  
**Input:**  
- Plaintext: `Royal Challengers Bengaluru`  
- Key: `31415`  

**Step 1 – Normalization:**  
`ROYALCHALLENGERSBENGALURU`  

**Step 2 – Encryption:**  
`URBELFKEEMFRHIFVWEFKJDPXU`  

**Step 3 – Hash Computation:**  
- Hash = `0a5c`  

**Final Transmitted Message:**  
`URBELFKEEMFRHIFVWEFKJDPXU0a5c`  

**Receiver Side:**  
- Extract hash: `0a5c`  
- Verify → valid  
- Decrypt → `ROYALCHALLENGERSBENGALURU`  

---

## Prompts  
- How to structure the message so the receiver can separate ciphertext and hash easily?  
- How does the receiver know where the ciphertext ends and the hash begins?  
- How to fix the hash size so both sender and receiver stay consistent?  
- What minimal assumptions are needed so both sides interpret the message the same way?  

## System Workflow  
Sender: Plaintext → Encryption → Ciphertext → Hash → Final Message  
Receiver: Final Message → Split → Verify → Decrypt → Plaintext  

## Hash Size Justification  
Since H = S mod 2^16, the output satisfies 0 ≤ H < 65536, which ensures the hash is always a 16-bit value.  