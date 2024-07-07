import torch

# Check if CUDA is available
is_cuda_available = torch.cuda.is_available()
print(f"CUDA Available: {is_cuda_available}")

if is_cuda_available:
    # Get the number of GPUs
    num_gpus = torch.cuda.device_count()
    print(f"Number of GPUs: {num_gpus}")

    # Print the name of each GPU
    for i in range(num_gpus):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")

    # Test tensor operations on GPU
    try:
        device = torch.device("cuda")
        tensor = torch.tensor([1.0, 2.0, 3.0], device=device)
        print(f"Tensor on GPU: {tensor}")
    except Exception as e:
        print(f"Error performing operations on GPU: {e}")
