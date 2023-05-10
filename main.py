import sys

from api import Api
from cli_parser import Parser


def main():
    try:
        settings = Parser().parse(sys.argv)

        if settings.get('help'):
            print(settings.get('help_text'))
            return

        top_friends = Api().get_top_friends(settings)

        for friend in top_friends:
            print(friend)
    except ValueError as e:
        print(f'Error: {e}')
        return


if __name__ == '__main__':
    main()