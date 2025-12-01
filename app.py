import sys

from lambda_calculus import Lexer, Normalizer, Parser
from macros import inline_macros, load_macros

if len(sys.argv) != 3:
    print("Usage: python app.py <lambda_file> <macro_file>")
    sys.exit(1)

lambda_file = sys.argv[1]
macro_file = sys.argv[2]

try:
    macros = load_macros(macro_file)
except Exception as e:
    print(f"Macro load error: {e}")
    sys.exit(1)

try:
    text = open(lambda_file).read().strip()
except FileNotFoundError:
    print(f"Error: file '{lambda_file}' not found")
    sys.exit(1)

try:
    expanded_text = inline_macros(text, macros)
except Exception as e:
    print(f"Macro expansion error: {e}")
    sys.exit(1)

lexer = Lexer(expanded_text)

parser = Parser(lexer, debug=False)
try:
    expr = parser.parse()
except SyntaxError as e:
    print(f"Syntax error: {e}")
    sys.exit(1)

normalizer = Normalizer()
try:
    result = normalizer.normalize(expr)
except RuntimeError as e:
    print(f"Normalization error: {e}")
    sys.exit(1)

print("Expanded expression:")
print(expanded_text)
print("Reduced result:")
print(result)
