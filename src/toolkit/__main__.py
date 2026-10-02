import argparse

from . import calculator
from . import converter


def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit",
        description="Vsevolod Begletsov's Toolkit (calculator and converter)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # calc
    calc_parser = subparsers.add_parser("calc", help="Вычислить выражение")
    calc_parser.add_argument("expression", type=str, help='Например: "2+2*2"')
    calc_parser.set_defaults(func=calculator.main)

    # convert
    conv_parser = subparsers.add_parser("convert", help="Перевести единицы")
    conv_parser.add_argument("value", type=str, help="Конвертируемое значение")
    conv_parser.add_argument(
        "--from", dest="from_unit", help="Из какой системы измерений хотите перевести значение", required=True
    )
    conv_parser.add_argument(
        "--to", dest="to_unit", help="В какую систему измерений хотите перевести число", required=True
    )
    conv_parser.set_defaults(func=converter.main)

    return parser


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "calc":
        return calculator.main([args.expression])
    elif args.command == "convert":
        return converter.main([str(args.value), "--from", args.from_unit, "--to", args.to_unit])
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(argv=None))
