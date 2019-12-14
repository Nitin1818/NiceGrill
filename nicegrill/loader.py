import logging
import json
import os
from nicegrill.modules._init import modules, classes


BLACKLIST = ["Loader", "Help", "Settings", "Misc"]

class loadmod:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def load(mod):
        try:
            imp = __import__(mod[0:-3].replace("/", "."))
            os.remove(mod)
        except Exception as e:
            os.remove(mod)
            loadmod.logger.error(e)
            return False
        for cls in vars(imp):
            if callable(vars(imp)[cls]):
                clss = vars(imp)[cls]
                classes.update({clss.__name__: {}})
                modules.update({clss.__name__: {}})
                for func in vars(clss):
                    if callable(vars(clss)[func]) and vars(clss)[func].__name__.endswith("xxx"):
                        modules[clss.__name__].update(
                            {vars(clss)[func].__name__[0:-3]: vars(clss)[func]})
                        classes.update({clss.__name__: vars(clss)[func].__name__[0:-3]})
                if not classes[clss.__name__]:
                    del classes[clss.__name__]
                    del modules[clss.__name__]
        return True

    def unload(mod):
        if mod.capitalize() in BLACKLIST:
            return False
        for clss in modules:
            print(mod, clss)
            if mod.lower() == clss.lower():
                del modules[clss]
                del classes[clss]
                return True