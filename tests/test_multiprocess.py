import pytest
import subprocess
import time
import uuid

from multiprocessing.pool import ThreadPool
from semaphore_win_ctypes.semaphore_win_ctypes import AcquireSemaphore, \
    CreateSemaphore, OpenSemaphore, SemaphoreWaitTimeoutException

TEST_SEMAPHORE_MAX_COUNT = 2
TEST_THREADS = TEST_SEMAPHORE_MAX_COUNT * 2
TEST_SEMAPHORE_CREATE_TIME_MS = 5000
TEST_SEMAPHORE_ACQUIRE_HOLD_TIME_S = 2
LAST_WAS_CTYPES = False


def unique_name():
    return str(uuid.uuid4())


@pytest.fixture
def ctypes_semaphore() -> str:
    """
    Create a semaphore using ctypes
    """
    name = unique_name()
    with CreateSemaphore(name=name, maximum_count=TEST_SEMAPHORE_MAX_COUNT):
        yield name


@pytest.fixture
def cpp_semaphore() -> str:
    """
    Create a semaphore using compiled C++ helper
    """
    name = unique_name()
    proc = subprocess.Popen([
        "SemaphoreHelper.exe",
        "create",
        name,
        str(TEST_SEMAPHORE_CREATE_TIME_MS),
        str(TEST_SEMAPHORE_MAX_COUNT),
        str(TEST_SEMAPHORE_MAX_COUNT)
    ])
    # let it start
    time.sleep(1)
    yield name
    proc.wait()


def mixed_acquire(params) -> int:
    name = params[0]
    index = params[1]
    if index % 2 == 0:
        c = cpp_acquire(name)
    else:
        c = ctypes_acquire(name)
    return c


def ctypes_acquire(name: str) -> int:
    try:
        with OpenSemaphore(name=name) as sem:
            with AcquireSemaphore(sem, timeout_ms=0):
                time.sleep(TEST_SEMAPHORE_ACQUIRE_HOLD_TIME_S)
        return 1
    except SemaphoreWaitTimeoutException:
        return 0


def cpp_acquire(name: str) -> int:
    p = subprocess.run([
        "SemaphoreHelper.exe",
        "open-and-acquire",
        name,
        str(TEST_SEMAPHORE_ACQUIRE_HOLD_TIME_S * 1000)
    ])
    if p.returncode == 0:
        return 1
    else:
        return 0


def test_multiprocess_ctypes(ctypes_semaphore: str):
    # Create subprocesses, let each try to acquire the Semaphore
    with ThreadPool(TEST_THREADS) as p:
        results = p.map(
            ctypes_acquire,
            [ctypes_semaphore for _ in range(TEST_THREADS)]
        )
    # Only some of them should succeed
    assert sum(results) == TEST_SEMAPHORE_MAX_COUNT


def test_multiprocess_ctypes_with_cpp_semaphore(cpp_semaphore: str):
    # Create subprocesses, let each try to acquire the Semaphore
    with ThreadPool(TEST_THREADS) as p:
        results = p.map(
            ctypes_acquire,
            [cpp_semaphore for _ in range(TEST_THREADS)]
        )
    # Only some of them should succeed
    assert sum(results) == TEST_SEMAPHORE_MAX_COUNT


def test_multiprocess_cpp_acquire_with_ctypes_semaphore(ctypes_semaphore: str):
    # Create subprocesses, let each try to acquire the Semaphore
    with ThreadPool(TEST_THREADS) as p:
        results = p.map(
            cpp_acquire,
            [ctypes_semaphore for _ in range(TEST_THREADS)]
        )
    # Only some of them should succeed
    assert sum(results) == TEST_SEMAPHORE_MAX_COUNT


def test_multiprocess_cpp_acquire_with_cpp_semaphore(cpp_semaphore: str):
    # Create subprocesses, let each try to acquire the Semaphore
    with ThreadPool(TEST_THREADS) as p:
        results = p.map(
            cpp_acquire,
            [cpp_semaphore for _ in range(TEST_THREADS)]
        )
    # Only some of them should succeed
    assert sum(results) == TEST_SEMAPHORE_MAX_COUNT


def test_multiprocess_mixed_with_cpp_semaphore(cpp_semaphore: str):
    # Create subprocesses, let each try to acquire the Semaphore
    with ThreadPool(TEST_THREADS) as p:
        results = p.map(
            mixed_acquire,
            [(cpp_semaphore, index) for index in range(TEST_THREADS)]
        )
    # Only some of them should succeed
    assert sum(results) == TEST_SEMAPHORE_MAX_COUNT


def test_multiprocess_mixed_with_ctypes_semaphore(ctypes_semaphore: str):
    # Create subprocesses, let each try to acquire the Semaphore
    with ThreadPool(TEST_THREADS) as p:
        results = p.map(
            mixed_acquire,
            [(ctypes_semaphore, index) for index in range(TEST_THREADS)]
        )
    # Only some of them should succeed
    assert sum(results) == TEST_SEMAPHORE_MAX_COUNT
