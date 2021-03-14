"""Top-level package for Windows Semaphore ctypes."""
from __future__ import annotations
from ctypes import POINTER, windll, WinError
from ctypes.wintypes import BOOL, DWORD, HANDLE, LONG, LPCWSTR, LPVOID
from typing import Union

__author__ = """Robert Alexander"""
__email__ = 'raalexander.phi@gmail.com'
__version__ = '0.1.2'

# https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
WAIT_OBJECT_0 = 0x00000000
WAIT_ABANDONED = 0x00000080
WAIT_TIMEOUT = 0x00000102
WAIT_FAILED = 0xFFFFFFFF
INFINITE = 0xFFFFFFFF

# https://docs.microsoft.com/en-us/windows/win32/sync/synchronization-object-security-and-access-rights
SEMAPHORE_ALL_ACCESS = 0x1F0003


class SemaphoreWaitTimeoutException(Exception):
    """
    WAIT_TIMEOUT
    """
    pass


LPSECURITY_ATTRIBUTES = LPVOID
LPLONG = POINTER(LONG)

"""
https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createsemaphoreexw
HANDLE CreateSemaphoreExW(
  LPSECURITY_ATTRIBUTES lpSemaphoreAttributes,
  LONG                  lInitialCount,
  LONG                  lMaximumCount,
  LPCWSTR               lpName,
  DWORD                 dwFlags,
  DWORD                 dwDesiredAccess
);
"""
CreateSemaphoreExW = windll.kernel32.CreateSemaphoreExW
CreateSemaphoreExW.argtypes = (LPSECURITY_ATTRIBUTES, LONG, LONG,
                               LPCWSTR, DWORD, DWORD)
CreateSemaphoreExW.restype = HANDLE

"""
https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-opensemaphorew
HANDLE OpenSemaphoreW(
  DWORD   dwDesiredAccess,
  BOOL    bInheritHandle,
  LPCWSTR lpName
);
"""
OpenSemaphoreW = windll.kernel32.OpenSemaphoreW
OpenSemaphoreW.argtypes = DWORD, BOOL, LPCWSTR
OpenSemaphoreW.restype = HANDLE

"""
https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
DWORD WaitForSingleObject(
  HANDLE hHandle,
  DWORD  dwMilliseconds
);
"""
WaitForSingleObject = windll.kernel32.WaitForSingleObject
WaitForSingleObject.argtypes = HANDLE, DWORD
WaitForSingleObject.restype = DWORD

"""
https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-releasesemaphore
BOOL ReleaseSemaphore(
  HANDLE hSemaphore,
  LONG   lReleaseCount,
  LPLONG lpPreviousCount
);
"""
ReleaseSemaphore = windll.kernel32.ReleaseSemaphore
ReleaseSemaphore.argtypes = HANDLE, LONG, LPLONG
ReleaseSemaphore.restype = BOOL

"""
https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
BOOL CloseHandle(
  HANDLE hObject
);
"""
CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = (HANDLE,)
CloseHandle.restype = BOOL


class Semaphore:
    def __init__(self, name: str = None):
        """
        Initialize Semaphore class

        :param name: A name for the Semaphore (default: unnamed)
        """
        self.name: str = name
        self.hHandle: HANDLE = HANDLE()

    def create(self,
               maximum_count: int = 1,
               initial_count: int = None,
               desired_access: DWORD = SEMAPHORE_ALL_ACCESS,
               ) -> Semaphore:
        """
        CreateSemaphoreExW

        :param maximum_count: The maximum count of the Semaphore
            (default: 1)
        :param initial_count: The initial count of the Semaphore
            (default: maximum_count)
        :param desired_access: The access mask for the semaphore object
            (default: SEMAPHORE_ALL_ACCESS)
        :raises OSError: The function has failed.
        :returns: The Semaphore, for chaining calls

        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createsemaphoreexw
        """
        assert not self.hHandle
        if initial_count is None:
            initial_count = maximum_count
        self.hHandle: HANDLE = CreateSemaphoreExW(
            None,
            LONG(initial_count),
            LONG(maximum_count),
            LPCWSTR(self.name),
            DWORD(0),  # reserved
            desired_access,
        )
        if not self.hHandle:
            raise WinError()
        return self

    def open(self,
             desired_access: DWORD = SEMAPHORE_ALL_ACCESS,
             inherit: bool = True,
             ) -> Semaphore:
        """
        OpenSemaphoreW

        :param desired_access: The access mask for the semaphore object
            (default: SEMAPHORE_ALL_ACCESS)
        :param inherit: If this value is TRUE, processes created by this
            process will inherit the handle.
        :raises OSError: The function has failed.
        :returns: The Semaphore, for chaining calls

        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-opensemaphorew
        """
        assert not self.hHandle
        assert self.name is not None
        self.hHandle: HANDLE = OpenSemaphoreW(
            desired_access,
            BOOL(inherit),
            LPCWSTR(self.name)
        )
        if not self.hHandle:
            raise WinError()
        return self

    def acquire(self, timeout_ms: int = None) -> Semaphore:
        """
        WaitForSingleObject
        :param timeout_ms: The time-out interval, in milliseconds. (default:
            None - infinite wait)
        :raises SemaphoreWaitTimeoutException: The time-out interval elapsed,
            and the object's state is nonsignaled.
        :raises OSError: The function has failed.
        :returns: The Semaphore, for chaining calls

        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
        """
        if timeout_ms is None:
            timeout_ms = INFINITE
        else:
            timeout_ms = DWORD(timeout_ms)
            assert timeout_ms != INFINITE, \
                "Use None to specify an infinite timeout"
        ret: DWORD = WaitForSingleObject(
            self.hHandle,
            timeout_ms
        )
        if ret == WAIT_OBJECT_0:
            return self
        elif ret == WAIT_TIMEOUT:
            raise SemaphoreWaitTimeoutException()
        elif ret == WAIT_FAILED:
            raise WinError()
        else:
            assert False, f"Unexpected return code: {ret}"

    def release(self, release_count: int = 1) -> int:
        """
        ReleaseSemaphore
        :param release_count: The amount to increase the semaphore's counter
        :returns: The previous count
        :raises OSError: When release() fails.

        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-releasesemaphore
        """
        previous_count: LONG = LONG(0)
        ret: BOOL = ReleaseSemaphore(
            self.hHandle,
            LONG(release_count),
            LPLONG(previous_count)
        )
        if not ret:
            raise WinError()
        return previous_count.value

    def close(self) -> None:
        """
        CloseHandle
        :raises OSError: When close() fails.

        https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
        """
        ret: BOOL = CloseHandle(
            self.hHandle
        )
        if not ret:
            raise WinError()
        self.hHandle = None

    def getvalue(self) -> int:
        assert self.hHandle is not None
        try:
            # quickly acquire and release to get the count
            self.acquire(0)
            return self.release() + 1
        except SemaphoreWaitTimeoutException:
            # acquire didn't immediately succeed, count must have been zero
            return 0


class CreateSemaphore:
    def __init__(self,
                 name: str = None,
                 maximum_count: int = 1,
                 initial_count: int = None,
                 desired_access: DWORD = SEMAPHORE_ALL_ACCESS,
                 ):
        self.sem = Semaphore(name)
        self.sem.create(maximum_count, initial_count, desired_access)

    def __enter__(self) -> CreateSemaphore:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sem.close()

    def getvalue(self) -> int:
        return self.sem.getvalue()


class OpenSemaphore:
    def __init__(self,
                 name: str = None,
                 desired_access: DWORD = SEMAPHORE_ALL_ACCESS,
                 inherit: bool = True,
                 ):
        self.sem = Semaphore(name)
        self.sem.open(desired_access, inherit)

    def __enter__(self) -> OpenSemaphore:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sem.close()

    def getvalue(self) -> int:
        return self.sem.getvalue()


class AcquireSemaphore:
    def __init__(self,
                 handle: Union[CreateSemaphore, OpenSemaphore],
                 timeout_ms: int = None
                 ):
        self.handle = handle
        self.timeout_ms = timeout_ms

    def __enter__(self) -> AcquireSemaphore:
        self.handle.sem.acquire(self.timeout_ms)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.sem.release()

    def getvalue(self) -> int:
        return self.handle.getvalue()
