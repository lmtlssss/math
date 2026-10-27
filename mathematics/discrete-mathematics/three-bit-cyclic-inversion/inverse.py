#!/usr/bin/env python3
"""Complete inversion of a cyclic Boolean–modular word map.

Author: lmtlssss🜐
License: MIT
Bit zero is the least significant bit. The parameter r defaults to 3.
"""
from __future__ import annotations
import argparse
import json
from typing import Iterator


def _check(width: int, c: int, k: int, target: int, r: int) -> None:
    if not isinstance(width, int) or not isinstance(r, int) or not 2 <= r < width:
        raise ValueError("Require integers 2 <= r < width.")
    for name, value in (("c", c), ("k", k), ("target", target)):
        if not isinstance(value, int) or not 0 <= value < (1 << width):
            raise ValueError(f"{name} must be an unsigned width-bit integer.")


def bits_le(value: int, width: int) -> list[int]:
    """Convert once to bytes, then read individual bits in constant-sized units."""
    raw = value.to_bytes((width + 7) // 8, "little")
    return [(raw[i // 8] >> (i % 8)) & 1 for i in range(width)]


def from_bits_le(bits: list[int]) -> int:
    raw = bytearray((len(bits) + 7) // 8)
    for i, bit in enumerate(bits):
        raw[i // 8] |= bit << (i % 8)
    return int.from_bytes(raw, "little")


def rotate_right(x: int, distance: int, width: int) -> int:
    mask = (1 << width) - 1
    return ((x >> distance) | (x << (width - distance))) & mask


def forward(x: int, c: int, k: int, width: int, r: int = 3) -> int:
    _check(width, c, k, x, r)
    return ((rotate_right(x, 1, width) ^ rotate_right(x, r, width))
            + (x & c) + k) % (1 << width)


def branches(target: int, c: int, k: int, width: int, r: int = 3
             ) -> Iterator[dict]:
    """Yield all 2**r seed paths, retaining every closure and carry bit."""
    _check(width, c, k, target, r)
    target_bits = bits_le((target - k) % (1 << width), width)
    mask_bits = bits_le(c, width)
    for seed in range(1 << r):
        initial = [(seed >> j) & 1 for j in range(r)]
        bits = initial.copy()
        carry = 0
        carries = [carry]
        for i in range(width):
            b = bits[i] & mask_bits[i]
            q = target_bits[i] ^ b ^ carry
            bits.append(bits[i + 1] ^ q)
            carry = (q + b + carry) // 2
            carries.append(carry)
        closure = bits[width:width + r]
        accepted = closure == initial
        yield {"seed": seed, "initial_bits": initial, "bits": bits,
               "carry_bits": carries, "closure_bits": closure,
               "accepted": accepted,
               "candidate": from_bits_le(bits[:width]), "steps": width}


def preimages(target: int, c: int, k: int, width: int, r: int = 3) -> list[int]:
    """Return the entire fiber. Work: 2**r * width local bit transitions."""
    return sorted(p["candidate"] for p in branches(target, c, k, width, r)
                  if p["accepted"])


def _integer(text: str) -> int:
    return int(text, 0)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--mask", type=_integer, required=True, dest="c")
    parser.add_argument("--constant", type=_integer, default=0, dest="k")
    parser.add_argument("--target", type=_integer, required=True)
    parser.add_argument("--rotation", type=int, default=3, dest="r")
    args = parser.parse_args()
    try:
        answers = preimages(args.target, args.c, args.k, args.width, args.r)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps({"width": args.width, "mask": args.c,
                     "constant": args.k, "target": args.target,
                     "rotation": args.r, "preimages": answers,
                     "seeds": 1 << args.r,
                     "local_updates": (1 << args.r) * args.width}, indent=2))


if __name__ == "__main__":
    main()
