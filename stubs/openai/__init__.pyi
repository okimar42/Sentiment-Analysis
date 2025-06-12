from typing import Optional, Dict, Any, List, Union, AsyncIterator
from typing_extensions import Literal

# Main client classes
class AsyncOpenAI:
    def __init__(
        self,
        api_key: Optional[str] = ...,
        organization: Optional[str] = ...,
        base_url: Optional[str] = ...,
        timeout: Optional[float] = ...,
        max_retries: int = ...,
        default_headers: Optional[Dict[str, str]] = ...,
        default_query: Optional[Dict[str, Any]] = ...,
        **kwargs: Any
    ) -> None: ...
    
    @property
    def chat(self) -> "AsyncChat": ...
    
    @property
    def completions(self) -> "AsyncCompletions": ...
    
    @property
    def embeddings(self) -> "AsyncEmbeddings": ...
    
    @property
    def images(self) -> "AsyncImages": ...

class OpenAI:
    def __init__(
        self,
        api_key: Optional[str] = ...,
        organization: Optional[str] = ...,
        base_url: Optional[str] = ...,
        timeout: Optional[float] = ...,
        max_retries: int = ...,
        default_headers: Optional[Dict[str, str]] = ...,
        default_query: Optional[Dict[str, Any]] = ...,
        **kwargs: Any
    ) -> None: ...
    
    @property
    def chat(self) -> "Chat": ...
    
    @property
    def completions(self) -> "Completions": ...
    
    @property
    def embeddings(self) -> "Embeddings": ...
    
    @property
    def images(self) -> "Images": ...

# Response classes
class ChatCompletion:
    id: str
    object: str
    created: int
    model: str
    choices: List["ChatCompletionChoice"]
    usage: Optional["CompletionUsage"]

class ChatCompletionChoice:
    index: int
    message: "ChatCompletionMessage"
    finish_reason: Optional[str]

class ChatCompletionMessage:
    role: str
    content: Optional[str]
    function_call: Optional[Dict[str, Any]]
    tool_calls: Optional[List[Dict[str, Any]]]

class CompletionUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

# Chat interfaces
class AsyncChat:
    @property
    def completions(self) -> "AsyncChatCompletions": ...

class Chat:
    @property
    def completions(self) -> "ChatCompletions": ...

class AsyncChatCompletions:
    async def create(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        frequency_penalty: Optional[float] = ...,
        function_call: Optional[Union[str, Dict[str, Any]]] = ...,
        functions: Optional[List[Dict[str, Any]]] = ...,
        logit_bias: Optional[Dict[str, int]] = ...,
        max_tokens: Optional[int] = ...,
        n: Optional[int] = ...,
        presence_penalty: Optional[float] = ...,
        response_format: Optional[Dict[str, Any]] = ...,
        seed: Optional[int] = ...,
        stop: Optional[Union[str, List[str]]] = ...,
        stream: Optional[bool] = ...,
        temperature: Optional[float] = ...,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = ...,
        tools: Optional[List[Dict[str, Any]]] = ...,
        top_p: Optional[float] = ...,
        user: Optional[str] = ...,
        **kwargs: Any
    ) -> ChatCompletion: ...

class ChatCompletions:
    def create(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        frequency_penalty: Optional[float] = ...,
        function_call: Optional[Union[str, Dict[str, Any]]] = ...,
        functions: Optional[List[Dict[str, Any]]] = ...,
        logit_bias: Optional[Dict[str, int]] = ...,
        max_tokens: Optional[int] = ...,
        n: Optional[int] = ...,
        presence_penalty: Optional[float] = ...,
        response_format: Optional[Dict[str, Any]] = ...,
        seed: Optional[int] = ...,
        stop: Optional[Union[str, List[str]]] = ...,
        stream: Optional[bool] = ...,
        temperature: Optional[float] = ...,
        tool_choice: Optional[Union[str, Dict[str, Any]]] = ...,
        tools: Optional[List[Dict[str, Any]]] = ...,
        top_p: Optional[float] = ...,
        user: Optional[str] = ...,
        **kwargs: Any
    ) -> ChatCompletion: ...

# Completion interfaces
class AsyncCompletions:
    async def create(
        self,
        model: str,
        prompt: Optional[Union[str, List[str]]] = ...,
        max_tokens: Optional[int] = ...,
        temperature: Optional[float] = ...,
        **kwargs: Any
    ) -> Any: ...

class Completions:
    def create(
        self,
        model: str,
        prompt: Optional[Union[str, List[str]]] = ...,
        max_tokens: Optional[int] = ...,
        temperature: Optional[float] = ...,
        **kwargs: Any
    ) -> Any: ...

# Embedding interfaces
class AsyncEmbeddings:
    async def create(
        self,
        input: Union[str, List[str]],
        model: str,
        **kwargs: Any
    ) -> Any: ...

class Embeddings:
    def create(
        self,
        input: Union[str, List[str]],
        model: str,
        **kwargs: Any
    ) -> Any: ...

# Image interfaces
class AsyncImages:
    async def generate(
        self,
        prompt: str,
        model: Optional[str] = ...,
        n: Optional[int] = ...,
        size: Optional[str] = ...,
        **kwargs: Any
    ) -> Any: ...

class Images:
    def generate(
        self,
        prompt: str,
        model: Optional[str] = ...,
        n: Optional[int] = ...,
        size: Optional[str] = ...,
        **kwargs: Any
    ) -> Any: ...

__all__ = [
    "AsyncOpenAI",
    "OpenAI",
    "ChatCompletion",
    "ChatCompletionChoice", 
    "ChatCompletionMessage",
    "CompletionUsage"
]