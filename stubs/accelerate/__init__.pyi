from typing import Any, Optional, Dict, Union, List

# Main accelerator class
class Accelerator:
    def __init__(self, 
                 mixed_precision: Optional[str] = ...,
                 gradient_accumulation_steps: int = ...,
                 device_placement: bool = ...,
                 **kwargs: Any) -> None: ...
    
    def prepare(self, *args: Any) -> Any: ...
    def backward(self, loss: Any) -> None: ...
    def clip_grad_norm_(self, parameters: Any, max_norm: float) -> Any: ...
    def wait_for_everyone(self) -> None: ...
    def save_state(self, output_dir: str) -> None: ...
    def load_state(self, input_dir: str) -> None: ...
    
    @property
    def device(self) -> Any: ...
    
    @property
    def is_main_process(self) -> bool: ...

# Utility functions
def notebook_launcher(function: Any, args: tuple = ..., num_processes: int = ..., **kwargs: Any) -> None: ...

def load_checkpoint_and_dispatch(
    model: Any,
    checkpoint: Union[str, Dict[str, Any]],
    device_map: Optional[Union[str, Dict[str, Any]]] = ...,
    **kwargs: Any
) -> Any: ...

def infer_auto_device_map(
    model: Any,
    max_memory: Optional[Dict[Union[int, str], Union[int, str]]] = ...,
    **kwargs: Any
) -> Dict[str, Any]: ...

__all__ = [
    "Accelerator",
    "notebook_launcher", 
    "load_checkpoint_and_dispatch",
    "infer_auto_device_map"
]