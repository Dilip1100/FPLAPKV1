Traceback (most recent call last):
  File "/opt/render/project/src/.venv/bin/gunicorn", line 8, in <module>
    sys.exit(run())
             ^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/wsgiapp.py", line 67, in run
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/base.py", line 236, in run
    super().run()
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/base.py", line 72, in run
    Arbiter(self).run()
    ^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/arbiter.py", line 58, in __init__
    self.setup(app)
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/arbiter.py", line 118, in setup
    self.app.wsgi()
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/base.py", line 67, in wsgi
    self.callable = self.load()
                    ^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
    return self.load_wsgiapp()
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
    return util.import_app(self.app_uri)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/util.py", line 371, in import_app
    mod = importlib.import_module(module)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.12.11/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/render/project/src/dash_app.py", line 203, in <module>
    dcc.Dropdown(
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/dash/development/base_component.py", line 425, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/dash/dcc/Dropdown.py", line 201, in __init__
    super(Dropdown, self).__init__(**args)
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/dash/development/base_component.py", line 143, in __init__
    raise TypeError(
TypeError: The `dcc.Dropdown` component (version 2.17.1) with the ID "salespeople-dropdown" received an unexpected keyword argument: `aria-label`
Allowed arguments: className, clearable, disabled, id, loading_state, maxHeight, multi, optionHeight, options, persisted_props, persistence, persistence_type, placeholder, search_value, searchable, style, value
==> Running 'gunicorn dash_app:server'
Traceback (most recent call last):
  File "/opt/render/project/src/.venv/bin/gunicorn", line 8, in <module>
    sys.exit(run())
             ^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/wsgiapp.py", line 67, in run
    WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]", prog=prog).run()
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/base.py", line 236, in run
    super().run()
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/base.py", line 72, in run
    Arbiter(self).run()
    ^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/arbiter.py", line 58, in __init__
    self.setup(app)
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/arbiter.py", line 118, in setup
    self.app.wsgi()
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/base.py", line 67, in wsgi
    self.callable = self.load()
                    ^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/wsgiapp.py", line 58, in load
    return self.load_wsgiapp()
           ^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/app/wsgiapp.py", line 48, in load_wsgiapp
    return util.import_app(self.app_uri)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/gunicorn/util.py", line 371, in import_app
    mod = importlib.import_module(module)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/python/Python-3.12.11/lib/python3.12/importlib/__init__.py", line 90, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 999, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/opt/render/project/src/dash_app.py", line 203, in <module>
    dcc.Dropdown(
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/dash/development/base_component.py", line 425, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/dash/dcc/Dropdown.py", line 201, in __init__
    super(Dropdown, self).__init__(**args)
  File "/opt/render/project/src/.venv/lib/python3.12/site-packages/dash/development/base_component.py", line 143, in __init__
    raise TypeError(
TypeError: The `dcc.Dropdown` component (version 2.17.1) with the ID "salespeople-dropdown" received an unexpected keyword argument: `aria-label`
