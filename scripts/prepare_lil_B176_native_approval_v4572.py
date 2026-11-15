"""Derive a ten-speech approval with B176's distinct actors and source controls."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_approval_preparation_v4572')
assert not ROOT.exists()
source=Path('scripts/approve_lil_B175_native_v4518.py')
target=Path('scripts/approve_lil_B176_native_v4572.py')
text=source.read_text(encoding='utf-8')
macro_start=text.index('    for r in doc[\'records\']:\n        for macro in re.findall')
macro_end=text.index("    names=read(doc['source_nameplate_consumer_proof'])",macro_start)
old_macros=text[macro_start:macro_end]
new_macros="""    for macro in ['FI','FA','FO']:
        r=doc['records'][0]
        reject(macro_negatives,'invented-'+macro,lambda r=r,m=macro:validate_source_macros(bytes.fromhex(r['source_hex']),r['english']+' {MACRO:'+m+'}'))
    assert len(macro_negatives)==3
    assert codec._complete_clause_at('Yes! With a flavor like this,'.split(),5)
    assert not codec._complete_clause_at(['this,'],0)
    assert not codec._complete_clause_at('Buy this,'.split(),1)
    assert not codec._complete_clause_at('With a flavor like this'.split(),4)
"""
replacements={
    'B175':'B176','lil_B175':'lil_B176',
    'lil_B175_layout_v1':'lil_B176_layout_v4',
    'native_approval_v4518':'native_approval_v4572',
    'fonts_v4517':'fonts_v4570',
    'all32_progressive_FE_native_planes_and256_alignment_cases':'all10_progressive_FE_native_planes_and80_alignment_cases',
    "assert len(font['cases'])==32 and font['current_original_macro_alignment_calls']==256":"assert len(font['cases'])==10 and font['current_original_macro_alignment_calls']==80",
    "==(23,9)":"==(9,1)",
    "len(font['negative_controls'])==24":"len(font['negative_controls'])==18",
    '.blocks[175]':'.blocks[176]',
    'Viewed all32 complete progressive/FE panels across four sheets. Recognition builds into encirclement, defiance, pirate-pride rebuke, sea challenge, sword mystery and departure; relief then turns into teasing and concern. All13 retained wordings remain coherent. No clipped leading/internal/final glyph, missing punctuation, overflow, blank page or stranded auxiliary was found. Woman and sword remain unnamed, admiral stays source-bound, and no boss/rank/relationship is added. Offline native rendering; no actual B175 gameplay claim.':
    'Viewed all10 complete panels across two sheets individually. Owner enthusiasm develops through Cook doubt, imperious insistence, practical compliance, maximal purchase order, casual repeated acknowledgment and an extravagant laugh. The final FE notice remains impersonal and prospective. All five retentions remain coherent. Complete leading/internal/final glyphs and punctuation, bounds and single-page consumption pass. The comma-delimited flavor phrase is complete; no broad weak-ending exemption. No invented rank,relationship,quantity,profit or active boom. Offline native rendering; no actual B176 gameplay claim.',
    'assert len(sheets)==4':'assert len(sheets)==2',
    'block=175':'block=176',
    "assert macros=={b'FI':4,b'FA':1}":'assert not macros',
    "=={'revise':19,'retain-wording':13}":"=={'revise':5,'retain-wording':5}",
    "assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==13":"assert sum(bool(r.get('qa_waivers')) for r in doc['records'])==3",
    "[('progressive',2),('FE-paper',254)]":"[('progressive',174),('FE-paper',254)]",
    old_macros:new_macros,
    "['native_ten_consumer_cases']['rows']":"['native_four_consumer_cases']['rows']",
    'assert len(names)==10':'assert len(names)==4',
    "    assert sum(bool(r['original_scratch_rings']) and bool(r['original_getter_writes']) and r['actor_ID'] in [2,9] for r in names)==4\n    assert sum(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['actor_ID'] in [183,184,185] for r in names)==6":
    "    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] and r['actor_ID'] in [174,175] for r in names)\n    assert {r['actor_ID']:r['text'] for r in names}=={174:'Owner',175:'Cook'}",
    'all32_native_progressive_FE_and_source_reconciliation':'all10_native_progressive_FE_and_source_reconciliation',
    'current_original_macro_alignment_calls=256':'current_original_macro_alignment_calls=80',
    'progressive_planes=23,FE_planes=9':'progressive_planes=9,FE_planes=1',
    'all32_current_native_speech_planes_pass':'all10_current_native_speech_planes_pass',
    'all32_source_facts_complete_exchange_and_individual_decisions_reconciled':'all10_source_facts_complete_exchange_and_individual_decisions_reconciled',
    'source_FI4_FA1_order_five_static_selectors_and_null_actor_FE_preserved':'source_FI0_FA0_FO0_two_static_selectors_and_impersonal_null_actor_FE_preserved',
    'source_three_presentations_one_resource_C200_two_ends_preserved_without_guessed_operands':'source_one_A000_C200_single_end_preserved_without_guessed_operands',
    'all32_five_review_gates_true':'all10_five_review_gates_true',
    'revised=19,retained=13':'revised=5,retained=5',
    'current_macro_alignment_cases=256,source_consumer_negatives=24,source_macro_negatives=9':'current_macro_alignment_cases=80,source_consumer_negatives=18,source_macro_negatives=3',
    'narrow_row_count_notes=13':'narrow_row_count_notes=3',
    "print('B175:32 five-gate reviews,19 revisions/13 retentions;23 progressive+9 FE planes,256 alignments and61 negative controls. Actual scene/release pending;no credit yet.')":
    "print('B176:10 five-gate reviews,5 revisions/5 retentions;9 progressive+1 FE planes,80 alignments and49 negatives. Actual scene/release pending;no credit yet.')",
}
derive(source,target,replacements)
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',{'source':str(source),'source_sha256':sha(source.read_bytes()),
    'target':str(target),'target_sha256':sha(target.read_bytes()),'B176_two_sheets_individually_viewed':True,
    'four_readonly_names_zero_scratch_paths':True,'no_source_macro_deletion_or_reordering_cases_exist':True,
    'complete_clause_positive_and_three_negatives_in_approval':True,'no_gameplay_or_ledger_credit':True})
