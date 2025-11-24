"""
===============================================================================
SIMULADOR DE ALU (UNIDAD ARITMÉTICO LÓGICA) DE 8 BITS
===============================================================================

Este programa simula el funcionamiento de una ALU real, incluyendo:
- Operaciones aritméticas (suma, resta)
- Operaciones lógicas (AND, OR, XOR, NOT)
- Cálculo de banderas de estado (Z, N, C, V)
- Restricción de 8 bits para simular hardware real
===============================================================================
"""

# ==============================================================================
# PASO 1: LA LÓGICA (BACKEND) - CLASE ALU
# ==============================================================================

class ALU:
    """
    Clase ALU que simula una Unidad Aritmético Lógica de 8 bits.
    
    SEPARACIÓN DE RESPONSABILIDADES:
    Esta clase NO contiene ninguna interfaz gráfica, solo la lógica pura
    de procesamiento. Esto simula el hardware real de una CPU.
    
    BANDERAS (FLAGS):
    Las ALU reales generan "señales de estado" después de cada operación.
    Estas banderas ayudan a la CPU a tomar decisiones (saltos condicionales, etc.)
    """
    
    # ===== CÓDIGOS DE OPERACIÓN (OPCODES) =====
    # En una CPU real, estos serían parte del conjunto de instrucciones
    OP_ADD = 0  # Suma (A + B)
    OP_SUB = 1  # Resta (A - B)
    OP_AND = 2  # AND lógico (A & B)
    OP_OR = 3   # OR lógico (A | B)
    OP_XOR = 4  # XOR lógico (A ^ B)
    OP_NOT = 5  # NOT lógico (~A) - solo usa operando A
    
    def __init__(self):
        """
        Inicializa la ALU con valores por defecto.
        
        En hardware real, estos serían registros de estado.
        """
        self.result = 0  # Registro de resultado de 8 bits
        self.flags = {
            'Z': 0,  # Zero flag - indica si el resultado es cero
            'N': 0,  # Negative flag - indica si el número es negativo (bit 7 = 1)
            'C': 0,  # Carry flag - indica desbordamiento en aritmética sin signo
            'V': 0   # Overflow flag - indica error de signo en aritmética con signo
        }
    
    def execute(self, a, b, opcode):
        """
        MÉTODO PRINCIPAL: Ejecuta una operación en la ALU.
        
        Este método simula el ciclo de ejecución de una instrucción en una CPU:
        1. Recibe los operandos y el código de operación
        2. Ejecuta la operación correspondiente
        3. Calcula las banderas de estado
        4. Retorna el resultado y las banderas
        
        Args:
            a (int): Operando A (0-255)
            b (int): Operando B (0-255)
            opcode (int): Código de operación (0-5)
        
        Returns:
            tuple: (resultado, banderas)
                - resultado (int): El resultado de la operación (0-255)
                - banderas (dict): Diccionario con estados de Z, N, C, V
        """
        # ===== PASO 1: ASEGURAR QUE LOS OPERANDOS SEAN DE 8 BITS =====
        # En hardware real, los registros tienen un tamaño fijo.
        # La operación & 0xFF asegura que solo usemos los 8 bits menos significativos.
        # 0xFF = 11111111 en binario = máscara de 8 bits
        a = a & 0xFF
        b = b & 0xFF
        
        # ===== PASO 2: RESETEAR BANDERAS =====
        # Cada operación recalcula todas las banderas desde cero
        self.flags = {'Z': 0, 'N': 0, 'C': 0, 'V': 0}
        
        # ===== PASO 3: EJECUTAR LA OPERACIÓN SEGÚN EL OPCODE =====
        # Esto simula el decodificador de instrucciones de una CPU
        if opcode == self.OP_ADD:
            self.result = self._add(a, b)
        elif opcode == self.OP_SUB:
            self.result = self._sub(a, b)
        elif opcode == self.OP_AND:
            self.result = self._and(a, b)
        elif opcode == self.OP_OR:
            self.result = self._or(a, b)
        elif opcode == self.OP_XOR:
            self.result = self._xor(a, b)
        elif opcode == self.OP_NOT:
            self.result = self._not(a)
        else:
            raise ValueError(f"Opcode inválido: {opcode}")
        
        # ===== PASO 4: CALCULAR BANDERAS DE ESTADO =====
        # Las banderas se actualizan automáticamente en hardware después de cada operación
        self._calculate_flags(a, b, opcode)
        
        # ===== PASO 5: RETORNAR RESULTADO Y BANDERAS =====
        # Retornamos una copia de las banderas para no exponer el estado interno
        return self.result, self.flags.copy()
    
    # ==========================================================================
    # OPERACIONES ARITMÉTICAS
    # ==========================================================================
    
    def _add(self, a, b):
        """
        SUMA DE 8 BITS (A + B)
        
        Proceso:
        1. Suma los dos números (puede dar más de 8 bits)
        2. Detecta si hubo carry (resultado > 255)
        3. Corta el resultado a 8 bits
        
        Ejemplo: 200 + 100 = 300
                 300 en binario = 100101100 (9 bits)
                 Carry activado (C=1)
                 Resultado cortado: 300 & 0xFF = 44 (00101100)
        """
        result = a + b
        
        # BANDERA CARRY: Se activa si el resultado excede 8 bits (> 255)
        # Esto indica desbordamiento en aritmética SIN SIGNO
        if result > 255:
            self.flags['C'] = 1
        
        # Cortar a 8 bits para simular registro de tamaño fijo
        return result & 0xFF
    
    def _sub(self, a, b):
        """
        RESTA DE 8 BITS (A - B)
        
        Proceso:
        1. Resta B de A (puede dar negativo)
        2. Detecta si se necesitó "borrow" (préstamo)
        3. Corta el resultado a 8 bits
        
        Ejemplo: 5 - 10 = -5
                 -5 en complemento a 2 (8 bits) = 11111011 = 251
                 Carry activado (C=1) porque hubo borrow
        """
        result = a - b
        
        # BANDERA CARRY: En resta, indica si hubo "borrow" (préstamo)
        # Esto ocurre cuando el resultado es negativo (A < B)
        if result < 0:
            self.flags['C'] = 1
        
        # La operación & 0xFF convierte automáticamente a complemento a 2
        # Ejemplo: -5 & 0xFF = 251 (representación de -5 en 8 bits)
        return result & 0xFF
    
    # ==========================================================================
    # OPERACIONES LÓGICAS (BIT A BIT)
    # ==========================================================================
    
    def _and(self, a, b):
        """
        AND LÓGICO (A & B)
        
        Operación bit a bit: el resultado tiene 1 solo donde AMBOS bits son 1
        
        Ejemplo: 
            A = 10101100
            B = 11110000
            R = 10100000 (AND bit a bit)
        """
        return (a & b) & 0xFF
    
    def _or(self, a, b):
        """
        OR LÓGICO (A | B)
        
        Operación bit a bit: el resultado tiene 1 donde AL MENOS UNO es 1
        
        Ejemplo:
            A = 10101100
            B = 11110000
            R = 11111100 (OR bit a bit)
        """
        return (a | b) & 0xFF
    
    def _xor(self, a, b):
        """
        XOR LÓGICO (A ^ B)
        
        Operación bit a bit: el resultado tiene 1 donde los bits son DIFERENTES
        
        Ejemplo:
            A = 10101100
            B = 11110000
            R = 01011100 (XOR bit a bit)
        
        Uso común: Comparación de bits, generación de paridad, cifrado simple
        """
        return (a ^ b) & 0xFF
    
    def _not(self, a):
        """
        NOT LÓGICO (~A)
        
        Operación bit a bit: invierte todos los bits (0→1, 1→0)
        
        Ejemplo:
            A = 10101100
            R = 01010011 (NOT bit a bit)
        
        NOTA: Solo usa el operando A, el operando B se ignora
        """
        return (~a) & 0xFF
    
    # ==========================================================================
    # CÁLCULO DE BANDERAS (FLAGS) - LA PARTE MÁS IMPORTANTE
    # ==========================================================================
    
    def _calculate_flags(self, a, b, opcode):
        """
        CALCULA LAS BANDERAS DE ESTADO después de cada operación.
        
        Esta es una de las funciones más importantes de una ALU real.
        Las banderas permiten a la CPU tomar decisiones basadas en resultados.
        
        BANDERAS IMPLEMENTADAS:
        
        1. Z (Zero Flag):
           - Se activa cuando el resultado es exactamente 0
           - Uso: Comparaciones (si A == B, entonces A - B = 0, Z=1)
        
        2. N (Negative Flag):
           - Se activa cuando el bit 7 (MSB) está en 1
           - En complemento a 2, bit 7 = 1 significa número negativo
           - Uso: Determinar si un número con signo es negativo
        
        3. C (Carry Flag):
           - SUMA: Se activa si hay desbordamiento (resultado > 255)
           - RESTA: Se activa si se necesitó "borrow" (A < B)
           - Uso: Detectar desbordamiento en aritmética SIN SIGNO
        
        4. V (Overflow Flag):
           - Se activa si hay error de signo en aritmética CON SIGNO
           - SUMA: Dos positivos dan negativo, o dos negativos dan positivo
           - RESTA: Restar negativo de positivo da negativo, etc.
           - Uso: Detectar desbordamiento en aritmética CON SIGNO (complemento a 2)
        """
        
        # ===== BANDERA Z (ZERO) =====
        # Comprueba si el resultado es exactamente cero
        # Uso típico: if (Z == 1) then branch (salto condicional)
        if self.result == 0:
            self.flags['Z'] = 1
        
        # ===== BANDERA N (NEGATIVE) =====
        # Comprueba el bit más significativo (bit 7)
        # 0x80 = 10000000 en binario - máscara para el bit 7
        # Si (resultado & 10000000) != 0, entonces bit 7 = 1
        if self.result & 0x80:
            self.flags['N'] = 1
        
        # ===== BANDERAS C (CARRY) y V (OVERFLOW) =====
        # Estas ya se calcularon en las funciones _add y _sub
        # Solo se afectan en operaciones ARITMÉTICAS, no en lógicas
        
        # Calcular overflow solo para operaciones aritméticas
        if opcode == self.OP_ADD:
            self._calculate_overflow_add(a, b)
        elif opcode == self.OP_SUB:
            self._calculate_overflow_sub(a, b)
    
    def _calculate_overflow_add(self, a, b):
        """
        CALCULA LA BANDERA V (OVERFLOW) PARA SUMA.
        
        TEORÍA DEL OVERFLOW EN SUMA:
        Overflow ocurre cuando el resultado de una suma tiene un signo
        incorrecto en representación de complemento a 2.
        
        Casos de overflow:
        1. Positivo + Positivo = Negativo ❌ (overflow!)
        2. Negativo + Negativo = Positivo ❌ (overflow!)
        3. Positivo + Negativo = Cualquiera ✓ (no puede haber overflow)
        
        EJEMPLO DE OVERFLOW:
        A = 100 (01100100) - positivo en complemento a 2
        B = 50  (00110010) - positivo en complemento a 2
        R = 150 (10010110) - ¡NEGATIVO! (bit 7 = 1)
        
        Esto es un error porque 100 + 50 debería ser positivo.
        La bandera V se activa para indicar este error.
        
        DETECCIÓN:
        - Si signo(A) == signo(B) pero signo(Resultado) != signo(A)
        - Entonces hubo overflow
        """
        
        # Extraer el bit de signo (bit 7) de cada número
        # Desplazamos 7 posiciones a la derecha para obtener solo el bit 7
        sign_a = (a & 0x80) >> 7           # 0 = positivo, 1 = negativo
        sign_b = (b & 0x80) >> 7           # 0 = positivo, 1 = negativo
        sign_result = (self.result & 0x80) >> 7  # 0 = positivo, 1 = negativo
        
        # LÓGICA DE DETECCIÓN:
        # Si A y B tienen el MISMO signo (ambos + o ambos -)
        # PERO el resultado tiene un signo DIFERENTE
        # Entonces ocurrió overflow
        if sign_a == sign_b and sign_a != sign_result:
            self.flags['V'] = 1
    
    def _calculate_overflow_sub(self, a, b):
        """
        CALCULA LA BANDERA V (OVERFLOW) PARA RESTA.
        
        TEORÍA DEL OVERFLOW EN RESTA:
        Overflow ocurre cuando el resultado de una resta tiene un signo
        incorrecto en representación de complemento a 2.
        
        Casos de overflow:
        1. Positivo - Negativo = Negativo ❌ (overflow!)
           (restar un negativo es como sumar un positivo)
        2. Negativo - Positivo = Positivo ❌ (overflow!)
           (restar un positivo de un negativo debería dar más negativo)
        
        EJEMPLO DE OVERFLOW:
        A = 100  (01100100) - positivo
        B = -50  (11001110) - negativo en complemento a 2
        A - B = A + (-B) = 100 + 50 = 150
        R = 150  (10010110) - ¡NEGATIVO! (bit 7 = 1)
        
        Esto es un error porque 100 - (-50) = 150 debería ser positivo.
        
        DETECCIÓN:
        - Si signo(A) != signo(B) y signo(Resultado) != signo(A)
        - Entonces hubo overflow
        """
        
        # Extraer el bit de signo (bit 7) de cada número
        sign_a = (a & 0x80) >> 7
        sign_b = (b & 0x80) >> 7
        sign_result = (self.result & 0x80) >> 7
        
        # LÓGICA DE DETECCIÓN:
        # Si A y B tienen signos DIFERENTES
        # Y el resultado NO tiene el mismo signo que A
        # Entonces ocurrió overflow
        if sign_a != sign_b and sign_a != sign_result:
            self.flags['V'] = 1
    
    @staticmethod
    def get_operation_name(opcode):
        """
        Retorna el nombre legible de la operación según su opcode.
        Útil para mostrar en la interfaz gráfica.
        """
        operations = {
            0: "ADD (Suma)",
            1: "SUB (Resta)",
            2: "AND",
            3: "OR",
            4: "XOR",
            5: "NOT"
        }
        return operations.get(opcode, "Desconocida")


# ==============================================================================
# PASO 2: LA INTERFAZ GRÁFICA (FRONTEND) - USANDO TKINTER
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox


class ALUSimulatorGUI:
    """
    INTERFAZ GRÁFICA para el simulador de ALU de 8 bits.
    
    DISEÑO:
    - Tema oscuro profesional (simula un panel de hardware)
    - Entradas para operandos A y B en formato decimal
    - Visualización interactiva de bits con checkbuttons bidireccionales
    - Botones para seleccionar cada operación
    - Botón de acumulador para ciclos de operación
    - Banderas mostradas como "luces LED" que se encienden/apagan
    - Barra de estado informativa
    - Resultado mostrado en 3 formatos: Decimal, Hexadecimal y Binario
    """
    
    def __init__(self, root):
        """Inicializa la interfaz gráfica"""
        self.root = root
        self.root.title("Simulador de ALU de 8 bits - Versión Pro")
        self.root.geometry("850x850")  # Reducido de 920 a 850
        self.root.resizable(False, False)
        
        # Crear instancia de la ALU (el motor de cálculo)
        self.alu = ALU()
        
        # Variables de control para prevenir loops infinitos de sincronización
        self.updating_from_text_a = False
        self.updating_from_bits_a = False
        self.updating_from_text_b = False
        self.updating_from_bits_b = False
        
        # Variable para toggle signed/unsigned
        self.show_signed = tk.IntVar(value=0)
        
        # Configurar estilos y crear widgets
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """
        Configura el tema visual oscuro profesional.
        
        PALETA DE COLORES:
        - Fondo oscuro: simula un panel de hardware
        - Azul brillante: para acentos y títulos
        - Verde brillante: para resultados y LEDs activos
        - Rojo: para LEDs de overflow/error
        """
        style = ttk.Style()
        style.theme_use('clam')
        
        # Definir paleta de colores
        self.bg_color = "#1a1a2e"        # Azul oscuro profundo
        self.fg_color = "#ffffff"         # Blanco para texto
        self.accent_color = "#0f4c75"    # Azul medio
        self.bright_accent = "#3282b8"   # Azul brillante
        self.result_color = "#00ff88"    # Verde neón
        self.led_off = "#2a2a3e"         # LED apagado
        self.led_on_green = "#00ff00"    # LED verde encendido
        self.led_on_red = "#ff3333"      # LED rojo encendido
        self.warning_color = "#ffaa00"   # Naranja para advertencias
        
        self.root.configure(bg=self.bg_color)
    
    def format_binary_nibbles(self, binary_str):
        """
        Formatea un string binario con espacios cada 4 bits (nibbles).
        Ejemplo: '11111111' -> '1111 1111'
        """
        if len(binary_str) != 8:
            return binary_str
        return f"{binary_str[:4]} {binary_str[4:]}"
    
    def to_signed_8bit(self, unsigned_value):
        """
        Convierte un valor unsigned (0-255) a signed usando complemento a 2.
        Rango: -128 a 127
        """
        if unsigned_value > 127:
            return unsigned_value - 256
        return unsigned_value
    
    def create_widgets(self):
        """Crea todos los elementos de la interfaz"""
        
        # ===== TÍTULO =====
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=5)
        
        tk.Label(
            title_frame,
            text="🖥️ SIMULADOR DE ALU - 8 BITS PRO",
            font=("Arial", 22, "bold"),
            bg=self.bg_color,
            fg=self.bright_accent
        ).pack()
        
        tk.Label(
            title_frame,
            text="Unidad Aritmético Lógica | Visualización Interactiva de Bits",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack()
        
        # ===== SECCIÓN DE OPERANDOS CON CHECKBUTTONS =====
        operands_frame = tk.LabelFrame(
            self.root,
            text="  OPERANDOS (0-255 en decimal)  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.bright_accent,
            bd=2,
            relief="groove"
        )
        operands_frame.pack(padx=20, pady=5, fill="x")
        
        # === OPERANDO A ===
        # Fila 1: Label, Entry, Binario
        tk.Label(
            operands_frame,
            text="Operando A:",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).grid(row=0, column=0, padx=15, pady=5, sticky="e")
        
        self.entry_a = tk.Entry(
            operands_frame,
            font=("Courier", 13, "bold"),
            width=12,
            justify="center",
            bg="#ffffff",
            fg="#000000"
        )
        self.entry_a.grid(row=0, column=1, padx=10, pady=5)
        self.entry_a.insert(0, "0")
        
        self.label_a_bin = tk.Label(
            operands_frame,
            text="Binario: 0000 0000",
            font=("Courier", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        self.label_a_bin.grid(row=0, column=2, padx=15, pady=5)
        
        # Fila 2: Checkbuttons para bits (TAREA 1)
        bits_frame_a = tk.Frame(operands_frame, bg=self.bg_color)
        bits_frame_a.grid(row=1, column=0, columnspan=3, pady=3)
        
        tk.Label(
            bits_frame_a,
            text="Bits:",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side="left", padx=5)
        
        # Crear IntVars y Checkbuttons para operando A (de Bit 7 a Bit 0)
        self.bit_vars_a = []
        self.bit_checks_a = []
        
        for i in range(7, -1, -1):  # De bit 7 a bit 0
            var = tk.IntVar(value=0)
            self.bit_vars_a.append(var)
            
            check = tk.Checkbutton(
                bits_frame_a,
                text=f"{i}",
                variable=var,
                font=("Courier", 9),
                bg=self.bg_color,
                fg=self.result_color,
                selectcolor=self.accent_color,
                activebackground=self.bg_color,
                activeforeground=self.result_color,
                command=lambda: self.sync_bits_to_text_a()
            )
            check.pack(side="left", padx=2)
            self.bit_checks_a.append(check)
        
        # Vincular evento de cambio de texto
        self.entry_a.bind("<KeyRelease>", self.update_binary_a)
        
        # === OPERANDO B ===
        # Fila 3: Label, Entry, Binario
        tk.Label(
            operands_frame,
            text="Operando B:",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).grid(row=2, column=0, padx=15, pady=5, sticky="e")
        
        self.entry_b = tk.Entry(
            operands_frame,
            font=("Courier", 13, "bold"),
            width=12,
            justify="center",
            bg="#ffffff",
            fg="#000000"
        )
        self.entry_b.grid(row=2, column=1, padx=10, pady=5)
        self.entry_b.insert(0, "0")
        
        self.label_b_bin = tk.Label(
            operands_frame,
            text="Binario: 0000 0000",
            font=("Courier", 10),
            bg=self.bg_color,
            fg="#888888"
        )
        self.label_b_bin.grid(row=2, column=2, padx=15, pady=5)
        
        # Fila 4: Checkbuttons para bits (TAREA 1)
        bits_frame_b = tk.Frame(operands_frame, bg=self.bg_color)
        bits_frame_b.grid(row=3, column=0, columnspan=3, pady=3)
        
        tk.Label(
            bits_frame_b,
            text="Bits:",
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side="left", padx=5)
        
        # Crear IntVars y Checkbuttons para operando B (de Bit 7 a Bit 0)
        self.bit_vars_b = []
        self.bit_checks_b = []
        
        for i in range(7, -1, -1):  # De bit 7 a bit 0
            var = tk.IntVar(value=0)
            self.bit_vars_b.append(var)
            
            check = tk.Checkbutton(
                bits_frame_b,
                text=f"{i}",
                variable=var,
                font=("Courier", 9),
                bg=self.bg_color,
                fg=self.result_color,
                selectcolor=self.accent_color,
                activebackground=self.bg_color,
                activeforeground=self.result_color,
                command=lambda: self.sync_bits_to_text_b()
            )
            check.pack(side="left", padx=2)
            self.bit_checks_b.append(check)
        
        # Vincular evento de cambio de texto
        self.entry_b.bind("<KeyRelease>", self.update_binary_b)
        
        # ===== SECCIÓN DE OPERACIONES =====
        operation_frame = tk.LabelFrame(
            self.root,
            text="  SELECCIONAR OPERACIÓN  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.bright_accent,
            bd=2,
            relief="groove"
        )
        operation_frame.pack(padx=20, pady=5, fill="x")
        
        # Crear botones para cada operación
        operations = [
            ("➕ ADD (Suma)", ALU.OP_ADD),
            ("➖ SUB (Resta)", ALU.OP_SUB),
            ("∧ AND", ALU.OP_AND),
            ("∨ OR", ALU.OP_OR),
            ("⊕ XOR", ALU.OP_XOR),
            ("¬ NOT A", ALU.OP_NOT)
        ]
        
        for i, (name, opcode) in enumerate(operations):
            btn = tk.Button(
                operation_frame,
                text=name,
                font=("Arial", 10, "bold"),
                bg=self.accent_color,
                fg="white",
                activebackground=self.bright_accent,
                activeforeground="white",
                width=13,
                height=2,
                command=lambda op=opcode: self.execute_operation(op),
                cursor="hand2",
                relief="raised",
                bd=3
            )
            btn.grid(row=i // 3, column=i % 3, padx=12, pady=8)
        
        # ===== SECCIÓN DE RESULTADO (3 FORMATOS) + BOTÓN ACUMULADOR =====
        result_frame = tk.LabelFrame(
            self.root,
            text="  RESULTADO  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.result_color,
            bd=2,
            relief="groove"
        )
        result_frame.pack(padx=20, pady=5, fill="x")
        
        # Frame para resultados numéricos
        results_container = tk.Frame(result_frame, bg=self.bg_color)
        results_container.pack(pady=3)
        
        # Resultado Decimal (con opción signed/unsigned)
        self.label_result_dec = tk.Label(
            results_container,
            text="Dec: ---",
            font=("Arial", 13, "bold"),
            bg=self.bg_color,
            fg=self.result_color
        )
        self.label_result_dec.pack(side="left", padx=10)
        
        # Resultado Hexadecimal
        self.label_result_hex = tk.Label(
            results_container,
            text="Hex: 0x--",
            font=("Courier", 13, "bold"),
            bg=self.bg_color,
            fg=self.result_color
        )
        self.label_result_hex.pack(side="left", padx=10)
        
        # Resultado en binario (8 bits completos con nibbles)
        self.label_result_bin = tk.Label(
            result_frame,
            text="Binario: ---- ----",
            font=("Courier", 12, "bold"),
            bg=self.bg_color,
            fg="#888888"
        )
        self.label_result_bin.pack(pady=2)
        
        # Toggle Signed/Unsigned
        self.check_signed = tk.Checkbutton(
            result_frame,
            text="Ver como Signed (Complemento a 2: -128 a 127)",
            variable=self.show_signed,
            font=("Arial", 9),
            bg=self.bg_color,
            fg=self.fg_color,
            selectcolor=self.accent_color,
            activebackground=self.bg_color,
            activeforeground=self.result_color,
            command=self.update_result_display
        )
        self.check_signed.pack(pady=2)
        
        # TAREA 2: Botón de Acumulador
        self.btn_accumulator = tk.Button(
            result_frame,
            text="🔄 Usar Resultado como A",
            font=("Arial", 10, "bold"),
            bg=self.warning_color,
            fg="#000000",
            activebackground="#ffcc33",
            activeforeground="#000000",
            width=25,
            height=1,
            command=self.accumulator_cycle,
            cursor="hand2",
            relief="raised",
            bd=3,
            state="disabled"  # Deshabilitado hasta que haya un resultado
        )
        self.btn_accumulator.pack(pady=5)
        
        # ===== SECCIÓN DE BANDERAS (FLAGS) - ESTILO LED =====
        flags_frame = tk.LabelFrame(
            self.root,
            text="  BANDERAS DE ESTADO (FLAGS)  ",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.bright_accent,
            bd=2,
            relief="groove"
        )
        flags_frame.pack(padx=20, pady=5, fill="x")
        
        # Descripción de cada bandera
        flag_info = {
            'Z': ('ZERO', 'Resultado = 0'),
            'N': ('NEGATIVE', 'Bit 7 = 1 (negativo)'),
            'C': ('CARRY', 'Desbordamiento sin signo'),
            'V': ('OVERFLOW', 'Error de signo')
        }
        
        self.flag_leds = {}
        
        # Crear "LEDs" para cada bandera
        for i, (flag, (name, desc)) in enumerate(flag_info.items()):
            # Frame contenedor para cada LED
            led_container = tk.Frame(flags_frame, bg=self.bg_color)
            led_container.grid(row=i // 2, column=i % 2, padx=25, pady=8, sticky="w")
            
            # LED (cuadrado que simula un indicador luminoso)
            led = tk.Label(
                led_container,
                text=f" {flag} ",
                font=("Arial", 16, "bold"),
                bg=self.led_off,
                fg="#555555",
                width=4,
                height=1,
                relief="raised",
                bd=3
            )
            led.pack(side="left", padx=10)
            
            # Información de la bandera
            info_frame = tk.Frame(led_container, bg=self.bg_color)
            info_frame.pack(side="left", padx=5)
            
            tk.Label(
                info_frame,
                text=name,
                font=("Arial", 10, "bold"),
                bg=self.bg_color,
                fg=self.fg_color
            ).pack(anchor="w")
            
            tk.Label(
                info_frame,
                text=desc,
                font=("Arial", 8),
                bg=self.bg_color,
                fg="#aaaaaa"
            ).pack(anchor="w")
            
            # Guardar referencia al LED
            self.flag_leds[flag] = led
        
        # ===== TAREA 3: BARRA DE ESTADO INFORMATIVA =====
        status_frame = tk.Frame(self.root, bg=self.accent_color, relief="sunken", bd=2)
        status_frame.pack(side="bottom", fill="x", padx=0, pady=0)
        
        self.status_label = tk.Label(
            status_frame,
            text="💡 Estado: Listo para operar",
            font=("Arial", 10),
            bg=self.accent_color,
            fg="white",
            anchor="w",
            padx=10,
            pady=5
        )
        self.status_label.pack(fill="x")
    
    # ==========================================================================
    # TAREA 1: SINCRONIZACIÓN BIDIRECCIONAL DE BITS
    # ==========================================================================
    
    def update_binary_a(self, event=None):
        """
        Actualiza la visualización binaria y los checkbuttons del operando A.
        SINCRONIZACIÓN: Texto → Checkboxes
        """
        if self.updating_from_bits_a:
            return  # Prevenir loop infinito
        
        self.updating_from_text_a = True
        
        try:
            value = int(self.entry_a.get())
            if 0 <= value <= 255:
                # Actualizar label binario con formato nibbles
                binary = format(value, '08b')
                binary_formatted = self.format_binary_nibbles(binary)
                self.label_a_bin.config(text=f"Binario: {binary_formatted}", fg="#00ff88")
                
                # Actualizar checkbuttons (de bit 7 a bit 0)
                for i in range(8):
                    bit_position = 7 - i  # Invertir: índice 0 = bit 7
                    bit_value = (value >> bit_position) & 1
                    self.bit_vars_a[i].set(bit_value)
            else:
                self.label_a_bin.config(text="Binario: (fuera de rango 0-255)", fg="#ff3333")
        except ValueError:
            self.label_a_bin.config(text="Binario: (valor inválido)", fg="#ff3333")
        
        self.updating_from_text_a = False
    
    def sync_bits_to_text_a(self):
        """
        Sincroniza los checkbuttons al campo de texto.
        SINCRONIZACIÓN: Checkboxes → Texto
        """
        if self.updating_from_text_a:
            return  # Prevenir loop infinito
        
        self.updating_from_bits_a = True
        
        # Calcular valor decimal desde los bits
        value = 0
        for i in range(8):
            bit_position = 7 - i  # índice 0 = bit 7
            if self.bit_vars_a[i].get() == 1:
                value += (1 << bit_position)
        
        # Actualizar campo de texto
        self.entry_a.delete(0, tk.END)
        self.entry_a.insert(0, str(value))
        
        # Actualizar label binario con formato nibbles
        binary = format(value, '08b')
        binary_formatted = self.format_binary_nibbles(binary)
        self.label_a_bin.config(text=f"Binario: {binary_formatted}", fg="#00ff88")
        
        self.updating_from_bits_a = False
    
    def update_binary_b(self,event=None):
        """
        Actualiza la visualización binaria y los checkbuttons del operando B.
        SINCRONIZACIÓN: Texto → Checkboxes
        """
        if self.updating_from_bits_b:
            return  # Prevenir loop infinito
        
        self.updating_from_text_b = True
        
        try:
            value = int(self.entry_b.get())
            if 0 <= value <= 255:
                # Actualizar label binario con formato nibbles
                binary = format(value, '08b')
                binary_formatted = self.format_binary_nibbles(binary)
                self.label_b_bin.config(text=f"Binario: {binary_formatted}", fg="#00ff88")
                
                # Actualizar checkbuttons (de bit 7 a bit 0)
                for i in range(8):
                    bit_position = 7 - i  # Invertir: índice 0 = bit 7
                    bit_value = (value >> bit_position) & 1
                    self.bit_vars_b[i].set(bit_value)
            else:
                self.label_b_bin.config(text="Binario: (fuera de rango 0-255)", fg="#ff3333")
        except ValueError:
            self.label_b_bin.config(text="Binario: (valor inválido)", fg="#ff3333")
        
        self.updating_from_text_b = False
    
    def sync_bits_to_text_b(self):
        """
        Sincroniza los checkbuttons al campo de texto.
        SINCRONIZACIÓN: Checkboxes → Texto
        """
        if self.updating_from_text_b:
            return  # Prevenir loop infinito
        
        self.updating_from_bits_b = True
        
        # Calcular valor decimal desde los bits
        value = 0
        for i in range(8):
            bit_position = 7 - i  # índice 0 = bit 7
            if self.bit_vars_b[i].get() == 1:
                value += (1 << bit_position)
        
        # Actualizar campo de texto
        self.entry_b.delete(0, tk.END)
        self.entry_b.insert(0, str(value))
        
        # Actualizar label binario con formato nibbles
        binary = format(value, '08b')
        binary_formatted = self.format_binary_nibbles(binary)
        self.label_b_bin.config(text=f"Binario: {binary_formatted}", fg="#00ff88")
        
        self.updating_from_bits_b = False
    
    # ==========================================================================
    # TAREA 2: BOTÓN DE CICLO DE ACUMULADOR
    # ==========================================================================
    
    def accumulator_cycle(self):
        """
        Toma el resultado actual y lo pone en el Operando A.
        Reinicia el Operando B a 0.
        Simula el comportamiento de un registro acumulador real.
        """
        try:
            # Obtener el resultado actual
            result_text = self.label_result.cget("text")
            
            if "Esperando" in result_text:
                return  # No hay resultado aún
            
            # Tomar el resultado de la ALU
            result_value = self.alu.result
            
            # Poner el resultado en el Operando A
            self.entry_a.delete(0, tk.END)
            self.entry_a.insert(0, str(result_value))
            self.update_binary_a()  # Actualizar visualización
            
            # Reiniciar Operando B a 0
            self.entry_b.delete(0, tk.END)
            self.entry_b.insert(0, "0")
            self.update_binary_b()  # Actualizar visualización
            
            # Actualizar estado
            self.status_label.config(
                text=f"🔄 Acumulador: Resultado {result_value} transferido a Operando A",
                bg=self.warning_color,
                fg="#000000"
            )
            
        except Exception as e:
            self.status_label.config(
                text=f"❌ Error en ciclo de acumulador: {str(e)}",
                bg=self.led_on_red,
                fg="white"
            )
    
    # ==========================================================================
    # EJECUCIÓN DE OPERACIONES
    # ==========================================================================
    
    def execute_operation(self, opcode):
        """
        MÉTODO PRINCIPAL: Ejecuta la operación seleccionada.
        
        Proceso:
        1. Lee los valores de A y B
        2. Valida que estén en el rango correcto (0-255)
        3. Llama a la ALU para ejecutar la operación
        4. Muestra el resultado en múltiples formatos
        5. Actualiza las "luces LED" de las banderas
        6. TAREA 3: Actualiza la barra de estado informativa
        """
        try:
            # ===== PASO 1: OBTENER VALORES DE LOS OPERANDOS =====
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            
            # ===== PASO 2: VALIDAR RANGO (0-255 para 8 bits) =====
            if not (0 <= a <= 255 and 0 <= b <= 255):
                messagebox.showerror(
                    "Error de Rango",
                    "Los operandos deben estar entre 0 y 255\n(valores de 8 bits)"
                )
                return
            
            # ===== PASO 3: EJECUTAR OPERACIÓN EN LA ALU =====
            result, flags = self.alu.execute(a, b, opcode)
            
            # Guardar resultado y operación actual para update_result_display
            self.current_result = result
            self.current_opcode = opcode
            
            # ===== PASO 4: MOSTRAR RESULTADO =====
            self.update_result_display()
            
            # Habilitar botón de acumulador
            self.btn_accumulator.config(state="normal")
            
            # ===== PASO 5: ACTUALIZAR "LUCES LED" DE LAS BANDERAS =====
            for flag, value in flags.items():
                led = self.flag_leds[flag]
                
                if value == 1:
                    # LED ENCENDIDO
                    if flag in ['C', 'V']:
                        led.config(bg=self.led_on_red, fg="white", relief="sunken")
                    else:
                        led.config(bg=self.led_on_green, fg="black", relief="sunken")
                else:
                    # LED APAGADO
                    led.config(bg=self.led_off, fg="#555555", relief="raised")
            
            # ===== TAREA 3: ACTUALIZAR BARRA DE ESTADO INFORMATIVA =====
            op_name = ALU.get_operation_name(opcode)
            self.update_status_bar(flags, op_name, a, b, result)
        
        except ValueError:
            messagebox.showerror(
                "Error de Entrada",
                "Por favor ingrese números enteros válidos (0-255)"
            )
    
    def update_result_display(self):
        """
        Actualiza la visualización del resultado según el toggle signed/unsigned.
        Se llama cuando se ejecuta una operación o cuando se cambia el checkbox.
        """
        if not hasattr(self, 'current_result'):
            return  # No hay resultado todavía
        
        result = self.current_result
        
        # Determinar si mostrar como signed o unsigned
        if self.show_signed.get() == 1:
            # Modo Signed: interpretar como complemento a 2
            result_display = self.to_signed_8bit(result)
            dec_text = f"Dec: {result_display:+d}"  # Con signo (+/-)
        else:
            # Modo Unsigned: 0-255
            result_display = result
            dec_text = f"Dec: {result_display}"
        
        # Actualizar decimal
        self.label_result_dec.config(text=dec_text)
        
        # Actualizar hexadecimal (siempre unsigned)
        self.label_result_hex.config(text=f"Hex: 0x{result:02X}")
        
        # Actualizar binario con formato nibbles
        binary = format(result, '08b')
        binary_formatted = self.format_binary_nibbles(binary)
        self.label_result_bin.config(
            text=f"Binario: {binary_formatted}",
            fg=self.result_color
        )
    
    # ==========================================================================
    # TAREA 3: BARRA DE ESTADO INFORMATIVA
    # ==========================================================================
    
    def update_status_bar(self, flags, op_name, a, b, result):
        """
        Actualiza la barra de estado con explicaciones en lenguaje humano.
        Explica por qué se encendieron las banderas críticas.
        """
        messages = []
        
        # Prioridad: V > C > N > Z
        if flags['V'] == 1:
            messages.append("⚠️ ¡OVERFLOW! Desbordamiento de signo detectado (error en aritmética con signo)")
        
        if flags['C'] == 1:
            if "ADD" in op_name:
                messages.append(f"🔴 CARRY: El resultado ({a}+{b}={a+b}) excedió 8 bits (>255)")
            elif "SUB" in op_name:
                messages.append(f"🔴 BORROW: Se necesitó préstamo ({a}-{b} fue negativo)")
        
        if flags['N'] == 1:
            messages.append(f"➖ NEGATIVO: El bit 7 está activo (valor {result} es negativo en complemento a 2)")
        
        if flags['Z'] == 1:
            messages.append("✅ ZERO: El resultado es exactamente cero")
        
        # Si no hay banderas activas
        if not messages:
            messages.append(f"✅ Operación exitosa: {op_name} = {result}. Todas las banderas en estado normal")
        
        # Mostrar el mensaje más importante (primero en la lista)
        status_text = " | ".join(messages[:2])  # Mostrar máximo 2 mensajes
        
        # Colorear según severidad
        if flags['V'] == 1 or flags['C'] == 1:
            bg_color = self.led_on_red
            fg_color = "white"
        elif flags['N'] == 1:
            bg_color = self.warning_color
            fg_color = "#000000"
        elif flags['Z'] == 1:
            bg_color = self.led_on_green
            fg_color = "#000000"
        else:
            bg_color = self.accent_color
            fg_color = "white"
        
        self.status_label.config(
            text=status_text,
            bg=bg_color,
            fg=fg_color
        )


# ==============================================================================
# PASO 3: EJECUCIÓN - PUNTO DE ENTRADA DEL PROGRAMA
# ==============================================================================

def main():
    """
    Función principal que inicia el simulador.
    
    Crea la ventana principal de Tkinter y la interfaz gráfica,
    luego inicia el bucle de eventos de la GUI.
    """
    # Crear ventana principal
    root = tk.Tk()
    
    # Crear la aplicación (esto crea todos los widgets)
    app = ALUSimulatorGUI(root)
    
    # Iniciar el bucle de eventos de Tkinter
    # Este bucle mantiene la ventana abierta y responde a eventos del usuario
    root.mainloop()


    
    def update_status_bar(self, flags, op_name, a, b, result):
        """
        Actualiza la barra de estado con explicaciones en lenguaje humano.
        Explica por qué se encendieron las banderas críticas.
        """
        messages = []
        
        # Prioridad: V > C > N > Z
        if flags['V'] == 1:
            messages.append("⚠️ ¡OVERFLOW! Desbordamiento de signo detectado (error en aritmética con signo)")
        
        if flags['C'] == 1:
            if "ADD" in op_name:
                messages.append(f"🔴 CARRY: El resultado ({a}+{b}={a+b}) excedió 8 bits (>255)")
            elif "SUB" in op_name:
                messages.append(f"🔴 BORROW: Se necesitó préstamo ({a}-{b} fue negativo)")
        
        if flags['N'] == 1:
            messages.append(f"➖ NEGATIVO: El bit 7 está activo (valor {result} es negativo en complemento a 2)")
        
        if flags['Z'] == 1:
            messages.append("✅ ZERO: El resultado es exactamente cero")
        
        # Si no hay banderas activas
        if not messages:
            messages.append(f"✅ Operación exitosa: {op_name} = {result}. Todas las banderas en estado normal")
        
        # Mostrar el mensaje más importante (primero en la lista)
        status_text = " | ".join(messages[:2])  # Mostrar máximo 2 mensajes
        
        # Colorear según severidad
        if flags['V'] == 1 or flags['C'] == 1:
            bg_color = self.led_on_red
            fg_color = "white"
        elif flags['N'] == 1:
            bg_color = self.warning_color
            fg_color = "#000000"
        elif flags['Z'] == 1:
            bg_color = self.led_on_green
            fg_color = "#000000"
        else:
            bg_color = self.accent_color
            fg_color = "white"
        
        self.status_label.config(
            text=status_text,
            bg=bg_color,
            fg=fg_color
        )


# ==============================================================================
# PASO 3: EJECUCIÓN - PUNTO DE ENTRADA DEL PROGRAMA
# ==============================================================================

def main():
    """
    Función principal que inicia el simulador.
    
    Crea la ventana principal de Tkinter y la interfaz gráfica,
    luego inicia el bucle de eventos de la GUI.
    """
    # Crear ventana principal
    root = tk.Tk()
    
    # Crear la aplicación (esto crea todos los widgets)
    app = ALUSimulatorGUI(root)
    
    # Iniciar el bucle de eventos de Tkinter
    # Este bucle mantiene la ventana abierta y responde a eventos del usuario
    root.mainloop()


# Este bloque solo se ejecuta si el archivo se corre directamente
# No se ejecuta si este archivo se importa como módulo en otro programa
if __name__ == "__main__":
    main()

    def update_status_bar(self, flags, op_name, a, b, result):
        """
        Actualiza la barra de estado con explicaciones en lenguaje humano.
        Explica por qué se encendieron las banderas críticas.
        """
        messages = []
        
        # Prioridad: V > C > N > Z
        if flags['V'] == 1:
            messages.append("⚠️ ¡OVERFLOW! Desbordamiento de signo detectado (error en aritmética con signo)")
