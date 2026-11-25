"""Allow an individually authored comparison-stage refinement; preserve sealed source-first drafts."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/join_source_first_editorial_comparison.py').read_text(encoding='utf-8'), {
    "            if len(decision) == 4:\n                assert decision[3] == 'place-name-localization-open'":
    """            if len(decision) == 4 and isinstance(decision[3],dict):
                assert row['decision'] == 'revision' and set(decision[3]) == {'english'}
                value = decision[3]['english']
                assert value.strip() == value and value != prior
                assert value.encode('cp932').decode('cp932') == value
                assert not any(v in value for v in ['\\n','\\t','  ','{LB','{ALIGN','{PAD}','%'])
                expected = row.get('source_macros',dict(FI=0,FA=0,FO=0))
                assert {m:len(re.findall(r'\\{MACRO:'+m+r'\\}',value)) for m in ['FI','FA','FO']} == expected
                row['english'] = row['logical_English'] = value
                row['comparison_stage_English_refinement'] = decision[3]
                row['original_clean_first_draft_preserved'] = True
            if len(decision) == 4 and isinstance(decision[3],str):
                assert decision[3] == 'place-name-localization-open'""",
})
exec(compile(source,__file__+'::individual-refinement-preserving-sealed-drafts','exec'),globals())
