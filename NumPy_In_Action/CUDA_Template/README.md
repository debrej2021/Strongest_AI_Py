# CUDA template: PyTorch custom extension

This folder is the GPU counterpart to the CPU extension in the parent folder.
It follows the same mathematical operation:

```text
output = clip(input, min_value, max_value) * scale
```

The main difference is execution:

| CPU extension | CUDA extension |
| --- | --- |
| AVX2 lets one CPU instruction handle four `float64` values. | Many GPU threads run concurrently; each thread handles one `float64` value. |
| `clip_scale.cpp` is compiled by the C++ compiler. | `clip_scale_cuda.cu` is compiled by NVIDIA's CUDA compiler, `nvcc`. |
| Runs with a CPU PyTorch installation. | Requires CUDA-enabled PyTorch and an NVIDIA GPU. |

`binding.cpp` connects the CUDA function to CPython. `model.py` puts that
function behind a normal PyTorch `nn.Module` and supplies a Python backward
function so it can participate in autograd.

## Run in Google Colab

1. In Colab, choose **Runtime → Change runtime type → T4 GPU** (or another GPU).
2. Upload this complete `CUDA_Template` folder, or clone/copy it into the notebook runtime.
3. In a notebook cell, change into the folder and build:

   ```python
   %cd /content/CUDA_Template
   !python setup.py build_ext --inplace
   !python test_run.py
   ```

4. Confirm the notebook sees a GPU before building:

   ```python
   import torch
   print(torch.cuda.is_available())
   print(torch.cuda.get_device_name(0))
   ```

The kernel intentionally uses `torch.float64` so it parallels the CPU and
NumPy examples. Most deep-learning workloads use `torch.float32`, `bfloat16`,
or `float16` for greater GPU throughput, so a production kernel would usually
provide versions for those data types as well.

`clip_scale_c.c` is a plain-C learning companion. It shows the direct CPU
memory loop without AVX2 or CUDA. It is intentionally not part of the CUDA
build; `.cu` is CUDA C++ and is compiled by `nvcc`.

## Files

- `clip_scale_cuda.cu`: CUDA kernel and tensor-facing CUDA function.
- `clip_scale_c.c`: plain-C CPU loop for comparison with the CUDA kernel.
- `binding.cpp`: CPython/PyTorch extension binding.
- `setup.py`: compilation configuration using `CUDAExtension`.
- `model.py`: `nn.Module` and autograd wrapper.
- `test_run.py`: correctness check and synchronized GPU timing example.
