"""Keep both complete verb-object phrases together after the first wrap refinement."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_phrase_wrap_v4619')
assert not ROOT.exists()
tools=[derive('dk4tool/dialogue/lil_B177_layout_v2.py','dk4tool/dialogue/lil_B177_layout_v3.py',{
    'def _word(value):':
        "# Preserve the complete takes-me-back expression and consumed-me object phrase.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('takes','me'),('consumed','me')})\n\ndef _word(value):",
})]
tools.append(derive('scripts/plan_lil_B177_layout_v4617.py','scripts/plan_lil_B177_layout_v4620.py',{
    'lil_B177_layout_v2':'lil_B177_layout_v3','lil_B177_layout_v4617':'lil_B177_layout_v4620',
    "OUTPUT=Path('translations/lil_B177_editorial_manuscript_v3.json')":
        "OUTPUT=Path('translations/lil_B177_editorial_manuscript_v4.json')",
}))
tools.append(derive('scripts/verify_lil_B177_fonts_v4618.py','scripts/verify_lil_B177_fonts_v4621.py',{
    'lil_B177_layout_v2':'lil_B177_layout_v3','lil_B177_fonts_v4618':'lil_B177_fonts_v4621',
    'lil_B177_editorial_manuscript_v3':'lil_B177_editorial_manuscript_v4',
}))
from dk4tool.dialogue.lil_B177_layout_v3 import _split_pair
for labels,index in [(['takes','me','back'],0),(['takes','me','back'],1),(['consumed','me'],0),(['start','selling'],0)]:
    assert _split_pair(labels,index)
for labels in [['takes','another'],['consumed','by'],['start','right'],['me','when']]:
    assert not _split_pair(labels,0)
proof=Path('work/analysis/lil_B177_fonts_v4618/all10_progressive_FE_native_planes_and80_alignment_cases.json')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,prior_native_proof=str(proof),prior_native_proof_sha256=sha(proof.read_bytes()),
    individually_viewed_prior_sheet=read(proof)['review_sheets'][0],
    remaining_R12_findings=['takes / me back still divides the full expression','consumed / me divides its direct object'],
    four_relevant_positive_and_four_unrelated_negative_boundary_cases_pass=True,
    English_source_facts_native_geometry_guards_and_source_commands_unchanged=True,
    no_waiver_or_ROM_registry_ledger_credit=True,full_goal_complete=False))
