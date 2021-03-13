=====
Usage
=====

A trivial example::

    from semaphore_win_ctypes import AcquireSemaphore, OpenSemaphore

    with OpenSemaphore('name') as semaphore:
        with AcquireSemaphore(created, timeout_ms=0):
           # Perform work here
           pass

Here `CreateSemaphore` creates a semaphore named `name` with a counter of 5.
Then an attempt is made to acquire the semaphore once, giving up immediately if the semaphore's counter was zero.
Inside the with blocks, your custom code can run.
The with block for AcquireSemaphore will exit, releasing the semaphore.
Finally, the with block for CreateSemaphore will exit, closing the handle to the semaphore.

If you prefer, you can manage the lifecycle of the semaphore handle yourself::

    from semaphore_win_ctypes import Semaphore

    semaphore = Semaphore('name')
    try:
        semaphore.open()
        semaphore.acquire(timeout_ms=0)
        # Perform work here
        semaphore.release()
    finally:
        semaphore.close()

Note that the above examples do not actually create the semaphore.
Since this module uses the Semaphore Object provided by the Windows API, any code written in any language could create the semaphore by calling CreateSemaphoreExW.
Of course, if you need to create the semaphore from python, you can run::

    from semaphore_win_ctypes import CreateSemaphore

    with CreateSemaphore('name', maximum_count=5) as semaphore:
       # Use the semaphore
       pass

Or::

    from semaphore_win_ctypes import Semaphore

    semaphore = Semaphore('name')
    try:
        semaphore.create(maximum_count=5)
        # Use the semaphore
    finally:
        semaphore.close()

