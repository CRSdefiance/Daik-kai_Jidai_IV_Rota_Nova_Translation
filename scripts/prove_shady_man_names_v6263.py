"""Exact parent/target snapshots:all name getters,621 fields,eight voices and sole changed primary."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v6097 import CurrentContext as ParentContext
from scripts.current_build_native_context_v6261 import CurrentContext as TargetContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_shrines_voices_v3167 import names as catalog_names
from scripts.seal_generic_speaker_labels_v5887 import fields
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_names_v6263');FIX=Path('work/analysis/shady_man_source_fixture_v6260/complete_B206_source_B22_fixture.json')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    run=Path('work/analysis/shady_man_source_run_v6262_buy');terminal=read(run/'terminal.json');assert terminal['terminal'] and terminal['observer_host_slots_restored']
    cap=Path(read(run/'run_plan.json')['capture_folder']);rp=cap/'capture_report.json';report=read(rp);fixture=read(FIX)['fixtures'][0]
    assert report['frames']==16001 and report['ROM_sha256']==fixture['research_ROM_sha256']
    assert len(report['read_only_capture_RAM_snapshots'])==1;snap=report['read_only_capture_RAM_snapshots'][0];assert snap['frame']==4000
    image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin');conf=read('translations/shop657_full_width_reflow_release_v1.json')
    context=ROOT/'actual_source_capture_context.json';save(context,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256=conf['directory_sha256']))
    inp=ROOT/'target_native_input.json';save(inp,dict(current_ROM=fixture['research_ROM'],current_ROM_sha256=fixture['research_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context)))
    adapted=checked_text(inspect.getsource(names),{
      'for ident in [2,4,13,23,109]:':'for ident in range(207):',
      "            print(dict(actor=ident,consumer=kind,text=value,rings=len(rings),writes=len(writes)),flush=True)":"            assert value",
      'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all414_original_consumers_and_owned_or_readonly_memory_paths_exact',
    });env=dict(names.__globals__);exec(compile(adapted,__file__+'::all207','exec'),env);versions=[]
    for case,path,Context in [('parent','work/analysis/current_V6220_native_v6228/current_native_input.json',ParentContext),('target',inp,TargetContext)]:
        ctx=Context(path,'unused-no-historical-ROM',ROOT/(case+'_current_context'));values={}
        for label,fn in [('original_consumers',env['names']),('catalog',catalog_names),('fields',fields)]:
            values[label]=ctx.execute(fn);ctx.machines.pop();assert not ctx.machines
        assert len(values['original_consumers']['rows'])==414 and len(values['catalog']['rows'])==207 and len(values['fields']['rows'])==621
        assert {r['original_voice_class'] for r in values['catalog']['rows']}==set(range(8))
        versions.append(dict(case=case,**values,context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    before,after=versions;diff=[];fd=[];cd=[]
    for a,b in zip(before['original_consumers']['rows'],after['original_consumers']['rows'],strict=True):
        assert all(a[k]==b[k] for k in ['actor_ID','consumer','getter','ownership_mode'])
        if a['text']!=b['text']:
            assert a['actor_ID']==173 and a['text']=='Suspicious Person' and b['text']=='Shady Man' and a['pointer']==b['pointer']
            assert not b['original_getter_writes'] and not b['original_scratch_rings'];diff.append(dict(actor_ID=173,consumer=b['consumer'],before=a['text'],after=b['text'],same_pointer=b['pointer']))
    for a,b in zip(before['catalog']['rows'],after['catalog']['rows'],strict=True):
        assert all(a[k]==b[k] for k in ['actor_ID','getter','original_voice_class'])
        if a['current_catalog_name']!=b['current_catalog_name']:assert b['actor_ID']==173 and b['current_catalog_name']=='Shady Man';cd.append(173)
    for a,b in zip(before['fields']['rows'],after['fields']['rows'],strict=True):
        assert all(a[k]==b[k] for k in ['actor_ID','column','getter','pointer'])
        if a['text_hex']!=b['text_hex']:
            assert b['actor_ID']==173 and b['column']==0 and bytes.fromhex(a['text_hex'])==b'Suspicious Person' and bytes.fromhex(b['text_hex'])==b'Shady Man';fd.append(dict(before=a,after=b))
    assert len(diff)==2 and cd==[173] and len(fd)==1
    oracle=derive('scripts/lil_current_font_oracles_v6122.py','scripts/shady_man_font_oracles_v6263.py',{'03a905a9e4a4df117b8a4b5280ec3c669a4db00547972397413bc8bebc4afbbd':sha(arm)})
    save(ROOT/'all207_distinct_names621_fields_eight_voices_and_one_changed_primary.json',dict(native_versions=versions,changed_consumer_cases=diff,changed_catalog_actor_IDs=cd,changed_field_consumers=fd,all414_parent_and414_target_name_consumers_pass=True,all621_parent_and621_target_fields_pass=True,all206_unaffected_actors_both_name_consumers_exact=True,all207_voice_classes_and_original_name_ownership_paths_exact=True,only_actor173_primary_changes_secondary_middle_and_all_pointers_exact=True,approved_names_Lil_Cristina_Man_Woman_Stranger_and_every_other_name_exact=True,source_owned_adapter=adapted,current_font_oracle_derivation=oracle,actual_source_fixture4000_snapshot_not_natural_event206=True,evidence={str(p):sha(p.read_bytes()) for p in [FIX,rp,context,inp,Path(__file__),Path('scripts/current_build_native_context_v6097.py'),Path('scripts/current_build_native_context_v6261.py')]},new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('828 distinct name calls,1242 field calls and414 catalog/voice calls pass;only173 primary label changes. All206 other actors and621 pointers exact.')
