from typing import Any, Dict, Optional, Union
from torch import Tensor

class PreTrainedTokenizer:
    def __call__(self, text: str, **kwargs: Any) -> Dict[str, Tensor]: ...
    def from_pretrained(cls, model_name: str, **kwargs: Any) -> "PreTrainedTokenizer": ...

class PreTrainedModel:
    def __call__(self, **kwargs: Any) -> Any: ...
    def eval(self) -> "PreTrainedModel": ...
    def from_pretrained(cls, model_name: str, **kwargs: Any) -> "PreTrainedModel": ...

class AutoTokenizer:
    @classmethod
    def from_pretrained(cls, model_name: str, **kwargs: Any) -> PreTrainedTokenizer: ...

class AutoModelForCausalLM:
    @classmethod
    def from_pretrained(cls, model_name: str, **kwargs: Any) -> PreTrainedModel: ...

class AutoModelForSequenceClassification:
    @classmethod
    def from_pretrained(cls, model_name: str, **kwargs: Any) -> PreTrainedModel: ...

class BitsAndBytesConfig:
    def __init__(self, **kwargs: Any) -> None: ...

__all__ = [
    "AutoTokenizer",
    "AutoModelForCausalLM", 
    "AutoModelForSequenceClassification",
    "BitsAndBytesConfig",
    "PreTrainedTokenizer",
    "PreTrainedModel"
]