import os
import importlib.util

config_paths = [
    os.environ.get('MARCOS_CLIENT_CONFIG'),
    "local_config.py",
    os.path.expanduser('~/.config/marcos_config.py'),
]

mod = None
for path in config_paths:
    if path and os.path.exists(path):
        spec = importlib.util.spec_from_file_location("_user_cfg", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        break

if mod:
    for name in dir(mod):
        if not name.startswith("_"):
            locals()[name] = getattr(mod, name)

    from . import default_config as mod

from . import default_config as default

for name in dir(default):
    if not name.startswith("_") and not name in locals():
        locals()[name] = getattr(default, name)