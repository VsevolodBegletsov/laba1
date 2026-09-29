import unittest

from src.toolkit import __main__
from src.toolkit import calculator
from src.toolkit import converter
from src.toolkit import errors


class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calculator.evaluate("8+2"), 10.0)

    def test_subtract(self):
        self.assertEqual(calculator.evaluate("8-2"), 6.0)

    def test_multiply(self):
        self.assertEqual(calculator.evaluate("6*5"), 30.0)

    def test_divide(self):
        self.assertEqual(calculator.evaluate("10/2"), 5.0)

    def test_divide_negative(self):
        self.assertEqual(calculator.evaluate("2/-5"), -0.4)

    def test_empty_expression(self):
        with self.assertRaises(errors.EmptyExceptionError):
            calculator.evaluate(" ")

    def test_divide_zero(self):
        with self.assertRaises(errors.ZeroDivisionError):
            calculator.evaluate("2/0")

    def test_parentheses(self):
        self.assertEqual(calculator.evaluate("(2*3)/5+-2*(9-10)"), 3.2)

    def test_order(self):
        self.assertEqual(calculator.evaluate("(2*3)/5+-2*(9-10)"), -0.8)

    def test_parentheses_error(self):
        self.assertEqual(calculator.validation("(2*3)/5+-2*(9-10"), 3.2)


class TestConverter(unittest.TestCase):

    def test_convert_mass(self):
        self.assertEqual(converter.convert("2500", "g", "kg"), 2.5)

    def test_convert_length(self):
        self.assertEqual(converter.convert("9673", "cm", "km"), 0.09673)

    def test_convert_degrees(self):
        self.assertEqual(converter.convert("300", "f", "k"), 422.04)

    def test_convert_degrees_wrong(self):
        self.assertEqual(converter.convert("300", "f", "k"), 122.04)

    def test_convert_degrees_error(self):
        with self.assertRaises(errors.SameSystemsError):
            converter.convert("9673", "cm", "cm")


class TestCLI(unittest.TestCase):

    def test_cli_calc(self):
        self.assertEqual(__main__.main(["calc", "2+2"]), 0)

    def test_cli_convert(self):
        self.assertEqual(__main__.main(["convert", "2500", "--from", "g", "--to", "kg"]), 0)

    def test_cli_calc_err_1(self):
        self.assertEqual(__main__.main(["calc", "2+"]), 0)

    def test_cli_calc_err_2(self):
        self.assertEqual(__main__.main(["calc", "+2"]), 0)

    # Executing the tests in the above test case class


if __name__ == "__main__":
    unittest.main()
