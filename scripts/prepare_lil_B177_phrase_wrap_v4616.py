"""Tighten two observed phrase boundaries while preserving complete B177 prose."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_phrase_wrap_v4616')
assert not ROOT.exists()
tools=[derive('dk4tool/dialogue/lil_B177_layout_v1.py','dk4tool/dialogue/lil_B177_layout_v2.py',{
    'def _word(value):':
        "# B177 visual review:keep the phrasal verb and the explicit start-selling instruction together.\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('me','back'),('start','selling')})\n\ndef _word(value):",
})]
tools.append(derive('scripts/plan_lil_B177_layout_v4614.py','scripts/plan_lil_B177_layout_v4617.py',{
    'lil_B177_layout_v1':'lil_B177_layout_v2','lil_B177_layout_v4614':'lil_B177_layout_v4617',
    "OUTPUT=Path('translations/lil_B177_editorial_manuscript_v2.json')":
        "OUTPUT=Path('translations/lil_B177_editorial_manuscript_v3.json')",
}))
tools.append(derive('scripts/verify_lil_B177_fonts_v4615.py','scripts/verify_lil_B177_fonts_v4618.py',{
    'lil_B177_layout_v1':'lil_B177_layout_v2','lil_B177_fonts_v4615':'lil_B177_fonts_v4618',
    'lil_B177_editorial_manuscript_v2':'lil_B177_editorial_manuscript_v3',
}))
from dk4tool.dialogue.lil_B177_layout_v2 import _split_pair
assert _split_pair(['takes','me','back'],1)
assert _split_pair(['start','selling'],0)
assert not _split_pair(['me','when'],0)
assert not _split_pair(['start','right'],0)
assert not _split_pair(['start'],0)
proof=Path('work/analysis/lil_B177_fonts_v4615/all10_progressive_FE_native_planes_and80_alignment_cases.json')
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tools=tools,initial_native_proof=str(proof),initial_native_proof_sha256=sha(proof.read_bytes()),
    individually_viewed_initial_sheets=read(proof)['review_sheets'],
    findings=[dict(id='DK4_MES_B177_R0012',finding='takes me / back divides the phrasal-verb expression'),
              dict(id='DK4_MES_B177_R0020',finding='start / selling divides the explicit instruction')],
    only_two_source_bound_protected_pairs_added=True,two_positive_and_three_negative_pair_checks_pass=True,
    reviewed_English_shared_metrics_guards_and_all_source_controls_unchanged=True,
    no_phrase_waiver_or_ROM_registry_ledger_credit=True,full_goal_complete=False))
