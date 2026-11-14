from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CppExtension


extension = CppExtension(
    name="torch_clip_scale",
    sources=["clip_scale.cpp"],
    extra_compile_args={"cxx": ["/O2", "/arch:AVX2"]},
)

setup(
    name="torch_clip_scale",
    version="0.1.0",
    ext_modules=[extension],
    cmdclass={"build_ext": BuildExtension},
)
