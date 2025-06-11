from typing import Optional, Dict, Any, Union, IO, Tuple, List
from typing_extensions import Literal

# Response class
class Response:
    status_code: int
    headers: Dict[str, str]
    content: bytes
    text: str
    url: str
    encoding: Optional[str]
    reason: str
    cookies: "RequestsCookieJar"
    history: List["Response"]
    request: "PreparedRequest"
    
    def json(self, **kwargs: Any) -> Any: ...
    def raise_for_status(self) -> None: ...
    def iter_content(self, chunk_size: Optional[int] = ..., decode_unicode: bool = ...) -> Any: ...
    def iter_lines(self, chunk_size: Optional[int] = ..., decode_unicode: bool = ..., delimiter: Optional[Union[str, bytes]] = ...) -> Any: ...

# Session class
class Session:
    def __init__(self) -> None: ...
    def request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = ...,
        data: Optional[Union[Dict[str, Any], str, bytes]] = ...,
        headers: Optional[Dict[str, str]] = ...,
        cookies: Optional[Dict[str, str]] = ...,
        files: Optional[Dict[str, IO[bytes]]] = ...,
        auth: Optional[Tuple[str, str]] = ...,
        timeout: Optional[Union[float, Tuple[float, float]]] = ...,
        allow_redirects: bool = ...,
        proxies: Optional[Dict[str, str]] = ...,
        verify: Union[bool, str] = ...,
        stream: bool = ...,
        cert: Optional[Union[str, Tuple[str, str]]] = ...,
        **kwargs: Any
    ) -> Response: ...
    
    def get(self, url: str, **kwargs: Any) -> Response: ...
    def post(self, url: str, data: Optional[Any] = ..., json: Optional[Any] = ..., **kwargs: Any) -> Response: ...
    def put(self, url: str, data: Optional[Any] = ..., **kwargs: Any) -> Response: ...
    def patch(self, url: str, data: Optional[Any] = ..., **kwargs: Any) -> Response: ...
    def delete(self, url: str, **kwargs: Any) -> Response: ...
    def head(self, url: str, **kwargs: Any) -> Response: ...
    def options(self, url: str, **kwargs: Any) -> Response: ...
    
    def close(self) -> None: ...

class PreparedRequest:
    method: Optional[str]
    url: Optional[str]
    headers: Dict[str, str]
    body: Optional[Union[str, bytes]]
    
class RequestsCookieJar:
    def get(self, name: str, default: Optional[str] = ..., domain: Optional[str] = ..., path: Optional[str] = ...) -> Optional[str]: ...

# Main module functions
def request(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = ...,
    data: Optional[Union[Dict[str, Any], str, bytes]] = ...,
    headers: Optional[Dict[str, str]] = ...,
    cookies: Optional[Dict[str, str]] = ...,
    files: Optional[Dict[str, IO[bytes]]] = ...,
    auth: Optional[Tuple[str, str]] = ...,
    timeout: Optional[Union[float, Tuple[float, float]]] = ...,
    allow_redirects: bool = ...,
    proxies: Optional[Dict[str, str]] = ...,
    verify: Union[bool, str] = ...,
    stream: bool = ...,
    cert: Optional[Union[str, Tuple[str, str]]] = ...,
    **kwargs: Any
) -> Response: ...

def get(url: str, params: Optional[Dict[str, Any]] = ..., **kwargs: Any) -> Response: ...
def post(url: str, data: Optional[Any] = ..., json: Optional[Any] = ..., **kwargs: Any) -> Response: ...
def put(url: str, data: Optional[Any] = ..., **kwargs: Any) -> Response: ...
def patch(url: str, data: Optional[Any] = ..., **kwargs: Any) -> Response: ...
def delete(url: str, **kwargs: Any) -> Response: ...
def head(url: str, **kwargs: Any) -> Response: ...
def options(url: str, **kwargs: Any) -> Response: ...

# Exception classes
class RequestException(Exception): ...
class HTTPError(RequestException): ...
class ConnectionError(RequestException): ...
class Timeout(RequestException): ...
class URLRequired(RequestException): ...
class TooManyRedirects(RequestException): ...
class MissingSchema(RequestException): ...
class InvalidSchema(RequestException): ...
class InvalidURL(RequestException): ...

__all__ = [
    "Response",
    "Session", 
    "PreparedRequest",
    "RequestsCookieJar",
    "request",
    "get",
    "post", 
    "put",
    "patch",
    "delete",
    "head", 
    "options",
    "RequestException",
    "HTTPError",
    "ConnectionError",
    "Timeout",
    "URLRequired",
    "TooManyRedirects",
    "MissingSchema",
    "InvalidSchema",
    "InvalidURL"
]