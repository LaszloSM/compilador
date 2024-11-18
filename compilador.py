import re
import keyword
import tkinter as tk
from tkinter import messagebox, scrolledtext
from graphviz import Digraph
from PIL import Image, ImageTk

# Patrones de análisis léxico
TOKENS_PYTHON = [
    ('COMENTARIO_LINEA', r'#.*'),
    ('CADENA_MULTILINEA', r'("""[\s\S]*?"""|\'\'\'[\s\S]*?\')'),
    ('CADENA', r'"[^"\n]*"|\'[^\']*\''),  
    ('OPERADOR_LOGICO', r'and|or|not|&&|\|\|'),  
    ('OPERADOR_COMPARACION', r'==|!=|<=|>=|<|>'),
    ('OPERADOR_ASIGNACION', r'[\+\-\*/]?='),  
    ('OPERADOR_ARITMETICO', r'[+\-*/%]'),
    ('PUNTUACION', r'[;,\(\)\{\}\[\]\.:]'),
    ('IDENTIFICADOR', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('NUMERO', r'\d+(\.\d+)?'),  
    ('ESPACIO', r'\s+'),  
]

PALABRAS_CLAVE = keyword.kwlist

# Funciones del compilador
def es_palabra_clave(palabra):
    return palabra in PALABRAS_CLAVE

def analizador_lexico(codigo_fuente):
    tokens_encontrados = []
    lineas = codigo_fuente.splitlines()

    for num_linea, linea in enumerate(lineas, start=1):
        posicion = 0
        while posicion < len(linea):
            for token_tipo, patron in TOKENS_PYTHON:
                patron_compilado = re.compile(patron)
                coincidencia = patron_compilado.match(linea, posicion)
                if coincidencia:
                    texto = coincidencia.group(0)
                    if token_tipo != 'ESPACIO':  
                        if token_tipo == 'IDENTIFICADOR' and es_palabra_clave(texto):
                            tokens_encontrados.append((num_linea, 'PALABRA_CLAVE', texto))
                        else:
                            tokens_encontrados.append((num_linea, token_tipo, texto))
                    posicion = coincidencia.end(0)
                    break
    return tokens_encontrados

# Implementación de árbol sintáctico descendente
def construir_arbol_sintactico(tokens):
    """
    Construye un árbol sintáctico descendente de acuerdo a las reglas gramaticales.
    """
    arbol = {}
    
    def analizar_expresion(tokens):
        if not tokens:
            return None, tokens
        
        token = tokens[0]
        tipo, valor = token[1], token[2]
        
        if tipo == "IDENTIFICADOR":
            return {"tipo": "IDENTIFICADOR", "valor": valor}, tokens[1:]
        elif tipo == "NUMERO":
            return {"tipo": "NUMERO", "valor": valor}, tokens[1:]
        elif tipo == "OPERADOR_ARITMETICO":
            operador = valor
            izquierda, tokens_restantes = analizar_expresion(tokens[1:])
            derecha, tokens_restantes = analizar_expresion(tokens_restantes)
            return {"tipo": "EXPRESION", "operador": operador, "izquierda": izquierda, "derecha": derecha}, tokens_restantes
        
        return None, tokens
    
    arbol, _ = analizar_expresion(tokens)
    return arbol

def construir_arbol_sintactico(tokens, nombre_programa):
    g = Digraph('G', format='png')
    g.attr(size='10,10', dpi='300')  # Tamaño y DPI
    nodo_id = 0
    pila_nodos = []

    def nuevo_nodo(etiqueta):
        nonlocal nodo_id
        nodo_id += 1
        return f"nodo{nodo_id}", etiqueta

    raiz_id, raiz_etiqueta = nuevo_nodo(f"Programa: {nombre_programa}")
    g.node(raiz_id, raiz_etiqueta, shape='rect', style='filled', fillcolor='#A0D3E8')
    nodo_actual = raiz_id

    for token in tokens:
        tipo, texto = token[1], token[2]
        if tipo in ["PALABRA_CLAVE", "OPERADOR_ASIGNACION", "OPERADOR_COMPARACION", "OPERADOR_ARITMETICO"]:
            id_hijo, etiqueta_hijo = nuevo_nodo(texto)
            g.node(id_hijo, etiqueta_hijo)
            g.edge(nodo_actual, id_hijo)
            pila_nodos.append(nodo_actual)
            nodo_actual = id_hijo
        elif tipo in ["NUMERO", "IDENTIFICADOR"]:
            id_hijo, etiqueta_hijo = nuevo_nodo(texto)
            g.node(id_hijo, etiqueta_hijo)
            g.edge(nodo_actual, id_hijo)
        elif tipo == "PUNTUACION" and texto == ';':
            if pila_nodos:
                nodo_actual = pila_nodos.pop()

    g.render('arbol_sintactico', format='png', view=True)
    messagebox.showinfo("Árbol Sintáctico", "Se generó el árbol sintáctico. Verifica 'arbol_sintactico.png'.")

# Funciones de análisis semántico
def analizador_semantico(tokens):
    errores = []
    variables_definidas = set()

    for _, tipo, valor in tokens:
        if tipo == 'IDENTIFICADOR' and valor not in variables_definidas:
            # Placeholder para detectar variables no definidas
            if valor not in PALABRAS_CLAVE:  # Evitar palabras clave
                errores.append(f"Variable '{valor}' no definida.")
            else:
                variables_definidas.add(valor)
    
    return errores

# Funciones de generación de código intermedio, optimización y máquina
def generar_codigo_intermedio(tokens):
    codigo_intermedio = []
    for _, tipo, valor in tokens:
        if tipo == 'IDENTIFICADOR':
            codigo_intermedio.append(f"LOAD {valor}")
        elif tipo == 'NUMERO':
            codigo_intermedio.append(f"PUSH {valor}")
        elif tipo == 'OPERADOR_ARITMETICO':
            codigo_intermedio.append(f"OPERATE {valor}")
    
    return codigo_intermedio

def optimizar_codigo(codigo_intermedio):
    codigo_optimizado = []
    for linea in codigo_intermedio:
        # Optimización básica: eliminar operaciones redundantes
        if "OPERATE" in linea:
            if len(codigo_optimizado) > 0 and codigo_optimizado[-1].startswith("OPERATE"):
                continue  # Saltar operaciones redundantes (como ejemplo)
        codigo_optimizado.append(linea)
    
    return codigo_optimizado

def generar_codigo_maquina(codigo_optimizado):
    codigo_maquina = []
    for linea in codigo_optimizado:
        # Generación de código máquina básica
        if "LOAD" in linea:
            codigo_maquina.append(f"LOAD_REG {linea.split()[-1]}")
        elif "PUSH" in linea:
            codigo_maquina.append(f"PUSH_REG {linea.split()[-1]}")
        elif "OPERATE" in linea:
            codigo_maquina.append(f"EXECUTE_OP {linea.split()[-1]}")
    
    return codigo_maquina

def ejecutar_codigo(codigo_fuente):
    try:
        # Capturar salida estándar y errores
        import io
        import sys

        # Redirigir salida estándar y errores
        buffer_salida = io.StringIO()
        sys.stdout = buffer_salida
        sys.stderr = buffer_salida

        # Ejecutar el código
        exec(codigo_fuente)

        # Restaurar salida estándar y errores
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

        # Obtener salida del buffer
        salida = buffer_salida.getvalue()

        # Mostrar la salida en un cuadro de mensaje
        messagebox.showinfo("Resultado del Código", salida if salida else "Código ejecutado sin salida.")
    except Exception as e:
        # Restaurar salida estándar y errores en caso de excepción
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        messagebox.showerror("Error en el Código", f"Error: {str(e)}")

# Funciones de la interfaz gráfica
def mostrar_resultados_lexicos(codigo_fuente):
    tokens = analizador_lexico(codigo_fuente)
    resultado = "\n".join(f"Línea {t[0]}: {t[1]} -> {t[2]}" for t in tokens)
    messagebox.showinfo("Análisis Léxico", resultado)

def mostrar_arbol_sintactico(codigo_fuente):
    tokens = analizador_lexico(codigo_fuente)
    construir_arbol_sintactico(tokens, "MiPrograma")

def mostrar_errores_semanticos(codigo_fuente):
    tokens = analizador_lexico(codigo_fuente)
    errores = analizador_semantico(tokens)
    if errores:
        messagebox.showerror("Errores Semánticos", "\n".join(errores))
    else:
        messagebox.showinfo("Análisis Semántico", "No se encontraron errores semánticos.")

def mostrar_codigo_intermedio(codigo_fuente):
    tokens = analizador_lexico(codigo_fuente)
    codigo_intermedio = generar_codigo_intermedio(tokens)
    messagebox.showinfo("Código Intermedio", "\n".join(codigo_intermedio))

def mostrar_codigo_optimizado(codigo_fuente):
    tokens = analizador_lexico(codigo_fuente)
    codigo_intermedio = generar_codigo_intermedio(tokens)
    codigo_optimizado = optimizar_codigo(codigo_intermedio)
    messagebox.showinfo("Código Optimizado", "\n".join(codigo_optimizado))

def mostrar_codigo_maquina(codigo_fuente):
    tokens = analizador_lexico(codigo_fuente)
    codigo_intermedio = generar_codigo_intermedio(tokens)
    codigo_optimizado = optimizar_codigo(codigo_intermedio)
    codigo_maquina = generar_codigo_maquina(codigo_optimizado)
    messagebox.showinfo("Código Máquina", "\n".join(codigo_maquina))

# Interfaz de inicio
def menu_compilador():
    ventana = tk.Tk()
    ventana.title("Compilador Python")
    ventana.geometry("700x600")
    ventana.config(bg="#2e3b4e")
    
    label_titulo = tk.Label(ventana, text="Compilador Python", font=("Arial", 24, "bold"), fg="#ffffff", bg="#2e3b4e")
    label_titulo.pack(pady=20)
    
    texto_codigo = scrolledtext.ScrolledText(ventana, width=80, height=20, font=("Courier New", 12))
    texto_codigo.pack(padx=20, pady=10)
    
    button_compilar = tk.Button(ventana, text="Compilar", width=20, height=2, font=("Arial", 14), bg="#4CAF50", fg="#ffffff", command=lambda: ventana_compilador(texto_codigo.get("1.0", tk.END)))
    button_compilar.pack(pady=10)

    button_salir = tk.Button(ventana, text="Salir", width=20, height=2, font=("Arial", 14), bg="#f44336", fg="#ffffff", command=ventana.quit)
    button_salir.pack(pady=5)

    ventana.mainloop()

def ventana_compilador(codigo_fuente):
    ventana_opciones = tk.Toplevel()
    ventana_opciones.title("Opciones de Compilación")
    ventana_opciones.geometry("700x600")
    ventana_opciones.config(bg="#2e3b4e")
    
    label_opciones = tk.Label(ventana_opciones, text="Seleccione una opción:", font=("Arial", 16), fg="#ffffff", bg="#2e3b4e")
    label_opciones.pack(pady=20)

    button_lexico = tk.Button(ventana_opciones, text="Análisis Léxico", width=30, height=2, font=("Arial", 12), command=lambda: mostrar_resultados_lexicos(codigo_fuente))
    button_lexico.pack(pady=10)

    button_arbol = tk.Button(ventana_opciones, text="Árbol Sintáctico", width=30, height=2, font=("Arial", 12), command=lambda: mostrar_arbol_sintactico(codigo_fuente))
    button_arbol.pack(pady=10)

    button_semantico = tk.Button(ventana_opciones, text="Análisis Semántico", width=30, height=2, font=("Arial", 12), command=lambda: mostrar_errores_semanticos(codigo_fuente))
    button_semantico.pack(pady=10)

    button_intermedio = tk.Button(ventana_opciones, text="Código Intermedio", width=30, height=2, font=("Arial", 12), command=lambda: mostrar_codigo_intermedio(codigo_fuente))
    button_intermedio.pack(pady=10)

    button_optimizado = tk.Button(ventana_opciones, text="Código Optimizado", width=30, height=2, font=("Arial", 12), command=lambda: mostrar_codigo_optimizado(codigo_fuente))
    button_optimizado.pack(pady=10)

    button_maquina = tk.Button(ventana_opciones, text="Código Máquina", width=30, height=2, font=("Arial", 12), command=lambda: mostrar_codigo_maquina(codigo_fuente))
    button_maquina.pack(pady=10)

    button_maquina.pack(pady=10)

    button_ejecutar = tk.Button(ventana_opciones,text="Ejecutar Código",width=30,height=2,font=("Arial", 12),command=lambda: ejecutar_codigo(codigo_fuente))
    button_ejecutar.pack(pady=10)

    ventana_opciones.mainloop()

if __name__ == "__main__":
    menu_compilador()
