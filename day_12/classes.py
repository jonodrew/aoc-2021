import dataclasses


@dataclasses.dataclass(frozen=True)
class Cave:
    name: str
    big: bool
