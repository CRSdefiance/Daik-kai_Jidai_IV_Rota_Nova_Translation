"""Source-lock sparse reconstruction to seven blocks,82 selectors/macros and source tails."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_relocation_preparation_v8809');assert not root.exists()
    result=derive('scripts/relocate_Hodram_B31_B53_v8728.py','scripts/relocate_Hodram_B54_B60_v8809.py',{
        'scripts.Hodram_B52_registered_route_context_v8707':'scripts.Hodram_B31_B53_registered_route_context_v8781',
        'work/analysis/Hodram_B31_B53_relocation_v8728':'work/analysis/Hodram_B54_B60_relocation_v8809',
        'work/analysis/Hodram_B31_B53_current_v8722/current_effective.json':'work/analysis/Hodram_B54_B60_current_v8799/current_effective.json',
        'translations/hodram_B31_B53_editorial_manuscript_v2.json':'translations/hodram_B54_B60_editorial_manuscript_v2.json',
        'work/analysis/Hodram_B31_B53_native_review_v8727/native_body_review.json':'work/analysis/Hodram_B54_B60_compiled_v8808/compiled_body_bindings.json',
        'work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json':'work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json',
        'work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json':'work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json',
        "view['all_three_complete_bodies_visually_read']":"view['compiled_bytes_and82_preambles_bound_to_viewed85_pages']",
        "len(doc['records'])==3":"len(doc['records'])==82",
        'assert oldend==cleanend==len(old)==len(clean) and old[:8]==clean[:8]':"assert oldend==cleanend and len(old)==len(clean) and old[:8]==clean[:8] and old[oldend:]==clean[cleanend:] and not any(old[oldend:])",
        "len(before)==9":"len(before)==len(g['all_current_commands'])",
        'in [34,113]':'in [1,20,23,24,36,84,113,114,119,141,254]',
        "source[1:].count(m)==value[1:].count(m)==0":"source[1:].count(m)==value[1:].count(m)",
        'len(fixups)==(4 if number==31 else 0)':"len(fixups)==len(source_control['operands_requiring_adjustment_when_resizing'])",
        'len(after)==9':'len(after)==len(before)',
        "assert bytes(inverse)==original,'Complete clean/current block inverse'":"assert bytes(inverse)+original[oldend:]==original,'Complete clean/current block inverse including separate source tail'",
        'source_tail_bytes=0':'source_tail_bytes=len(old)-oldend',
        'if a!=b]==[31,53]':"if a!=b]==[g['block'] for g in packet['groups']]",
        'for i in [31,53]:':"for i in [g['block'] for g in packet['groups']]:",
        'SC1_B31_B53_RESEARCH_ONLY.DK4':'SC1_B54_B60_RESEARCH_ONLY.DK4',
        'other323_blocks_byte_exact=True':'other318_blocks_byte_exact=True',
        'source_relative_sites=4':'source_relative_sites=24',
        'complete18commands3sixbytepreambles4relatives1query8opaquecontrols2normalends_preserved=True':'complete152commands82sixbytepreambles24relatives6queries33nonprose_controls7normalends_preserved=True',
        "'Two research blocks reconstructed:'":"'Seven research blocks reconstructed:'",
        '18commands/3preambles/4relatives20cases/query/8opaquecontrols/fullends preserved;323otherblocks/currentarchive/cleanblocks/wholeNDS inverses pass. No ROM orcredit.':'152commands/82preambles/24relatives120cases/6queries/33nonprosecontrols/7fullends preserved;318otherblocks/currentarchive/cleanblocks/wholeNDS inverses pass. No ROM orcredit.',
    })
    root.mkdir(parents=True);save(root/'source_locked_relocation_derivation.json',dict(derivation=result,
        actual_scope='SC1 blocks54-60,82 utterances,152commands,24relative sites,source macrosFI3/FA4/FO0,one FE selector,separate2byte source tails in57/59',
        source_current_offsets_andallocations_equal_before_rebuild=True,all_native_addresses_andunowned_reconstruction_guards_preserved=True,
        research_archives_only_no_ROM_registration_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
