
  # 1. GPU 모델, VRAM, 드라이버 버전
neo@neo-pc:~/toy-project/2_watch_tower$ nvidia-smi  
Tue Mar 17 15:09:22 2026       
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.288.01             Driver Version: 560.94       CUDA Version: 12.6     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 3080 Ti     On  | 00000000:01:00.0 Off |                  N/A |
|  0%   30C    P8              10W / 350W |    748MiB / 12288MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A        24      G   /Xwayland                                 N/A      |
|    0   N/A  N/A       463      G   /Xwayland                                 N/A      |
|    0   N/A  N/A     85937      G   /xfwm4                                    N/A      |
+---------------------------------------------------------------------------------------+


  # 2. CUDA 버전  
neo@neo-pc:~/toy-project/2_watch_tower$   nvcc --version 2>/dev/null || echo "nvcc not installed"   
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2023 NVIDIA Corporation
Built on Mon_Apr__3_17:16:06_PDT_2023
Cuda compilation tools, release 12.1, V12.1.105
Build cuda_12.1.r12.1/compiler.32688072_0

  # 3. WSL에서 GPU 인식 확인 
neo@neo-pc:~/toy-project/2_watch_tower$  ls /usr/lib/wsl/lib/libcuda* 2>/dev/null && echo "WSL CUDA lib OK" || echo "WSL CUDA lib not found"  
/usr/lib/wsl/lib/libcuda.so  /usr/lib/wsl/lib/libcuda.so.1  /usr/lib/wsl/lib/libcuda.so.1.1  /usr/lib/wsl/lib/libcudadebugger.so.1
WSL CUDA lib OK