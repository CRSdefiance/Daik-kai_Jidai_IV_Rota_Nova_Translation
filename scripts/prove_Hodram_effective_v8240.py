"""Bind28clean/current Hodram B137/B45/B46 speeches through original captain1dispatch;noFEobjects."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B137_B45_B46_effective_v8240')
SOURCE=Path('work/analysis/Hodram_B137_B45_B46_current_v8239/28_exact_clean_current_refs_after_whole_source_glosses.json')
NAMES=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')
PRIOR=Path('work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json')
if __name__=='__main__':
    assert not ROOT.exists();source,names,prior=map(read,[SOURCE,NAMES,PRIOR])
    assert source['clean_whole_exchanges_and27_prior_B44_source_callbacks_read_before_current_English']
    assert names['measured_default_macro_lengths']==dict(FI=6,FA=9,FO=15)
    assert names['candidate_sha256']==source['current_ROM_sha256'] and names['candidate']==source['current_ROM']
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(names['current_native_input'],'unused-no-historical-ROM',ROOT/'current_context')
    image=NdsImage.open(source['current_ROM']);ns={**inherited.__dict__,'SOURCE':SOURCE,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    adapters=prior['source_owned_dispatch_adapters']
    for name,text in adapters.items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],binding=ns['bind_current_catalog'](image)
    derived=checked_text(inspect.getsource(inherited.expanded_current_body),{
        "b'Lil'":"b'Hodram'","b'Argot'":"b'Bergstrom'","b'Argot Co.'":"b'Bergstrom Fleet'"})
    exec(compile(derived,__file__+'::measured-Hodram-macros','exec'),ns)
    voices={r['source_selector']:r['original_voice_class'] for r in names['native_static_selector_andvoice_resolution']['rows']}
    cases=[];rows=[]
    for row in source['records']:
        for label,key in [('clean-Japanese','source_hex'),('current-English','current_hex')]:
            raw=bytes.fromhex(row[key]);result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            is_FE=raw[0]==254
            assert result['resolved_actor_ID']==(None if is_FE else raw[0])
            assert result['source_voice_class']==(None if is_FE else voices[raw[0]])
            boundary=next(r for r in result['boundaries'] if r['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            if is_FE:
                assert len(result['FE_original_null_actor_calls'])==1
                assert result['FE_original_null_actor_calls'][0]['args'][2]==0
                assert bytes.fromhex(boundary['text_hex']).count(b'Bergstrom Fleet')==0
            cases.append(dict(id=row['id'],file_path=row['file_path'],version=label,**result))
            if label=='current-English':
                body=bytes.fromhex(boundary['text_hex']);selected=ns['CATALOG_LOOKUP'].get(raw[1:]);template=selected['target'] if selected else raw[1:]
                assert body==template.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
                rows.append(dict(id=row['id'],file_path=row['file_path'],block=row['block'],source_reference=row['source_reference'],current_reference=row['current_reference'],source_selector=raw[0],
                    current_raw_storage_hex=raw[1:].hex(),effective_predecessor_template_hex=template.hex(),effective_predecessor_template=template.decode('cp932'),
                    effective_predecessor_paragraph=' '.join(template.decode('cp932').split()),current_actual_default_expanded_hex=body.hex(),
                    registered_catalogue_match=result['registered_catalog_match'],native_UI_body_unexecuted=True,kind=row['kind']))
    assert len(cases)==56 and len(rows)==28 and not ctx.machines
    assert sum(r['source_selector']==254 for r in rows)==0
    save(ROOT/'all28_effective_English_templates56_original_dispatches_no_FE.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),
        native_names_packet=str(NAMES),native_names_packet_sha256=sha(NAMES.read_bytes()),registered_current_catalogue_binding=binding,
        source_current_dispatches=cases,effective_current_records=rows,source_owned_dispatch_adapters=adapters,source_owned_measured_macro_body_adapter=derived,
        all28_progressive_speakers_andvoices_match=True,no_FE_objects_no_FE_dispatch_or_display_coverage_claim=True,
        all_six_static_source_speakers_not_invented_from_incidental_r1=True,all28_actual_body_name_bounds_andpagination_pending=True,
        all_original_dispatch_ABI_input_andunowned4MiB_guards_preserved=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        isolated_speech_dispatch_not_whole_VM_branch_setup_UI_oractual_gameplay=True,
        ordinary_captain1_opening_context_no_unlock_orstate_fixture=True,
        new_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,PRIOR,Path(__file__)]},full_goal_complete=False))
    print('56 original dispatches/28 effective templates;catalogue matches',sum(r['registered_catalogue_match'] is not None for r in rows))
    for r in rows:print(r['id'],repr(r['effective_predecessor_paragraph']))
