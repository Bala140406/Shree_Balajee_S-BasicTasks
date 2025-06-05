import random
# No other modules are used
# Generate a random polynomial of degree k-1 with the secret as the constant term
def make_polynomial(secret, k):
    coefficients = [secret]
    for _ in range(k - 1):
        coefficients.append(random.randint(1, 100))  # Giving out random coefficients
    return coefficients

# Evaluate the polynomial at a some x
def evaluate_polynomial(coeffs, x):
    result = 0
    for i in range(len(coeffs)):
        result += coeffs[i] * (x ** i)
    return result

# Generate n shares from the polynomial
def generate_shares(secret, n, k):
    poly = make_polynomial(secret, k)
    shares = []
    for i in range(1, n + 1):
        x = i
        y = evaluate_polynomial(poly, x)
        shares.append((x, y))
    return shares

# Lagrange Interpolation method 
def reconstruct_secret(shares):
    secret = 0
    k = len(shares)

    for i in range(k):
        xi, yi = shares[i]
        li = 1

        for j in range(k):
            if i != j:
                xj, _ = shares[j]
                li *= (0 - xj) / (xi - xj)

        secret += yi * li

    return round(secret)
secret = 2025
n = 5      # Total shares
k = 3      # Minimum shares needed to reconstruct

shares = generate_shares(secret, n, k)
print("Generated Shares:", shares)

# Taking any k number of share to find the secret
recovered = reconstruct_secret(shares[:k])
print("Recovered Secret:", recovered)
