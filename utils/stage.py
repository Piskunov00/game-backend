from enum import Enum


class Stage(Enum):
    """ Дополнение к Enum для возможности принадлежности к нескольким типам """

    FULL = 'All available stages'
    ONLY_VALIDATE = 'Only validate with form'
    ONLY_AUTHENTICATING = 'Only validate with form'

    @property
    def _code(self):
        return {
            Stage.FULL: 1 + 2,
            Stage.ONLY_VALIDATE: 1,
            Stage.ONLY_AUTHENTICATING: 2,
        }.get(self, 0)

    def __getitem__(self, item):
        return {
                   'validate_form': 1,
                   'authenticated': 2,
               }.get(item, 0) & self._code
