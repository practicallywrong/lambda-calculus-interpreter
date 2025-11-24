import re


def load_macros(filename):
    macros = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                raise SyntaxError(f"Invalid macro line: {line}")
            name, expr = line.split("=", 1)
            macros[name.strip()] = expr.strip()
    return macros


def inline_macros(text, macros):
    if not macros:
        return text

    names = list(macros.keys())
    pattern = re.compile(r"\b(" + "|".join(names) + r")\b")

    prev_text = None
    while prev_text != text:
        prev_text = text
        text = pattern.sub(lambda m: macros[m.group(0)], text)

    return text
