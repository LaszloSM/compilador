import re

class Token:
    def __init__(self, value, token_type, line):
        self.value = value
        self.type = token_type
        self.line = line

    def __repr__(self):
        return f"Token('{self.value}', {self.type}), (Linea: {self.line})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.current_line = 1
        self.token_patterns = [
            (re.compile(r'\b(if|else|while|return|for|break|continue|print)\b'), 'KEYWORD'),
            (re.compile(r'[a-zA-Z_]\w*'), 'IDENTIFIER'),
            (re.compile(r'\d+\.\d+'), 'FLOAT'),
            (re.compile(r'\d+'), 'INTEGER'),
            (re.compile(r'==|!=|<=|>=|<|>|\+|\-|\*|\/|%|='), 'OPERATOR'),  # Añadido operador %
            (re.compile(r'[{}()\[\];,]'), 'DELIMITER'),
            (re.compile(r'//.*'), 'COMMENT'),
            (re.compile(r'/\*[\s\S]*?\*/'), 'COMMENT'),
            (re.compile(r'#.*'), 'COMMENT'),
            (re.compile(r'"[^"]*"'), 'STRING'),
            (re.compile(r"\'[^\']*\'"), 'STRING'),
            (re.compile(r'\s+'), None),  # Espacios en blanco (ignorar)
        ]

    def tokenize(self):
        tokens = []
        code = self.code

        while code:
            match = None
            for pattern, token_type in self.token_patterns:
                match = pattern.match(code)
                if match:
                    if token_type:  # Solo agregar el token si no es un espacio en blanco
                        token = Token(
                            match.group(0),
                            token_type,
                            self.current_line
                        )
                        tokens.append(token)
                    # Avanzar el puntero en el código fuente
                    code = code[match.end():]
                    self._update_position(match.group(0))
                    break
            if not match:
                # Mejor manejo del error con el token exacto no reconocido
                unrecognized_token = re.match(r'\S+', code)  # Encuentra el primer token no reconocido
                if unrecognized_token:
                    error_token = unrecognized_token.group(0)
                    raise ValueError(f"Error léxico en la línea {self.current_line}: Token no reconocido '{error_token}'")
                else:
                    raise ValueError(f"Error léxico en la línea {self.current_line}: Secuencia no reconocida cerca de '{code[:20]}'")
        return tokens

    def _update_position(self, text):
        lines = text.splitlines()
        if len(lines) > 1:
            self.current_line += len(lines) - 1

def mostrar_menu():
    print("=== Menú de Análisis Léxico ===")
    print("1. Escribir código personalizado")
    print("2. Probar con código de ejemplo 1")
    print("3. Probar con código de ejemplo 2")
    print("4. Salir")

def ejecutar_analizador(codigo_fuente):
    lexer = Lexer(codigo_fuente)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            print("Escriba su código (máximo 1000 caracteres):")
            codigo_fuente = input()
            if len(codigo_fuente) > 1000:
                print("Error: El código excede el límite de 1000 caracteres.")
            else:
                ejecutar_analizador(codigo_fuente)

        elif opcion == '2':
            codigo_fuente = '''
            int main() {
                int x = 10;
                float y = 20.5;
                if (x > y) {
                    x = x + 1;
                }
                return 0;
            }
            '''
            ejecutar_analizador(codigo_fuente)

        elif opcion == '3':
            codigo_fuente = '''
            for (int i = 0; i < 10; i++) {
                if (i % 2 == 0) {
                    continue;
                } else {
                    break;
                }
            }
            '''
            ejecutar_analizador(codigo_fuente)

        elif opcion == '4':
            print("Saliendo del programa...")
            break

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()
