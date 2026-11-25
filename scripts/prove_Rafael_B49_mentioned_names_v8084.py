"""Bind three spoken name components to clean identities and six original getters."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_native_given_name_table import string
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_mentioned_names_v8084')
SOURCE=Path('work/analysis/Rafael_next_clean_v8073/complete_clean_SC0_B49_EV0_andcoverage_before_current_English.json')
INPUT=Path('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json')
PRECEDENT=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
if __name__=='__main__':
    assert not ROOT.exists();source,inp,prior=map(read,[SOURCE,INPUT,PRECEDENT]);clean=NdsImage.open(source['source_ROM']);current=NdsImage.open(inp['current_ROM'])
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256'] and sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    clean_arm,arm=clean.read_file('/__arm9__.bin'),current.read_file('/__arm9__.bin');chosen=[1,28,29];rows=[]
    for actor in chosen:
        versions=[]
        for version,binary in [('clean-Japanese',clean_arm),('current-English-name-fields',arm)]:
            table=struct.unpack_from('<I',binary,0xCDAC0)[0]-0x02000000;assert table==0x120B80
            fields=[]
            for col,kind in [(0,'given'),(4,'surname'),(8,'middle')]:
                at=table+32*actor+col;fields.append(dict(kind=kind,table_field=at,table_field_hex=binary[at:at+4].hex(),**string(binary,struct.unpack_from('<I',binary,at)[0])))
            versions.append(dict(version=version,fields=fields))
        rows.append(dict(actor_ID=actor,versions=versions))
    assert [[f.get('text') for f in r['versions'][0]['fields']] for r in rows]==[['ホドラム','ベルグストロン','ヨアキム'],['ジェームズ','クリフォード',None],['マルティン','シュパイヤー',None]]
    adapter=checked_text(prior['source_owned_name_adapter'],{'all_fourteen_original_consumers':'all_six_original_consumers'})
    env={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(adapter,__file__+'::three-mentioned-identities','exec'),env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop()
    assert len(native['rows'])==6 and {r['actor_ID'] for r in native['rows']}==set(chosen) and not ctx.machines
    for r in rows:r['native_getters']=[n for n in native['rows'] if n['actor_ID']==r['actor_ID']]
    assert next(f.get('text') for f in rows[0]['versions'][1]['fields'] if f['kind']=='given')=='Hodram'
    assert next(f.get('text') for f in rows[0]['versions'][1]['fields'] if f['kind']=='middle')=='Joakim'
    save(ROOT/'three_clean_mentioned_identities_six_native_getters_component_only_review.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],records=rows,
        scoped_body_components=[dict(source_record_index=142,source_component='ホドラム・ベル…なんとか',actor_ID=1,
            rule='Retain approved Hodram and the deliberately unfinished surname joke. Do not fill in a complete surname or add an uncle relationship, naval rank or biography.'),
            dict(source_record_index=158,source_component='クリフォード',actor_ID=28,rule='Review the spoken surname component only; do not insert James merely because the full getter supplies it.'),
            dict(source_record_index=175,source_component='マルティン・シュパイヤー',actor_ID=29,rule='Retain a source-compatible current name after comparison; the source identifies the Hanseatic League, without an invented personal title.')],
        source_owned_name_adapter=adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        body_component_identity_binding_not_actual_headers_full_catalogue_UI_all207_orfull_biography_approval=True,
        current_B49_English_dialogue_bodies_still_unread=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,PRECEDENT,Path(__file__)]}))
    print('Three mentioned identities/six native getters bound;Hodram/Joakim preserved. Truncated surname joke remains incomplete;B49English dialogue still unread.')
