# Instalación — lo único que necesitas: `uv`

> Para todo el curso te basta con una herramienta: **`uv`**. Ella se encarga del
> resto, **incluido Python**: no tienes que instalar Python por separado. Esta
> guía cabe en una página; sigue el carril de tu sistema.

## 🍎 macOS (o Linux)

Opción A — con [Homebrew](https://brew.sh) (recomendada si ya lo usas):

```bash
brew install uv
```

Opción B — script oficial (si no tienes Homebrew):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Después de instalar, **cierra y reabre la terminal** (para que reconozca `uv`).

## 🪟 Windows (PowerShell)

Abre **PowerShell** y ejecuta:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Después de instalar, **cierra y reabre PowerShell**. Usa preferentemente
**Windows Terminal** o **PowerShell 7** (se ven mejor los acentos).

## Verifica que quedó bien

En cualquier sistema, ejecuta:

```bash
uv --version
```

**Salida esperada (el número puede variar):**

```
uv 0.11.x (...)
```

Necesitas **uv 0.11 o superior**. Si `uv --version` muestra algo menor, actualiza
con el mismo comando de instalación de arriba (es idempotente: lo deja al día).

Si ves una versión, ¡listo! Ya puedes entrar al primer laboratorio:

```bash
cd labs/lab-01-primer-dia
```

y seguir su `README.md`. El propio lab creará su entorno con Python 3.13 la
primera vez que corras el preparador.

## ¿Algo falló?

- `command not found: uv` / `'uv' no se reconoce…` → cierra y reabre la terminal;
  si insiste, reinicia la sesión.
- Cada laboratorio trae su propio `docs/troubleshooting.md` con las curas
  detalladas por sistema (ExecutionPolicy en Windows, PATH en macOS, acentos,
  antivirus, etc.).
