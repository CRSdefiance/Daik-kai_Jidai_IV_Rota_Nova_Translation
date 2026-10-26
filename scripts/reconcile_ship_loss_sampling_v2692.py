"""Reuse still-current RGB controls;bind loss/surrender-specific unchanged source."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/ship_loss_sampling_v2692')
DOC=Path('translations/ship_loss_contextual_editorial_manuscript_v1.json')
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
    for a,b in [(0x72484,0x7251C),(0x7251C,0x72BE0),(0x53D44,0x53DCC),(0x53F4C,0x53F9C),(0x54058,0x54144),(0x54164,0x54240)]:
        assert arm[a:b]==clean[a:b];spans.append(dict(start=a,end=b,sha256=sha(arm[a:b])))
    policy=('Reuse the completed V2684 full-palette current-V2674 binding without repeating emulator runs or RGB execution. Its four preserved historical2082named-target capture and2138role1defeat holds match whole current native ink,gray detail andblank-paper masks;its nine corruptions reject missing boundary glyphs,wrong name andstray ink/gray pixels. Those actual samples establish named-vessel substitution andmember/direct kind0 panel/return behavior,not activation of selected2074-2081or2090-2105. All24selected reports use original53D44role1withone ship-name argument. Fresh three-table/source binding andcurrent complete native pipelines cover selection,loader,printf,literal-name macro scope,wrapping andwhole fonts. Original7251Cstatus predicates,72484surrender probability,UIconstructor andreturn code remain clean exact. Capture/own surrender/enemy surrender are distinct original branches withflagship results handled separately. Current22/23boundary copies are checked separately. Exact complete proper-name-plus-punctuation final rows receive individual case-bound dispositions;no blanket orphan exception is given. These checks leave no new translation-specific display/control finding requiring individual conditional capture/surrender visits under the user representative-sampling policy. No crew,Hull,RNG,shipresult,roster identity or original event outcome is forced. New emulator runs,earned staffing andactual activation of these24are not claimed.')
    ROOT.mkdir(parents=True)
    save(ROOT/'representative_reconciliation.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],reference=str(REFERENCE),reference_sha256=sha(REFERENCE.read_bytes()),
        evidence={str(REFERENCE):sha(REFERENCE.read_bytes()),str(DOC):sha(DOC.read_bytes()),doc['native_context_proof']:sha(Path(doc['native_context_proof']).read_bytes()),'docs/editorial_testing_scope_v1870.md':sha(Path('docs/editorial_testing_scope_v1870.md').read_bytes())},
        reused_historical_holds=old['historical_holds'],reused_negative_controls=old['negative_controls'],source_exact_spans=spans,
        historical_actual_IDs=[2082,2138],actual_selected_capture_surrender_IDs=[],new_emulator_runs=0,new_RGB_execution=0,
        current_candidate_identical_to_completed_representative_proof=True,original_capture_surrender_constructor_and_return_code_clean_exact=True,
        selected_families=[t['family'] for t in context['voice_tables']],policy_resolution=policy,no_open_translation_specific_display_or_control_finding=True,
        review_sheet=old['review_sheet'],review_sheet_sha256=old['review_sheet_sha256'],historical_sheet_labels_not_selected24_activation=True,
        native_and_visual_completion_still_pending=True,completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Existing current-V2674 representative proof remains exact:4historical holds/9negative controls reused;capture/surrender source predicates/UIreturns clean exact. No selected24activation or new emulator run.')
