#!/usr/bin/env python

"""Tests for `semaphore_win_ctypes` package."""

import pytest

from semaphore_win_ctypes.semaphore_win_ctypes import *


def test_basic():
    sem = Semaphore()
    sem.create(attr=None, initial_count=1, maximum_count=1, name="Testing")
    sem.acquire(0)
    old_count = sem.release(release_count=1)
    assert old_count == 0
    sem.close()


def test_too_many_acquires():
    sem = Semaphore()
    sem.create(attr=None, initial_count=1, maximum_count=1, name="Testing")
    sem.acquire(0)
    with pytest.raises(SemaphoreWaitTimeoutException) as _:
        sem.acquire(0)
    sem.close()


def test_too_many_releases():
    sem = Semaphore()
    sem.create(attr=None, initial_count=1, maximum_count=1, name="Testing")
    with pytest.raises(OSError) as _:
        sem.release(release_count=1)
    sem.close()


def test_acquire_release_cycle():
    sem = Semaphore()
    sem.create(attr=None, initial_count=1, maximum_count=1, name="Testing")
    for _ in range(10):
        sem.acquire(0)
        old_count = sem.release(release_count=1)
        assert old_count == 0
    sem.close()


def test_too_many_closes():
    sem = Semaphore()
    sem.create(attr=None, initial_count=1, maximum_count=1, name="Testing")
    sem.close()
    with pytest.raises(OSError) as _:
        sem.close()


def test_low_starting_value():
    sem = Semaphore()
    sem.create(attr=None, initial_count=0, maximum_count=5, name="Testing")
    # fail: count is zero
    with pytest.raises(SemaphoreWaitTimeoutException) as _:
        sem.acquire(0)
    # release up to the max of 5
    for expected_count in range(5):
        old_count = sem.release(release_count=1)
        assert old_count == expected_count
    # additional release is an error
    with pytest.raises(OSError) as _:
        sem.release(release_count=1)
    sem.close()

