# Sistema Integral de Gestión - Software FJ

Proyecto académico de la Fase 4 del curso Programación (213023) de la UNAD.
Implementa un sistema orientado a objetos para gestionar clientes, servicios
y reservas, sin base de datos, con manejo robusto de excepciones.

## Objetivo

Construir una aplicación estable, modular y extensible que aplique abstracción,
herencia, polimorfismo, encapsulación y manejo avanzado de excepciones,
garantizando que el sistema siga funcionando ante errores durante su ejecución.

## Características

- Clase abstracta EntidadBase y clase Cliente con validaciones
- Clase abstracta Servicio con tres servicios especializados (polimorfismo)
- Clase Reserva con manejo de estados y excepciones
- 4 excepciones personalizadas
- Bloques try/except/else/finally y encadenamiento de excepciones
- Registro de eventos y errores en archivo de logs (eventos.log)
- Simulación de 10 operaciones (válidas e inválidas)

## Cómo ejecutar

1. Asegúrate de tener Python 3 instalado.
2. Ejecuta en la terminal: python software-fj.py
3. Se generará el archivo eventos.log con el registro de la ejecución.

## Tecnologías

- Python 3
- Módulo logging (registro de eventos)
- Módulo abc (clases abstractas)

## Integrantes del equipo

- Jerson Adrián Collo - (Lider)
- Ingrith Toro - (Revisora)
- (Nombre 3) - (Consolidador)
- (Nombre 4) - (rol)
- (Nombre 5) - (rol)

## Licencia

Proyecto académico - UNAD 2026.
