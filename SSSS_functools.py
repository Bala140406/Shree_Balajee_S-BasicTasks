import numpy
import random
from functools import reduce

# Prime number (must be larger than the secret)
PRIME = 208351617316091241234326746312124448251235562226470491514186331217050270460481

# Generate random polynomial coefficients with secret as the constant term
def generate_coeffs(secret, k):
    coeffs = [secret] + [random.randrange(0, PRIME) for _ in range(k - 1)]
    return coeffs

# Evaluate the polynomial at a given x
def eval_polynomial(x, coeffs):
    return sum((coeff * pow(x, i, PRIME)) % PRIME for i, coeff in enumerate(coeffs)) % PRIME

# Split secret into n shares
def split_secret(secret, n, k):
    coeffs = generate_coeffs(secret, k)
    shares = [(i, eval_polynomial(i, coeffs)) for i in range(1, n + 1)]
    return shares

# Lagrange interpolation to recover the secret
def reconstruct_secret(shares):
    def lagrange_basis(i, x):
        xi, _ = shares[i]
        num = den = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = (num * (-xj)) % PRIME
                den = (den * (xi - xj)) % PRIME
        return num * pow(den, -1, PRIME)

    secret = 0
    for i, (_, yi) in enumerate(shares):
        li = lagrange_basis(i, 0)
        secret = (secret + yi * li) % PRIME
    return secret

# 🔥 Demo Time
if __name__ == "__main__":
    secret = 123456789  # Replace with your private key or secret
    n = 5  # total shares
    k = 3  # threshold

    shares = split_secret(secret, n, k)
    print("Shares:")
    for s in shares:
        print(s)

    # Choose any k shares to reconstruct
    selected_shares = random.sample(shares, k)
    recovered_secret = reconstruct_secret(selected_shares)
    print("\nRecovered Secret:", recovered_secret)
