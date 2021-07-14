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

* Can only be `shared between python processes`_ if a common parent python process coordinates
* Cannot be acquired by code written in other programming languages

Instead, this module provides wrappers for these low level Windows Semaphore APIs:

* `CreateSemaphoreExW`_
* `OpenSemaphoreW`_
* `WaitForSingleObject`_
* `ReleaseSemaphore`_
* `CloseHandle`_

Since the Windows Semaphore API uses named semaphores to permit sharing between processes, you can now share your semaphore more freely.
Check the documentation of those APIs for details about how semaphores behave on Windows.

Dependencies
------------

This module requires no runtime dependencies.

See Also
--------

PyPI:

* https://pypi.org/project/semaphore-win-ctypes/

Documentation:

* https://semaphore-win-ctypes.readthedocs.io/

Related Python standard library code:

* `Python threading.Semaphore`_
* `Python multiprocessing.Semaphore`_
* `Python asyncio.Semaphore`_

Similar work on other platforms:

* `POSIX IPC`_ for better semaphores on POSIX (I.E. Linux, UNIX-like, etc.) OSes.

Other items:

* `windows semaphore helper`_ -- C++ demo of working with Windows Semaphore APIs

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.


.. _`shared between python processes`: https://stackoverflow.com/a/28854553
.. _`built-in semaphore support`: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Semaphore
.. _`CreateSemaphoreExW`: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createsemaphoreexw
.. _`OpenSemaphoreW`: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-opensemaphorew
.. _`WaitForSingleObject`: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
.. _`ReleaseSemaphore`: https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-releasesemaphore
.. _`CloseHandle`: https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`Python threading.Semaphore`: https://docs.python.org/3/library/threading.html#threading.Semaphore
.. _`Python multiprocessing.Semaphore`: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Semaphore
.. _`Python asyncio.Semaphore`: https://docs.python.org/3/library/asyncio-sync.html#asyncio.Semaphore
.. _`POSIX IPC`: https://semanchuk.com/philip/posix_ipc/
.. _`windows semaphore helper`: https://github.com/ralexander-phi/windows-semaphore-helper
