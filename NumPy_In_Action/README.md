# PyTorch C++ CPU Extension

This project mirrors the NumPy clip-and-scale example with a small PyTorch C++
extension and a Python `nn.Module` wrapper.

The C++ function accepts a contiguous CPU `torch.float64` tensor, clips values
to the configured range, multiplies by a scale, and returns a **new tensor**.
It does not modify the input. The `ClipAndScale` class in `model.py` exposes the
operation through the normal PyTorch module interface.

`clip_scale_c.c` is included as a plain-C companion for learning and comparison.
It shows the pointer-and-loop idea, but the PyTorch extension is built from
`clip_scale.cpp`: PyTorch's supported tensor C++ API (`torch::Tensor` and
`torch/extension.h`) is C++, not C. The `.c` file is not part of the build.

## Build and run (PowerShell)

Open PowerShell in this folder and run:

```powershell
cmd /k '"C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat"'
```

In the Command Prompt window that opens, run:

```cmd
python setup.py build_ext --inplace
python test_run.py
```

The extension is compiled for AVX2. It requires an x64 CPU that supports AVX2;
the current machine reports AVX2 support. The installed PyTorch build is
CPU-only, so this example uses CPU tensors and does not include a CUDA kernel.

## Files

- `clip_scale.cpp`: C++ extension function and Python binding.
- `clip_scale_c.c`: plain-C version of the core in-place array loop, for comparison.
- `setup.py`: PyTorch build configuration for MSVC.
- `model.py`: Python `nn.Module` wrapper.
- `test_run.py`: small example and a basic timing comparison.
