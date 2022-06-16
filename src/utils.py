from typing import Union, Literal

IntStrType = Union[int, str]


class ResponseCodeBracket:
    @staticmethod
    def _code_xxx(code: IntStrType, first_digit: Literal[2, 3, 4, 5]) -> bool:
        code = int(code)
        upper_ = first_digit * 100 + 100
        lower_ = first_digit * 100 - 1
        return lower_ < code < upper_

    def code_2xx(self, code: IntStrType) -> bool:
        return self._code_xxx(code=code, first_digit=2)

    def code_3xx(self, code: IntStrType) -> bool:
        return self._code_xxx(code=code, first_digit=3)

    def code_4xx(self, code: IntStrType) -> bool:
        return self._code_xxx(code=code, first_digit=4)

    def code_5xx(self, code: IntStrType) -> bool:
        return self._code_xxx(code=code, first_digit=5)
