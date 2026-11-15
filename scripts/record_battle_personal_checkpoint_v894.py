"""Archive native/release/startup progress without granting actual-body completion."""

import struct
from pathlib import Path
from shutil import copy2

from dk4tool.patch.battle_personal_editorial import current_entries
from dk4tool.patch.gunnery_deck_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.finish_refit_display_v712 import load
from scripts.prepare_work_comments_v842 import machine_at
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/battle_personal_v894')
RELEASE=Path('work/analysis/battle_personal_v893')
ROM=Path('out/all_routes_combined_v893_candidate.nds')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_personal_v894_893_encounter')


def main():
    assert not (ROOT/'checkpoint.json').exists()
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert ledger['records_editorially_completed']==856 and ledger['records_with_source_and_prose_pass']==884
    assert ledger['current_integrated_candidate']['profile']=='all-routes-unified-v888'
    release=read(RELEASE/'registered_release_verification.json')
    assert release['candidate_sha256']==sha(ROM.read_bytes())
    assert release['patch_sha256']==sha(ROM.with_suffix('.xdelta').read_bytes())
    assert len(release['changed_native_message_IDs'])==18
    assert release['all_prior_profiles471_batches114_accepted_layers_preserved']
    assert release['bad_source_stale_record_manual_spacing_breaks_and_wrong_arguments_rejected']==[True]*9
    fonts=Path('work/analysis/battle_personal_v892/native_font_proof.json')
    assert len(read(fonts)['cases'])==25
    assert read('work/analysis/battle_personal_v892/visual_review.json')['all25_previews_visually_reviewed']
    startup=read(RELEASE/'ordinary_startup_verification.json');assert startup['all7_full_screen_pairs_exact']
    save(RELEASE/'ordinary_startup_visual_review.json',{'startup_proof_sha256':sha((RELEASE/'ordinary_startup_verification.json').read_bytes()),
        'all7_startup_captures_visually_reviewed':True,'visual_review_pending':False,
        'title_character_selection_confirmation_and_opening_complete':True,'full_goal_complete':False})
    report,images,receipt=load(CAP,sha(ROM.read_bytes()),13200)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    fixtures=report['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==2
    rom=NdsImage.open(ROM);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    transitions=[]
    for frame in (4800,5200,10000,12200,13200):
        path=CAP/f'frame_{frame:06d}_arm9_ram.bin';raw=path.read_bytes();cpu,get=machine_at(arm,raw)
        context=get(0x3F0F8);fields=list(struct.unpack('<2I',cpu.mem_read(context+8,8)))
        assert get(0x7F244)==1
        transitions.append({'frame':frame,'RAM':str(path),'RAM_sha256':sha(raw),'context_object':context,
            'original_fields8_12':fields,'actual_captain_ID':1})
    assert transitions[0]['original_fields8_12']==[0,0]
    assert transitions[-1]['original_fields8_12']==[0,1]
    source_preservation=read(ROOT/'encounter_terminal_source_preservation.json')
    assert source_preservation['source_and_disposable_donors_unchanged']
    encounter=ROOT/'original_encounter_verification.json'
    save(encounter,{'candidate_sha256':sha(ROM.read_bytes()),'capture_receipt':receipt,'frames':13200,
        'original_transition_to_battle_predicate_seen_without_mode_injection':transitions,
        'two_coordinate_only_fixtures_no_actor_text_code_enemy_stats_or_outcome_assignment':True,
        'source_donor_and_disposable_copy_unchanged':True,
        'actual_revised_Cabin_body_not_activated':True,'normal_Cabin_navigation_return_still_pending':True,
        'scope':'Fresh cold-boot tutorial encounter and original automatic duel with existing authorized ship coordinate approach. Confirms original battle predicate initialization only;no new25-body gameplay,complete route or hardware claim.',
        'full_goal_complete':False})
    before=NdsImage.open('out/all_routes_combined_v888_candidate.nds')
    old=previous_entries(before.read_file('/COMMON/MESFILE.DK4'),before.read_file('/__arm9__.bin'))
    new=current_entries(common,arm)
    assert all(old[n].text==new[n].text for n in (676,677))
    user=ROOT/'user676_677_current_preservation.json'
    save(user,{'candidate_sha256':sha(ROM.read_bytes()),'exact_repaired676_677_bytes_preserved':True,
        'reference_proof':'work/analysis/gunnery_deck_v889/user676_677_current_preservation.json',
        'new_actual_shop_activation_claimed':False,'global_formatting_watch_still_open':True})
    save(ROOT/'editorial_ledger_before_checkpoint.json',ledger)
    candidate={'path':str(ROM),'sha256':sha(ROM.read_bytes()),'profile':'all-routes-unified-v893',
        'MESFILE_sha256':sha(common),'ARM9_sha256':sha(arm),'patch':str(ROM.with_suffix('.xdelta')),
        'patch_sha256':release['patch_sha256'],'manifest':str(ROM.with_suffix('.manifest.json')),
        'status':'experimental-native-copy-font-layout-patch-startup-and-original-encounter-verified-revised-Cabin-body-and-return-pending',
        'details':'docs/battle_personal_v894_checkpoint.md','full_goal_complete':False}
    ledger['pending_registered_battle_personal_candidate']=candidate
    ledger['next_integrated_profile_for_goal_continuation']='all-routes-unified-v893'
    ledger['battle_personal_v894']={'status':'registered-native-font-layout-startup-encounter-verified-actual-revised-body-and-return-pending',
        'native_message_IDs':list(range(1571,1596)),'revised':18,'retained':7,'completed_entries_added':0,
        'candidate':candidate,'native_font_proof':str(fonts),'registered_release_proof':str(RELEASE/'registered_release_verification.json'),
        'original_encounter_proof':str(encounter),'no_completion_credit_until_actual_body_and_transition_gates_pass':True}
    ledger['active_source_prose_drafts']['status']='three-older-context-unmapped-and25-battle-personal-integrated-native-layout-startup-verified-actual-body-pending'
    ledger['active_source_prose_drafts']['production_manuscript']='translations/battle_personal_editorial_manuscript_v2.json'
    checkpoint=('V894 integrates25 source-reviewed battle-personal comments1571-1595 into registered experimental V893:18 revisions and7 retentions. '
        'All125 selector/control cases,all25 original native-font planes with x0 alignment and216x36 bounds,7336 full native copies,178 cache sequences,471 batches/114 accepted layers and exact clean-input patch pass. '
        'Seven ordinary cold-boot/New Game frames match V888. A fresh13200-frame original encounter with two coordinate-only fixtures initializes the native0/1 battle predicate without assigning it. '
        'Representative revised Cabin body RGB display and normal navigation return remain pending,so no25-entry completion credit is added. V888 remains the last fully scene-verified current reference;V893 is the registered pending candidate. '
        '856 complete (633 revised/223 retained),884 source/prose reviewed. Older750-752,special actors1885-1888,and all unreviewed shared/routes/player prose/raw coverage remain. '
        'Separate graphics/all18 plaques,Samwell header and later older-record re-audit remain open;canonical unchanged;full goal active.')
    ledger['latest_checkpoint']=checkpoint
    ledger['research_checkpoints'].append({'id':'V894-Battle-personal25-native-integration-and-real-encounter',
        'proof':str(encounter),'registered_release':str(RELEASE/'registered_release_verification.json'),
        'completed_entries_added':0,'this_goal_turn_classification':'progress:25 source/prose reviews,all native glyph/layout checks,registered combined ROM/exact patch,ordinary startup and original battle initialization',
        'full_goal_complete':False})
    assert ledger['records_editorially_completed']==856 and ledger['records_revised_and_integrated']==633
    assert ledger['retained_wordings_editorially_completed']==223
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==884
    save(ledger_path,ledger)
    save('out/editorial_review_pending_battle_personal.json',candidate)
    doc=Path('docs/battle_personal_v894_checkpoint.md')
    with doc.open('x',encoding='utf-8') as f:
        f.write('# V894: battle personal editorial integration\n\n'+checkpoint+'\n\n'
            '## Source and English\n\nThe clean Japanese and individual hobby contexts determine the18 revisions. Generic alcohol replaces invented rum;Maria takes an unspecified break rather than a source-unproven smoke. The explicit Naval Warfare Encyclopedia title,reading delay,fishing priority,sword/model care,food/grooming thoughts,training exertion,experiment,nodding-off gag,card-reading offer,duel move,sleepy inability and sad flowers are retained naturally. Seven fluent current lines remain. All25 have exact clean/canonical/current references and per-record natural-dialogue-v2 gates. The explanatory romanization typo Kaizen is corrected to Kaisen in productionv2;source and shipped prose are unchanged.\n\n'
            '## Native formatting and registration\n\nAll25 original selector/native-font/independent word planes match. Rows start at x0 and fit216x36 with complete leading/trailing letters. The standard story audit rejects this COMMON manuscript format;its actual failure log remains. The dedicated original consumer audit has zero errors/unwaived warnings. Only18 selected strings and COMMON selection metadata differ from V888;all3643 other strings,opaque payloads,all art/routes/HELP/ARM7/overlays,native code,section/BSS/startup/cache arenas and123040 staged bytes remain exact. The full registry stack is471 manifest batches/114 accepted layers. The clean-input xdelta reconstructs the candidate byte-for-byte.\n\n'
            '## Actual scope and remaining gates\n\nSeven ordinary no-save cold-boot/New Game captures equal V888 and were visually reviewed. A separate13200-frame fresh cold boot uses the existing five-ship disposable save and two8-byte ship-coordinate fixtures. Original tutorial/duel code changes mode fields from0/0 to0/1 without any battle flag,actor,text or outcome injection. Both donor files remain unchanged. This is targeted automated emulator evidence,not earned travel/recruitment,an actual revised Cabin body,normal Cabin return,a full route or hardware verification. Representative revised battle-personal body RGB holds and normal return remain required before any of these25 entries become completed. All screenshots/research/ROMs stay on E.\n\n'
            '## Candidate\n\nExperimental `out/all_routes_combined_v893_candidate.nds`,SHA256 '+candidate['sha256']+'. Exact patch SHA256 '+candidate['patch_sha256']+'. Canonical accepted base remains `out/raphael_natural_v2_accepted_base.nds`,SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe. Human cold-boot acceptance is required before canonical promotion.\n')
    for p in map(Path,('docs/translation_progress.md','docs/editorial_review_goal.md','docs/todo.md','docs/known_issues.md')):
        with p.open('a',encoding='utf-8') as f:f.write('\n\n## V894: battle personal integration and original encounter\n\n'+checkpoint+' See [V894 checkpoint](battle_personal_v894_checkpoint.md).\n')
    archive=Path('E:/Rota Nova translations/Editorial review/V894 Battle personal native integration');assert not archive.exists()
    paths=set()
    for directory in ('work/analysis/battle_personal_v890','work/analysis/battle_personal_v891','work/analysis/battle_personal_v892','work/analysis/battle_personal_v893','work/analysis/battle_personal_v894'):
        paths.update(p for p in Path(directory).rglob('*') if p.is_file() and p.suffix.lower() not in ('.nds','.dsv','.bin','.log'))
    paths.update(Path(p) for p in ('translations/battle_personal_editorial_manuscript_v1.json','translations/battle_personal_editorial_manuscript_v2.json',
        'translations/battle_personal_editorial_release_v1.json','translations/editorial_review_current_v1.json','translations/release_stack.json',
        'dk4tool/patch/battle_personal_editorial.py','scripts/build_integrated_release.py',str(doc),str(ROM.with_suffix('.manifest.json')),str(ROM.with_suffix('.xdelta'))))
    paths.update(Path('scripts').glob('*battle_personal*v89*.py'))
    copied=[]
    for p in sorted(paths):
        target=archive/p.absolute().relative_to(Path.cwd());target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
        assert sha(p.read_bytes())==sha(target.read_bytes());copied.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    for folder in (CAP,Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_personal_v893_newgame')):
        for p in folder.iterdir():
            if p.suffix not in ('.json','.jsonl','.png'):continue
            target=archive/'captures'/folder.name/p.name;target.parent.mkdir(parents=True,exist_ok=True);copy2(p,target)
            assert sha(p.read_bytes())==sha(target.read_bytes());copied.append({'source':str(p),'archive':str(target),'sha256':sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json',{'files':copied,'all_hashes_verified':True,'no_new_guide_promotion_or_body_completion_credit':True})
    save(ROOT/'checkpoint.json',{'candidate':candidate,'archive':str(archive),'archived_files':len(copied),
        'completed_entries':856,'source_prose_reviewed':884,'actual_revised_body_and_return_pending':True,
        'all_completed_counts_unchanged':True,'goal_turn_classification':'progress','full_goal_complete':False})
    print('V894 checkpoint saved:',len(copied),'archived files;856 complete,884 source/prose. V893 actual revised body/return pending.',flush=True)


if __name__=='__main__':main()
