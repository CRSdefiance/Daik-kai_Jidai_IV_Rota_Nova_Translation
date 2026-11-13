"""Freeze release inputs for15 reviewed sighting paragraphs and two native labels."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.sighting_layout_v1069 import compiled
from scripts.sighting_labels_v1083b import FIELDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_release_v1084')
SOURCE=Path('translations/sighting_editorial_manuscript_v6.json')
MANUSCRIPT=Path('translations/sighting_editorial_manuscript_v7.json')
ROM=Path('out/all_routes_combined_v1034_candidate.nds')


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    doc=read(SOURCE);rom=NdsImage.open(ROM)
    assert sha(ROM.read_bytes())==doc['current_ROM_sha256']
    label_path=Path('work/analysis/sighting_labels_v1083b/native_label_proof.json');labels=read(label_path)
    assert labels['candidate_sha256']==doc['current_ROM_sha256']
    assert labels['complete_Armed_Latina_and_NUL_survive_original_initializer'] and labels['all153_other_initialized_ship_records_exact']
    assert labels['default_fixed_ship_index']==115 and len(labels['all81_bearing_getter_ABI_cases'])==81
    previews=labels['native_font_previews']
    for r in previews:assert sha(Path(r['preview']).read_bytes())==r['preview_sha256']
    ROOT.mkdir(parents=True)
    visual=ROOT/'visual_review.json';old_visual=Path(doc['visual_review'])
    assert sha(old_visual.read_bytes())==doc['visual_review_sha256']
    save(visual,{'reviewed_dialogue_visual_proof':str(old_visual),'reviewed_dialogue_visual_proof_sha256':sha(old_visual.read_bytes()),
        'all15_current_paragraphs_and_six_native_sheets_reviewed':True,
        'native_label_proof':str(label_path),'native_label_proof_sha256':sha(label_path.read_bytes()),
        'two_complete_native_label_and_capture_notice_previews_visually_reviewed':previews,
        'complete_Armed_Latina_capital_A_final_a_and_NUL_verified_by_original_initializer':True,
        'close_range_vicinity_is_grammatical_in_all15_reviewed_paragraphs':True,
        'blocking_errors':0,'unwaived_warnings':0,'visual_review_pending':False,
        'scope':'Only these15 paragraphs,two source-owned labels,and their mapped native consumers. Global uppercase weak-word and full editorial audits remain open.',
        'actual_registered_scene_and_copy_gates_pending':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    arm=rom.read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    label_rows=[]
    for i,(at,current,target) in enumerate(FIELDS):
        assert arm[at:at+len(current)]==current
        text=target.split(b'\0')[0].decode('ascii')
        label_rows.append({'id':'CLOSE_RANGE_BEARING_LABEL' if i==0 else 'ARMED_LATINA_DEFAULT_SHIP_LABEL',
            'file_path':'/__arm9__.bin','offset':at,'allocation_bytes':len(current),
            'source_hex':clean[at:at+len(current)].hex(),'canonical_source_hex':canonical[at:at+len(current)].hex(),
            'current_text_hex':current.hex(),'replacement_hex':target.hex(),'english':text,
            'source_meaning':'At very close range;close by.' if i==0 else 'Armed version of the established Latina ship class.',
            'context':'Original6567C returns this first argument to the two mapped sighting callers;original companion compass labels remain unchanged.' if i==0 else 'OriginalCD27C initializes fixed NPC ship115 from metadata0211DB5C;the complete name is copied into the bounded19-byte model field. The label actually appeared in a native capture notice.',
            'localization_note':'The existing15-paragraph grammar uses in the vicinity and preserves the source location meaning without changing compass bearings.' if i==0 else 'Retain established Latina and use Armed consistently with adjacent armed ship variants. Do not alter player-entered names or other ship metadata.',
            'review':{key:True for key in ('source','context','localization','naturalness','formatting')}})
    for row in doc['records']:row['compiled_hex']=compiled(row).hex()
    doc.update(reviewed_research_manuscript=str(SOURCE),reviewed_research_manuscript_sha256=sha(SOURCE.read_bytes()),
        current_COMMON_sha256=sha(rom.read_file('/COMMON/MESFILE.DK4')),current_ARM9_sha256=sha(arm),
        native_label_records=label_rows,native_label_proof=str(label_path),native_label_proof_sha256=sha(label_path.read_bytes()),
        visual_review=str(visual),visual_review_sha256=sha(visual.read_bytes()),
        status='15-paragraphs-and-two-native-labels-approved-for-registered-insertion;actual-and-completion-pending')
    save(MANUSCRIPT,doc)
    save(ROOT/'input_provenance.json',{'source_manuscript':str(SOURCE),'source_manuscript_sha256':sha(SOURCE.read_bytes()),
        'release_manuscript':str(MANUSCRIPT),'release_manuscript_sha256':sha(MANUSCRIPT.read_bytes()),
        'two_label_owned_allocations':[r['allocation_bytes'] for r in label_rows],
        'failed_source_guard_predecessor_retained':'scripts/probe_sighting_labels_v1083.py',
        'correct_bearing_pointer_is_from_original_getter_proof':'0214511C;not0214521C',
        'no_ROM_or_registry_or_builder_change_yet':True,'no_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Release manuscriptV7 freezes15 native-approved paragraphs and two complete bounded labels. No ROM built.',flush=True)


if __name__=='__main__':main()
