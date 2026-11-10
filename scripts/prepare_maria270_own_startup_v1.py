"""Freeze the own-candidate startup plan for the already-qualified minimal worker.

Keep preparation separate from native DLL loading. No terminal, startup approval
or getter receipt is emitted here; the complete independent verifier remains.
"""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
original=Path('scripts/run_maria301_registered_startup_v1.py').read_text(encoding='utf-8')
assert original.count('    harness.main()\n')==1
prefix=original.split('    harness.main()\n')[0]
source=checked_text(prefix,{
    'scripts.build_registered_maria301_v1':'scripts.build_registered_maria270_v1',
    'Own cumulative Maria301 candidate':'Own cumulative Maria270 candidate',
})+"    save(ROOT/'worker_argv.json',dict(argv=sys.argv[1:],candidate_sha256=digest(CANDIDATE),new_credit=0))\n    print('Prepared exact31,000-frame own-candidate Maria startup plan forminimal coldboot worker.')\n\nif __name__=='__main__':main()\n"
exec(compile(source,__file__+'::same-complete-frozen-startup-plan-independent-minimal-worker','exec'),globals())
