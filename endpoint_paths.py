from dataclasses import dataclass

HOME = 'http://127.0.0.1:8000'


@dataclass(frozen=True)
class EndPointPath:
    relative: str

    @property
    def full(self):
        return HOME + self.relative


ALL_MOVIES = EndPointPath(relative='/all_movies')
