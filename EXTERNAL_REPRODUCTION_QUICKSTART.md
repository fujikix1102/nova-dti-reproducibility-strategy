# Independent reproduction quickstart

This is a short English guide for an unrelated external executor.

1. Download the tagged release and read its `README.md`.
2. Obtain the two input files through the documented, licensed route. Do not use restricted or unpublished data.
3. Stage the three scripts and the two inputs in the directory layout shown in the README.
4. Build the Docker image.
5. Run the representative case once, then run `verify_manifest.py`.
6. Report the result through a GitHub Issue using the success or mismatch template.

Expected contract: 81 matched daily records, 27 event–station groups, 3 events, 9 stations, 2,000 bootstrap replicates, seed `20261108`, and `formal_pass=false`.

Expected input SHA-256:

```text
jma: e3cdb24f08f8bd65f5ffafac40d771592869fd1843999f0cbd6510739c7eb7f9
gpm: 6d7b1e467c293da2966c200a60d6f9e3639e1ccf7702fd0076c84e1e305a7a86
```

Expected bootstrap output SHA-256: `d554b1856868d38ad12577b679ad34709c46b12facc99dfb3d57ed768822e201`. The deterministic tolerance is 0 bytes; numeric tolerance is not defined. A current-image mismatch must be reported rather than silently accepted.

Please include the Docker image ID, OS, architecture, Docker version, runtime, command, exit code, verifier JSON, and SHA-256 values. A mismatch is useful evidence; do not silently repair inputs or overwrite the frozen release.

Maintainer-side and clean-room runs are not third-party evidence. Until an unrelated executor submits a report, the package remains `UNVERIFIED`.
