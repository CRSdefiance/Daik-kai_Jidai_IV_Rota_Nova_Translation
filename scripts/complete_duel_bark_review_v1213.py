"""Close16 source-reviewed reactions with complete fonts and original timed gameplay."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
from shutil import copy2
from dk4tool.patch import duel_bark_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_bark_layout_v1200 import IDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/duel_bark_completion_v1213')
FINAL=Path('translations/duel_bark_editorial_final_review_v1.json')
DOC=Path('docs/duel_bark_v1213_editorial_completion.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V1213 Timed duel reaction completion')


def main():
    assert not ROOT.exists() and not FINAL.exists() and not DOC.exists() and not ARCHIVE.exists()
    release_path=Path('work/analysis/duel_bark_release_v1205/registered_release_verification.json')
    actual_path=Path('work/analysis/duel_bark_terminal_v1211/terminal_gameplay_verification.json')
    startup_path=Path('work/analysis/duel_bark_release_v1205/ordinary_startup_verification.json')
    shop_path=Path('work/analysis/duel_bark_release_v1205/photographed_shop_formatting.json')
    release,actual,startup,shop=map(read,(release_path,actual_path,startup_path,shop_path))
    path=Path(release['candidate']);digest=sha(path.read_bytes())
    assert digest==release['candidate_sha256']==actual['candidate_sha256']==startup['candidate_sha256']==shop['candidate_sha256']
    assert release['complete_reconstruction_byte_exact'] and len(startup['pairs'])==8
    assert len(actual['actual_new_reaction_holds'])==4 and len(actual['actual_preserved_escape_holds'])==2
    assert len(actual['all31_fixture_replays'])==31 and actual['source_and_disposable_saves_unchanged']
    assert len(actual['two_rejected_duration2_in_one_frame_gap_commands_applied_no_input_or_fixture'])==2
    rom=NdsImage.open(path);common=rom.read_file('/COMMON/MESFILE.DK4');arm=rom.read_file('/__arm9__.bin')
    entries=owned.current_entries(common,arm);config=read(owned.CONFIG);manuscript_path=Path(config['manuscript']);doc=read(manuscript_path)
    fonts_path=Path(doc['native_font_proof']);fonts=read(fonts_path)
    assert len(fonts['cases'])==36 and fonts['ARM9_sha256']==sha(arm)
    scope=('All16 timed duel-action voice alternatives have clean Japanese/source/voice context and natural-English '
        'review, complete original loader/PIC/ASCII/CP932 font and crop evidence,65615 exact five-table dispatch '
        'checks,92 complete moved-block native copies18 cache sequences and preservation of the20 earlier static '
        'duel alternatives. Original timed A inputs produce1958 positive and1966 negative feedback in four '
        'complete native bitmap/RGB holds. Fourteen other alternatives have family sample evidence, not individual '
        'actual activations. Two current1973 escape holds and13 source-call regressions preserve the earlier fix. '
        'All31 disclosed positive-health/ship/contact fixtures occur before the duel and have complete4MiB delta, '
        'identity and RNG audits. No actor IDs, messages, RNG values or results are injected. Two duration-invalid '
        'input intentions were rejected before any input or fixture; the exact accepted controller schedule and '
        'all reached navigation targets are verified. Normal A dismissal reaches the original loss/Game Over '
        'and ordinary title menu; source/disposable saves remain unchanged. This is targeted headless testing, '
        'not earned progress, a full route or hardware verification.')
    records=[]
    for row in doc['records']:
        n=row['message_id'];assert n in IDS and all(row['review'].values()) and entries[n].text.hex()==row['compiled_hex']
        case=next(c for c in fonts['cases'] if c['message_ID']==n)
        record=deepcopy(row)
        record.update(before_reference=row['current_reference'],before_text_hex=row['current_text_hex'],
            current_reference={k:v for k,v in asdict(entries[n]).items() if k!='text'},current_text_hex=entries[n].text.hex(),
            current_English=entries[n].text.decode('cp932'),
            decision='revised-and-integrated' if row['editorial_decision']=='revise' else 'retained-and-editorially-reviewed',
            completed_candidate_reference=str(path),completed_candidate_sha256=digest,
            complete_native_font_proof=str(fonts_path),complete_native_font_proof_sha256=sha(fonts_path.read_bytes()),
            complete_native_formatted_lines=case['lines'],
            actual_holds=[r for r in actual['actual_new_reaction_holds'] if r['message_ID']==n],
            individual_actual_activation_not_claimed_when_actual_holds_empty=True,
            status='complete-with-source-native-and-representative-original-timing-gameplay')
        records.append(record)
    assert len(records)==16 and sum(r['editorial_decision']=='revise' for r in records)==11
    ledger_path=Path('translations/editorial_review_current_v1.json');ledger=read(ledger_path)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1229,914,315,1283)
    existing=[n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(existing)==len(set(existing))==1228 and not set(existing).intersection(IDS)
    assert sum(len(f.get('records',[])) for f in ledger['completed_editorial_families'])==1229
    assert set(IDS)<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    old_counts=deepcopy(ledger['completed_editorial_record_counts_by_file'])
    old_source_counts=deepcopy(ledger['source_prose_reviewed_counts_by_file'])
    ROOT.mkdir(parents=True)
    save(FINAL,{'format':'dk4-editorial-final-review-v1','family':'Shared-timed-duel-reactions1957-1972',
        'records':records,'native_message_IDs':list(IDS),'source_and_prose_already_counted':True,
        'new_completed_entries':16,'new_revised_completed':11,'new_retained_completed':5,
        'candidate':str(path),'candidate_sha256':digest,'registered_release':str(release_path),
        'registered_release_sha256':sha(release_path.read_bytes()),'actual_proof':str(actual_path),
        'actual_proof_sha256':sha(actual_path.read_bytes()),'actual_verification_scope':scope,
        'native_sheet_startup_and_actual_reaction_escape_loss_GameOver_title_captures_visually_reviewed':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    family={'id':'Shared-timed-duel-reactions1957-1972','native_message_IDs':list(IDS),'records':records,
        'final_review':str(FINAL),'documentation':str(DOC),'actual_verification_scope':scope}
    ledger['completed_editorial_families'].append(family)
    ledger['coverage_units'].append({'id':family['id'],'status':'complete-with-source-native-and-representative-gameplay-evidence',
        'native_message_IDs':list(IDS),'final_review':str(FINAL),'actual_proof':str(actual_path),'full_goal_complete':False})
    ledger.update(records_editorially_completed=1245,records_revised_and_integrated=925,retained_wordings_editorially_completed=320)
    ledger['reviewed_but_incomplete_COMMON_IDs']=[n for n in ledger['reviewed_but_incomplete_COMMON_IDs'] if n not in IDS]
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==38
    common_ids=[n for f in ledger['completed_editorial_families'] for n in f.get('native_message_IDs',[])]
    assert len(common_ids)==len(set(common_ids))==1244
    assert not set(common_ids).intersection(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert sum(len(f.get('records',[])) for f in ledger['completed_editorial_families'])==1245
    # Reconcile stale per-file summaries with unique exact completed IDs. Earlier
    # headline totals already included static20+escape13; their cached per-file
    # summary had not been advanced. The source summary also omitted these16 drafts.
    by_file={'/COMMON/MESFILE.DK4':len(set(common_ids)),'/data/SC2.DK4':1}
    source_by_file={'/COMMON/MESFILE.DK4':len(set(common_ids))+len(ledger['reviewed_but_incomplete_COMMON_IDs']),'/data/SC2.DK4':1}
    assert sum(by_file.values())==1245 and sum(source_by_file.values())==1283
    ledger['completed_editorial_record_counts_by_file']=by_file
    ledger['source_prose_reviewed_counts_by_file']=source_by_file
    counts_path=ROOT/'exact_coverage_reconciliation.json'
    save(counts_path,{'prior_per_file_completed_summary':old_counts,'prior_per_file_source_summary':old_source_counts,
        'completed_record_sums_before_after':[1229,1245],'unique_COMMON_IDs_before_after':[1228,1244],
        'corrected_completed_counts_by_file':by_file,'corrected_source_prose_counts_by_file':source_by_file,
        'completed_COMMON_IDs':sorted(set(common_ids)),'reviewed_incomplete_COMMON_IDs':ledger['reviewed_but_incomplete_COMMON_IDs'],
        'headlines_already_counted_prior33_and_no_duplicate_credit_awarded':True,
        'old_source_summary_omitted16_drafts_that_were_in_headline1283':True,
        'non_COMMON_completed_route_record':'Lil SC2 B294 R73','full_goal_complete':False})
    ledger['coverage_reconciliation_v1213']={'proof':str(counts_path),'per_file_summaries_recomputed_from_exact_unique_IDs':True}
    drafts=ledger['active_source_prose_drafts'];drafts['native_message_IDs']=[n for n in drafts['native_message_IDs'] if n not in IDS]
    drafts['manuscripts']=[p for p in drafts['manuscripts'] if 'duel_bark_editorial_manuscript' not in p]
    drafts['manuscript_record_subsets_pending']={p:[n for n in values if n not in IDS] for p,values in drafts['manuscript_record_subsets_pending'].items() if any(n not in IDS for n in values)}
    drafts.update(status='older3-context;successful-shot;15-sighting-remaining-UI',
        note='38 reviewed incomplete COMMON entries remain, additional to the broader unreviewed shared/routes/raw-source inventory and14 unreviewed special moves.')
    ledger['duel_bark_prose_v1200'].update(actual_gameplay_pending=False,completed_entries=16,final_review=str(FINAL),actual_proof=str(actual_path))
    ledger['previous_registered_formatting_candidate_before_V1206']=deepcopy(ledger['latest_registered_formatting_candidate'])
    ledger['latest_registered_formatting_candidate']={'path':str(path),'sha256':digest,'profile':release['profile'],
        'MESFILE_sha256':sha(common),'ARM9_sha256':sha(arm),'patch':release['patch'],'patch_sha256':release['patch_sha256'],
        'status':'experimental;16-timed-reactions-complete;inherited-remaining-checks-and-broader-goal-open',
        'release_verification':str(release_path),'original_reaction_verification':str(actual_path)}
    ledger['previous_native_relocation_reference_before_V1206']=deepcopy(ledger['current_native_relocation_reference'])
    ledger['current_native_relocation_reference']={'candidate':str(path),'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),
        'parser':'dk4tool.patch.duel_bark_editorial.current_entries','release_config':owned.CONFIG,
        'requires_guarded_single8192_cache_policy':True,'opaque1484byte_prefix_and_carrier1931_are_owned_and_hash_locked':True,
        'only16_reviewed_reactions_changed_from_V1189_and_all_other3652_texts_exact':True,'candidate_experimental_broader_goal_pending':True}
    checkpoint=('V1213 completes16 timed duel-action reactions:11 revisions,5 retained wordings. Counts1245 complete '
        '(925 revised,320 retained),1283 source/prose reviewed;38 reviewed COMMON entries remain incomplete plus '
        'the broader unreviewed shared/routes/raw-source inventory and14 special moves. Exact unique record IDs '
        'reconcile the stale per-file summaries:1244 COMMON+1 SC2 completed;1282 COMMON+1 SC2 source/prose reviewed. '
        'V1206 preserves all471 batches114 accepted layers and every unselected text/graphic/route/font.65615 '
        'dispatch,36 complete new/preserved native fonts,92 native copies18 sequences and13 escape-source '
        'regressions pass. Actual1958/1966 have four complete font/RGB holds;1973 has two preserved current '
        'holds. All31 pre-duel fixtures and the exact accepted A-input schedule pass;two invalid-duration '
        'intentions were rejected before any change. Natural combat reaches original loss/GameOver/title. '
        'Eight startup frames and photographed676/677 shop formatting pass; the clean-input patch reconstructs '
        'exactly. No section/BSS/cache/arena/ITCM or123040-byte staged growth. V1206 remains experimental; '
        'canonical and prior whole-batch scene-verified V997 unchanged. All18 plaques and separate graphics '
        'audit remain open. Full editorial goal active.')
    ledger['latest_checkpoint']=checkpoint;save(ledger_path,ledger)
    DOC.write_text('# V1213: timed duel reaction editorial completion\n\n'+checkpoint+'\n\n'+scope+
        '\n\nCombined ROM: `E:/Rota Nova translations/Generated/out/all_routes_combined_v1206_candidate.nds`'
        '\n\nProfile: `all-routes-unified-v1206`; canonical base `out/raphael_natural_v2_accepted_base.nds`, SHA256 `3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.'
        '\n\nROM SHA256: `'+digest+'`\n\nPatch SHA256: `'+release['patch_sha256']+'`'
        '\n\nOnly COMMON21, its native pointer metadata and the existing108-byte static formatter front change '
        'from V1189. Actual timed inputs confirm both positive and negative feedback; other14 voice alternatives '
        'are covered by source and native-font evidence. User testing and explicit acceptance are required '
        'before canonical promotion. User cold-boot targets are title/New Game, ordinary town/shop dialogue, '
        'and both duel timing reaction types. Broader route/scene/hardware coverage is not claimed.\n',encoding='utf8')
    for file in ('docs/translation_progress.md','docs/known_issues.md','docs/todo.md'):
        with Path(file).open('a',encoding='utf8') as stream:stream.write('\n\n## V1213: timed duel reactions verified\n\n'+checkpoint+'\n\nSee [V1213 evidence](duel_bark_v1213_editorial_completion.md).\n')
    pins_path=Path('translations/rom_retention_pins.json');pins=read(pins_path)
    pin='E:/Rota Nova translations/Generated/out/all_routes_combined_v1206_candidate.nds'
    assert not any(r['path']==pin for r in pins);pins.append({'path':pin,'reason':'Latest verified timed duel-reaction source; needed for remaining full editorial inventory and14 special moves.'});save(pins_path,pins)
    save(ROOT/'completion_checkpoint.json',{'candidate':str(path),'candidate_sha256':digest,'counts':[1245,925,320,1283],
        'final_review':str(FINAL),'documentation':str(DOC),'exact_per_file_reconciliation':str(counts_path),
        'full_goal_active_and_canonical_not_promoted':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    files=[Path(__file__),FINAL,DOC,manuscript_path,ledger_path,pins_path,Path(owned.CONFIG),Path('translations/release_stack.json'),
        Path('scripts/build_integrated_release.py'),Path('docs/translation_progress.md'),Path('docs/known_issues.md'),Path('docs/todo.md'),
        Path('dk4tool/patch/duel_bark_editorial.py'),path.with_suffix('.manifest.json'),path.with_suffix('.xdelta')]
    files += [p for p in Path('scripts').glob('*.py') if any(t in p.name for t in ('v1199','v1200','v1201','v1202','v1203','v1204','v1205','v1207','v1208','v1209','v1210','v1211','v1212','v1213'))]
    files += [Path('translations/duel_bark_editorial_manuscript_v1.json')]
    for folder in ('duel_bark_context_v1199','duel_bark_prose_v1200','duel_bark_native_v1201','duel_bark_native_v1202',
        'duel_bark_copies_v1203','duel_bark_escape_regression_v1203','duel_bark_native_review_v1204','duel_bark_release_v1205',
        'duel_bark_live_v1207','duel_bark_inputs_v1209','duel_bark_actual_v1210','duel_bark_terminal_v1211','duel_bark_completion_v1213'):
        files += [p for p in (Path('work/analysis')/folder).rglob('*') if p.is_file() and p.suffix not in ('.nds','.dsv')]
    ARCHIVE.mkdir(parents=True);archived=[]
    for source in dict.fromkeys(files):
        relative=source.absolute().relative_to(Path.cwd());dest=ARCHIVE/relative;dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();archived.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    external=[Path(r[key]) for r in actual['actual_new_reaction_holds'] for key in ('RAM','capture')]
    external += [CAP/f"frame_{r['frame']:06d}_arm9_ram.bin" for r in actual['actual_preserved_escape_holds']]
    external += [Path(r['capture']) for r in actual['actual_preserved_escape_holds']]
    external += [Path(actual['terminal_report']),CAP/'navigation_command_journal.json']
    for source in dict.fromkeys(external):
        relative=source.absolute().relative_to(Path('E:/Rota Nova translations').absolute());dest=ARCHIVE/'external_E'/relative
        dest.parent.mkdir(parents=True,exist_ok=True);copy2(source,dest)
        assert dest.read_bytes()==source.read_bytes();archived.append({'source':str(source),'path':str(dest),'sha256':sha(dest.read_bytes())})
    save(ARCHIVE/'archive_manifest.json',{'files':archived,'candidate_physical_E_path':pin,'candidate_sha256':digest,
        'all_copied_sources_proofs_and_selected_actual_RAM_images_byte_exact':True,'new_completed_entries':16,'full_goal_complete':False})
    print('16 reactions complete;1245 completed/1283 source-prose reviewed;38 reviewed COMMON entries remain.',flush=True)
    print('Archive:',ARCHIVE,'files:',len(archived),flush=True)


if __name__=='__main__':main()
