"""Fresh Lil current getters/voices/default lengths before the proposed six-consumer correction."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.audit_native_given_name_table import string
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_before_names_v8200')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
INPUT=Path('work/analysis/current_V8172_Lil_native_v8198/current_native_input.json')
CLEAN_NAMES=Path('work/analysis/Hodram_B137_B45_B46_clean_names_v8182/six_clean_static_identity_fields_before_current_English.json')
if __name__=='__main__':
    assert not ROOT.exists();current,inp,clean_names=map(read,[CURRENT,INPUT,CLEAN_NAMES]);assert inp['current_ROM_sha256']==current['current_ROM_sha256']
    chosen=[1,2,9,16];source_actors=sorted({r['source_selector'] for r in current['records']});assert source_actors==[1,9,16]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    name_adapter=checked_text(inspect.getsource(names),{'for ident in [2,4,13,23,109]:':'for ident in SELECTED_ACTORS:',
        'actor = root+4+32*ident':'actor = root+0x19E4 if ident==2 else root+4+32*ident','all_ten_original_consumers':'all_eight_original_consumers'})
    env={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(name_adapter,__file__+'::four-getter-identities','exec'),env)
    native=ctx.execute(env['names']);ctx.machines.pop();voices=ctx.execute(selectors,source_actors);ctx.machines.pop()
    macro_adapter=checked_text(inspect.getsource(expand),{'captain==3':'captain==2',"b'Maria'":"b'Lil'","b'Li'":"b'Argot'","b'Li Clan'":"b'Argot Co.'"})
    menv=dict(expand.__globals__);exec(compile(macro_adapter,__file__+'::Lil-current-defaults','exec'),menv)
    defaults=[]
    for actor in chosen:
        result=ctx.execute(menv['expand'],b'FI FA FO',actor);ctx.machines.pop();defaults.append(result)
        assert all(bytes.fromhex(c['output_hex'])==b'Lil Argot Argot Co.' for c in result['cases'])
    image=NdsImage.open(inp['current_ROM']);arm=image.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000;assert table==0x120B80
    fields=[]
    for actor in chosen:
        values=[]
        for col,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
            at=table+32*actor+col;values.append(dict(kind=kind,table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,struct.unpack_from('<I',arm,at)[0])))
        fields.append(dict(actor_ID=actor,current_fields=values,clean_fields=next(n['fields'] for n in clean_names['records'] if n['source_actor_ID']==actor),original_getters=[r for r in native['rows'] if r['actor_ID']==actor]))
    assert len(native['rows'])==8 and len(voices['rows'])==3 and not ctx.machines
    save(ROOT/'four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        selected_source_static_actors=source_actors,additional_player_identity_for_FI=2,native_eight_progressive_andfull_getters=native,
        native_static_selector_andvoice_resolution=voices,complete_clean_andcurrent_name_fields=fields,
        measured_default_macro_lengths=dict(FI=3,FA=5,FO=9),synthetic_defaults_all_four_actors=defaults,synthetic_alignment_cases=16,
        source_macro_counts=dict(FI=1,FA=0,FO=0),all_synthetic_default_checks_not_extra_source_macros=True,
        source_owned_name_adapter=name_adapter,source_owned_macro_adapter=macro_adapter,
        proposed_target_Gerhard_Adernkatz_not_yet_in_current_ROM=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        current_Hodram_B137_B45_B46_dialogue_bodies_not_consulted=True,no_new_credit_orROM_registry_changes=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,INPUT,CLEAN_NAMES,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('CurrentLil:8namegetters/3sourcevoices/16synthetic alignments;FI3/FA5/FO9.Allguards pass.GerhardtargetAdernkatz notyet applied.')
