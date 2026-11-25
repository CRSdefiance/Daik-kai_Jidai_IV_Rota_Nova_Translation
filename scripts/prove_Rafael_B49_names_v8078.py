"""Bind nine clean identities and18 current native getters before B49 English body comparison."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.audit_native_given_name_table import string
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_names_v8078')
GLOSS=Path('work/analysis/Rafael_B49_clean_gloss_v8075/61_first_clean_glosses_seven_source_identities_before_current_English.json')
SOURCE_NAMES=Path('work/analysis/Rafael_B49_clean_names_v8074/seven_clean_static_identity_fields_before_current_English.json')
INPUT=Path('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json')
START=Path('work/analysis/Rafael_B48_context_binding_v8069/own_Rafael_startup_andstrict_captain0_context.json')
if __name__=='__main__':
    assert not ROOT.exists()
    gloss,source_names,inp,start=map(read,[GLOSS,SOURCE_NAMES,INPUT,START])
    assert gloss['current_English_never_exposed_for_this_batch'] and all(r['current_English_body_unread'] for r in gloss['records'])
    chosen=sorted({r['source_selector'] for r in gloss['records'] if r['source_selector']!=254})
    assert chosen==[0,2,4,5,6,8,9]
    excluded=[r['id'] for r in gloss['records'] if r['source_selector']==254];assert len(excluded)==0
    current=NdsImage.open(inp['current_ROM']);assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    name_adapter=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in SELECTED_ACTORS:',
        'actor = root+4+32*ident':'actor = root+0x19E4 if ident==0 else root+4+32*ident',
        'all_ten_original_consumers':'all_fourteen_original_consumers'})
    env={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(name_adapter,__file__+'::seven-static-speakers','exec'),env)
    native=ctx.execute(env['names']);ctx.machines.pop()
    voice_adapter=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert captain==0'})
    env=dict(selectors.__globals__);exec(compile(voice_adapter,__file__+'::captain0-voices','exec'),env)
    voices=ctx.execute(env['selectors'],chosen);ctx.machines.pop()
    assert len(native['rows'])==14 and {r['actor_ID'] for r in native['rows']}==set(chosen)
    fields=[]
    arm=current.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000;assert table==0x120B80
    for ident in chosen:
        values=[]
        for col,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
            at=table+32*ident+col
            values.append(dict(kind=kind,table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,struct.unpack_from('<I',arm,at)[0])))
        clean=next(r for r in source_names['records'] if r['source_actor_ID']==ident)
        getters=[r for r in native['rows'] if r['actor_ID']==ident]
        assert {r['consumer'] for r in getters}=={'progressive-nameplate','full-catalogue'}
        fields.append(dict(actor_ID=ident,clean_fields=clean['fields'],current_fields=values,original_getters=getters))
    macro_adapter=checked_text(inspect.getsource(expand),{
        'captain==3':'captain==0',"b'Maria'":"b'Rafael'","b'Li'":"b'Castor'","b'Li Clan'":"b'Castor Co.'"})
    env=dict(expand.__globals__);exec(compile(macro_adapter,__file__+'::measured-own-Rafael-defaults','exec'),env)
    defaults=[]
    for ident in chosen:
        result=ctx.execute(env['expand'],b'FI FA FO',ident);ctx.machines.pop();defaults.append(result)
        assert all(bytes.fromhex(c['output_hex'])==b'Rafael Castor Castor Co.' for c in result['cases'])
    assert not ctx.machines and start['actual_original_captain_ID']==0 and start['all_whole_RGB_actor_andcaptain_controls_equal']
    save(ROOT/'seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        source_name_packet=str(SOURCE_NAMES),source_name_packet_sha256=sha(SOURCE_NAMES.read_bytes()),
        selected_source_static_actors=chosen,native_fourteen_progressive_andfull_getters=native,
        native_static_selector_andvoice_resolution=voices,complete_clean_andcurrent_name_fields=fields,
        measured_default_macro_lengths=dict(FI=6,FA=6,FO=10),synthetic_defaults_all_seven_actors=defaults,
        all28_default_macro_alignments_with4MiB_ABI_actor_roles_RNG_andinput_guards=True,
        source_two_FI_R311_R388_other_default_probes_synthetic_not_new_source_macros=True,
        no_source_FE_objects_no_FE_consumer_assumed=True,
        source_actors_remain_executable_speaker_state_not_prose=True,
        current_English_B49_bodies_still_unread=True,
        native_complete_nameplanes_actual_headers_full_catalogue_UI_andeditorial_naming_decisions_pending=True,
        source_owned_name_adapter=name_adapter,source_owned_voice_adapter=voice_adapter,
        source_owned_macro_adapter=macro_adapter,current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(Path(p).read_bytes()) for p in [GLOSS,SOURCE_NAMES,INPUT,START,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Native names/voices/defaults pass;English B49 bodies remain unread.')
    for r in fields:print(r['actor_ID'],[f.get('text') for f in r['current_fields']],[(n['consumer'],n['text']) for n in r['original_getters']])
