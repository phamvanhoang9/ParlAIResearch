import torch

# Check if CUDA (NVIDIA GPU support) is available
if torch.cuda.is_available():
    # Get the number of available GPUs
    num_gpus = torch.cuda.device_count()

    print(f"Number of available GPUs: {num_gpus}")

    # Iterate through available GPUs and print their properties
    for i in range(num_gpus):
        gpu = torch.cuda.get_device_properties(i)
        print(f"GPU {i} Name: {gpu.name}")
        print(f"GPU {i} Memory Total: {gpu.total_memory / 1024**3:.2f} GB")
        print(f"GPU {i} Compute Capability: {gpu.major}.{gpu.minor}") 
else:
    print("CUDA is not available. Only CPU is accessible.")
