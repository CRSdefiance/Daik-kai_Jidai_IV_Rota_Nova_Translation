"""Rebuild24 complete exchanges with both qualified menu arities and full inverses."""
from pathlib import Path
from copy import deepcopy
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')

source=checked_text(Path('scripts/rebuild_maria337_reviewed_v1.py').read_text(encoding='utf-8'),{
    'from scripts.meaning_maria337_clean_v1 import ROOT':'from scripts.rebuild_maria390_reviewed_v1 import ROOT',
    'from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices':'from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices',
    "ROOT/'plan_visual_v5/automatic_plans.json'":"ROOT/'plan_continuity_v3/automatic_plans.json'",
    "ROOT/'menu_native_approved_v1.json'":"ROOT/'menu_native_approved_v2.json'",
    '==(337,335,335,339)':'==(390,373,373,373)',
    'list(range(125,137))':'list(range(152,176))',
    "approval['all339_final_pages_directly_viewed']":"approval['all373_final_pages_directly_viewed']",
    "approval['all_names_andtwo_captions_directly_viewed']":"approval['all_names_and17_captions_directly_viewed']",
    "len(menu['menus'])==1":"len(menu['menus'])==8",
    'len(ordinary)==335 and len(typed)==2':'len(ordinary)==373 and len(typed)==17',
    "word=0x2100,offset=rows[0]['current_reference']['command_offset']":"word=rows[0]['source_word'],offset=rows[0]['current_reference']['command_offset']",
    'len(groups)==12':'len(groups)==24',
    "sum(len(g['text_records']) for g in groups)==335 and sum(len(g['native_objects']) for g in groups)==1":"sum(len(g['text_records']) for g in groups)==373 and sum(len(g['native_objects']) for g in groups)==8",
    'source_editorial_objects=337,source_speeches=335,speech_count=335':'source_editorial_objects=390,source_speeches=373,speech_count=373',
    'total_rendered_speech_count=335,typed_choice_count=2,compound_objects=1':'total_rendered_speech_count=373,typed_choice_count=17,compound_objects=8',
    'rom_retention_pins.Maria337.pending.json':'rom_retention_pins.Maria390.pending.json',
    'Preserve Maria337 source-qualified':'Preserve Maria390 source-qualified',
    'source_objects=337,physical_bodies=335,reviewed_blocks=12':'source_objects=390,physical_bodies=373,reviewed_blocks=24',
})


def main():
    # Add the standard source-manuscript identity to a new alias; retain the
    # original exact menu and visual proofs without modifying their successful files.
    priorpath=ROOT/'menu_native_approved_v1.json';out=ROOT/'menu_native_approved_v2.json'
    assert not out.exists()
    prior=load(priorpath);docpath=ROOT/'formatting_v1/formatting_input.json';doc=load(docpath)
    assert prior['runtime']==doc['runtime'] and prior['offline_visual_approved'] and len(prior['menus'])==8
    assert digest(prior['original_receipt'])==prior['original_receipt_sha256']
    assert digest(prior['visual_receipt'])==prior['visual_receipt_sha256']
    alias=deepcopy(prior)
    alias.update(manuscript=str(docpath),manuscript_sha256=digest(docpath),
        original_approved_menu_proof=str(priorpath),original_approved_menu_proof_sha256=digest(priorpath),
        no_caption_bytes_native_proof_visual_review_orindices_changed=True)
    save(out,alias)
    env={**globals(),'__name__':'scripts.maria390_reconstruction_execution'}
    exec(compile(source,__file__+'::same-complete-block-controls-storage-allocation-andinverses-both-menu-arities','exec'),env)
    env['main']()


if __name__=='__main__':main()
