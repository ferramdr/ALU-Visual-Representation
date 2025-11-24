# 🖥️ Simulador de CPU - ALU de 8 Bits

**Simulador educativo de una Unidad Aritmético-Lógica (ALU) de 8 bits con interfaz gráfica en Python/Tkinter**

Este proyecto simula el funcionamiento de un procesador real, mostrando visualmente cómo opera una ALU, cómo se calculan las banderas de estado, y cómo funciona un ciclo de reloj (clock) en un CPU.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso Básico](#-uso-básico)
- [Funcionalidades Detalladas](#-funcionalidades-detalladas)
- [Arquitectura del Código](#-arquitectura-del-código)
- [Aspectos Educativos](#-aspectos-educativos)
- [Capturas de Pantalla](#-capturas-de-pantalla)

---

## ✨ Características Principales

### 🔧 Operaciones de la ALU

- **Aritméticas**: ADD (Suma), SUB (Resta)
- **Lógicas**: AND, OR, XOR, NOT

### 🚦 Sistema de Banderas (Flags)

- **Z (Zero)**: Se activa cuando el resultado es 0
- **N (Negative)**: Se activa cuando el bit 7 está en 1 (número negativo en complemento a 2)
- **C (Carry)**: Indica desbordamiento en aritmética sin signo
- **V (Overflow)**: Indica error de signo en aritmética con signo

### 🎨 Interfaz Profesional

- Tema oscuro estilo hardware (#1a1a2e)
- Indicadores LED para las banderas (verde/rojo)
- Visualización en 3 formatos: Decimal, Hexadecimal, Binario
- Formato de nibbles (espacios cada 4 bits: `1111 1111`)

### ⚡ Características Avanzadas

#### 1. **Visualización Interactiva de Bits**

- 8 checkbuttons por cada registro (Bit 7 a Bit 0)
- **Sincronización bidireccional**:
  - ✍️ Escribir número → checkbuttons se actualizan
  - ☑️ Hacer clic en bit → número se actualiza
- Sistema anti-loops infinitos

#### 2. **Botón de Acumulador**

- Simula un registro acumulador real
- Transfiere el resultado al Registro ACC
- Reinicia el Registro B (TMP) a 0
- Útil para operaciones en cadena

#### 3. **Barra de Estado Informativa**

- Mensajes en lenguaje humano sobre las banderas
- Ejemplos:
  - `⚠️ ¡OVERFLOW! Desbordamiento de signo detectado`
  - `🔴 CARRY: El resultado (200+100=300) excedió 8 bits (>255)`
- Colores dinámicos según severidad

#### 4. **Toggle Signed/Unsigned**

- Checkbox para interpretar resultados como complemento a 2
- **Unsigned**: 0 a 255 (valor estándar)
- **Signed**: -128 a 127 (complemento a 2)
- Ejemplo: `11111111` = 255 (unsigned) o -1 (signed)

#### 5. **Simulación de Reloj (Clock)** 🆕

La característica más impresionante: **el procesador "piensa" por sí mismo**

- **LED de Pulso**: Parpadea rojo ↔ verde simulando el clock
- **Terminología de Procesador**:
  - Registro Acumulador (ACC) - antes "Operando A"
  - Registro B (TMP) - antes "Operando B"
- **Modo Automático**:
  1. Presiona `▶ Iniciar Reloj (Auto)`
  2. Cada 1.5 segundos:
     - Genera un número aleatorio para Registro B
     - Ejecuta la operación seleccionada
     - Actualiza ACC con el resultado
     - Muestra el pulso del reloj
  3. El procesador trabaja continuamente hasta presionar `⏹ Detener Reloj`

---

## 📦 Requisitos

- **Python 3.8+**
- **Tkinter** (incluido por defecto en Python)
- No requiere bibliotecas externas

---

## 🚀 Instalación

```bash
# Clonar o descargar el repositorio
git clone <URL_DEL_REPO>
cd "Funcionamiento del ALU"

# Ejecutar el simulador
python alu_simulator.py
```

---

## 🎮 Uso Básico

### Operación Manual

1. **Ingresa valores** en los registros ACC y TMP (0-255)
2. **Selecciona una operación** (ADD, SUB, AND, etc.)
3. **Observa**:
   - El resultado en 3 formatos
   - Las banderas LED activadas
   - La explicación en la barra de estado
4. (Opcional) **Activa "Ver como Signed"** para interpretar complemento a 2

### Modo Reloj Automático

1. **Selecciona una operación** (ej: ADD)
2. **Presiona "▶ Iniciar Reloj (Auto)"**
3. **Observa** cómo el procesador:
   - Genera datos aleatorios
   - Ejecuta operaciones automáticamente
   - Actualiza el acumulador
   - Parpadea el LED de pulso
4. **Presiona "⏹ Detener Reloj"** para parar

### Interacción con Bits

1. **Escribe un número** (ej: 170) → Los bits se activan automáticamente
2. **Haz clic en un bit** (ej: Bit 7) → El número se actualiza (+128)
3. Los binarios se muestran con formato nibbles: `1010 1010`

---

## 🔍 Funcionalidades Detalladas

### Operaciones Aritméticas

#### ADD (Suma)

```
ACC = 200, TMP = 100
200 + 100 = 300 (en 9 bits)
Resultado: 44 (300 & 0xFF)
Banderas: C=1 (hubo carry)
```

#### SUB (Resta)

```
ACC = 5, TMP = 10
5 - 10 = -5 (en complemento a 2)
Resultado: 251 (0xFB)
Banderas: C=1 (borrow), N=1 (negativo)
```

### Operaciones Lógicas

#### AND

```
ACC = 170 (10101010)
TMP = 85  (01010101)
Resultado: 0 (00000000)
Banderas: Z=1 (resultado cero)
```

#### XOR

```
ACC = 170 (10101010)
TMP = 85  (01010101)
Resultado: 255 (11111111)
Banderas: N=1 (bit 7 activo)
```

### Sistema de Banderas

| Bandera | Nombre   | Cuándo se activa              | Color LED | Prioridad |
| ------- | -------- | ----------------------------- | --------- | --------- |
| **V**   | Overflow | Error en aritmética con signo | 🔴 Rojo   | Alta      |
| **C**   | Carry    | Desbordamiento sin signo      | 🔴 Rojo   | Alta      |
| **N**   | Negative | Bit 7 = 1                     | 🟢 Verde  | Media     |
| **Z**   | Zero     | Resultado = 0                 | 🟢 Verde  | Baja      |

---

## 🏗️ Arquitectura del Código

### Backend: Clase `ALU`

```python
class ALU:
    """Lógica pura de la ALU sin interfaz gráfica"""

    def execute(self, a: int, b: int, opcode: int) -> tuple:
        """Ejecuta operación y retorna (resultado, banderas)"""
```

**Responsabilidades**:

- Ejecutar operaciones (ADD, SUB, AND, OR, XOR, NOT)
- Calcular banderas (Z, N, C, V)
- Aplicar máscara de 8 bits (`& 0xFF`)

### Frontend: Clase `ALUSimulatorGUI`

```python
class ALUSimulatorGUI:
    """Interfaz gráfica con Tkinter"""
```

**Responsabilidades**:

- Crear todos los widgets (entradas, botones, LEDs)
- Sincronizar bits ↔ texto
- Controlar simulación de reloj
- Actualizar visualización de resultados

### Métodos Clave

#### Sincronización Bidireccional

```python
def update_binary_a(self):      # Texto → Checkboxes
def sync_bits_to_text_a(self):  # Checkboxes → Texto
```

#### Simulación de Reloj

```python
def start_clock(self):          # Inicia ciclo automático
def stop_clock(self):           # Detiene ciclo
def clock_tick(self):           # Ejecuta un ciclo (1.5s)
def pulse_clock_led(self):      # Parpadeo LED
```

#### Visualización

```python
def update_result_display(self):    # Actualiza Dec/Hex/Bin
def format_binary_nibbles(self):    # Formato 1111 1111
def to_signed_8bit(self):           # Convierte a complemento a 2
```

---

## 🎓 Aspectos Educativos

### Conceptos Enseñados

1. **Arquitectura de Computadoras**

   - Funcionamiento de una ALU
   - Registros (ACC, TMP)
   - Ciclos de reloj

2. **Representación Numérica**

   - Binario, Decimal, Hexadecimal
   - Complemento a 2
   - Nibbles (medio byte)

3. **Banderas de Estado**

   - Por qué existen
   - Cuándo se activan
   - Diferencia entre Carry y Overflow

4. **Operaciones Bit a Bit**
   - AND, OR, XOR, NOT
   - Máscaras de bits
   - Desplazamientos lógicos

### Comentarios en el Código

- **+500 líneas** de comentarios explicativos
- Ejemplos prácticos de cada concepto
- Explicación de teoría (ej: cálculo de overflow)

---

## 📸 Capturas de Pantalla

### Modo Normal

```
🖥️ SIMULADOR DE CPU - ALU DE 8 BITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
● Ciclo de Reloj: [DETENIDO]

REGISTROS DEL PROCESADOR (0-255)
  Registro Acumulador (ACC): 255
  Binario: 1111 1111
  Bits: ☑7 ☑6 ☑5 ☑4 ☑3 ☑2 ☑1 ☑0

  Registro B (TMP): 100
  Binario: 0110 0100
  Bits: ☐7 ☑6 ☑5 ☐4 ☐3 ☑2 ☐1 ☐0

RESULTADO
  Dec: 99  |  Hex: 0x63
  Binario: 0110 0011
  ☑ Ver como Signed (-128 a 127)
  [🔄 Usar Resultado como A]
  [▶ Iniciar Reloj (Auto)]

BANDERAS DE ESTADO (FLAGS)
  🟢 Z  ZERO          Resultado = 0
  🟢 N  NEGATIVE      Bit 7 = 1
  🔴 C  CARRY         Desbordamiento sin signo
  🔴 V  OVERFLOW      Error de signo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Operación exitosa: ADD = 99
```

### Modo Reloj Activo

```
● Ciclo de Reloj: [ACTIVO - EJECUTANDO]
    ^-- LED parpadeando rojo ↔ verde

[⏹ Detener Reloj]  ← Botón rojo

ACC actualiz ándose automáticamente cada 1.5s
TMP recibiendo valores aleatorios (0-255)
```

---

## 🛠️ Tamaño y Especificaciones

- **Ventana**: 850x850 píxeles
- **Líneas de código**: ~1,450 (con comentarios)
- **Velocidad de reloj**: 1.5 segundos por ciclo
- **Arquitectura**: Separación backend/frontend
- **Performance**: Instantánea para todas las operaciones

---

## 📝 Notas Técnicas

### Formato de Nibbles

Todos los binarios se muestran con un espacio cada 4 bits:

```
Antes: 11111111
Ahora: 1111 1111
```

### Toggle Signed/Unsigned

- **Hex y Binario**: Siempre muestran valor raw (unsigned)
- **Decimal**: Cambia según el toggle
- **Banderas**: No se ven afectadas (calculadas correctamente)

### Prevención de Loops

Se usan 4 flags de control para evitar loops infinitos en la sincronización bidireccional:

```python
self.updating_from_text_a = False
self.updating_from_bits_a = False
self.updating_from_text_b = False
self.updating_from_bits_b = False
```
