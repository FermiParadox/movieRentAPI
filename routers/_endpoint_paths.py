from dataclasses import dataclass

HOME = 'http://127.0.0.1:8000'


class PathCreationError(Exception):
    pass


@dataclass(frozen=True)
class EndPointPath:
    relative: str

    @property
    def full(self):
        return HOME + self.relative

    def __post_init__(self):
        self.raise_if_no_slash_at_start()
        self.raise_if_slash_at_end()

    def raise_if_no_slash_at_start(self):
        if not self.relative.startswith('/'):
            raise PathCreationError("Relative path must start with a slash / .")

    def raise_if_slash_at_end(self):
        """ '...the prefix must not include a final /'
        See https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter"""
        if self.relative.endswith('/'):
            raise PathCreationError("Relative path must not end with a slash / .")


ALL_MOVIES = EndPointPath(relative='/all_movies')
MOVIES_BY_CAT = EndPointPath(relative='/movies_by_cat')
MOVIE_BY_ID = EndPointPath(relative='/movie_details/{movie_id}')
