from dataclasses import dataclass, field
from typing import FrozenSet


@dataclass(frozen=True)
class ProtectedPaths:
    all_paths: FrozenSet
    ignored: FrozenSet
    protected: FrozenSet = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'protected', frozenset(self.all_paths - self.ignored))
