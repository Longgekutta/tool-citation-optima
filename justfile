# tool-citation-optima justfile
default:
    @just --list

setup:
    @python -c "import sys; print(f'Environment OK: Python {sys.version}')"

run:
    @python main.py run

test:
    @python -m unittest discover tests

health:
    @python main.py health

clean:
    @python -c "import shutil, pathlib; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
