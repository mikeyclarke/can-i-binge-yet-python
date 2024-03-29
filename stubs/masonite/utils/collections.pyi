from .structures import data_get as data_get
from _typeshed import Incomplete
from typing import Any, Callable, Iterable, Iterator, TypeVar

T = TypeVar('T', bound=Collection)

class Collection:
    __appends__: list[Any]
    def __init__(self, items: list[Any] | None = ...) -> None: ...
    def take(self, number: int) -> list[Any]: ...
    def first(self, callback: Callable[[Any], bool] | None = ...) -> Any: ...
    def last(self, callback: Callable[[Any], bool] | None = ...) -> Any: ...
    def all(self) -> list[Any]: ...
    def avg(self, key: str | None = ...) -> int | None: ...
    def max(self, key: str | None = ...) -> int | None: ...
    def chunk(self, size: int) -> int: ...
    def collapse(self) -> Collection: ...
    def contains(self, key: str, value: Any | None = ...) -> bool: ...
    def count(self) -> int: ...
    def diff(self, items: Collection | list[Any]) -> Collection: ...
    def each(self, callback: Callable[[Any], Any]) -> None: ...
    def every(self, callback: Callable[[Any], bool]) -> bool: ...
    def filter(self, callback: Callable[[Any], bool]) -> Collection: ...
    def flatten(self) -> Collection: ...
    def forget(self, *keys: list[str]) -> Collection: ...
    def for_page(self, page: int, number: int) -> Collection: ...
    def get(self, key: str, default: Any | None = ...) -> Any | None: ...
    def implode(self, glue: str = ..., key: str | None = ...) -> str: ...
    def is_empty(self) -> bool: ...
    def map(self, callback: Callable[[Any], Any]) -> Collection: ...
    def map_into(self, cls: T, method: str | None = ..., **kwargs: Any) -> Collection: ...
    def merge(self, items: Collection | list[Any]) -> Collection: ...
    def pluck(self, value: Any, key: str | None = ...) -> Collection: ...
    def pop(self) -> Any: ...
    def prepend(self, value: Any) -> Collection: ...
    def pull(self, key: str) -> Any: ...
    def push(self, value: Any) -> None: ...
    def put(self, key: str, value: Any) -> Collection: ...
    def random(self, count: int | None = ...) -> None | Collection | Any: ...
    def reduce(self, callback: Callable[[Any, Any], Any], initial: Any = ...) -> Any: ...
    def reject(self, callback: Callable[[Any], bool]) -> None: ...
    def reverse(self) -> None: ...
    def serialize(self) -> list[Any]: ...
    def add_relation(self, result: dict[str, Any] | None = ...) -> Collection: ...
    def shift(self) -> Any: ...
    def sort(self, key: str | None = ...) -> Collection: ...
    def sum(self, key: str | None = ...) -> int | None: ...
    def to_json(self, **kwargs: Any) -> str: ...
    def group_by(self, key: str) -> Collection: ...
    def transform(self, callback: Callable[[Any], Any]) -> None: ...
    def unique(self, key: str | None = ...) -> Collection: ...
    def where(self, key: str, *args: Any) -> Collection: ...
    def zip(self, items: Collection | list[Any]) -> Collection: ...
    def set_appends(self, appends: list[str]) -> Collection: ...
    def __iter__(self) -> Iterator[Any]: ...
    def __eq__(self, other: object) -> bool: ...
    def __getitem__(self, item: slice | str) -> Collection | Any: ...
    def __setitem__(self, key: str, value: Any) -> None: ...
    def __delitem__(self, key: str) -> None: ...
    def __ne__(self, other: object) -> bool: ...
    def __len__(self) -> int: ...
    def __le__(self, other: Collection | list[Any]) -> bool: ...
    def __lt__(self, other: Collection | list[Any]) -> bool: ...
    def __ge__(self, other: Collection | list[Any]) -> bool: ...
    def __gt__(self, other: Collection | list[Any]) -> bool: ...

def collect(iterable: Iterable[Any]) -> Collection: ...
def flatten(iterable: Iterable[Any]) -> list[Any]: ...
