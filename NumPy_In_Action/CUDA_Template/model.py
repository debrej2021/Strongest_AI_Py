from torch import Tensor, nn

import torch_clip_scale_cuda


class _ClipAndScaleCudaFunction(torch.autograd.Function):
    @staticmethod
    def forward(ctx, input: Tensor, min_value: float, max_value: float, scale: float) -> Tensor:
        ctx.save_for_backward(input)
        ctx.min_value = min_value
        ctx.max_value = max_value
        ctx.scale = scale
        return torch_clip_scale_cuda.clip_and_scale(input, min_value, max_value, scale)

    @staticmethod
    def backward(ctx, grad_output: Tensor):
        (input,) = ctx.saved_tensors
        # d(clip(x, min, max) * scale)/dx is scale inside the range and zero outside.
        mask = (input >= ctx.min_value) & (input <= ctx.max_value)
        return grad_output * mask * ctx.scale, None, None, None


class ClipAndScaleCuda(nn.Module):
    """CUDA implementation of fused clip-and-scale for float64 tensors."""

    def __init__(
        self,
        min_value: float = 0.0,
        max_value: float = 50.0,
        scale: float = 2.0,
    ) -> None:
        super().__init__()
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")
        self.min_value = min_value
        self.max_value = max_value
        self.scale = scale

    def forward(self, input: Tensor) -> Tensor:
        return _ClipAndScaleCudaFunction.apply(
            input, self.min_value, self.max_value, self.scale
        )
