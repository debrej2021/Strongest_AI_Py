import time

import torch

from model import ClipAndScale


print(f"PyTorch {torch.__version__}")
print("CUDA available:", torch.cuda.is_available())

# Small correctness example.
model = ClipAndScale(min_value=0.0, max_value=50.0, scale=2.0)
example = torch.tensor([-10.0, 5.0, 25.0, 100.0], dtype=torch.float64)
print("Original tensor:       ", example)
print("After custom operation:", model(example))
print("Input is unchanged:     ", example)

# A simple timing comparison. Both paths return a new tensor and do equivalent
# work. Timings vary with CPU load, thermal state, and PyTorch thread settings.
count = 10_000_000
data = torch.empty(count, dtype=torch.float64).uniform_(-100.0, 100.0)

# Warm up PyTorch and the extension before timing.
torch.clamp(data, 0.0, 50.0) * 2.0
model(data)

start = time.perf_counter()
reference = torch.clamp(data, 0.0, 50.0) * 2.0
torch_time = time.perf_counter() - start

start = time.perf_counter()
custom = model(data)
custom_time = time.perf_counter() - start

print(f"\n--- Benchmark on {count:,} float64 elements ---")
print(f"PyTorch (clamp then multiply): {torch_time * 1000:.2f} ms")
print(f"Custom C++ fused operation:    {custom_time * 1000:.2f} ms")
print("Results close:", torch.allclose(reference, custom))
