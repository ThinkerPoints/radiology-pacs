import pkgutil, importlib
import measurements, annotations, navigation, tools

def load_plugins():
    for pkg in [measurements, annotations, navigation, tools]:
        for _, mod, _ in pkgutil.iter_modules(pkg.__path__):
            importlib.import_module(f"{pkg.__name__}.{mod}")
