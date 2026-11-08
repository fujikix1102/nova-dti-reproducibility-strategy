FROM python:3.12.8-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/repro
COPY requirements-lock.txt ./
COPY work/run_representative_case.py work/verify_representative_case.py ./work/

# The archived JMA–GPM scripts and source data are intentionally not copied
# into this image. Mount them at runtime so the image cannot rewrite the archive.
ENTRYPOINT ["python", "work/run_representative_case.py"]
