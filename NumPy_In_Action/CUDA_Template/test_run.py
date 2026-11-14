import time

import torch

from model import ClipAndScaleCuda


if not torch.cuda.is_available():
    raise SystemExit("This template needs CUDA-enabled PyTorch and an NVIDIA GPU.")

print(f"PyTorch: {torch.__version__}")
print("GPU:", torch.cuda.get_device_name(0))

model = ClipAndScaleCuda(0.0, 50.0, 2.0)
example = torch.tensor([-10.0, 5.0, 25.0, 100.0], dtype=torch.float64, device="cuda")
print("Original tensor:       ", example)
print("After custom operation:", model(example))

count = 10_000_000
data = torch.empty(count, dtype=torch.float64, device="cuda").uniform_(-100.0, 100.0)

# GPU operations are asynchronous. Synchronize around timing so the measured
# interval includes the actual GPU computation.
torch.clamp(data, 0.0, 50.0) * 2.0
model(data)
torch.cuda.synchronize()

start = time.perf_counter()
reference = torch.clamp(data, 0.0, 50.0) * 2.0
torch.cuda.synchronize()
torch_time = time.perf_counter() - start

start = time.perf_counter()
custom = model(data)
torch.cuda.synchronize()
custom_time = time.perf_counter() - start

print(f"\n--- Benchmark on {count:,} CUDA float64 elements ---")
print(f"PyTorch (clamp then multiply): {torch_time * 1000:.2f} ms")
print(f"Custom CUDA fused kernel:      {custom_time * 1000:.2f} ms")
print("Results close:", torch.allclose(reference, custom))
