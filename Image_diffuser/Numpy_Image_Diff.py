import numpy as np

np.random.seed(0)
image = np.array([0.0, 1.0, 1.0, 0.0])        # a tiny "picture"
steps, beta = 10, 0.1

# Forward: add noise step by step
x = image.copy()
noises = []
for _ in range(steps):
    n = np.random.randn(4)
    noises.append(n)
    x = np.sqrt(1 - beta) * x + np.sqrt(beta) * n
print("noisy:", x.round(2))

# Reverse: a perfect "model" that knows the noise, removes it step by step
for n in reversed(noises):
    x = (x - np.sqrt(beta) * n) / np.sqrt(1 - beta)
print("recovered:", x.round(2))   # back to [0, 1, 1, 0]