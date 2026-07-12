from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESAMIENTO_DIR = BASE_DIR / "Procesamiento"

for path in [str(BASE_DIR), str(PROCESAMIENTO_DIR)]:
    if path not in sys.path:
        sys.path.append(path)

from Procesamiento.bienvenida import main


if __name__ == "__main__":
    main()
