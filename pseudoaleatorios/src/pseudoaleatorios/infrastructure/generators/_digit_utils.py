from __future__ import annotations


def middle_extract(n: int, pad_to: int = 8, take: int = 4) -> int:
    """
    Zero-pad `n` to `pad_to` digits and return the central `take` digits as an int.
    This is the core operation shared by the middle-squares and related methods.
    """
    s = str(n).zfill(pad_to)
    # If n² overflowed the expected width, truncate to the rightmost pad_to digits
    if len(s) > pad_to:
        s = s[-pad_to:]
    start = (len(s) - take) // 2
    return int(s[start : start + take])


def detect_period(seq: tuple[int, ...]) -> int | None:
    """
    Return the first repeated-value period length, or None if the sequence
    ends before any value repeats.
    """
    seen: dict[int, int] = {}
    for i, v in enumerate(seq):
        if v in seen:
            return i - seen[v]
        seen[v] = i
    return None


def sieve_of_eratosthenes(lo: int, hi: int) -> list[int]:
    """Return all primes in [lo, hi] via the Sieve of Eratosthenes."""
    if hi < 2:
        return []
    sieve = bytearray([1]) * (hi + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(hi**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i in range(max(lo, 2), hi + 1) if sieve[i]]
