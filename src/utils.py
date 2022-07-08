from typing import Union, Literal, Optional, NoReturn

IntStr = Union[int, str]
OptionalRaise = Optional[NoReturn]


class ResponseCode:
    @staticmethod
    def _is_xxx(code: IntStr, first_digit: Literal[2, 3, 4, 5]) -> bool:
        code = int(code)
        upper_ = first_digit * 100 + 100
        lower_ = first_digit * 100 - 1
        return lower_ < code < upper_

    def is_2xx(self, code: IntStr) -> bool:
        return self._is_xxx(code=code, first_digit=2)

    def is_3xx(self, code: IntStr) -> bool:
        return self._is_xxx(code=code, first_digit=3)

    def is_4xx(self, code: IntStr) -> bool:
        return self._is_xxx(code=code, first_digit=4)

    def is_5xx(self, code: IntStr) -> bool:
        return self._is_xxx(code=code, first_digit=5)


