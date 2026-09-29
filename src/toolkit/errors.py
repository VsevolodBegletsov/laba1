class Error(Exception):
    message = "Ошибка"

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class CalculatorError(Error):
    default_message = "Ошибка валидации калькулятора"


class EmptyExceptionError(CalculatorError):
    default_message = "Введено пустое выражение"


class ExceptionStartError(CalculatorError):
    default_message = "Недопустимое начало выражения"


class ExceptionEndError(CalculatorError):
    default_message = "Недопустимое окончание выражения"


class WrongFloatError(CalculatorError):
    default_message = "Неверно введено число с плавающей точкой"


class OperatorsCountError(CalculatorError):
    default_message = "Обнаружено недопустимое количество операторов"


class WrongSymbolsError(CalculatorError):
    default_message = "Обнаружены недопустимые символы"


class ZeroDivisionError(CalculatorError):
    default_message = "Деление на ноль запрещено"


class ConverterError(Error):
    default_message = "Ошибка валидации конвертера"


class SameSystemsError(ConverterError):
    default_message = "Одинаковые системы измерения недопустимы"


class AbsoluteZeroError(ConverterError):
    default_message = "Абсолютный ноль запрещён"


class ConverterSymbolsError(ConverterError):
    default_message = "Обнаружены недопустимые знаки в конвертируемом значении"


class WrongGroupsError(ConverterError):
    default_message = "Системы измерения из несоответствующих групп"


class CLIError(Error):
    default_message = "Ошибка аргументов командной строки"


class EmptyStrokeError(CLIError):
    default_message = "Введены пустые аргументы"
