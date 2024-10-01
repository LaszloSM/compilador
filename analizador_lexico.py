import re
import tkinter as tk
from tkinter import messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

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

    def tokenize(self):  # <--- Corrige la indentación aquí
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
                    code = code[match.end():]
                    self._update_position(match.group(0))
                    break
            if not match:
                unrecognized_token = re.match(r'\S+', code)
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

# Función para graficar el árbol sintáctico jerárquico
def graficar_arbol_sintactico(tokens):
    G = nx.DiGraph()

    # Crear nodos y relaciones entre tokens
    root_node = "Raíz"
    G.add_node(root_node)
    
    for i, token in enumerate(tokens):
        current_node = f"{token.value} ({token.type})"
        G.add_node(current_node)
        if i == 0:
            G.add_edge(root_node, current_node)
        else:
            G.add_edge(f"{tokens[i-1].value} ({tokens[i-1].type})", current_node)

    pos = graphviz_layout(G, prog='dot')  # Utilizar disposición de tipo 'dot' para un árbol jerárquico
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color=EVANGELION_PURPLE, font_size=9, font_color=EVANGELION_GREEN, font_weight='bold', node_size=3000, edge_color=EVANGELION_ORANGE)
    plt.title("Árbol Sintáctico Descendente", fontsize=16, color=EVANGELION_GREEN)
    plt.show()

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

# Función para mostrar el árbol sintáctico
def mostrar_analizador_sintactico(tokens):
    graficar_arbol_sintactico(tokens)

def graficar_arbol_sintactico(tokens):
    G = nx.DiGraph()
    
    # Crear nodos y relaciones entre tokens (simplificación)
    for i, token in enumerate(tokens):
        G.add_node(f"{token.value} ({token.type})")
        if i > 0:
            G.add_edge(f"{tokens[i-1].value} ({tokens[i-1].type})", f"{token.value} ({token.type})")
    
    pos = nx.spring_layout(G, k=1.5, iterations=50)  # Diseño del gráfico
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_color=EVANGELION_PURPLE, font_size=9, font_color=EVANGELION_GREEN, font_weight='bold', node_size=3000, edge_color=EVANGELION_ORANGE)
    plt.title("Árbol Sintáctico Descendente", fontsize=16, color=EVANGELION_GREEN)
    plt.show()

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
    boton_sintactico = tk.Button(ventana_resultado_lexico, text="Abrir Analizador Sintáctico", command=lambda: mostrar_analizador_sintactico(tokens), bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
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
    codigo_ejemplo_python_2 = '''a = 10
b = 20
suma = a + b
print(suma)
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_python_2)

# Función para cargar el código de ejemplo en C 1
def cargar_ejemplo_c_1():
    codigo_ejemplo_c_1 = '''#include <stdio.h>
int main() {
   printf("Hola, Mundo");
   return 0;
}
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_c_1)

# Función para cargar el código de ejemplo en C 2
def cargar_ejemplo_c_2():
    codigo_ejemplo_c_2 = '''#include <stdio.h>
int main() {
   int a = 10;
   int b = 20;
   int suma = a + b;
   printf("%d", suma);
   return 0;
}
'''
    texto_codigo.delete(1.0, tk.END)
    texto_codigo.insert(tk.END, codigo_ejemplo_c_2)

# Función para centrar la ventana
def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

# Función para mostrar la ventana principal del analizador
def mostrar_analizador():
    ventana_principal = tk.Tk()
    ventana_principal.title("Analizador Léxico y Sintáctico")
    ventana_principal.configure(bg=EVANGELION_BLACK)

    # Definir el tamaño de la ventana
    ancho = 1200
    alto = 800

    # Centrar la ventana
    centrar_ventana(ventana_principal, ancho, alto)

    ventana_principal.geometry(f"{ancho}x{alto}")

    # Label de selección de lenguaje
    label_lenguaje = tk.Label(ventana_principal, text="Selecciona el lenguaje:", bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
    label_lenguaje.pack(pady=10)

    global lenguaje_var
    lenguaje_var = tk.StringVar(value="Python")

    # Opciones de selección de lenguaje
    opcion_python = tk.Radiobutton(ventana_principal, text="Python", variable=lenguaje_var, value="Python", bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
    opcion_python.pack()
    opcion_c = tk.Radiobutton(ventana_principal, text="C", variable=lenguaje_var, value="C", bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
    opcion_c.pack()

    # Área de texto para el código fuente
    global texto_codigo
    texto_codigo = scrolledtext.ScrolledText(ventana_principal, wrap=tk.WORD, bg=EVANGELION_GRAY, fg=EVANGELION_GREEN)
    texto_codigo.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Botones de análisis y carga de ejemplos
    frame_botones = tk.Frame(ventana_principal, bg=EVANGELION_BLACK)
    frame_botones.pack(pady=10)

    boton_analizar = tk.Button(frame_botones, text="Analizar", command=analizar_codigo, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_analizar.grid(row=0, column=0, padx=10)

    boton_ejemplo_python_1 = tk.Button(frame_botones, text="Cargar Ejemplo Python 1", command=cargar_ejemplo_python_1, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_ejemplo_python_1.grid(row=0, column=1, padx=10)

    boton_ejemplo_python_2 = tk.Button(frame_botones, text="Cargar Ejemplo Python 2", command=cargar_ejemplo_python_2, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_ejemplo_python_2.grid(row=0, column=2, padx=10)

    boton_ejemplo_c_1 = tk.Button(frame_botones, text="Cargar Ejemplo C 1", command=cargar_ejemplo_c_1, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_ejemplo_c_1.grid(row=1, column=1, padx=10)

    boton_ejemplo_c_2 = tk.Button(frame_botones, text="Cargar Ejemplo C 2", command=cargar_ejemplo_c_2, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
    boton_ejemplo_c_2.grid(row=1, column=2, padx=10)

    ventana_principal.mainloop()

# Pantalla de inicio
pantalla_inicio = tk.Tk()
pantalla_inicio.title("Pantalla de Inicio")
pantalla_inicio.configure(bg=EVANGELION_BLACK)

# Definir el tamaño de la ventana
ancho_inicio = 600
alto_inicio = 400

# Centrar la ventana
centrar_ventana(pantalla_inicio, ancho_inicio, alto_inicio)

pantalla_inicio.geometry(f"{ancho_inicio}x{alto_inicio}")

# Texto de bienvenida
label_bienvenida = tk.Label(pantalla_inicio, text="Bienvenido al Analizador Léxico y Sintáctico", font=("Helvetica", 16), bg=EVANGELION_BLACK, fg=EVANGELION_GREEN)
label_bienvenida.pack(pady=50)

# Botón para iniciar la aplicación
boton_iniciar = tk.Button(pantalla_inicio, text="Iniciar", command=iniciar, bg=EVANGELION_PURPLE, fg=EVANGELION_GREEN)
boton_iniciar.pack(pady=20)

pantalla_inicio.mainloop()
