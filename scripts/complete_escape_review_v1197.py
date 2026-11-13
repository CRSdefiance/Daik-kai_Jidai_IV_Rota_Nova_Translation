"""Complete13 escape notices with corrected source contracts and actual defeat evidence."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.patch.escape_direct_entries import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/escape_completion_v1197')
FINAL=Path('translations/escape_editorial_final_review_v1.json')
DOC=Path('docs/escape_v1197_editorial_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1197 Direct escape correction and completion')
IDS=(*range(1951,1957),*range(1973,1980))


def main():
    assert not ROOT.exists() and not FINAL.exists() and not DOC.exists() and not ARCHIVE.exists()
    release_path=Path('work/analysis/escape_direct_release_v1188/registered_release_verification.json')
    actual_path=Path('work/analysis/escape_terminal_v1194/terminal_gameplay_verification.json')
    startup_path=Path('work/analysis/escape_direct_release_v1188/ordinary_startup_verification.json')
    release,actual,startup=map(read,(release_path,actual_path,startup_path))
    assert release['complete_reconstruction_byte_exact'] and len(actual['all31_fixture_replays'])==31
    assert len(actual['actual_complete_holds'])==2 and actual['source_and_disposable_saves_unchanged']
    assert len(startup['pairs'])==8 and startup['all8_complete_startup_title_NewGame_frames_exact']
    path=Path(release['candidate']);assert sha(path.read_bytes())==release['candidate_sha256']==actual['candidate_sha256']==startup['candidate_sha256']
    rom=NdsImage.open(path);arm=rom.read_file('/__arm9__.bin');common=rom.read_file('/COMMON/MESFILE.DK4')
    entries=current_entries(common,arm)
    manuscript_path=Path('translations/duel_editorial_manuscript_v5.json');doc=read(manuscript_path)
    fonts_path=Path(doc['escape_font_proof']);fonts=read(fonts_path)
    assert len(fonts['cases'])==1417 and fonts['ARM9_sha256']==sha(arm)
    pipeline=read(doc['direct_escape_source_pipeline']);assert len(pipeline['all13_direct_pipeline_cases'])==13
    scope=('All13 escape alternatives have clean Japanese/source-context/natural-English review, unchanged '
        'source substitutions,1417 corrected direct-frame argument/full-native-font cases,416 unchanged '
        'voice selections and13 original53F0C loader/printf/macro/wrap pipelines. Original gameplay '
        'selects1973 in a natural duel defeat after disclosed low-positive starting HP and a native shield '
        'transfer to inventory. Two full native-font/RGB holds prove complete words and uniform margins. '
        'All31 fixtures precede the duel and pass complete4MiB delta/RNG/identity audits. Normal A input '
        'dismisses the notice, advances abandon-ship/loss messages, reaches Game Over and returns to the '
        'ordinary title menu. Other12 IDs have family sample evidence, not individual actual activations. '
        'This is targeted headless testing, not earned progress, a route playthrough or hardware proof.')
    records=[]
    for row in doc['records']:
        n=row['message_id']
        if n not in IDS:continue
        assert all(row['review'].values()) and entries[n].text.hex()==row['compiled_hex']
        cases=[i for i,c in enumerate(fonts['cases']) if c['message_ID']==n]
        assert len(cases)==(235 if n<1973 else 1)
        record=deepcopy(row)
        record.update(before_reference=row['current_reference'],before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},
            current_text_hex=entries[n].text.hex(),current_English=entries[n].text.decode('cp932'),
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            complete_native_font_case_indices=cases,native_font_proof=str(fonts_path),native_font_proof_sha256=sha(fonts_path.read_bytes()),
            completed_candidate_reference=str(path),completed_candidate_sha256=release['candidate_sha256'],
            actual_holds=[r for r in actual['actual_complete_holds'] if r['message_ID']==n],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True,
            status='complete-with-source-native-and-representative-original-defeat-gameplay')
        records.append(record)
    assert len(records)==13 and sum(r['editorial_decision']=='revise' for r in records)==10
    ROOT.mkdir(parents=True)
    save(FINAL,{'format':'dk4-editorial-final-review-v1','family':'Shared-escape-notices1951-1956-and1973-1979',
        'records':records,'native_message_IDs':list(IDS),'source_and_prose_already_counted':True,
        'new_completed_entries':13,'new_revised_completed':10,'new_retained_completed':3,
        'candidate':str(path),'candidate_sha256':release['candidate_sha256'],
        'registered_release':str(release_path),'registered_release_sha256':sha(release_path.read_bytes()),
        'actual_proof':str(actual_path),'actual_proof_sha256':sha(actual_path.read_bytes()),
        'actual_verification_scope':scope,'historical_wrong_queued_parent_format_approval_superseded':True,
        'native_and_startup_sheets_and_actual_notice_loss_GameOver_title_captures_visually_reviewed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    checkpoint=('V1197 completes13 escape notices:10 revised and3 retained. Counts1229 complete '
        '(914 revised,315 retained),1267 source/prose reviewed;38 reviewed COMMON entries remain incomplete '
        'in addition to the broader unreviewed shared/routes/raw-source inventory. V1189 corrects the actual '
        'direct caller02053F40/+274 after V1166 split Everyone.122324 dispatch/ABI,3668 modal,140 status, '
        '1417 full fonts and13 original source pipelines pass. Two actual1973 font/RGB holds,31 pre-duel '
        'fixture audits and ordinary A defeat/GameOver/title transitions pass. Eight ordinary startup '
        'captures and the photographed676/677 shop formatting pass. All471 batches114 accepted layers, '
        'all COMMON/prose/routes/graphics/fonts and the123040-byte staged payload are preserved; the '
        'clean-input patch reconstructs exactly. V1189 remains experimental; canonical and prior '
        'whole-batch scene-verified V997 remain unchanged. All18 plaques and the separate graphics audit '
        'remain open. The full editorial goal remains active.')
    DOC.write_text('# V1197: direct escape editorial completion\n\n'+checkpoint+'\n\n'+scope+
        '\n\nCombined ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1189_candidate.nds`'
        '\n\nROM SHA256: `'+release['candidate_sha256']+'`'
        '\n\nPatch SHA256: `'+release['patch_sha256']+'`'
        '\n\nThis supersedes the escape-format approval in V1174; its static20 completion remains valid. '
        'The original failure and rejected status-constant experiment remain documented in V1187. '
        'No section, cache, arena, BSS, ITCM or source-owned allocation is enlarged. '
        'The next source inventory contains30 unreviewed combat barks/special moves; source and consumer '
        'context must be completed before prose approval. Older COMMON750-752, the successful-shot '
        'sample and remaining sighting/Armed Latina checks remain pending.\n',encoding='utf8')
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1216,904,312,1267)
    assert set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    family={'id':'Shared-escape-notices1951-1956-and1973-1979','native_message_IDs':list(IDS),'records':records,
        'final_review':str(FINAL),'documentation':str(DOC),'actual_verification_scope':scope}
    assert all(f['id']!=family['id'] for f in ledger['completed_editorial_families'])
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append({'id':family['id'],'status':'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs':list(IDS),'final_review':str(FINAL),'actual_proof':str(actual_path),'full_goal_complete':False})
    ledger.update(records_editorially_completed=1229,records_revised_and_integrated=914,retained_wordings_editorially_completed=315)
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==38
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs'] if n not in IDS]
    drafts['manuscripts']=[s for s in drafts['manuscripts'] if 'duel_editorial_manuscript' not in s]
    drafts['manuscript_record_subsets_pending']={k:[n for n in v if n not in IDS] for k,v in drafts['manuscript_record_subsets_pending'].items() if any(n not in IDS for n in v)}
    drafts.update(status='older3-context;successful-shot;15-sighting-remaining-UI',note='38 reviewed incomplete COMMON entries are additional to the broader unreviewed shared/routes/raw-source inventory. Duel static20 and escape13 are complete on separate evidence.')
    ledger['previous_registered_formatting_candidate_before_V1189']=deepcopy(ledger['latest_registered_formatting_candidate'])
    ledger['latest_registered_formatting_candidate']={'path':str(path),'sha256':release['candidate_sha256'],'profile':release['profile'],
        'MESFILE_sha256':sha(common),'ARM9_sha256':sha(arm),'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'status':'experimental;static20-and-escape13-complete;broader-goal-and-inherited-UI-checks-open',
        'release_verification':str(release_path),'original_escape_verification':str(actual_path)}
    ledger['previous_native_relocation_reference_before_V1189']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(path),'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'parser':'dk4tool.patch.escape_direct_entries.current_entries','parser_module_sha256':sha(Path('dk4tool/patch/escape_direct_entries.py').read_bytes()),
        'release_config':'translations/escape_direct_formatting_release_v1.json','requires_guarded_single8192_cache_policy':True,
        'opaque1484byte_prefix_and_carrier1931_are_owned_and_hash_locked':True,
        'all3668_COMMON_entries_unchanged_from_V1166':True,'candidate_experimental_broader_goal_pending':True}
    ledger['duel_prose_v1103'].update(formatting_status='static20-and-escape13-complete-with-source-native-and-separate-representative-original-gameplay',
        escape_final_review=str(FINAL),escape_actual_proof=str(actual_path))
    ledger['escape_direct_binding_erratum_v1187'].update(corrected_native_format_proofs_pass_actual_combined_ROM_replay_pending=False,
        superseding_complete_review=str(FINAL),superseding_actual_gameplay=str(actual_path))
    ledger['latest_checkpoint']=checkpoint;save(ledger_path,ledger)
    for file in ('docs/translation_progress.md','docs/known_issues.md'):
        with Path(file).open('a',encoding='utf8') as stream:stream.write('\n\n## V1197: direct escape correction verified\n\n'+checkpoint+'\n\nSee [V1197 evidence](escape_v1197_editorial_completion.md).\n')
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path)
    pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1189_candidate.nds'
    assert not any(row['path']==pin for row in pins)
    pins.append({'path':pin,'reason':'Latest registered source-bound direct escape formatter; required for remaining full editorial inventory and native source context.'});save(pins_path,pins)
    save(ROOT/'completion_checkpoint.json',{'candidate':str(path),'candidate_sha256':release['candidate_sha256'],'counts':[1229,914,315,1267],
        'reviewed_incomplete_COMMON':ledger['reviewed_but_incomplete_COMMON_IDs'],'final_review':str(FINAL),'documentation':str(DOC),
        'startup_sheet_visually_reviewed':True,'whole_goal_active_and_canonical_not_promoted':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    # Preserve reproducible new sources/proofs in an explicit E-drive archive.
    files=[Path(__file__),FINAL,DOC,manuscript_path,ledger_path,pins_path,Path('translations/release_stack.json'),
        Path('translations/escape_direct_formatting_release_v1.json'),Path('scripts/build_integrated_release.py'),
        Path('docs/translation_progress.md'),Path('docs/known_issues.md'),Path('docs/escape_direct_v1187_checkpoint.md'),
        Path('dk4tool/patch/escape_direct_formatting.py'),Path('dk4tool/patch/escape_direct_entries.py')]
    files += [p for p in Path('scripts').glob('*.py') if any(tag in p.name for tag in ('v1182','v1183','v1184','v1185','v1186','v1187','v1188','v1190','v1191','v1192','v1193','v1194','v1196','v1197'))]
    for folder in ('escape_direct_frame_v1182','escape_direct_runtime_v1184','escape_direct_runtime_v1184c','escape_direct_fonts_v1185',
        'escape_direct_source_v1186c','escape_binding_erratum_v1187','escape_direct_release_v1188','escape_actual_holds_v1193',
        'escape_terminal_v1194','escape_completion_v1197','escape_direct_live_v1190'):
        files += [p for p in (Path('work/analysis')/folder).rglob('*') if p.is_file() and p.suffix not in ('.nds','.dsv')]
    files += [path.with_suffix('.manifest.json'),path.with_suffix('.xdelta')]
    ARCHIVE.mkdir(parents=True);rows=[]
    for source in dict.fromkeys(files):
        relative=source.absolute().relative_to(Path.cwd());dest=ARCHIVE/relative
        dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();rows.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    external=[]
    for key in ('failed_actual_holds',):
        for h in read('work/analysis/escape_binding_erratum_v1187/actual_failure_and_native_successor.json')[key]:
            for k in ('RAM','image'):external.append(Path(h[k]))
    external += [Path(h[k]) for h in actual['actual_complete_holds'] for k in ('RAM','capture')]
    for source in dict.fromkeys(external):
        relative=source.absolute().relative_to(Path('E:/Rota Nova translations').absolute());dest=ARCHIVE/'external_E'/relative
        dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();rows.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':rows,'candidate_physical_E_path':pin,'candidate_sha256':release['candidate_sha256'],
        'new_completed_entries':13,'all_sources_and_proofs_copied_byte_exact':True,'full_goal_complete':False})
    print('13 escape entries complete;1229 completed/1267 source-prose reviewed;38 reviewed COMMON entries remain.',flush=True)
    print('Archive:',ARCHIVE,'files:',len(rows),flush=True)


if __name__=='__main__':main()
