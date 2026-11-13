"""Execute both original name getters for every actor on exact target and parent snapshots."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.generic_speaker_label_data_v1 import EXPECTED,TABLE
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_shrines_voices_v3167 import names as catalog_names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/generic_speaker_names_v5884')
MANIFEST=Path('work/analysis/generic_speaker_label_fixtures_v5882/two_complete_existing_exchanges_with_target_name_data.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    fixture=next(r for r in read(MANIFEST)['fixtures'] if r['case']=='tea')
    cap=Path(read('work/analysis/generic_speaker_label_run_v5883_tea/run_plan.json')['capture_folder'])
    rp=cap/'capture_report.json';report=read(rp)
    assert report['frames']==8001 and report['ROM_sha256']==fixture['research_ROM_sha256']
    assert read('work/analysis/generic_speaker_label_run_v5883_tea/terminal.json')['terminal']
    assert len(report['read_only_capture_RAM_snapshots'])==1
    snap=report['read_only_capture_RAM_snapshots'][0];assert snap['frame']==4000
    rom=Path(fixture['research_ROM']);image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin')
    conf=read('translations/shop657_full_width_reflow_release_v1.json')
    context=ROOT/'actual_tea_capture_context.json'
    save(context,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,
        snapshot_sha256=snap['sha256'],directory_sha256=conf['directory_sha256']))
    inp=ROOT/'target_native_input.json';save(inp,dict(current_ROM=str(rom),current_ROM_sha256=sha(rom.read_bytes()),
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context)))
    adapted=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in range(207):',
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all414_original_consumers_and_owned_or_readonly_memory_paths_exact'})
    env=dict(names.__globals__);exec(compile(adapted,__file__+'::all-actor-original-getters','exec'),env)
    cases=[]
    for case,path in [('parent','work/analysis/lil_B200_voices_v5827/current_native_input.json'),('target',inp)]:
        ctx=CurrentContext(path,'unused-no-historical-ROM-read',ROOT/(case+'_current_context'))
        result=ctx.execute(env['names']);ctx.machines.pop()
        catalog=ctx.execute(catalog_names);ctx.machines.pop();assert not ctx.machines
        assert len(result['rows'])==414 and len(catalog['rows'])==207
        assert {r['original_voice_class'] for r in catalog['rows']}==set(range(8))
        cases.append(dict(case=case,original_consumers=result,catalog=catalog,
            context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    before,after=cases;differences=[]
    for a,b in zip(before['original_consumers']['rows'],after['original_consumers']['rows'],strict=True):
        assert (a['actor_ID'],a['consumer'],a['getter'],a['ownership_mode'])==(b['actor_ID'],b['consumer'],b['getter'],b['ownership_mode'])
        if a['text']!=b['text']:
            ident=b['actor_ID'];assert ident in EXPECTED and a['text']==EXPECTED[ident][1] and b['text']==EXPECTED[ident][2]
            pointer=struct.unpack_from('<I',arm,TABLE+ident*32)[0]
            assert a['pointer']==b['pointer']==pointer and not b['original_getter_writes'] and not b['original_scratch_rings']
            differences.append(dict(actor_ID=ident,consumer=b['consumer'],previous=a['text'],target=b['text'],same_pointer=pointer))
    assert len(differences)==6
    catalog_changes=[]
    for a,b in zip(before['catalog']['rows'],after['catalog']['rows'],strict=True):
        assert a['actor_ID']==b['actor_ID'] and a['getter']==b['getter'] and a['original_voice_class']==b['original_voice_class']
        if a['current_catalog_name']!=b['current_catalog_name']:
            assert b['actor_ID'] in EXPECTED and b['current_catalog_name']==EXPECTED[b['actor_ID']][2]
            catalog_changes.append(b['actor_ID'])
    assert catalog_changes==[164,165,172]
    save(ROOT/'all207_progressive_catalogue_names_eight_voices_and_exact_three_changes.json',dict(
        native_versions=cases,changed_consumer_cases=differences,changed_catalog_actor_IDs=catalog_changes,
        all414_target_getters_and414_parent_getters_executed=True,all204_unaffected_actors_both_name_consumers_exact=True,
        all207_voice_classes_and_original_name_ownership_paths_exact=True,
        six_changed_getters_are_same_readonly_pointers_no_scratch_or_RAM_writes=True,
        approved_proper_names_and_original_progressive_aliases_unchanged=True,
        target_snapshot_actual_tea_fixture_frame4000_not_natural_event184_activation=True,
        parent_ARM9_exact_V5872=sha(NdsImage.open('out/all_routes_combined_v5872_candidate.nds').read_file('/__arm9__.bin'))==read('work/analysis/lil_B200_voices_v5827/current_native_input.json')['current_ARM9_sha256'],
        source_owned_adapter=adapted,evidence={str(p):sha(p.read_bytes()) for p in [MANIFEST,rp,context,inp,Path(__file__)]},
        new_emulator_runs=0,new_review_credit=0,no_registered_release_or_editorial_ledger_change=True,full_goal_complete=False))
    print('Both original consumers for207actors pass on parent and target;onlysix Man/Woman/Stranger results change. All204 other actors/eightvoiceclasses exact.')
