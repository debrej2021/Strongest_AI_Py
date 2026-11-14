#include <torch/extension.h>
#include <immintrin.h>

#include <cstdint>

// Return a new CPU float64 tensor with values clipped to [min_value, max_value]
// and then multiplied by scale. The input tensor is left unchanged.
torch::Tensor clip_and_scale(torch::Tensor input,
                             double min_value,
                             double max_value,
                             double scale) {
    TORCH_CHECK(input.device().is_cpu(), "input must be a CPU tensor");
    TORCH_CHECK(input.scalar_type() == torch::kFloat64,
                "input must have dtype torch.float64");
    TORCH_CHECK(input.is_contiguous(), "input must be contiguous");
    TORCH_CHECK(min_value <= max_value,
                "min_value must be less than or equal to max_value");

    auto output = torch::empty_like(input);
    const auto count = input.numel();
    const double* source = input.data_ptr<double>();
    double* destination = output.data_ptr<double>();

    // AVX2 registers hold four float64 values. This fuses clipping and scaling
    // into one pass and writes each result to the new output tensor.
    const __m256d v_min = _mm256_set1_pd(min_value);
    const __m256d v_max = _mm256_set1_pd(max_value);
    const __m256d v_scale = _mm256_set1_pd(scale);
    int64_t i = 0;
    for (; i <= count - 4; i += 4) {
        __m256d values = _mm256_loadu_pd(source + i);
        values = _mm256_max_pd(values, v_min);
        values = _mm256_min_pd(values, v_max);
        values = _mm256_mul_pd(values, v_scale);
        _mm256_storeu_pd(destination + i, values);
    }

    // Handle the remaining zero to three elements.
    for (; i < count; ++i) {
        double value = source[i];
        if (value < min_value) value = min_value;
        if (value > max_value) value = max_value;
        destination[i] = value * scale;
    }

    return output;
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, module) {
    module.def("clip_and_scale", &clip_and_scale,
               "Fused clip and scale for contiguous CPU float64 tensors");
}
