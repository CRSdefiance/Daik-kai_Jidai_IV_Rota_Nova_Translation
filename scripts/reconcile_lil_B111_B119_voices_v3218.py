"""Bind all six real dynamic selectors and every source static actor to current code."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.reconcile_lil_shrines_voices_v3167 import names
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B111_B119_voices_v3218')
SOURCE=Path('work/analysis/lil_B111_B119_source_v3217b/complete150_reachable_Lil_clean_current_context.json')

def dynamic(arm,common,raw,plan,selectors):
    cpu,get,provider=machine(arm,common,raw,plan)
    before=bytes(cpu.mem_read(0x02000000,0x400000));root=get(0xCB184);captain=get(0x7F244)
    controller=get(0xCB1A8)+0x2090;rows=[]
    for prefix in selectors:
        role=prefix-207
        strict=get(0x825E4,controller,role);selected=get(0x82478,controller,role);resolved=get(0x2434C,prefix)
        assert selected==resolved and 0<=resolved<207
        actor=root+0x19E4 if resolved==captain else root+4+32*resolved
        voice=get(0x7E988,actor);assert 0<=voice<8
        rows.append(dict(source_selector=prefix,role_index=role,strict_assignment=strict,
            original_speech_fallback_actor=selected,resolved_actor_ID=resolved,actor_object=actor,source_voice_class=voice))
    assert bytes(cpu.mem_read(0x02000000,0x400000))==before
    assert next(r for r in rows if r['source_selector']==207)['resolved_actor_ID']==captain==2
    return dict(rows=rows,all_actor_role_RNG_and_unowned4MiB_exact=True,
        current_executed_instruction_addresses=len(provider.executed_current),
        historical_London_context_not_selected_new_scene_participation=True)

if __name__=='__main__':
    assert not ROOT.exists()
    source=read(SOURCE);ROOT.mkdir(parents=True);image=NdsImage.open(source['current_ROM'])
    assert sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256']
    context=ROOT/'historical_source_context.json'
    save(context,dict(actual_snapshot=source['actual_historical_snapshot'],actual_snapshot_sha256=source['actual_historical_snapshot_sha256']))
    inputpath=ROOT/'current_native_input.json'
    save(inputpath,dict(current_ROM=source['current_ROM'],current_ROM_sha256=source['current_ROM_sha256'],
        current_ARM9_sha256=source['current_ARM9_sha256'],current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),
        native_context_proof=str(context)))
    ctx=CurrentContext(inputpath,source['historical_snapshot_ROM'],ROOT/'current_context')
    result=ctx.execute(names);ctx.machines.pop()
    rows=source['records']+source['typed_actor_style_records']
    selectors=sorted({r['source_selector'] for r in rows if 207<=r['source_selector']<224})
    assert selectors==[207,208,209,214,215,220]
    roles=ctx.execute(dynamic,selectors);ctx.machines.pop();assert not ctx.machines
    byid={r['actor_ID']:r for r in result['rows']}
    static=sorted({r['source_selector'] for r in source['records'] if r['source_selector']<207})
    assert len(result['rows'])==207 and {r['original_voice_class'] for r in result['rows']}==set(range(8))
    save(ROOT/'current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        catalog=result,dynamic_selectors=roles,
        eight_voice_groups={str(i):[dict(actor_ID=r['actor_ID'],current_name=r['current_catalog_name'])
            for r in result['rows'] if r['original_voice_class']==i] for i in range(8)},
        selected_static_source_selectors={str(i):byid[i] for i in static},
        all_six_dynamic_selectors_bind_actual_current_original_roles_without_assignment=True,
        virtual_source_prefix_must_match_each_actual_4100_header_not_assumed_D0=True,
        source_4100_style_comes_from_original_actor_record_byte1C=True,
        no_roster_role_event_RNG_or_outcome_fixture=True,original_name_ring_scratch_ownership_reused_not_runtime_repair=True,
        current_native_input=str(inputpath),current_native_input_sha256=sha(inputpath.read_bytes()),
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        canonical_Maria32_not_dispatched_under_Lil_company_context=True,
        no_new_nameplate_observation_or_name_asset_change=True,new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Current207catalog/eightvoices/sixCF-D0-D1-D6-D7-DCroles pass;allunownedstate exact.')
    print('STATIC',{i:byid[i]['current_catalog_name'] for i in static})
    print('DYNAMIC',roles['rows'])
