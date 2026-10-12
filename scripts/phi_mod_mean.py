#!/usr/bin/env python3
"""
scripts/phi_mod_mean.py — φ modulo mean, asserted.

Recomputes φ from the quadratic x² - x - 1 = 0 rather than importing
a constant. Three independent computation paths (quadratic formula,
Newton iteration, continued fraction truncation) must agree.

Exit 0 iff all assertions hold. Exit 1 otherwise.
"""

from __future__ import annotations

import math
import sys

TOL = 1e-12


def phi_from_quadratic() -> float:
    """Positive root of x² - x - 1 = 0."""
    return (1.0 + math.sqrt(5.0)) / 2.0


def phi_from_newton(seed: float = 1.0, steps: int = 60) -> float:
    """Newton iteration on f(x) = x² - x - 1."""
    x = seed
    for _ in range(steps):
        fx = x * x - x - 1.0
        fpx = 2.0 * x - 1.0
        x = x - fx / fpx
    return x


def phi_from_cf(depth: int = 80) -> float:
    """Continued fraction [1; 1, 1, ...] truncated at `depth` levels."""
    x = 1.0
    for _ in range(depth):
        x = 1.0 + 1.0 / x
    return x


def geometric_mean(a: float, b: float) -> float:
    return math.sqrt(a * b)


def arithmetic_mean(a: float, b: float) -> float:
    return (a + b) / 2.0


def frac(x: float) -> float:
    """x mod 1 for positive x."""
    return x - math.floor(x)


def workload_dispatch(N: int = 64, M: int = 1000) -> dict:
    """Compute φ identity and Fibonacci residues mod M."""
    assert abs(phi_from_quadratic() ** 2 - (phi_from_quadratic() + 1.0)) < TOL, \
        "golden identity failed"

    fib = [0, 1]
    for _ in range(N):
        fib.append(fib[-1] + fib[-2])

    residues = [f % M for f in fib[2:N + 2]]
    mean_residue = sum(residues) / len(residues)
    return {"N": N, "M": M, "mean": mean_residue}


def main() -> int:
    p_q = phi_from_quadratic()
    p_n = phi_from_newton()
    p_c = phi_from_cf()

    checks = [
        ("A1  phi^2 = phi + 1",                 p_q * p_q,             p_q + 1.0),
        ("A2  1/phi = phi - 1",                 1.0 / p_q,             p_q - 1.0),
        ("A3  phi mod 1 = 1/phi",               frac(p_q),             1.0 / p_q),
        ("A4  geo_mean(phi, 1/phi) = 1",        geometric_mean(p_q, 1.0 / p_q), 1.0),
        ("A5  arith_mean(phi, 1/phi) = sqrt5/2", arithmetic_mean(p_q, 1.0 / p_q), math.sqrt(5.0) / 2.0),
        ("A6  newton == quadratic",             p_n,                   p_q),
        ("A7  cf[80] == quadratic",             p_c,                   p_q),
    ]

    print(f"phi (quadratic) = {p_q!r}")
    print(f"phi (newton)    = {p_n!r}")
    print(f"phi (cf[80])    = {p_c!r}")
    print()

    all_ok = True
    for name, lhs, rhs in checks:
        err = abs(lhs - rhs)
        ok = err < TOL
        all_ok = all_ok and ok
        mark = "OK  " if ok else "FAIL"
        print(f"  [{mark}] {name:<40} lhs={lhs!r} rhs={rhs!r} err={err:.3e}")

    if all_ok:
        print("\nall phi-mod-mean assertions hold")
        return 0
    print("\nASSERTION FAILURE", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
