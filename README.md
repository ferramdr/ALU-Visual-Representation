🖥️ Simulador de ALU de 8 bits

Estructura del Programa
Backend - Clase ALU
- Características Implementadas
Clase 
ALU
 - Lógica pura sin interfaz gráfica:

Operaciones Aritméticas:

✓ ADD (Suma): A + B con detección de carry
✓ SUB (Resta): A - B con detección de borrow
Operaciones Lógicas (bit a bit):

✓ AND: Resultado tiene 1 solo donde ambos bits son 1
✓ OR: Resultado tiene 1 donde al menos uno es 1
✓ XOR: Resultado tiene 1 donde los bits son diferentes
✓ NOT: Invierte todos los bits (solo operando A)
Restricción de 8 bits:

Todos los resultados se cortan usando & 0xFF
Simula el tamaño fijo de registros en hardware real
🚩 Sistema de Banderas (Flags)
El sistema calcula 4 banderas principales después de cada operación:

Z (Zero Flag)

Se activa cuando el resultado es exactamente 0
Útil para comparaciones (A == B → A - B = 0, Z=1)
N (Negative Flag)

Se activa cuando el bit 7 (MSB) está en 1
En complemento a 2, indica número negativo
Detecta con máscara: resultado & 0x80
C (Carry Flag)

En suma: Desbordamiento sin signo (resultado > 255)
En resta: Indica "borrow" necesario (A < B)
No se afecta en operaciones lógicas
V (Overflow Flag)

Detecta errores de signo en complemento a 2
En suma: Dos positivos dan negativo, o dos negativos dan positivo
En resta: Signos incorrectos según operación
Solo para operaciones aritméticas
📚 Comentarios Educativos
Cada función incluye:

Explicación teórica del funcionamiento
Ejemplos numéricos con binarios
Casos especiales (overflow, carry, etc.)
Uso típico en procesadores reales
Ejemplo de documentación:

def _calculate_overflow_add(self, a, b):
    """
    CALCULA LA BANDERA V (OVERFLOW) PARA SUMA.
    TEORÍA DEL OVERFLOW EN SUMA:
    Overflow ocurre cuando el resultado de una suma tiene un signo
    incorrecto en representación de complemento a 2.
    EJEMPLO DE OVERFLOW:
    A = 100 (01100100) - positivo
    B = 50  (00110010) - positivo
    R = 150 (10010110) - ¡NEGATIVO! (bit 7 = 1)
    Esto es un error porque 100 + 50 debería ser positivo.
    """
Frontend - Interfaz Gráfica con Tkinter
📊 Secciones de la Interface
1. Entrada de Operandos

Campos para A y B (0-255 en decimal)
Visualización binaria en tiempo real
Validación automática de rango
Fuente monoespaciada (Courier) para binarios
2. Controles de Operación

6 botones con símbolos matemáticos:
➕ ADD (Suma)
➖ SUB (Resta)
∧ AND
∨ OR
⊕ XOR
¬ NOT A
Efectos visuales al pasar el mouse
3. Visualización de Resultados (3 formatos simultáneos)

El resultado se muestra en tres formatos al mismo tiempo:

Formato 1: Decimal y Hexadecimal
ADD (Suma) = 200 (Dec) = 0xC8 (Hex)
Formato 2: Binario completo (8 bits)
Binario: 11001000
4. Banderas LED (Indicadores Luminosos)

Cada bandera tiene:

LED cuadrado que cambia de color:
Apagado: Gris oscuro (#2a2a3e), relieve elevado
Encendido: Verde (#00ff00) para Z y N, Rojo (#ff3333) para C y V, relieve hundido
Nombre completo: ZERO, NEGATIVE, CARRY, OVERFLOW
Descripción breve de qué representa
Ejemplo visual:

┌─────┐  ZERO
│  Z  │  Resultado = 0
└─────┘
┌─────┐  CARRY
│  C  │  Desbordamiento sin signo
└─────┘
🔄 Actualización en Tiempo Real
Los valores binarios de A y B se actualizan mientras el usuario escribe
Validación visual con colores (verde = válido, rojo = error)
Mensajes de error claros en cuadros de diálogo
PASO 3: Ejecución
if __name__ == "__main__":
    main()
El bloque estándar permite:

Ejecutar directamente: python alu_simulator.py
Importar como módulo sin ejecutar automáticamente
🧪 Ejemplo de Uso
Caso 1: Suma con Carry
Entrada:

A = 200
B = 100
Operación: ADD
Resultado:

Decimal: 44
Hexadecimal: 0x2C
Binario: 00101100
Banderas:

Z = 0 (resultado no es cero)
N = 0 (bit 7 = 0, positivo)
C = 1 ✓ (200 + 100 = 300 > 255, hubo carry)
V = 0 (no hay error de signo)
Caso 2: Resta con Borrow
Entrada:

A = 5
B = 10
Operación: SUB
Resultado:

Decimal: 251
Hexadecimal: 0xFB
Binario: 11111011
Banderas:

Z = 0 (resultado no es cero)
N = 1 ✓ (bit 7 = 1, número negativo en complemento a 2)
C = 1 ✓ (5 - 10 < 0, se necesitó borrow)
V = 0 (no hay error de signo)
Nota: 251 es la representación en 8 bits de -5 en complemento a 2

Caso 3: Operación Lógica XOR
Entrada:

A = 170 (10101010)
B = 85 (01010101)
Operación: XOR
Resultado:

Decimal: 255
Hexadecimal: 0xFF
Binario: 11111111
Banderas:

Z = 0
N = 1 ✓ (bit 7 = 1)
C = 0 (no aplica en operaciones lógicas)
V = 0 (no aplica en operaciones lógicas)

Este simulador permite aprender:
- Cómo funciona una ALU real a nivel de bits
- El concepto de complemento a 2 para números negativos
- La diferencia entre overflow (V) y carry (C)
- Operaciones lógicas bit a bit
- Cómo las banderas ayudan a la CPU a tomar decisiones
- Diseño de interfaces para aplicaciones educativas
- El código está ampliamente comentado para facilitar el estudio y comprensión de cada concepto.
