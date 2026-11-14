/*
 * Plain-C companion to the CUDA implementation.
 *
 * This is the same one-value-at-a-time CPU algorithm. It exists for studying
 * the memory loop beside the AVX2 C++ and CUDA versions. It is not compiled by
 * setup.py and it cannot launch CUDA kernels on its own.
 */

#include <stddef.h>

void clip_and_scale_c(double *data,
                      size_t count,
                      double min_value,
                      double max_value,
                      double scale) {
    for (size_t index = 0; index < count; ++index) {
        double value = data[index];

        if (value < min_value) {
            value = min_value;
        }
        if (value > max_value) {
            value = max_value;
        }

        data[index] = value * scale;
    }
}
