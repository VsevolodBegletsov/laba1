import argparse
from . import errors

systems_length = {
    'mm': 1000000,
    'cm': 100000,
    'm': 1000,
    'km': 1,
}
systems_mass = {
    'g': 1000,
    'kg': 1,
}
systems_degrees = {
    'c': [0, 1, -274.15],
    'f': [32, 1.8, -459.67],
    'k': [274.15, 1, 0]
}

def validation(value, fr, to):
    value = value.replace(' ', '')
    value = value.replace(',', '.')
    if fr == to:
        raise errors.SameSystemsError()
    if float(value)<=systems_degrees[fr][2]:
        raise errors.AbsoluteZeroError()
    for i in value:
        if i not in '0123456789.':
            raise errors.ConverterSymbolsError()
    for i in [systems_length, systems_mass, systems_degrees]:
        if fr in i and to not in i:
            raise errors.WrongGroupsError()
    return value

def convert(value, fr, to):
    value = validation(value, fr, to)
    if fr in systems_length:
        return float(value)*systems_length[to]/systems_length[fr]
    elif fr in systems_mass:
        return float(value)*systems_mass[fr]/systems_mass[to]
    elif fr in systems_degrees:
        if fr == 'c':
            return float(value)*systems_degrees[to][1]+systems_degrees[to][0]
        else:
            if fr=='f' and to=='k':
                return (float(value)+459.67)*systems_degrees[fr][1]**-1
            if fr=='k' and to=='f':
                return (float(value) - systems_degrees[fr][0]+1)*systems_degrees[to][1]+systems_degrees[to][0]
            return (float(value)-systems_degrees[fr][0])/systems_degrees[fr][1]

def evaluate(value, fr, to):
    return convert(value, fr, to)

def build_parser():
    parser = argparse.ArgumentParser(
        prog="toolkit converter",
        description="Сконвертировать различные значения",
    )
    parser.add_argument(
        "value",
        type=str,
        help='Значение, которое вы конвертируете',
    )
    parser.add_argument(
        "--from",
        dest="from_unit",
        required=True,
        help="...",
    )
    parser.add_argument(
        "--to",
        dest="to_unit",
        required=True,
        help="...",
    )
    return parser

def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        result = evaluate(args.value, args.from_unit, args.to_unit)
    except Exception as e:
        print(f"Ошибка: {e}")
        return 2

    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())