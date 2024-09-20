import re
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Colores inspirados en Evangelion 01
EVANGELION_PURPLE = "#4B0082"
EVANGELION_GREEN = "#7FFF00"
EVANGELION_BLACK = "#1C1C1C"
EVANGELION_GRAY = "#2F4F4F"
EVANGELION_ORANGE = "#EF7F02"


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
    ventana_resultado_lexico.geometry("400x300")
    ventana_resultado_lexico.configure(bg=EVANGELION_BLACK)


    resultado_texto = scrolledtext.ScrolledText(ventana_resultado_lexico, wrap=tk.WORD, bg=EVANGELION_GRAY, fg=EVANGELION_GREEN)
    resultado_texto.pack(expand=True, fill=tk.BOTH)


    for token in tokens:
        resultado_texto.insert(tk.END, f"{token}\n")


    # Botón para abrir el analizador sintáctico
    boton_sintactico = tk.Button(ventana_resultado_lexico, text="Abrir Analizador Sintáctico", command=mostrar_analizador_sintactico, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_sintactico.pack(pady=10)


# Función para cargar el código de ejemplo 1
def cargar_ejemplo_1():
    codigo_ejemplo_1 = '''int main() {
    int x = 10;
    float y = 20.5;
    if (x > y) {
        x = x + 1;
    }
    return 0;
}
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_1)


# Función para cargar el código de ejemplo 2
def cargar_ejemplo_2():
    codigo_ejemplo_2 = '''for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) {
        continue;
    } else {
        break;
    }
}
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_2)


# Función para mostrar el analizador léxico
def mostrar_analizador():
    ventana_principal = tk.Tk()
    ventana_principal.title("Analizador Léxico")
    ventana_principal.geometry("600x400")
    ventana_principal.configure(bg=EVANGELION_BLACK)


    global texto_codigo
    texto_codigo = scrolledtext.ScrolledText(ventana_principal, wrap=tk.WORD, width=70, height=15, bg=EVANGELION_GRAY, fg=EVANGELION_GREEN)
    texto_codigo.pack(padx=10, pady=10)


    frame_botones = tk.Frame(ventana_principal, bg=EVANGELION_BLACK)
    frame_botones.pack(pady=10)


    boton_ejemplo_1 = tk.Button(frame_botones, text="Cargar Ejemplo 1", command=cargar_ejemplo_1, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_ejemplo_1.grid(row=0, column=0, padx=10)


    boton_ejemplo_2 = tk.Button(frame_botones, text="Cargar Ejemplo 2", command=cargar_ejemplo_2, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_ejemplo_2.grid(row=0, column=1, padx=10)


    global lenguaje_var
    lenguaje_var = tk.StringVar(value="Python")
    boton_python = tk.Radiobutton(frame_botones, text="Python", variable=lenguaje_var, value="Python", bg=EVANGELION_BLACK, fg=EVANGELION_GREEN, selectcolor=EVANGELION_PURPLE)
    boton_python.grid(row=1, column=0, padx=10)


    boton_c = tk.Radiobutton(frame_botones, text="C", variable=lenguaje_var, value="C", bg=EVANGELION_BLACK, fg=EVANGELION_GREEN, selectcolor=EVANGELION_PURPLE)
    boton_c.grid(row=1, column=1, padx=10)


    boton_analizar = tk.Button(ventana_principal, text="Analizar Código", command=analizar_codigo, font=("Arial", 12), bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_analizar.pack(pady=10)


    ventana_principal.mainloop()


# Pantalla de inicio
pantalla_inicio = tk.Tk()
pantalla_inicio.title("Pantalla de Inicio")
pantalla_inicio.configure(bg=EVANGELION_BLACK)

# Desactivar redimensionado
pantalla_inicio.resizable(False, False)

# Fuentes personalizadas
titulo_fuente = ("Lucida Console", 24, "bold")
boton_fuente = ("Lucida Console", 12, "bold")
bienvenida_fuente = ("Lucida Console", 8, "bold")

# Función para centrar una ventana en el monitor
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    posicion_x = int((pantalla_ancho / 2) - (ancho / 2))
    posicion_y = int((pantalla_alto / 2) - (alto / 2))
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")
    
# Centrar la ventana
centrar_ventana(pantalla_inicio, 400, 220)

# Título con nueva fuente
bienvenida = tk.Label(pantalla_inicio, text="COMPILADOR", bg=EVANGELION_BLACK, fg=EVANGELION_GREEN, font=titulo_fuente)
bienvenida.pack(pady=30)

# Botón con nueva fuente
boton_iniciar = tk.Button(pantalla_inicio, text="Iniciar", command=iniciar, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN, font=boton_fuente)
boton_iniciar.pack()

# Mensaje de bienvenida con nueva fuente, alineado a la derecha
creadores_texto = "Creado por: Iván Martínez, Laszlo Sierra"
bienvenida = tk.Label(pantalla_inicio, text=creadores_texto, bg=EVANGELION_BLACK, fg=EVANGELION_ORANGE, font=bienvenida_fuente, anchor="e", justify="right")
bienvenida.pack(pady=30, fill="x", padx=20)

pantalla_inicio.mainloop()

