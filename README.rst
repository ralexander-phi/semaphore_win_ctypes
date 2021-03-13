========================
Windows Semaphore ctypes
========================


.. image:: https://img.shields.io/pypi/v/semaphore_win_ctypes.svg
        :target: https://pypi.python.org/pypi/semaphore_win_ctypes
        :alt: Latest Version

.. image:: https://readthedocs.org/projects/semaphore-win-ctypes/badge/?version=latest
        :target: https://semaphore-win-ctypes.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


A ctypes wrapper for Windows Semaphore Objects


* Free software: MIT license
* Documentation: https://semaphore-win-ctypes.readthedocs.io.

Use Case
--------

This module was created to overcome limitations of Python's `built-in semaphore support`_.
Specifically, the built-in semaphores:

* Cannot be shared between python sub-processes
* Cannot interact with other programming languages

Instead, this module provides wrappers for these low level Windows Semaphore APIs:

* `CreateSemaphoreExW`_
* `OpenSemaphoreW`_
* `WaitForSingleObject`_
* `ReleaseSemaphore`_
* `CloseHandle`_

Since the Windows Semaphore API uses named semaphores to permit sharing between processes, you can now share your semaphore more freely.
Check the documentation for those APIs for details about how semaphores behave on Windows.

Dependencies
------------

This module requires no runtime dependencies.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _built-in semaphore support: https://docs.python.org/3/library/threading.html#threading.Semaphore
.. _CreateSemaphoreExW: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createsemaphoreexw
.. _OpenSemaphoreW: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-opensemaphorew
.. _WaitForSingleObject: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
.. _ReleaseSemaphore: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-releasesemaphore
.. _CloseHandle: https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
