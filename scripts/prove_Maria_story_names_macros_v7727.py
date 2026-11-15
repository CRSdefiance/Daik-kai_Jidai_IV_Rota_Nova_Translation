"""Bind eight static story speakers, sixteen full getters and actual source macros."""
import inspect,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.reconcile_lil_B142_B145_voices_v3572 import selectors
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.audit_native_given_name_table import string
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_names_macros_v7727')
SOURCE=Path('work/analysis/maria_story_chain_gloss_v7726/all67_clean_whole_exchange_glosses_before_current_English.json')
INPUT=Path('work/analysis/current_V7717_native_v7720/route3/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();source=read(SOURCE);inp=read(INPUT)
    assert source['all67_glosses_precede_current_English_exposure'] and source['current_English_bodies_unread']
    chosen=sorted({r['source_selector'] for r in source['records']});assert chosen==[1,3,9,10,26,74,116,155]
    assert all(v<207 for v in chosen)
    current=NdsImage.open(inp['current_ROM']);clean=NdsImage.open(source['source_ROM'])
    assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']
    assert sha(Path(source['source_ROM']).read_bytes())==source['source_ROM_sha256']
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    text=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in SELECTED_ACTORS:',
        'actor = root+4+32*ident':'actor = root+0x19E4 if ident==3 else root+4+32*ident',
        'all_ten_original_consumers':'all_sixteen_original_consumers'})
    ns={**names.__globals__,'SELECTED_ACTORS':chosen};exec(compile(text,__file__+'::eight-actors-two-getters','exec'),ns)
    native=ctx.execute(ns['names']);ctx.machines.pop()
    voice_text=checked_text(inspect.getsource(selectors),{'assert captain==2':'assert captain==3'})
    ve=dict(selectors.__globals__);exec(compile(voice_text,__file__+'::Maria-static-selectors','exec'),ve)
    voices=ctx.execute(ve['selectors'],chosen);ctx.machines.pop()
    fields=[]
    for actor in chosen:
        versions=[]
        for label,image in [('clean-Japanese',clean),('current-English-names-only',current)]:
            arm=image.read_file('/__arm9__.bin');table=struct.unpack_from('<I',arm,0xCDAC0)[0]-0x02000000
            assert table==0x120B80
            columns=[]
            for col,kind in [(0,'given-name-or-role'),(4,'surname'),(8,'middle-name')]:
                at=table+32*actor+col;pointer=struct.unpack_from('<I',arm,at)[0]
                columns.append(dict(kind=kind,table_field=at,table_field_hex=arm[at:at+4].hex(),**string(arm,pointer)))
            versions.append(dict(version=label,ARM9_sha256=sha(arm),fields=columns))
        fields.append(dict(actor_ID=actor,versions=versions))
    defaults=[]
    for actor in chosen:
        result=ctx.execute(expand,b'FI FA FO',actor);ctx.machines.pop();defaults.append(result)
    actual=[]
    for row in source['records']:
        raw=bytes.fromhex(row['source_hex'])
        if not any(token in raw[1:] for token in [b'FI',b'FA',b'FO']):continue
        result=ctx.execute(expand,raw[1:],raw[0]);ctx.machines.pop()
        actual.append(dict(id=row['id'],file_path=row['file_path'],source_reference=row['source_reference'],source_hex=row['source_hex'],**result))
    assert not ctx.machines and len(native['rows'])==16 and len(voices['rows'])==8
    assert all(bytes.fromhex(c['output_hex'])==b'Maria Li Li Clan' for r in defaults for c in r['cases'])
    macro_counts={t.decode():sum(bytes.fromhex(r['source_hex'])[1:].count(t) for r in source['records']) for t in [b'FI',b'FA',b'FO']}
    save(ROOT/'eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json',dict(
        candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],source_gloss=str(SOURCE),source_gloss_sha256=sha(SOURCE.read_bytes()),
        current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),actual_original_captain_ID=3,
        exact_static_source_selectors=chosen,all_eight_selectors_below_dynamic_role_range=True,
        native_sixteen_progressive_and_full_name_consumers=native,original_static_selector_and_voice_resolution=voices,
        complete_clean_andcurrent_static_name_fields=fields,synthetic_defaults_not_added_to_source=defaults,
        actual_source_paragraph_macro_expansions=actual,source_macro_counts=macro_counts,measured_current_macro_ascii_lengths=dict(FI=5,FA=2,FO=7),
        source_owned_name_adapter=text,source_owned_voice_adapter=voice_text,source_owned_macro_adapter=inspect.getsource(expand),
        all_macro_four_alignment_canaries_and_unowned4MiB_preserved=True,
        current_English_dialogue_bodies_still_unread=True,current_name_assets_not_dialogue_exposure=True,
        macro_default_measurement_not_custom_player_name_coverage=True,native_getters_not_actual_scene_headers_orwhole_catalogue_UI=True,
        branch_setup_whole_VM_controls_native_fonts_actual_scenes_release_pending=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,new_emulator_runs=0,new_credit=0,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,INPUT,Path(__file__)]},full_goal_complete=False))
    print('SPEAKERS',[(r['actor_ID'],r['consumer'],r['text']) for r in native['rows']])
    print('SOURCE_MACROS',macro_counts,'paragraphs',len(actual),'alignments',4*(len(defaults)+len(actual)))
    print('Static selection/getters/source macros only;current English dialogue unread;zero credit.')
