import urllib
import importlib
import os
from database.allinone import get_func


modules = {}
classes = {}
imported = []
watchouts = []
cmds = {}


def loads():
    if get_func():
        for name in get_func():
            urllib.request.urlretrieve(name[1], "./" + name[0])
            try:
                imported.append(__import__(name[0][0:-3]))
                print("Module is loaded: {}".format(
                    name[0][0:-3].capitalize()))
            except ImportError as e:
                print("Module can not be loaded: {}\n\n{}".format(
                    name[0][0:-3].capitalize(), e))
            os.remove(name[0])
    base = os.path.basename(__name__)
    for f in os.listdir("/".join(base.split(".")[:2])):
        if not f.startswith("_") and f.endswith(".py"):
            try:
                f = os.path.join(".".join(base.split(".")[:2] + [f[:-3]]))
                imported.append(importlib.import_module(f))
                print("Module is loaded: {}".format(f[18::].capitalize()))
            except ImportError as e:
                print("Module can not be loaded: {}\n\n{}".format(
                    f[18::].capitalize(), e))
    imports()


def imports():
    for module in imported:
        for var in vars(module):
            if callable(vars(module)[var]):
                getclss = vars(module)[var]
                classes.update({getclss.__name__: {}})
                modules.update({getclss.__name__: {}})
                for cmd in vars(getclss):
                    if "watchout" in str(vars(getclss)[cmd]):
                        watchouts.append(vars(getclss)[cmd])
                    if callable(vars(getclss)[cmd]) and vars(
                            getclss)[cmd].__name__.endswith("xxx"):
                        modules[getclss.__name__].update(
                            {vars(getclss)[cmd].__name__.replace("xxx", ""): vars(getclss)[cmd]})
                        classes[getclss.__name__].update(
                            {vars(getclss)[cmd].__name__.replace("xxx", ""): vars(getclss)[cmd]})
                        cmds.update({vars(getclss)[cmd].__name__.replace(
                            "xxx", ""): vars(getclss)[cmd]})
                if not classes[getclss.__name__]:
                    del classes[getclss.__name__]
                    del modules[getclss.__name__]
