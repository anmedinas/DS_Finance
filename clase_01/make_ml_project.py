# Creación programática de la estructura de proyecto
# Ejecutar esto para inicializar cualquier nuevo proyecto del curso

from pathlib import Path
from datetime import date
import json

def crear_estructura_proyecto(nombre_proyecto: str, base_dir: str = ".") -> None:
    """
    Crea la estructura estándar de directorios para un proyecto ML Finance.

    Parameters
    ----------
    nombre_proyecto : str
        Nombre del proyecto (se convierte a snake_case)
    base_dir : str
        Directorio base donde crear el proyecto
    """
    nombre = nombre_proyecto.lower().replace(" ", "_")
    raiz = Path(base_dir) / nombre

    directorios = [
        "data/raw", "data/processed", "data/external",
        "notebooks", "src", "models", "reports/figures", "tests",
    ]

    for d in directorios:
        (raiz / d).mkdir(parents=True, exist_ok=True)
        (raiz / d / ".gitkeep").touch()

    (raiz / "src" / "__init__.py").write_text("")

    gitignore = """# Datos y modelos grandes
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep
models/**/*.pkl
models/**/*.joblib
models/**/*.h5

# Credenciales y secretos
.env
*.key
credentials.json
secrets.yaml

# Python
__pycache__/
*.pyc
*.pyo
.ipynb_checkpoints/

# Entornos
.venv/
venv/

# Sistema operativo
.DS_Store
Thumbs.db

# IDEs
.vscode/
.idea/

# Outputs temporales
*.log
mlruns/"""

    (raiz / ".gitignore").write_text(gitignore)

    readme = f"""# {nombre_proyecto}

**Creado**: {date.today().isoformat()}  
**Curso**: Machine Learning Aplicado a las Finanzas — USACH

## Descripción

> Describir aquí el problema financiero que aborda el proyecto.

## Reproducción

```bash
git clone <url>
cd {nombre}
conda env create -f environment.yml
conda activate {nombre}
jupyter lab
```

## Estructura

```
data/       → Datos (raw inmutable, processed derivado)
notebooks/  → Exploración y desarrollo
src/        → Código modular reutilizable
models/     → Artefactos serializados + metadata
reports/    → Resultados finales
```
"""
    (raiz / "README.md").write_text(readme)

    env_yml = f"""name: {nombre}
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - pip
  - pandas>=2.0
  - numpy>=1.25
  - scikit-learn>=1.3
  - matplotlib>=3.7
  - seaborn>=0.12
  - jupyterlab>=4.0
  - ipykernel
  - pip:
    - yfinance>=0.2.30
    - xgboost>=2.0
    - lightgbm>=4.0
    - shap>=0.44
    - mlflow>=2.10
    - python-dotenv>=1.0
"""
    (raiz / "environment.yml").write_text(env_yml)

    print(f"Proyecto '{nombre}' creado en: {raiz.resolve()}")
    print("\nEstructura generada:")
    for item in sorted(raiz.rglob("*")):
        nivel = len(item.relative_to(raiz).parts) - 1
        prefijo = "    " * nivel + ("├── " if nivel > 0 else "")
        print(f"{prefijo}{item.name}")


# Crear un proyecto de práctica
crear_estructura_proyecto("practica_setup", base_dir=".")