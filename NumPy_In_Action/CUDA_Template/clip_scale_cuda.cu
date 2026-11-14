#include <torch/extension.h>

#include <ATen/cuda/CUDAContext.h>
#include <c10/cuda/CUDAGuard.h>
#include <c10/cuda/CUDAException.h>

// Each GPU thread handles one float64 value. CUDA launches many such threads
// concurrently across the GPU's streaming multiprocessors.
__global__ void clip_and_scale_kernel(const double* input,
                                      double* output,
                                      int64_t count,
                                      double min_value,
                                      double max_value,
                                      double scale) {
    const int64_t index = static_cast<int64_t>(blockIdx.x) * blockDim.x + threadIdx.x;
    if (index < count) {
        double value = input[index];
        value = value < min_value ? min_value : value;
        value = value > max_value ? max_value : value;
        output[index] = value * scale;
    }
}

torch::Tensor clip_and_scale_cuda(torch::Tensor input,
                                  double min_value,
                                  double max_value,
                                  double scale) {
    TORCH_CHECK(input.is_cuda(), "input must be a CUDA tensor");
    TORCH_CHECK(input.scalar_type() == torch::kFloat64,
                "input must have dtype torch.float64");
    TORCH_CHECK(input.is_contiguous(), "input must be contiguous");
    TORCH_CHECK(min_value <= max_value,
                "min_value must be less than or equal to max_value");

    c10::cuda::CUDAGuard device_guard(input.device());
    auto output = torch::empty_like(input);
    const int64_t count = input.numel();
    constexpr int threads_per_block = 256;
    const int blocks = static_cast<int>((count + threads_per_block - 1) / threads_per_block);

    clip_and_scale_kernel<<<blocks, threads_per_block, 0, at::cuda::getDefaultCUDAStream()>>>(
        input.data_ptr<double>(),
        output.data_ptr<double>(),
        count,
        min_value,
        max_value,
        scale);
    C10_CUDA_KERNEL_LAUNCH_CHECK();

    return output;
}
