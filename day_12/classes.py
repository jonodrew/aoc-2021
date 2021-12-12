import dataclasses


@dataclasses.dataclass(frozen=True)
class Cave:
    name: str
    big: bool

    def __repr__(self):
        return self.name
