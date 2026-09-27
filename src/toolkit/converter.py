import argparse

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
    'c': [0, 1],
    'f': [32, 1.8],
    'k': [274.15, 1]
}

def convert(value, fr, to):
    if fr in systems_length:
        return float(value)*systems_length[to]/systems_length[fr]
    elif fr in systems_mass:
        return float(value)*systems_mass[fr]/systems_mass[to]
    elif fr in systems_degrees:
        if fr == 'c':
            return float(value)*systems_degrees[to][1]+systems_degrees[to][0]
        else:
            return float(value)/systems_degrees[to][1]-systems_degrees[to][0]

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