# Herramientas de Depuración por Lenguaje

## JavaScript & TypeScript
-**Debugger de Navegador**: Usa `debugger;` para pausar la ejecución.
-**Log Avanzado**: `console.table()`, `console.time()`, `console.trace()`, `console.assert()`.
-**Profiling**: `performance.mark()` y `performance.measure()`.
-**.vscode/launch.json**: Configura debuggers para Node.js y Jest para capturar errores sin `console.log`.

## Python
-**PDB/Breakpoint**: Usa `breakpoint()` (Python 3.7+) o `import pdb; pdb.set_trace()`.
-**Post-mortem**: `pdb.post_mortem()` después de una excepción para inspeccionar el estado final.
-**IPDB**: Interfaz mejorada para el debugger.
-**Profiling**: `cProfile` y `pstats` para encontrar funciones lentas.

## Go
-**Delve (dlv)**: El debugger estándar para Go (`dlv debug main.go`).
-**Stack Traces**: `runtime/debug.PrintStack()`.
-**Pprof**: Profiling de memoria y CPU visitando `/debug/pprof/`.
-**Recovery**: Usa `recover()` con `debug.PrintStack()` en deferments.
