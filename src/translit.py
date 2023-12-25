from argparse import ArgumentParser
from csv import writer as csv_writer

from transliteration import transliteration

DEFAULT_PASSWORD = "dVEjRhm5"
STOP_WORDS = ["stop", "STOP"]


def valid_name(name: str) -> bool:
    is_valid = True
    if len(name.split()) != 3:
        is_valid = False
    return is_valid


def parse_cli_arguments():
    parser = ArgumentParser()
    parser.add_argument("-t", "--target", help="Path to .csv file")
    parser.add_argument("-i",
                        "--interactive",
                        action="store_true",
                        help="Enable interactive mode")
    parser.add_argument("-wp",
                        "--without-print",
                        action="store_true",
                        help="Disable data printing")
    parser.add_argument("-p",
                        "--password",
                        help="Change default password",
                        default=DEFAULT_PASSWORD)
    parser.add_argument(
        "names",
        nargs="+",
        default=[""],
        help="Names in format \"Surname First name Patronymic\"")
    return parser.parse_args()


def main():
    cli_arguments = parse_cli_arguments()
    names = cli_arguments.names
    for name in names:
        if not valid_name(name):
            names.remove(name)
    if cli_arguments.interactive:
        try:
            while True:
                name = input(
                    "Введите имя пользователя (Фамилия Имя Отчество) или слово STOP (чтобы закончить): "
                ).strip()
                if name in STOP_WORDS:
                    break
                if valid_name(name):
                    names.append(name)
                else:
                    print("С данным именем что-то не так")

        except KeyboardInterrupt:
            print()

    rows = [['username:', 'password:', 'firstname:', 'lastname:']]

    for name in names:
        splitted_name = name.split()
        formatted_name = transliteration(name.lower()).split()
        login = f"{formatted_name[0]}.{formatted_name[1][0]}.{formatted_name[2][0]}"
        rows.append(
            ([login, DEFAULT_PASSWORD, splitted_name[1], splitted_name[2]]))

    if cli_arguments.target:
        writer = csv_writer(open(cli_arguments.target, "w"))
        writer.writerows(rows)

    if names and not cli_arguments.without_print:
        try:
            from pandas import DataFrame
            df = DataFrame(rows[1:], columns=rows[0])
            print(df)
        except ImportError:
            for row in rows:
                print("\t".join(row))


if __name__ == "__main__":
    main()
