#include <torch/extension.h>

torch::Tensor clip_and_scale_cuda(torch::Tensor input,
                                  double min_value,
                                  double max_value,
                                  double scale);

PYBIND11_MODULE(TORCH_EXTENSION_NAME, module) {
    module.def("clip_and_scale", &clip_and_scale_cuda,
               "Fused CUDA clip and scale for contiguous float64 tensors");
}
