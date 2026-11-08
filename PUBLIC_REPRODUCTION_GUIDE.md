# Public reproduction guide

This package is intended for unrelated researchers and developers who want to run the representative JMA–GPM v2 case without private coordination.

## Public entry point

Publish this directory as the root of a GitHub repository. A release must contain:

1. the Dockerfile and the one-page README;
2. the frozen manifest and its SHA-256;
3. the seeded verification program;
4. input-data access instructions and license records;
5. expected output, tolerance, runtime, and known limitations;
6. the issue templates in `.github/ISSUE_TEMPLATE/`.

Do not claim a public URL, release, Zenodo record, or external evaluation until it has actually been created and checked.

## Reproduction path

```bash
docker build --tag nova-dti-jma-gpm:2026-11-08 .
python3 work/verify_manifest.py \
  outputs/docker-seeded-reproduction-manifest-20261108.json \
  --code-dir <staged-root>/code \
  --base-dir <staged-root>/nova/external_data/real_events \
  --output-dir <staged-root>/nova/external_data/real_events/independent_events_comparison_expanded \
  --log <staged-root>/docker-run-log.json
```

The fixed contract is 81 matched daily records, 27 event–station groups, 3 events, 9 stations, 2,000 bootstrap replicates, seed `20261108`, and `formal_pass=false`.

## How to report a result

Open a GitHub Issue using one of the reproduction templates. Attach the verifier JSON, Docker image identifier, operating system, Python/Docker versions, input and output SHA-256 values, runtime, and any error log. Do not attach restricted data or credentials.

## Interpretation boundary

The case is a corrected exploratory comparison. A successful run confirms computational and structural agreement with the frozen contract; it does not establish calibration, causal validity, observational discovery, or formal scientific validation.

## Public release sequence

1. Confirm data provenance and redistribution permission.
2. Publish a tagged GitHub release with the frozen manifest.
3. Enable Issues and add the reproduction labels.
4. Optionally archive the exact release in Zenodo after the GitHub release exists.
5. Share the public link in relevant communities without targeting a private contact list.
