# Independent reproduction quickstart

This is a short English guide for an unrelated external executor.

1. Download the tagged release and read its `README.md`.
2. Obtain the two input files through the documented, licensed route. Do not use restricted or unpublished data.
3. Stage the three scripts and the two inputs in the directory layout shown in the README.
4. Build the Docker image.
5. Run the representative case once, then run `verify_manifest.py`.
6. Report the result through a GitHub Issue using the success or mismatch template.

Expected contract: 81 matched daily records, 27 event–station groups, 3 events, 9 stations, 2,000 bootstrap replicates, seed `20261108`, and `formal_pass=false`.

Please include the Docker image ID, OS, architecture, Docker version, runtime, command, exit code, verifier JSON, and SHA-256 values. A mismatch is useful evidence; do not silently repair inputs or overwrite the frozen release.
