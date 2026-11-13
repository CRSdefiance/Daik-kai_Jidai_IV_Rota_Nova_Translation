"""Pure349-source SC3 successor with complete read-only research rehearsal."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

_original=Path('dk4tool/patch/maria363_release_v1.py').read_text(encoding='utf-8')
_derived=checked_text(_original,{
    'from scripts import finalize_maria363_research_v1 as finisher':'from scripts import finalize_maria349_research_v1 as finisher',
    'list(range(216,253))':'list(range(275,286))',
    'scripts/finalize_maria363_research_v1.py':'scripts/finalize_maria349_research_v1.py',
    'maria363_complete_research_rehearsal':'maria349_complete_research_rehearsal',
    'Sealed363 five-gate reviews and29 scoped names:202 revisions/161 retentions. Registration/once-only credit remain.':
        'Sealed349 five-gate reviews and19 scoped names:184 revisions/165 retentions. Registration/once-only credit remain.',
    '(363,351,266,85,12,5,29,353,940,38,97683)':'(349,341,179,162,8,3,19,347,330,7,77043)',
    '37 complete reviewed exchanges':'11 complete reviewed exchanges',
    'exact29 scoped name reviews':'exact19 scoped name reviews',
    "for r in stored['records'])==38, '38 complete original FE panels'":"for r in stored['records'])==7, '7 complete original FE panels'",
    'work/Maria_B216_B252_clean_20261110':'work/Maria_B275_B285_clean_20261110',
    'dk4-reviewed-maria363-release-v1':'dk4-reviewed-maria349-release-v1',
    '"len(styles[\'objects\']) == 12"':'"len(styles[\'objects\']) == 27"',
})
exec(compile(_derived,__file__+'::same-pure-source-current-compound-transaction-rehearsal-andwhole-inverses','exec'),globals())
