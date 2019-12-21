import logging
import functools
from nicegrill.modules._init import modules, classes, watchouts
from telethon import events


BLACKLIST = ["Loader", "Help", "Settings", "Misc"]


class loadmod:

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    def load(mod, client):
        try:
            imp = __import__(mod[0:-3].replace("/", "."))
        except Exception as e:
            loadmod.logger.error(e)
            return False
        for cls in vars(imp):
            if callable(vars(imp)[cls]):
                clss = vars(imp)[cls]
                classes.update({clss.__name__: {}})
                modules.update({clss.__name__: {}})
                for func in vars(clss):
                    if "watchout" in str(vars(clss)[func]):
                        watchouts.append(vars(clss)[func])
                        client.add_event_handler(
                            functools.partial(
                                vars(clss)[func]), events.NewMessage(
                                outgoing=True, incoming=True, forwards=False))
                    if callable(vars(clss)[func]) and vars(
                            clss)[func].__name__.endswith("xxx"):
                        modules[clss.__name__].update(
                            {vars(clss)[func].__name__[0:-3]: vars(clss)[func]})
                        classes.update(
                            {clss.__name__: vars(clss)[func].__name__[0:-3]})
                if not classes[clss.__name__]:
                    del classes[clss.__name__]
                    del modules[clss.__name__]
        return True

    def unload(mod, client):
        if mod.capitalize() in BLACKLIST:
            return False
        for watchout in client.list_event_handlers():
            if mod in str(watchout[0]):
                client.remove_event_handler(watchout[0])
        for clss in modules:
            if mod.lower() == clss.lower():
                del modules[clss]
                del classes[clss]
                return True
