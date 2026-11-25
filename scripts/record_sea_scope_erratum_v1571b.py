"""Correct the old no-lookout pilot transition label without changing its evidence."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/sea_scope_erratum_v1571b');assert not root.exists()
    source=Path('work/analysis/sea_registration_pilot_verified_v1552j/original_registration_and_no_lookout_verified.json')
    old=read(source)
    assert old['normal_modal_A_dismissal_and_return_to_sea6850']
    picture=Path('E:/Rota Nova translations/Generated/work/emulation_v193/sea_registration_live_v1552h_1542/frame_006850_navigation.png')
    report=read(old['terminal_report']);row=next(r for r in report['frames_captured'] if r['frame']==6850)
    assert sha(picture.read_bytes())==row['PNG_sha256']
    text='V1552j pilot label erratum: after closing No lookout at6850,the actual screen is Info Mode/Inspect over the sea,with the unidentified target still selected. The old return_to_sea key proves normal modal close only;it does not prove the Sea View interface. This correction changes no ROM,inputs,captures,source text or completion counts. The same distinction for the revised6300 run is already corrected in V1568b.'
    root.mkdir(parents=True)
    proof={'supersedes_scope_label_in':str(source),'source_sha256':sha(source.read_bytes()),'capture':str(picture),'capture_sha256':row['PNG_sha256'],
        'actual6850_Inspect_interface_visually_reviewed':True,'correction':text,'all_primary_evidence_unchanged':True,'full_goal_complete':False}
    target=root/'transition_scope_erratum.json';save(target,proof)
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    ledger['newly_observed_sea_inspection_modal_defects']['pilot_transition_scope_erratum']=str(target)
    save(ledger_path,ledger)
    for name in ['known_issues.md','sea_responses_v1570_integration_checkpoint.md','editorial_handoff_current.md']:
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n'+text+'\n')
    dest=Path('E:/Rota Nova translations/Editorial review/V1571 sea inspection integration and open modals/errata');dest.mkdir()
    copy2(target,dest/target.name);assert sha(target.read_bytes())==sha((dest/target.name).read_bytes())
    print('Old6850 transition scope corrected to Inspect;all originals retained,no ROM or completion change.')
