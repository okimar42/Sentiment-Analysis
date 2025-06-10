from typing import Any, Iterator, Optional

class Submission:
    id: str
    title: str
    selftext: str
    url: str
    score: int
    num_comments: int
    author: Optional["Redditor"]
    created_utc: float
    subreddit: "Subreddit"
    
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class Comment:
    id: str
    body: str
    score: int
    author: Optional["Redditor"]
    created_utc: float
    
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class Redditor:
    name: str
    
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class Subreddit:
    display_name: str
    
    def hot(self, limit: int = ...) -> Iterator[Submission]: ...
    def new(self, limit: int = ...) -> Iterator[Submission]: ...
    def top(self, time_filter: str = ..., limit: int = ...) -> Iterator[Submission]: ...
    def search(self, query: str, **kwargs: Any) -> Iterator[Submission]: ...

class Reddit:
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    
    def subreddit(self, display_name: str) -> Subreddit: ...
    def submission(self, id: str = ..., url: str = ...) -> Submission: ...

__all__ = ["Reddit", "Submission", "Comment", "Redditor", "Subreddit"]