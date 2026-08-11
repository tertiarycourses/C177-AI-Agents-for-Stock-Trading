#!/usr/bin/env bash
# Single-command aligned build of the NON-WSQ courseware from the single source
# (course_data.py + data_domainN.py). Produces in the course's courseware/: the
# PPT, LP and LG as DOCX + PDF, with page-numbered Tables of Contents in LP/LG.
#
# Generic: the course repo and the LP/LG filenames are derived from
# course_data.py, so this orchestrator is course-agnostic. Override the target
# repo with the COURSE_REPO environment variable.
#
# Pipeline: run the python-pptx / python-docx generators, render to PDF with
# LibreOffice, inject a static page-numbered TOC (LibreOffice can't update the
# TOC field headless), then re-render the LP/LG PDFs.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SOFFICE="${SOFFICE:-soffice}"

# Isolate this build from any other concurrent LibreOffice conversion. Without
# a dedicated user profile, Windows forwards a headless request to whichever
# soffice instance is already running, which can leave the expected PDF absent.
LO_PROFILE_DIR="$(mktemp -d)"
if command -v cygpath >/dev/null 2>&1; then
  LO_PROFILE_PATH="$(cygpath -m "$LO_PROFILE_DIR")"
else
  LO_PROFILE_PATH="$LO_PROFILE_DIR"
fi
LO_PROFILE_URL="file:///$LO_PROFILE_PATH"
trap 'rm -rf -- "$LO_PROFILE_DIR"' EXIT

# Git Bash on Windows may have LibreOffice installed without `soffice` on PATH.
if ! command -v "$SOFFICE" >/dev/null 2>&1 && [[ ! -x "$SOFFICE" ]]; then
  for candidate in \
    "/c/Program Files/LibreOffice/program/soffice.exe" \
    "/c/Program Files (x86)/LibreOffice/program/soffice.exe"
  do
    if [[ -x "$candidate" ]]; then
      SOFFICE="$candidate"
      break
    fi
  done
fi
if ! command -v "$SOFFICE" >/dev/null 2>&1 && [[ ! -x "$SOFFICE" ]]; then
  echo "LibreOffice soffice was not found. Install it or set SOFFICE to its executable." >&2
  exit 2
fi

# Resolve the course repo + short title from the single source (course_data.py).
IFS=$'\t' read -r REPO SHORT <<< "$(python3 - "$HERE" <<'PY'
import os, sys
here = sys.argv[1]; sys.path.insert(0, here)
import course_data as C
def find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d,"courseware")) and os.path.isdir(os.path.join(d,"labs")): return d
    return os.path.dirname(os.path.dirname(start))
print(find_repo(here) + "\t" + C.SHORT_TITLE)
PY
)"
CW="$REPO/courseware"

echo "==> Generate PPT / LP / LG from the single source"
python3 "$HERE/build_slides.py"
python3 "$HERE/build_lesson_plan.py"
python3 "$HERE/build_learner_guide.py"
python3 "$HERE/build_labs.py"

PPT="$(ls -t "$CW"/*.pptx | head -1)"
LP="$CW/LP-$SHORT.docx"
LG="$CW/LG-$SHORT.docx"

echo "==> Render PDFs (pass 1)"
"$SOFFICE" "-env:UserInstallation=$LO_PROFILE_URL" --headless --convert-to pdf --outdir "$CW" "$PPT" >/dev/null 2>&1
"$SOFFICE" "-env:UserInstallation=$LO_PROFILE_URL" --headless --convert-to pdf --outdir "$CW" "$LP"  >/dev/null 2>&1
"$SOFFICE" "-env:UserInstallation=$LO_PROFILE_URL" --headless --convert-to pdf --outdir "$CW" "$LG"  >/dev/null 2>&1

echo "==> Inject page-numbered Table of Contents (LP + LG)"
python3 "$HERE/inject_toc.py" "$LP" "${LP%.docx}.pdf" 2
python3 "$HERE/inject_toc.py" "$LG" "${LG%.docx}.pdf" 2

echo "==> Render PDFs (pass 2 — with built TOC)"
"$SOFFICE" "-env:UserInstallation=$LO_PROFILE_URL" --headless --convert-to pdf --outdir "$CW" "$LP" >/dev/null 2>&1
"$SOFFICE" "-env:UserInstallation=$LO_PROFILE_URL" --headless --convert-to pdf --outdir "$CW" "$LG" >/dev/null 2>&1

echo "==> Done. Artifacts in courseware/:"
ls -1 "$CW"/*.pptx "$CW"/*.docx "$CW"/*.pdf
