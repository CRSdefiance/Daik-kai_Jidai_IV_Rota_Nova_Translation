"""Bind every clean/current speech through original own-Maria dispatch and current catalogue."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_effective_v7729')
SOURCE=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
NAMES=Path('work/analysis/maria_story_names_macros_v7727/eight_static_speakers_sixteen_getters_clean_fields_actual_source_macros.json')
PRIOR=Path('work/analysis/maria_B207_consumers_v7682/all18_effective_Maria_bodies36_dispatches_four_getters_two_voices.json')
def expanded_Maria_body(body):
    selected=CATALOG_LOOKUP.get(body)
    target=selected['target'] if selected else body
    return target.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan'),None if selected is None else {k:v for k,v in selected.items() if k!='target'}
if __name__=='__main__':
    assert not ROOT.exists();source,names,prior=map(read,[SOURCE,NAMES,PRIOR])
    assert source['all67_clean_whole_context_glosses_precede_current_English_exposure'] and names['measured_current_macro_ascii_lengths']==dict(FI=5,FA=2,FO=7)
    assert sha(NAMES.read_bytes())==source['names_andmacros_packet_sha256']
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    image=NdsImage.open(source['current_ROM']);ns={**inherited.__dict__,'SOURCE':SOURCE,'route':3,'route_mask':8,'CATALOG_LOOKUP':{}}
    adapters=prior['source_owned_dispatch_adapters']
    for name,text in adapters.items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image)
    original=inspect.getsource(inherited.expanded_current_body)
    derived=checked_text(original,{"b'Lil'":"b'Maria'","b'Argot'":"b'Li'","b'Argot Co.'":"b'Li Clan'"})
    exec(compile(derived,__file__+'::measured-Maria-macros','exec'),ns)
    voices={r['source_selector']:r['original_voice_class'] for r in names['original_static_selector_and_voice_resolution']['rows']}
    cases=[];rows=[]
    for row in source['records']:
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(row[key]);result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            assert result['resolved_actor_ID']==row['source_selector'] and result['source_voice_class']==voices[raw[0]]
            cases.append(dict(id=row['id'],file_path=row['file_path'],version=label,**result))
            if label=='current-English':
                boundary=next(r for r in result['boundaries'] if r['kind']=='unexecuted-progressive-body')
                body=bytes.fromhex(boundary['text_hex']);selected=ns['CATALOG_LOOKUP'].get(raw[1:]);template=selected['target'] if selected else raw[1:]
                assert body==template.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
                rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=raw[0],
                    current_raw_storage_hex=raw[1:].hex(),effective_predecessor_template_hex=template.hex(),effective_predecessor_template=template.decode('cp932'),
                    effective_predecessor_paragraph=' '.join(template.decode('cp932').split()),current_actual_default_expanded_hex=body.hex(),
                    registered_catalogue_match=result['registered_catalog_match'],native_UI_body_unexecuted=True))
    assert len(cases)==134 and len(rows)==67 and not ctx.machines
    save(ROOT/'all67_effective_English_templates134_original_dispatches.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        native_names_packet=str(NAMES),native_names_packet_sha256=sha(NAMES.read_bytes()),registered_current_catalogue_binding=binding,
        source_current_dispatches=cases,effective_current_records=rows,source_owned_dispatch_adapters=adapters,source_owned_measured_macro_body_adapter=derived,
        all67_original_static_speakers_andvoices_match=True,all_original_dispatch_ABI_input_andunowned4MiB_guards_preserved=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        isolated_speech_dispatch_not_whole_VM_branch_setup_UI_oractual_gameplay=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('134 original dispatches/67 effective templates;catalogue matches',sum(r['registered_catalogue_match'] is not None for r in rows))
    for r in rows:
        if r['registered_catalogue_match'] is not None:print(r['id'],repr(r['effective_predecessor_paragraph']))
