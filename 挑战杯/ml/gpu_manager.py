import torch
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo

class GPUManager:
    def __init__(self):
        self.device = None
        self.handle = None
        self._init_gpu()
    
    def _init_gpu(self):
        if torch.cuda.is_available():
            nvmlInit()
            self.device = torch.device("cuda")
            torch.backends.cudnn.benchmark = True
            torch.cuda.set_per_process_memory_fraction(0.8)
        else:
            raise RuntimeError("No GPU available")

    def get_status(self):
        handle = nvmlDeviceGetHandleByIndex(0)
        mem = nvmlDeviceGetMemoryInfo(handle)
        return {
            "total": mem.total,
            "used": mem.used,
            "utilization": torch.cuda.utilization()
        }

gpu_manager = GPUManager()