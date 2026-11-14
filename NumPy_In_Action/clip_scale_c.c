/*
 * C-language companion to clip_scale.cpp.
 *
 * This file contains the same CPU array loop in plain C, but it is not the
 * PyTorch extension entry point. PyTorch's public C++ extension interface uses
 * C++ (torch/extension.h), so setup.py builds clip_scale.cpp. This .c file is
 * here to make the underlying pointer-and-loop idea easy to compare with the
 * NumPy C extension. It can be compiled separately as a C library, but cannot
 * directly use torch::Tensor or be imported as this PyTorch module.
 */

#include <stddef.h>

/* Process one contiguous array of doubles in place. */
void clip_and_scale_c(double *data,
                      size_t count,
                      double min_value,
                      double max_value,
                      double scale) {
    for (size_t i = 0; i < count; ++i) {
        double value = data[i];

        if (value < min_value) {
            value = min_value;
        }
        if (value > max_value) {
            value = max_value;
        }

        data[i] = value * scale;
    }
}
