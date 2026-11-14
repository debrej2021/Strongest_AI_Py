from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension


extension = CUDAExtension(
    name="torch_clip_scale_cuda",
    sources=["binding.cpp", "clip_scale_cuda.cu"],
    extra_compile_args={
        "cxx": ["-O3"],
        "nvcc": ["-O3"],
    },
)

setup(
    name="torch_clip_scale_cuda",
    version="0.1.0",
    ext_modules=[extension],
    cmdclass={"build_ext": BuildExtension},
)
