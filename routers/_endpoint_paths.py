from dataclasses import dataclass
from re import sub


HOME = 'http://127.0.0.1:8000'


class PathCreationError(Exception):
    pass


@dataclass(frozen=True)
class EndpointPath:
    fastapi_format: str

    @property
    def stripped_relative(self):
        return sub(r'\{.+}', '', self.fastapi_format)

    @property
    def full(self):
        return HOME + self.stripped_relative

    def __post_init__(self):
        self.raise_if_no_slash_at_start()
        self.raise_if_slash_at_end()

    def raise_if_no_slash_at_start(self):
        if not self.fastapi_format.startswith('/'):
            raise PathCreationError("Relative path must start with a slash / .")

    def raise_if_slash_at_end(self):
        """ '...the prefix must not include a final /'
        See https://fastapi.tiangolo.com/tutorial/bigger-applications/#another-module-with-apirouter"""
        if self.fastapi_format.endswith('/'):
            raise PathCreationError("Relative path must not end with a slash / .")


ALL_MOVIES = EndpointPath(fastapi_format='/all_movies')
MOVIES_BY_CAT = EndpointPath(fastapi_format='/movies_by_cat')
MOVIE_BY_ID = EndpointPath(fastapi_format='/movie_details/{movie_id}')
RENT = EndpointPath(fastapi_format='/rent_movie/{movie_id}')
RETURN = EndpointPath(fastapi_format='/return/{movie_id}')
