"""Run the portable project's publication and interaction-data checks."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
checks = [
    'verify_refinement.py',
    'verify_faculty_life.py',
    'verify_global_learning.py',
    'verify_internships.py',
    'verify_compact_editorial.py',
    'verify_information_design.py',
]
for check in checks:
    print(f'Checking {check}', flush=True)
    result = subprocess.run([sys.executable, '-X', 'utf8', check], cwd=root)
    if result.returncode:
        raise SystemExit(result.returncode)
print(f'All {len(checks)} checks passed.')
