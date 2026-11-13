"""Close15 special-call reviews with original source,fonts and gameplay."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.patch import duel_special_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_special_layout_v1216 import IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_special_completion_v1246')
FINAL=Path('translations/duel_special_editorial_final_review_v1.json')
DOC=Path('docs/duel_special_v1246_editorial_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1246 Special move completion')


def main():
    assert not ROOT.exists() and not FINAL.exists() and not DOC.exists() and not ARCHIVE.exists()
    release_path=Path('work/analysis/duel_special_release_v1223/registered_release_verification.json')
    actual_path=Path('work/analysis/duel_long_terminal_v1245b/terminal_gameplay_verification.json')
    startup_path=Path('work/analysis/duel_special_release_v1223/ordinary_startup_verification.json')
    shop_path=Path('work/analysis/duel_special_release_v1223/photographed_shop_formatting.json')
    release,actual,startup,shop=map(read,(release_path,actual_path,startup_path,shop_path))
    path=Path(release['candidate']);digest=sha(path.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']==startup['candidate_sha256']==shop['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and len(startup['pairs'])==8
    assert len(actual['actual_special_holds'])==6 and len(actual['all31_fixture_replays'])==31
    assert actual['source_and_disposable_saves_unchanged'] and actual['original_random_chance10_percent_not_forced']
    assert actual['actual_native_component_and_carrier_copy_confirm_original_new_dispatch']
    rom=NdsImage.open(path);common,arm=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    entries=owned.current_entries(common,arm);config=read(owned.CONFIG)
    manuscript_path=Path(config['manuscript']);manuscript=read(manuscript_path)
    fonts_path=Path(manuscript['native_font_proof']);fonts=read(fonts_path)
    assert len(fonts['cases'])==51 and len(fonts['excluded_cases'])==49 and fonts['ARM9_sha256']==sha(arm)
    assert sha(Path('translations/release_stack.json').read_bytes())==read(path.with_suffix('.manifest.json'))['release_stack_sha256']
    scope=('All15 special-call alternatives have clean Japanese,original actor/method/side/duration context, '
        'faithful natural-English review and complete original native fonts/crops. Nine original special '
        'methods map15 calls,including Julio2146 outside the prior14-entry group.131324 dispatch cases, '
        '7336 warm/cold copies180 cache sequences,49 exclusions and13 original escape regressions pass. '
        'Original Hodram methodF114 naturally selects1990 in an actual cold-boot duel; six complete '
        '208x36 bitmap and144x12 RGB crop holds pass. The14 other alternatives have representative '
        'family evidence,not individual actual activations. All31 fixtures occur before duel5772,last5770, '
        'with complete4MiB delta,208 actor identity,RNG/event-word and input audits. Disposable prerequisites '
        'set stamina/agility1,spirit/luck100 through original setters;native positive HP maximum;shield49 '
        'moves to inventory. Luck100 gives the original unforced10percent chance. No actor ID,numeric '
        'message,RNG seed,eligibility flag or result is injected. No healing,revival,relocation or ability '
        'change occurs during/after combat. The special returns to original combat,natural victory and '
        'ordinary sea aftermath;source/disposable saves remain exact. This is targeted headless testing, '
        'not earned progression,a whole route or hardware verification.')
    records=[]
    for row in manuscript['records']:
        n=row['message_id'];assert n in IDS and all(row['review'].values()) and entries[n].text.hex()==row['compiled_hex']
        case=next(c for c in fonts['cases'] if c['message_ID']==n)
        r=deepcopy(row)
        r.update(before_reference=row['current_reference'],before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},
            current_text_hex=entries[n].text.hex(),current_English=entries[n].text.decode('cp932'),
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            completed_candidate_reference=str(path),completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=[h for h in actual['actual_special_holds'] if h['message_ID']==n],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True,
            status='complete-with-source-native-and-representative-original-special-gameplay')
        records.append(r)
    assert len(records)==15 and sum(r['editorial_decision']=='revise' for r in records)==9
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],
        ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1245,925,320,1298)
    existing=[n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(existing)==len(set(existing))==1244 and not set(existing).intersection(IDS)
    assert set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    ROOT.mkdir(parents=True)
    save(FINAL,{'format':'dk4-editorial-final-review-v1','family':'Shared-duel-specials1980-1993-and2146',
        'records':records,'native_message_IDs':list(IDS),'source_and_prose_already_counted':True,
        'new_completed_entries':15,'new_revised_completed':9,'new_retained_completed':6,
        'candidate':str(path),'candidate_sha256':digest,'registered_release':str(release_path),
        'registered_release_sha256':sha(release_path.read_bytes()),'actual_proof':str(actual_path),
        'actual_proof_sha256':sha(actual_path.read_bytes()),'actual_verification_scope':scope,
        'all15_native_previews_startup_and_actual_special_combat_victory_return_visually_reviewed':True,
        'victory_HP_zero_observed_at8622_not_premature8502':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family={'id':'Shared-duel-specials1980-1993-and2146','native_message_IDs':list(IDS),'records':records,
        'final_review':str(FINAL),'documentation':str(DOC),'actual_verification_scope':scope}
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append({'id':family['id'],'status':'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs':list(IDS),'final_review':str(FINAL),'actual_proof':str(actual_path),'full_goal_complete':False})
    ledger.update(records_editorially_completed=1260,records_revised_and_integrated=934,retained_wordings_editorially_completed=326)
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    completed=[n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(completed)==len(set(completed))==1259
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==38 and not set(completed).intersection(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert sum(len(f.get('records',[])) for f in ledger['completed_editorial_families'])==1260
    by_file={'/COMMON/MESFILE.DK4':1259,'/data/SC2.DK4':1}
    source_by_file={'/COMMON/MESFILE.DK4':1297,'/data/SC2.DK4':1}
    ledger['completed_editorial_record_counts_by_file']=by_file
    ledger['source_prose_reviewed_counts_by_file']=source_by_file
    save(ROOT/'exact_coverage_reconciliation.json',{'unique_completed_COMMON_IDs':sorted(completed),
        'reviewed_incomplete_COMMON_IDs':ledger['reviewed_but_incomplete_COMMON_IDs'],
        'completed_counts_by_file':by_file,'source_prose_counts_by_file':source_by_file,
        'new_completed15_previously_counted_in_source1298_no_duplicate_credit':True,'full_goal_complete':False})
    drafts=ledger['active_source_prose_drafts']
    drafts['native_message_IDs']=[n for n in drafts['native_message_IDs'] if n not in IDS]
    drafts['manuscripts']=[p for p in drafts['manuscripts'] if 'duel_special_editorial_manuscript' not in p]
    drafts['manuscript_record_subsets_pending']={p:[n for n in ns if n not in IDS] for p,ns in drafts['manuscript_record_subsets_pending'].items() if any(n not in IDS for n in ns)}
    drafts.update(status='no-active-special-draft;38-older-reviewed-entries-and-broader-inventory-open',
        note='750-752 context,successful Lookout shot and remaining sighting UI checks persist;broader shared/routes/raw-source inventory remains unreviewed.')
    ledger['duel_special_prose_v1216'].update(actual_gameplay_pending=False,completed_entries=15,
        final_review=str(FINAL),actual_proof=str(actual_path))
    ledger['latest_registered_formatting_candidate'].update(
        status='experimental;15-special-calls-complete;older-remaining-checks-and-broader-goal-open',
        original_special_verification=str(actual_path))
    checkpoint=('V1246 completes15 original duel special calls,including Julio2146:9 revisions and6 retained. '
        'Counts1260 complete (934 revised,326 retained),1298 source/prose reviewed;38 reviewed COMMON entries '
        'remain incomplete plus broader shared/routes/raw-source inventory. V1224 retains all471 batches114 '
        'accepted layers and previous routes,graphics,fonts and unselected prose.131324 dispatch,51 full '
        'fonts49 exclusions,7336 copies180 cache sequences,13 escape pipelines,eight ordinary startup frames '
        'and photographed676/677 formatting pass;clean-input patch reconstructs exactly. Original1990 special '
        'has six complete native bitmap/RGB holds,31 pre-duel fixture audits and natural combat/victory/sea '
        'aftermath. Disclosed native-range ability/HP/equipment prerequisites only before combat;Luck100 '
        'uses original unforced10percent chance;RNG,actor IDs,eligibility flags and results unchanged. '
        'No allocation or123040-byte staged growth. V1224 experimental;canonical and V997 unchanged. '
        'All18 plaques and separate graphics audit open. Full editorial goal remains active.')
    ledger['latest_checkpoint']=checkpoint;save(ledger_path,ledger)
    DOC.write_text('# V1246 special-move editorial completion\n\n'+checkpoint+'\n\n## Verification scope\n\n'+scope+
        '\n\n## Candidate\n\nROM SHA256: `'+digest+'`. Patch SHA256: `'+release['patch_sha256']+'`.\n\n'
        'The candidate remains experimental. Canonical promotion requires explicit user acceptance. '
        'Only1990 has actual individual activation evidence;the other14 receive the documented representative family sample. '
        'Earlier failed/no-special runs remain preserved. V1245 correctly rejected its premature HP-zero expectation; '
        'V1245b binds victory to actual frame8622. Every other proof and source capture remains unchanged.\n\n'
        'Actual proof: `'+str(actual_path)+'`. Final review: `'+str(FINAL)+'`. '
        'Guide captures: `E:/Rota Nova translations/Guide screenshots/V1224 Special move`. '
        'Those captures disclose isolated ability/health/equipment testing prerequisites.\n\n'
        'Remaining: older38 reviewed entries plus the complete unreviewed shared,route and raw-source inventory. '
        'Revisit older record-based checks after the full editorial goal;do not treat this batch as the whole goal.\n',encoding='utf-8')
    for p in ('docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md'):
        with Path(p).open('a',encoding='utf-8') as f:f.write('\n\n## V1246 special-move review completion\n\n'+checkpoint+'\n\nSee [evidence](duel_special_v1246_editorial_completion.md).\n')
    ARCHIVE.mkdir(parents=True)
    files={Path(__file__).absolute(),FINAL.absolute(),DOC.absolute(),ledger_path.absolute(),
        path.with_suffix('.manifest.json').absolute(),path.with_suffix('.xdelta').absolute()}
    for p in config['dependencies']:files.add(Path(p).absolute())
    for p in [owned.CONFIG,str(actual_path),str(release_path),str(startup_path),str(shop_path),
              'translations/release_stack.json','translations/rom_retention_pins.json','scripts/build_integrated_release.py',
              'scripts/native_duel_contact_v1169.py','scripts/native_duel_special_fixture_v1232.py',
              'docs/known_issues.md','docs/todo.md','docs/translation_progress.md','docs/editorial_review_goal.md']:
        files.add(Path(p).absolute())
    for pattern in ('*duel_long*.py','*duel_health_limits*.py'):
        files.update(p.absolute() for p in Path('scripts').glob(pattern))
    for folder in [Path('work/analysis/duel_long_terminal_v1245b'),Path('work/analysis/duel_long_actual_v1244'),
                   Path('work/analysis/duel_long_live_v1243'),ROOT]:
        files.update(p.absolute() for p in folder.rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.png'))
    copies=[]
    for source in sorted(files):
        relative=source.relative_to(Path.cwd().absolute());dest=ARCHIVE/'Repository'/relative
        dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert sha(source.read_bytes())==sha(dest.read_bytes())
        copies.append({'source':str(source),'archived':str(dest),'sha256':sha(dest.read_bytes())})
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/duel_long_v1243_1224')
    external=[cap/'capture_report.json',cap/'navigation_command_journal.json']
    for frame in (5770,7622,7662,7822,8022,8622,10982,11782):
        external += [cap/f'frame_{frame:06d}_arm9_ram.bin',cap/f'frame_{frame:06d}_navigation.png']
    for source in external:
        dest=ARCHIVE/'Actual original duel'/source.name;dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert source.read_bytes()==dest.read_bytes()
        copies.append({'source':str(source),'archived':str(dest),'sha256':sha(dest.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':copies,'all_copies_hash_verified':True,
        'candidate_physical_E_path':'E:/Rota Nova translations/Generated/out/all_routes_combined_v1224_candidate.nds',
        'candidate_sha256':digest,'new_completed_entries':15,'full_goal_complete':False})
    save(ROOT/'archive_receipt.json',{'archive':str(ARCHIVE),'files':len(copies),
        'manifest_sha256':sha((ARCHIVE/'archive_manifest.json').read_bytes())})
    print('15 special calls complete;1260 completed/1298 source-prose;38 older reviewed entries and full inventory remain.',flush=True)
    print('Exact source/proof/archive copies:',len(copies),flush=True)


if __name__=='__main__':main()
