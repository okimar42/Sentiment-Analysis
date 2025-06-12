from typing import Any, Dict, Optional, Union, List, Tuple
from torch import Tensor

# Base classes
class PreTrainedTokenizer:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, 
                 text: Union[str, List[str]], 
                 padding: Union[bool, str] = ...,
                 truncation: Union[bool, str] = ...,
                 max_length: Optional[int] = ...,
                 return_tensors: Optional[str] = ...,
                 **kwargs: Any) -> Dict[str, Tensor]: ...
    def encode(self, text: str, **kwargs: Any) -> List[int]: ...
    def decode(self, token_ids: Union[List[int], Tensor], **kwargs: Any) -> str: ...
    def batch_decode(self, sequences: Union[List[List[int]], Tensor], **kwargs: Any) -> List[str]: ...
    @classmethod
    def from_pretrained(cls, 
                       model_name: str, 
                       token: Optional[str] = ...,
                       trust_remote_code: bool = ...,
                       cache_dir: Optional[str] = ...,
                       local_files_only: bool = ...,
                       **kwargs: Any) -> "PreTrainedTokenizer": ...

class PreTrainedModel:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, **kwargs: Any) -> Any: ...
    def forward(self, **kwargs: Any) -> Any: ...
    def eval(self) -> "PreTrainedModel": ...
    def train(self, mode: bool = True) -> "PreTrainedModel": ...
    def cuda(self, device: Optional[Union[int, str]] = ...) -> "PreTrainedModel": ...
    def cpu(self) -> "PreTrainedModel": ...
    def to(self, device: Any = ..., dtype: Any = ..., **kwargs: Any) -> "PreTrainedModel": ...
    def parameters(self) -> Any: ...
    def named_parameters(self) -> Any: ...
    def generate(self, **kwargs: Any) -> Tensor: ...
    @classmethod
    def from_pretrained(cls, 
                       model_name: str,
                       token: Optional[str] = ...,
                       trust_remote_code: bool = ...,
                       device_map: Union[str, Dict[str, Any]] = ...,
                       cache_dir: Optional[str] = ...,
                       low_cpu_mem_usage: bool = ...,
                       torch_dtype: Optional[Any] = ...,
                       quantization_config: Optional[Any] = ...,
                       local_files_only: bool = ...,
                       **kwargs: Any) -> "PreTrainedModel": ...

# Auto classes
class AutoTokenizer:
    @classmethod
    def from_pretrained(cls, 
                       model_name: str,
                       token: Optional[str] = ...,
                       trust_remote_code: bool = ...,
                       cache_dir: Optional[str] = ...,
                       local_files_only: bool = ...,
                       **kwargs: Any) -> PreTrainedTokenizer: ...

class AutoModelForCausalLM:
    @classmethod
    def from_pretrained(cls, 
                       model_name: str,
                       token: Optional[str] = ...,
                       trust_remote_code: bool = ...,
                       device_map: Union[str, Dict[str, Any]] = ...,
                       cache_dir: Optional[str] = ...,
                       low_cpu_mem_usage: bool = ...,
                       torch_dtype: Optional[Any] = ...,
                       quantization_config: Optional[Any] = ...,
                       local_files_only: bool = ...,
                       **kwargs: Any) -> PreTrainedModel: ...

class AutoModelForSequenceClassification:
    @classmethod
    def from_pretrained(cls, 
                       model_name: str,
                       token: Optional[str] = ...,
                       trust_remote_code: bool = ...,
                       device_map: Union[str, Dict[str, Any]] = ...,
                       cache_dir: Optional[str] = ...,
                       low_cpu_mem_usage: bool = ...,
                       torch_dtype: Optional[Any] = ...,
                       quantization_config: Optional[Any] = ...,
                       local_files_only: bool = ...,
                       **kwargs: Any) -> PreTrainedModel: ...

# Quantization configuration
class BitsAndBytesConfig:
    def __init__(self, 
                 load_in_8bit: bool = ...,
                 load_in_4bit: bool = ...,
                 llm_int8_enable_fp32_cpu_offload: bool = ...,
                 bnb_4bit_use_double_quant: bool = ...,
                 bnb_4bit_quant_type: str = ...,
                 bnb_4bit_compute_dtype: Optional[Any] = ...,
                 **kwargs: Any) -> None: ...

# Model outputs
class ModelOutput:
    logits: Optional[Tensor]
    hidden_states: Optional[Tuple[Tensor, ...]]
    attentions: Optional[Tuple[Tensor, ...]]
    def __getitem__(self, key: str) -> Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def keys(self) -> Any: ...
    def values(self) -> Any: ...
    def items(self) -> Any: ...

__all__ = [
    "AutoTokenizer",
    "AutoModelForCausalLM", 
    "AutoModelForSequenceClassification",
    "BitsAndBytesConfig",
    "PreTrainedTokenizer",
    "PreTrainedModel",
    "ModelOutput"
]