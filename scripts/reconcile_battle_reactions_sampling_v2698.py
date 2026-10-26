"""Reuse still-current RGB controls;bind unchanged reaction contexts/source."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_reactions_sampling_v2698')
DOC=Path('translations/battle_reactions_contextual_editorial_manuscript_v1.json')
REFERENCE=Path('work/analysis/ship_sinking_sampling_v2684/representative_control_and_rgb_reconciliation.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);old=read(REFERENCE)
    assert old['candidate']==doc['current_ROM'] and old['candidate_sha256']==doc['current_ROM_sha256']
    assert len(old['historical_holds'])==4 and len(old['negative_controls'])==9 and all(c['rejected'] for c in old['negative_controls'])
    assert old['historical_actual_IDs']==[2082,2138] and old['no_open_translation_specific_display_or_control_finding']
    for p,digest in old['evidence'].items():assert sha(Path(p).read_bytes())==digest,p
    assert sha(Path(old['review_sheet']).read_bytes())==old['review_sheet_sha256']
    rom=NdsImage.open(doc['current_ROM']);arm=rom.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(arm)==doc['current_ARM9_sha256'];context=read(doc['native_context_proof'])
    spans=[]
    for a,b in [(0x65968,0x65A00),(0x65B08,0x65B90),(0x70FA0,0x71088),(0x74094,0x74328),(0x751E0,0x756FC),(0x7E0AC,0x7E158),(0x53F0C,0x53F4C),(0x54058,0x54144),(0x54164,0x54240)]:
        assert arm[a:b]==clean[a:b];spans.append(dict(start=a,end=b,sha256=sha(arm[a:b])))
    policy=('Reuse the still-current completed V2684 full-palette V2674 proof without repeating emulator orRGBexecution. Its four preserved historical actual2082named-target/direct and2138role1holds match whole current native ink,gray detail andblank-paper masks;its nine corruptions reject missing boundary glyphs,wrong name andstray ink/gray pixels. These establish the shared kind0 portrait panel andnormal returns,not selected2147-2178activation. All32current reactions havezero original substitutions anduse original53F0Cdirect-actor selection. Fresh four-table828actor-choice proof andcurrent32whole pipelines/full independent font planes bind their exact text andpresentation;all32old full-palette cases match. Four original event contexts distinguish optional setup encouragement,own-ship-hit surprise andinjury. Original setup RNG/mood/voice andactor24exclusion are retained;not every stored setup voice is claimed reachable through that caller. Original hit/probability/HP/health-state predicates andconstructor/return code are clean exact. No distinct new translation-specific display/control risk requires individual conditional visits under the user representative-sampling policy. No health,RNG,mood,eligibility,actor identity,result or event is forced. No selected32activation,new emulator run,earned duty or full-route claim is made.')
    ROOT.mkdir(parents=True)
    save(ROOT/'representative_reconciliation.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],reference=str(REFERENCE),reference_sha256=sha(REFERENCE.read_bytes()),
        evidence={str(REFERENCE):sha(REFERENCE.read_bytes()),str(DOC):sha(DOC.read_bytes()),doc['native_context_proof']:sha(Path(doc['native_context_proof']).read_bytes()),'docs/editorial_testing_scope_v1870.md':sha(Path('docs/editorial_testing_scope_v1870.md').read_bytes())},
        reused_historical_holds=old['historical_holds'],reused_negative_controls=old['negative_controls'],source_exact_spans=spans,
        historical_actual_IDs=[2082,2138],actual_selected_reaction_IDs=[],new_emulator_runs=0,new_RGB_execution=0,
        current_candidate_identical_to_completed_representative_proof=True,original_reaction_predicates_constructor_and_return_code_clean_exact=True,
        selected_families=[t['first_ID'] for t in context['voice_tables']],policy_resolution=policy,no_open_translation_specific_display_or_control_finding=True,
        review_sheet=old['review_sheet'],review_sheet_sha256=old['review_sheet_sha256'],historical_sheet_labels_not_selected32_activation=True,
        native_and_visual_completion_still_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Existing current-V2674 representative proof exact:4historical holds/9controls reused;reaction source predicates/UIreturns clean exact. No selected32activation or new emulator run.')
