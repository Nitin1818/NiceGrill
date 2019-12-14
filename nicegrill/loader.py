import logging
import importlib
import os
from nicegrill.modules import _init

BLACKLIST = ["Loader", "Help", "Settings"]

class loadmod:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def load(mod):
        try:
            imp = importlib.import_module(mod[0:-3].replace("/", "."))
        except Exception as e:
            os.remove(mod)
            loadmod.logger.error(e)
            return False
        for cls in vars(imp):
            if callable(vars(imp)[cls]):
                clss = vars(imp)[cls]
                for func in vars(clss):
                    if callable(vars(clss)[func]) and vars(clss)[func].__name__.endswith("xxx"):
                        _init.modules.update(
                            {vars(clss)[func].__name__.replace("xxx", ""): vars(clss)[func]})
                        _init.classes.update({clss.__name__: vars(clss)[func].__name__})
        return True

    def unload(mod):
        if mod.capitalize() in BLACKLIST:
            return False
        try:
            imp = importlib.import_module(f"nicegrill.modules.{mod.lower()}")
        except Exception as e:
            loadmod.logger.error(e)
            return False
        clss = vars(imp)[mod.capitalize()]
        for func in vars(clss):
            if callable(vars(clss)[func]) and vars(clss)[func].__name__.endswith("xxx"):
                try:
                    del _init.modules[vars(clss)[func].__name__.replace("xxx", "")]
                    del _init.classes[mod.capitalize()]
                except KeyError as e:
                    loadmod.logger.error(e)
                    return False
        return True
