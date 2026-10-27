"""Close only the first/middle-name audit error;preserve all other name/art leads."""

from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_name_v896')


def main():
    proof=ROOT/'name_policy_resolution.json';p=read(proof)
    assert p['all6144_actual_name_bitmap_cells_match_independent_font']
    assert p['duel_Hodram_label_is_consistent_with_recorded_user_name_decision']
    path=Path('translations/editorial_review_current_v1.json');ledger=read(path)
    assert ledger['records_editorially_completed']==856 and ledger['records_with_source_and_prose_pass']==884
    save(ROOT/'editorial_ledger_before_name_resolution.json',ledger)
    ledger['battle_personal_v894']['additional_duel_header_name_lead']={'proof':str(proof),'proof_sha256':sha(proof.read_bytes()),
        'status':'resolved:first-name-Hodram-and-middle-name-Joakim-match-documented-user-policy-no-ROM-fix-needed'}
    ledger['approved_name_roles']={'policy':p['policy'],'policy_sha256':p['policy_sha256'],
        'captain1_full_name':'Hodram Joakim Bergstrom','captain1_first_name':'Hodram','captain1_middle_name':'Joakim',
        'note':'The approved Joakim spelling is the middle name. Hodram remains the user-selected phonetic first name. Historical technical case labels Joakim identify native captain1;they do not authorize replacing his first name. No shipped dialogue,save,name or artwork is changed by this audit correction.'}
    ledger['research_checkpoints'].append({'id':'V896-duel-name-policy-resolution','proof':str(proof),
        'source_and_native_evidence':'Unmodified fresh captain1 control,original virtual first-name getter,and all6144 actual duel-name bitmap cells match documented first Hodram/middle Joakim.',
        'completed_entries_added':0,'previous_goal_turn_classification':'progress:V893 integrated25 native-verified battle comments and real original encounter initialized',
        'this_goal_turn_classification':'progress:incorrect first-middle-name mismatch lead resolved from actual policy/native/fresh-game evidence',
        'all_other_name_art_graphics_and_older_record_scope_unchanged':True,'full_goal_complete':False})
    save(path,ledger)
    doc=Path('docs/duel_name_v896_resolution.md')
    with doc.open('x',encoding='utf-8') as f:
        f.write('# V896: duel first-name audit correction\n\n'
            'The V894 lead confused the user-approved middle name Joakim with the first name. The existing documented decision is **Hodram Joakim Bergstrom**:retain the faithful first-name adaptation Hodram rather than original Latin Hoodlum,and use Joakim rather than Joachim for the middle name. See `translations/character_name_localization_policy_v1.json`.\n\n'
            'Unmodified V893 cold-boots with no cartridge save,savestate,unlock or RAM/ROM fixture. The retained RIGHT input selects genuine captain1. His actual fresh17-byte name fields at actor+32/49/66 are Hodram/Bergstrom/Joakim. The original duel actor pointer resolves the same actual captain;its virtual name getter0201371C returns actor+32,Hodram. The getter and setup match clean code. All6144 actual source-name bitmap cells match independent original font cells,including first/final letters and blanks. The duel first-name label is correct.\n\n'
            'No name patch,player-name overwrite,save or artwork edit is warranted by this lead. The older source donor may still contain historical middle-name spellings;this proof does not certify every save,caption or name consumer. The distinct Samwell header and separate graphics/all18 plaques remain open. Historical V894 observations are retained;this successor records the corrected interpretation. No prose or completion credit is added.\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V896: duel first/middle-name audit correction\n\nThe documented full name is Hodram Joakim Bergstrom. Fresh no-save captain1,original own-name getter and all6144 actual duel-name cells confirm Hodram is the correct first-name label. Joakim is the approved middle name. The V894 mismatch interpretation is corrected;no ROM/name overwrite or completion credit. Other name/graphics/prose scope remains open. See [V896 evidence](duel_name_v896_resolution.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V896 Duel first middle name resolution');assert not archive.exists();rows=[]
    paths=[p for p in ROOT.iterdir() if p.is_file()]+[Path(__file__),Path('scripts/verify_duel_name_policy_v896.py'),Path('scripts/run_joakim_name_control_v896.py'),
        Path('translations/character_name_localization_policy_v1.json'),path,doc]
    for p in paths:
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert sha(target.read_bytes())==sha(p.read_bytes());rows.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    cap=Path(read(ROOT/'fresh_control_run_plan.json')['folder'])
    for p in cap.iterdir():
        if p.suffix not in ('.json','.jsonl','.png'):continue
        target=archive/'fresh_control'/p.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert sha(target.read_bytes())==sha(p.read_bytes());rows.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':rows,'all_hashes_verified':True,'no_completion_or_global_name_coverage_credit':True})
    print('V896 naming lead closed against documented policy;no ROM edit;all other audit scope retained.',flush=True)


if __name__=='__main__':main()
