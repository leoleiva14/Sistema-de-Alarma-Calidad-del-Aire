# Primer avance

Hola Mariano, Leonardo y Leonardo.

Gracias por el envío del primer avance.

## Documentación

### Aspectos de forma

- Formato
  - La documentación no está en el formato solicitado.
- Ecuaciones
  - Las ecuaciones deben ser escritas directamente en Markdown (con MkDocs).

#### Formato de `tasks.py`

Reporte de advertencias y errores según [PEP 8](https://peps.python.org/pep-0008/).

Evaluado con `$ flake8 tasks.py`.

```
tasks.py:6:1: F401 'datetime.datetime' imported but unused
tasks.py:29:1: E302 expected 2 blank lines, found 1
tasks.py:52:1: E302 expected 2 blank lines, found 1
tasks.py:63:1: E302 expected 2 blank lines, found 1
tasks.py:69:1: E302 expected 2 blank lines, found 1
tasks.py:72:12: F821 undefined name 'sqlite3'
tasks.py:73:1: W293 blank line contains whitespace
tasks.py:77:1: W293 blank line contains whitespace
tasks.py:80:1: W293 blank line contains whitespace
tasks.py:84:1: W293 blank line contains whitespace
tasks.py:86:5: F841 local variable 'aqi_stats' is assigned to but never used
tasks.py:87:1: W293 blank line contains whitespace
tasks.py:89:80: E501 line too long (93 > 79 characters)
tasks.py:90:80: E501 line too long (93 > 79 characters)
tasks.py:91:1: W293 blank line contains whitespace
tasks.py:92:5: F841 local variable 'moments' is assigned to but never used
tasks.py:93:1: W293 blank line contains whitespace
tasks.py:101:1: W293 blank line contains whitespace
tasks.py:109:1: W293 blank line contains whitespace
tasks.py:120:1: W293 blank line contains whitespace
tasks.py:134:1: W293 blank line contains whitespace
tasks.py:143:1: W293 blank line contains whitespace
tasks.py:148:1: E305 expected 2 blank lines after class or function definition, found 1
tasks.py:155:80: E501 line too long (83 > 79 characters)
```

#### Formato de `models.py`

Reporte de advertencias y errores según [PEP 8](https://peps.python.org/pep-0008/).

Evaluado con `$ flake8 models.py`.

```
models.py:1:1: F401 'sqlalchemy.DateTime' imported but unused
models.py:16:1: E302 expected 2 blank lines, found 1
models.py:37:1: E305 expected 2 blank lines after class or function definition, found 1
```

### Aspectos de fondo

- Modelos de probabilidad
  - Es necesario obtener un modelo de probabilidad. Pueden usar [Fitter](https://fitter.readthedocs.io/en/latest/) o en general [Stats](https://docs.scipy.org/doc/scipy/reference/stats.html) de SciPy.
  - En la parte de modelos de probabilidad de los datos debe haber un histograma con la función de densidad de probabilidad superpuesta y los detalles de la distribución (nombre, ecuación, parámetros).

## Nota

La nota de la revisión es de 2.4/5.