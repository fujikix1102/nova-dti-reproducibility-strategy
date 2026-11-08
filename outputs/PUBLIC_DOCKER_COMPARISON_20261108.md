# Public Docker comparison

The fixed Docker path was run twice with seed `20261108`.

| Contract | Result |
|---|---:|
| matched daily records | 81 |
| event–station groups | 27 |
| events | 3 |
| stations | 9 |
| bootstrap replicates | 2,000 |
| `formal_pass` | `false` |

The seeded bootstrap output was byte-for-byte identical across the two runs. SHA-256: `d554b1856868d38ad12577b679ad34709c46b12facc99dfb3d57ed768822e201`.

The input CSVs are not included in this public repository. Use [FETCH_AND_VERIFY_INPUTS.md](../FETCH_AND_VERIFY_INPUTS.md) and the input hashes in [PUBLIC_DOCKER_REPRODUCTION_MANIFEST_20261108.json](PUBLIC_DOCKER_REPRODUCTION_MANIFEST_20261108.json).
