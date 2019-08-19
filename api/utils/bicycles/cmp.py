def cmp(dct1, dct2, include=None, exclude=None):
    """ Сравнить словари по определенным ключам """
    def _cmp(dct1, dct2, reverse=False):
        r = 1 + reverse
        for key, value in dct1.items():
            if exclude and key in exclude:
                continue
            if include and key not in include:
                continue
            if key not in dct2:
                print(f'{key} not in dct{3-r}, but dct{r}[{key}]=={value}')
                return False
            if dct2[key] != value:
                print(f'dct{r}[{key}]=={value}, but dct{3-r}[{key}]=={dct2[key]}')
                return False
            return True

    return _cmp(dct1, dct2) and _cmp(dct2, dct1, True)
