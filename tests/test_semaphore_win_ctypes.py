"""Tests for `semaphore_win_ctypes` package."""

import datetime
import pytest
import uuid

from ctypes.wintypes import DWORD
from semaphore_win_ctypes import Semaphore, \
    SemaphoreWaitTimeoutException, CreateSemaphore, OpenSemaphore, \
    AcquireSemaphore


@pytest.fixture
def unique_name():
    return str(uuid.uuid4())


def test_basic_with_statements(unique_name):
    with pytest.raises(OSError):
        # Error: Doesn't exist yet
        with OpenSemaphore(unique_name):
            pass

    with CreateSemaphore(unique_name) as created:
        assert created.getvalue() == 1
        with OpenSemaphore(unique_name) as opened:
            assert opened.getvalue() == 1
            with AcquireSemaphore(created, timeout_ms=0) as acquired:
                assert acquired.getvalue() == 0
                with pytest.raises(SemaphoreWaitTimeoutException):
                    # Already acquired
                    with AcquireSemaphore(opened, timeout_ms=0):
                        pass
            with AcquireSemaphore(opened, timeout_ms=0):
                with pytest.raises(SemaphoreWaitTimeoutException):
                    # Already acquired
                    with AcquireSemaphore(created, timeout_ms=0):
                        pass

    with pytest.raises(OSError):
        # Error: CreateSemaphore with statement destroyed the semaphore already
        with OpenSemaphore(unique_name):
            pass


def test_release(unique_name):
    sem = Semaphore(unique_name).create()
    try:
        assert sem.name == unique_name
        sem.acquire(0)
        old_count = sem.release()
        assert old_count == 0
    finally:
        sem.close()


def test_multi_release(unique_name):
    sem = Semaphore(unique_name).create(maximum_count=5, initial_count=5)
    try:
        for _ in range(5):
            sem.acquire(0)
        with pytest.raises(SemaphoreWaitTimeoutException):
            # Can't acquire 6 times
            sem.acquire(0)

        old_count = sem.release(release_count=5)
        assert old_count == 0

        for _ in range(5):
            sem.acquire(0)
        with pytest.raises(SemaphoreWaitTimeoutException):
            # Can't acquire 6 times
            sem.acquire(0)
    finally:
        sem.close()


def test_old_count(unique_name):
    sem = Semaphore(unique_name).create(maximum_count=5, initial_count=5)
    try:
        for _ in range(5):
            sem.acquire(0)
        with pytest.raises(SemaphoreWaitTimeoutException):
            # Can't acquire 6 times
            sem.acquire(0)

        for expected_count in range(5):
            old_count = sem.release(release_count=1)
            assert old_count == expected_count
    finally:
        sem.close()


def test_create_error():
    with pytest.raises(OSError):
        # initial count can't be larger than maximum
        Semaphore().create(maximum_count=1, initial_count=2)


def test_open_without_create(unique_name):
    with pytest.raises(OSError) as _:
        # Doesn't exist, can't open
        Semaphore(unique_name).open()

    # Create it, then it will open
    sem1 = Semaphore(unique_name).create()
    sem2 = Semaphore(unique_name).open()
    assert sem1.getvalue() == 1
    assert sem2.getvalue() == 1
    sem2.close()
    sem1.close()

    with pytest.raises(OSError) as _:
        # No longer exists, can't open
        Semaphore(unique_name).open()


def test_too_many_acquires():
    sem = Semaphore().create()
    try:
        sem.acquire(0)
        with pytest.raises(SemaphoreWaitTimeoutException) as _:
            sem.acquire(0)
    finally:
        sem.close()


def test_too_many_releases():
    sem = Semaphore().create()
    try:
        with pytest.raises(OSError) as _:
            sem.release(release_count=1)
    finally:
        sem.close()


def test_acquire_release_cycle():
    sem = Semaphore().create()
    try:
        for _ in range(10):
            sem.acquire(0)
            old_count = sem.release(release_count=1)
            assert old_count == 0
    finally:
        sem.close()


def test_too_many_closes():
    sem = Semaphore().create()
    sem.close()
    with pytest.raises(OSError) as _:
        sem.close()


def test_low_starting_value():
    sem = Semaphore().create(5, 0)
    try:
        assert sem.getvalue() == 0
        # fail: count is zero
        with pytest.raises(SemaphoreWaitTimeoutException) as _:
            sem.acquire(0)
        # release up to the max of 5
        for expected_count in range(5):
            assert sem.getvalue() == expected_count
            old_count = sem.release(release_count=1)
            assert old_count == expected_count
        # additional release is an error
        with pytest.raises(OSError) as _:
            sem.release(release_count=1)
    finally:
        sem.close()


def test_default_initial_count(unique_name):
    sem = Semaphore(unique_name).create(5)
    try:
        other_sems = []
        other_handles = []
        for _ in range(5):
            other = Semaphore(unique_name)
            handle = other.open()
            handle.acquire(0)
            other_sems.append(other)
            other_handles.append(handle)
        fail_sem = Semaphore(unique_name)
        fail_handle = fail_sem.open()
        with pytest.raises(SemaphoreWaitTimeoutException) as _:
            fail_handle.acquire(0)
        fail_sem.close()
        for other in other_sems:
            other.close()
    finally:
        sem.close()


@pytest.mark.parametrize('timeout_ms', [0, 1, 500])
def test_timeout(timeout_ms: int):
    sem = Semaphore().create()
    try:
        sem.acquire(0)
        start_time = datetime.datetime.now()
        with pytest.raises(SemaphoreWaitTimeoutException) as _:
            sem.acquire(timeout_ms=timeout_ms)
        end_time = datetime.datetime.now()
        delta_ms = (end_time - start_time).total_seconds() * 1000
        assert timeout_ms <= delta_ms <= (timeout_ms+50)
    finally:
        sem.close()


def test_wait_failure():
    sem = Semaphore().create(desired_access=DWORD(0))
    with pytest.raises(OSError):
        sem.acquire()
