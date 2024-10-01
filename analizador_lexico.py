import re
import tkinter as tk
from tkinter import messagebox, scrolledtext


# Colores inspirados en Evangelion 01
EVANGELION_PURPLE = "#734f9a"
EVANGELION_GREEN = "#8bd450"
EVANGELION_BLACK = "#1c1c1c"
EVANGELION_GRAY = "#2f4f4f"
EVANGELION_ORANGE = "#ec7744"


# Palabras clave para Python
python_keywords = r'\b(False|await|else|import|pass|None|break|except|in|raise|True|class|finally|is|return|' \
                  r'and|continue|for|lambda|try|as|def|from|nonlocal|while|assert|del|global|not|with|' \
                  r'async|elif|if|or|yield|print)\b'


# Palabras clave para C
c_keywords = r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|' \
             r'if|inline|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|' \
             r'union|unsigned|void|volatile|while|print)\b'


# Operadores de Python
python_operators = r'==|!=|<=|>=|<|>|\+|\-|\*|\/|%|=|//|>>|<<|\*\*|\+=|\-=|\*=|\/=|%=|&|\||\^|~'


# Operadores de C
c_operators = r'==|!=|<=|>=|<|>|\+|\-|\*|\/|%|=|>>|<<|\+=|\-=|\*=|\/=|%=|&|\||\^|~|&&|\|\|'


# Delimitadores comunes
delimiters = r'[{}()\[\];:,]'


# Comentarios en Python
python_comments = r'#.*'


# Comentarios en C
c_comments = r'//.*|/\*[\s\S]*?\*/'


# Strings comunes
strings = r'"[^"]*"|\'[^\']*\''


# Identificadores comunes
identifiers = r'[a-zA-Z_]\w*'


# Números (flotantes e enteros)
floats = r'\d+\.\d+'
integers = r'\d+'


# Espacios en blanco
whitespace = r'\s+'


# Clase Token
class Token:
    def __init__(self, value, token_type, line):
        self.value = value
        self.type = token_type
        self.line = line


    def __repr__(self):
        return f"- Línea: {self.line} - Token: [ {self.value} ]   -> {self.type}"


# Clase Lexer (Analizador Léxico)
class Lexer:
    def __init__(self, code, language):
        self.code = code
        self.current_line = 1


        # Define patrones según el lenguaje
        if language == "Python":
            self.token_patterns = [
                (re.compile(python_keywords), 'KEYWORD'),
                (re.compile(python_operators), 'OPERATOR'),
                (re.compile(python_comments), 'COMMENT'),
                (re.compile(strings), 'STRING'),
                (re.compile(floats), 'FLOAT'),
                (re.compile(integers), 'INTEGER'),
                (re.compile(identifiers), 'IDENTIFIER'),
                (re.compile(delimiters), 'DELIMITER'),
                (re.compile(whitespace), None),  # Ignorar espacios en blanco
            ]
        elif language == "C":
            self.token_patterns = [
                (re.compile(c_keywords), 'KEYWORD'),
                (re.compile(c_operators), 'OPERATOR'),
                (re.compile(c_comments), 'COMMENT'),
                (re.compile(strings), 'STRING'),
                (re.compile(floats), 'FLOAT'),
                (re.compile(integers), 'INTEGER'),
                (re.compile(identifiers), 'IDENTIFIER'),
                (re.compile(delimiters), 'DELIMITER'),
                (re.compile(whitespace), None),  # Ignorar espacios en blanco
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
                # Mejor manejo del error con el token no reconocido
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


# Función para iniciar la aplicación
def iniciar():
    pantalla_inicio.destroy()
    mostrar_analizador()


# Función para analizar el código léxicamente
def analizar_codigo():
    codigo = texto_codigo.get("1.0", tk.END).strip()
    if not codigo:
        messagebox.showerror("Error", "Debe ingresar algún código para analizar.")
        return
    try:
        lenguaje = lenguaje_var.get()
        lexer = Lexer(codigo, lenguaje)
        tokens = lexer.tokenize()
        mostrar_resultado_lexico(tokens)
    except ValueError as e:
        messagebox.showerror("Error Léxico", str(e))


def mostrar_analizador_sintactico():
    messagebox.showinfo("Analizador Sintáctico", "Analizador sintáctico aún no implementado.")


# Función para mostrar los tokens del análisis léxico en otra ventana
def mostrar_resultado_lexico(tokens):
    ventana_resultado_lexico = tk.Toplevel()
    ventana_resultado_lexico.title("Resultado del Análisis Léxico")
    ventana_resultado_lexico.configure(bg=EVANGELION_BLACK)


    # Definir el tamaño de la ventana
    ancho = 1200
    alto = 800


    # Centrar la ventana
    centrar_ventana(ventana_resultado_lexico, ancho, alto)


    ventana_resultado_lexico.geometry(f"{ancho}x{alto}")


    resultado_texto = scrolledtext.ScrolledText(ventana_resultado_lexico, wrap=tk.WORD, bg=EVANGELION_GRAY, fg=EVANGELION_GREEN)
    resultado_texto.pack(expand=True, fill=tk.BOTH)


    for token in tokens:
        resultado_texto.insert(tk.END, f"{token}\n")


    # Botón para abrir el analizador sintáctico
    boton_sintactico = tk.Button(ventana_resultado_lexico, text="Abrir Analizador Sintáctico", command=mostrar_analizador_sintactico, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_sintactico.pack(pady=10)
# Función para cargar el código de ejemplo en Python 1
def cargar_ejemplo_python_1():
    codigo_ejemplo_python_1 = '''def saludo():
    print("Hola, mundo")
saludo()
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_python_1)


# Función para cargar el código de ejemplo en Python 2
def cargar_ejemplo_python_2():
    codigo_ejemplo_python_2 = '''for i in range(5):
    if i % 2 == 0:
        print(f"{i} es par")
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_python_2)


# Función para cargar el código de ejemplo en C 1
def cargar_ejemplo_c_1():
    codigo_ejemplo_c_1 = '''int main() {
    int x = 10;
    float y = 20.5;
    if (x > y) {
        x = x + 1;
    }
    return 0;
}
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_c_1)


# Función para cargar el código de ejemplo en C 2
def cargar_ejemplo_c_2():
    codigo_ejemplo_c_2 = '''for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) {
        continue;
    } else {
        break;
    }
}
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_c_2)


# Función para mostrar el analizador léxico
def mostrar_analizador():
    ventana_principal = tk.Tk()
    ventana_principal.title("Analizador Léxico")
    ventana_principal.configure(bg=EVANGELION_BLACK)


    # Definir el tamaño de la ventana
    ancho = 1000
    alto = 750


    # Centrar la ventana
    centrar_ventana(ventana_principal, ancho, alto)


    ventana_principal.geometry(f"{ancho}x{alto}")


    # Etiqueta del lenguaje
    etiqueta_lenguaje = tk.Label(ventana_principal, text="Seleccione el lenguaje:", font=("Courier New", 12), bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
    etiqueta_lenguaje.pack(pady=10)


    # Opción de lenguaje
    global lenguaje_var
    lenguaje_var = tk.StringVar(value="Python")
    opcion_python = tk.Radiobutton(ventana_principal, text="Python", variable=lenguaje_var, value="Python", font=("Courier New", 12), bg=EVANGELION_BLACK, fg=EVANGELION_ORANGE)
    opcion_c = tk.Radiobutton(ventana_principal, text="C", variable=lenguaje_var, value="C", font=("Courier New", 12), bg=EVANGELION_BLACK, fg=EVANGELION_ORANGE)
    opcion_python.pack()
    opcion_c.pack()


    # Área de texto para el código fuente
    global texto_codigo
    texto_codigo = scrolledtext.ScrolledText(ventana_principal, wrap=tk.WORD, bg=EVANGELION_GRAY, fg=EVANGELION_GREEN)
    texto_codigo.pack(expand=True, fill=tk.BOTH)


    # Botón para analizar el código
    boton_analizar = tk.Button(ventana_principal, text="Analizar Código", command=analizar_codigo, font=("Courier New", 12), bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_analizar.pack(pady=10)


    # Menú de ejemplos
    menu_ejemplos = tk.Menu(ventana_principal)
    ventana_principal.config(menu=menu_ejemplos)


    submenu_python = tk.Menu(menu_ejemplos, tearoff=0)
    submenu_python.add_command(label="Ejemplo Python 1", command=cargar_ejemplo_python_1)
    submenu_python.add_command(label="Ejemplo Python 2", command=cargar_ejemplo_python_2)
    menu_ejemplos.add_cascade(label="Ejemplos Python", menu=submenu_python)


    submenu_c = tk.Menu(menu_ejemplos, tearoff=0)
    submenu_c.add_command(label="Ejemplo C 1", command=cargar_ejemplo_c_1)
    submenu_c.add_command(label="Ejemplo C 2", command=cargar_ejemplo_c_2)
    menu_ejemplos.add_cascade(label="Ejemplos C", menu=submenu_c)


    ventana_principal.mainloop()


# Función para centrar la ventana
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    posicion_x = int((pantalla_ancho / 2) - (ancho / 2))
    posicion_y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")


# Pantalla de inicio
pantalla_inicio = tk.Tk()
pantalla_inicio.title("Analizador Léxico")
pantalla_inicio.configure(bg=EVANGELION_BLACK)
pantalla_inicio.resizable(False, False)


# Configurar tamaño y centrar la pantalla de inicio
centrar_ventana(pantalla_inicio, 400, 350)


# Fuentes
titulo_fuente = ("Courier New", 20, "bold")
bienvenida_fuente = ("Courier New", 12)
boton_fuente = ("Courier New", 14)


# Widgets en la pantalla de inicio
etiqueta_titulo = tk.Label(pantalla_inicio, text="COMPILADOR", font=titulo_fuente, bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
etiqueta_titulo.pack(pady=30)


etiqueta_bienvenida = tk.Label(pantalla_inicio, text="Bienvenido al COMPILADOR\nElige tu lenguaje y código a analizar", font=bienvenida_fuente, bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
etiqueta_bienvenida.pack(pady=10)


boton_iniciar = tk.Button(pantalla_inicio, text="Iniciar", command=iniciar, font=boton_fuente, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
boton_iniciar.pack(pady=20)
etiqueta_bienvenida = tk.Label(pantalla_inicio, text="by:\nIvan Martinez\nLaszlo Sierra", font=bienvenida_fuente, bg=EVANGELION_BLACK, fg=EVANGELION_ORANGE)
etiqueta_bienvenida.pack(pady=10)


pantalla_inicio.mainloop()



