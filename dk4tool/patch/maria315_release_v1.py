"""Pure315-source SC3 successor with exact read-only research rehearsal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

original = Path('dk4tool/patch/maria363_release_v1.py').read_text(encoding='utf-8')
derived = checked_text(original, {
    'from scripts import finalize_maria363_research_v1 as finisher': 'from scripts import finalize_maria315_research_v1 as finisher',
    'list(range(216,253))': 'list(range(286,303))',
    'scripts/finalize_maria363_research_v1.py': 'scripts/finalize_maria315_research_v1.py',
    'maria363_complete_research_rehearsal': 'maria315_complete_research_rehearsal',
    'Sealed363 five-gate reviews and29 scoped names:202 revisions/161 retentions. Registration/once-only credit remain.':
        'Sealed315 five-gate reviews and14 scoped names:162 revisions/153 retentions. Registration/once-only credit remain.',
    '(363,351,266,85,12,5,29,353,940,38,97683)': '(315,309,196,113,6,3,14,309,320,13,91844)',
    '37 complete reviewed exchanges': '17 complete reviewed exchanges',
    'exact29 scoped name reviews': 'exact14 scoped name reviews',
    "for r in stored['records'])==38, '38 complete original FE panels'":
        "for r in stored['records'])==13, '13 complete original FE panels'",
    'work/Maria_B216_B252_clean_20261110': 'work/Maria_B286_B302_clean_20261110',
    'for index in range(3):': 'for index in range(4):',
    'dk4-reviewed-maria363-release-v1': 'dk4-reviewed-maria315-release-v1',
    "\"len(styles['objects']) == 12\"": "\"len(styles['objects']) == 17\"",
})
exec(compile(derived, __file__+'::same-pure-source-current-compound-transaction-rehearsal-andwhole-inverses', 'exec'), globals())
