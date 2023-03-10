

csvseparator = ";;"


def spell2filename(spellname: str) -> str:
    illegals = ',<>:"/\|?*\'() '
    a = spellname.lower()
    for c in illegals:
        a = a.replace(c, '_')
    return a

