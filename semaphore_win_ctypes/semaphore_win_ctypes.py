"""Main module."""

from ctypes import *
from ctypes.wintypes import BOOL, DWORD, HANDLE, LPCWSTR, LONG


class SemaphoreMaximumCountWouldBeExceededException(Exception):
    """
    When performing a Semaphore.release() the semaphore's maximum value would be exceeded
    """
    pass


class SemaphoreWaitAbandonedException(Exception):
    """
    WAIT_ABANDONED
    """
    pass


class SemaphoreWaitTimeoutException(Exception):
    """
    WAIT_TIMEOUT
    """
    pass


class SemaphoreWaitFailedException(Exception):
    """
    WAIT_FAILED
    """
    pass


class Semaphore:
    def __init__(self):
        self.hHandle: HANDLE = None

    def create(self, attr=None, initial_count: int = 1, maximum_count: int = 1, name: str = None) -> None:
        """
        I.E:
        CreateSemaphoreW()
        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createsemaphorew
        LPSECURITY_ATTRIBUTES lpSemaphoreAttributes,
        LONG                  lInitialCount,
        LONG                  lMaximumCount,
        LPCWSTR               lpName
        """
        self.hHandle: HANDLE = windll.kernel32.CreateSemaphoreW(
            attr,
            LONG(initial_count),
            LONG(maximum_count),
            LPCWSTR(name)
        )
        if not self.hHandle:
            raise WinError()

    def open(self, name: str, desired_access: int, inherit: bool = True) -> None:
        """
        I.E.:
        OpenSemaphoreW()
        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-opensemaphorew
        DWORD   dwDesiredAccess,
        BOOL    bInheritHandle,
        LPCWSTR lpName
        """
        self.hHandle: HANDLE = windll.kernel32.OpenSemaphoreW(
            DWORD(desired_access),
            BOOL(inherit),
            LPCWSTR(name)
        )
        if not self.hHandle:
            raise WinError()

    def acquire(self, timeout_ms: int) -> None:
        """
        Try to decrement the semaphore's counter.

        timeout_ms:
          0 -> Don't wait
          non-zero -> Wait the specified number of milliseconds
          INFINITE -> Wait as long as needed

        I.E.:
        WaitForSingleObject()
        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
        HANDLE hHandle,
        DWORD  dwMilliseconds
        """
        assert self.hHandle
        ret: DWORD = windll.kernel32.WaitForSingleObject(
            self.hHandle,
            DWORD(timeout_ms)
        )
        if ret == 0x80:
            raise SemaphoreWaitAbandonedException()
        elif ret == 0x0:
            return
        elif ret == 0x102:
            raise SemaphoreWaitTimeoutException()
        elif ret == 0xFFFFFFFF:
            raise SemaphoreWaitFailedException()
        else:
            assert False, f"Unknown return code: {ret}"

    def release(self, release_count: int = 1) -> int:
        """
        Release the specified count.
        If the release would exceed the semaphore limit, raises SemaphoreMaximumCountWouldBeExceeded
        Returns the previous count

        I.E.:
        ReleaseSemaphore()
        https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-releasesemaphore
        HANDLE hSemaphore,
        LONG   lReleaseCount,
        LPLONG lpPreviousCount
        """
        assert self.hHandle
        lPreviousCount: c_long = c_long(0)
        ret: BOOL = windll.kernel32.ReleaseSemaphore(
            self.hHandle,
            c_long(release_count),
            pointer(lPreviousCount)
        )
        if not ret:
            raise WinError()
        return lPreviousCount.value

    def close(self) -> None:
        """
        I.E.:
        https://docs.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
        BOOL CloseHandle(
          HANDLE hObject
        );
        """
        assert self.hHandle
        ret: BOOL = windll.kernel32.CloseHandle(
            self.hHandle
        )
        if not ret:
            raise WinError()

    def unlink(self) -> None:
        """
        Which is this?
        """
        pass
