class Parser:
    @staticmethod
    def index(array: list, key: str):
        for index, item in enumerate(array):
            if item == key:
                return index

        return -1

    def parse(self, argv: list) -> dict:
        argv = argv[1:]

        parsed = dict()

        parsed['help'] = False

        if len(argv) == 1:
            if argv[0] == '-h' or argv[0] == '--help':
                parsed['help'] = True
                parsed['help_text'] = \
                    '-id <id> - мы хотим получить топ друзей пользователя с этим идентификатором\n'

                return parsed

            raise ValueError('Неправильный набор параметров. Вызовите утилиту с флагом -h или --help')

        if '-id' not in argv:
            raise ValueError('Вы не ввели id пользователя')

        id_index = self.index(argv, '-id')

        if (id_index == len(argv) - 1) or (argv[id_index + 1] is None):
            raise ValueError('Вы не ввели id пользователя')

        parsed['id'] = argv[id_index + 1]
        try:
            int(parsed['id'])
        except ValueError:
            raise ValueError('id должен быть целочисленным типом')

        if len(argv) != 2:
            raise ValueError('Неверное количество параметров')

        return parsed

