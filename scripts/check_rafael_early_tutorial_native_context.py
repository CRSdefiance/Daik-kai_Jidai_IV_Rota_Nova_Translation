"""Qualify actual captain0 dispatch/default macros without changing native instructions."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.generic_name_macro_owned_v5886b import expand as original_progressive
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as original_FE

ROOT=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104')
SOURCE=Path('work/analysis/Rafael_early_tutorial_B42_B43_current_20261104/current_effective.json')
MANUSCRIPT=Path('translations/rafael_B42_B43_contextual_editorial_manuscript_v1.json')
PRECEDENT=Path('work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json')
RELEASE=Path('work/analysis/Hodram_B191_B210_release_verified_20261104/registered_release_verification.json')
STARTUP=Path('work/analysis/Rafael_early_tutorial_registered_context_20261104/registered_Rafael_context_v1.json')
NAMES={b'FI':b'Rafael',b'FA':b'Castor',b'FO':b'Castor Co.'}

def expanded(body):
    for key,value in NAMES.items():body=body.replace(key,value)
    return body

if __name__=='__main__':
    assert not ROOT.exists()
    current,doc,prior=map(load,[SOURCE,MANUSCRIPT,PRECEDENT]);assert current['records']==len(doc['records'])==40
    ctx=RegisteredRuntime(RELEASE,STARTUP,captain=0)
    assert current['runtime']==ctx.receipt() and doc['current_ROM_sha256']==ctx.receipt()['candidate_sha256']
    env={**inherited.__dict__,'SOURCE':SOURCE,'route':0,'route_mask':1,'CATALOG_LOOKUP':{}}
    adapters=prior['source_owned_dispatch_adapters']
    catalog=checked_text(adapters['bind_current_catalog'],{'12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b':sha(ctx.arm)})
    for key,text in adapters.items():exec(compile(catalog if key=='bind_current_catalog' else text,__file__+'::same-'+key,'exec'),env)
    body_adapter=checked_text(prior['source_owned_macro_body_adapter'],{"b'Hodram'":"b'Rafael'","b'Bergstrom'":"b'Castor'","b'Bergstrom Fleet'":"b'Castor Co.'"})
    exec(compile(body_adapter,__file__+'::measured-Rafael-defaults','exec'),env)
    env['CATALOG_LOOKUP'],catalog_proof=env['bind_current_catalog'](ctx.image)
    progressive_adapter=checked_text(prior['source_owned_progressive_adapter'],{'captain==1':'captain==0'})
    progressive_env=dict(original_progressive.__globals__);exec(compile(progressive_adapter,__file__+'::same-macro-ABI-captain0','exec'),progressive_env)
    fe_env=dict(original_FE.__globals__);exec(compile(prior['source_owned_FE_adapter'],__file__+'::same-null-actor-FE','exec'),fe_env)
    measure=ctx.execute(progressive_env['expand'],b'FI FA FO',0)
    assert len(measure['cases'])==4 and all(c['output_hex']==b'Rafael Castor Castor Co.'.hex() for c in measure['cases'])
    clean=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC0.DK4')).blocks
    stored=IlnkContainer.parse(ctx.image.read_file('/data/SC0.DK4')).blocks
    drafts={r['id']:r for r in doc['records']};rows=[];alignments=0
    ROOT.mkdir()
    for group in current['groups']:
        assert all(a['word']==b['word'] for a,b in zip(group['all_source_commands'],group['all_current_commands'],strict=True))
        for item in group['records']:
            row=drafts[item['id']];at=item['source_reference']['offset'];raw=bytes.fromhex(item['source_hex']);header=bytes.fromhex(item['source_complete_preamble_hex'])
            assert len(header)==6 and header.hex()=='0040ffff00'+format(item['source_selector'],'02x')
            assert clean[row['block']][at-5:at+len(raw)+1]==header[:5]+raw+b'\0'
            current_raw=bytes.fromhex(item['current_hex']);now=item['current_reference']['offset']
            assert stored[row['block']][now-5:now+len(current_raw)+1]==header[:5]+current_raw+b'\0'
            dispatch=ctx.execute(env['dispatch'],current_raw[0],current_raw[1:])
            assert dispatch['resolved_actor_ID']==(None if row['source_selector']==254 else row['source_selector'])
            logical=row['english']
            for key in NAMES:logical=logical.replace('{MACRO:'+key.decode()+'}',key.decode())
            body=logical.encode('ascii');expected=expanded(body);is_FE=row['source_selector']==254
            logical_proof=ctx.execute(fe_env['expand'] if is_FE else progressive_env['expand'],body,*(() if is_FE else (row['source_selector'],)))
            assert len(logical_proof['cases'])==4 and all(c['output_hex']==expected.hex() for c in logical_proof['cases'])
            alignments+=4
            rows.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
                complete_source_andcurrent_preamble_hex=header.hex(),selector_byte_consumed_as_command_state_not_text_NUL=True,
                original_current_dispatch=dispatch,logical_English=row['english'],expanded_logical_hex=expected.hex(),four_native_macro_alignments=logical_proof,
                current_Source4000_native_inventory_consumes_complete_command=True,
                original_UI_preparation_andmodal_painter_boundaries_bridged_not_actual_scene_coverage=True))
        save(ROOT/f'B{group["block"]}_native_context.json',dict(records=[r for r in rows if r['source_reference']['block']==group['block']],runtime=ctx.receipt(),new_credit=0))
        print('Rafael native source/current context block',group['block'],'pass',flush=True)
    assert len(rows)==40 and alignments==160
    zero=[r['id'] for r in doc['records'] if r['source_selector']==0];assert len(zero)==6
    save(ROOT/'40_native_selectors_macros_andcomplete_preamble_bindings.json',dict(runtime=ctx.receipt(),records=rows,
        current_registered_catalogue_binding=catalog_proof,default_macro_measurement=measure,
        measured_default_names={k.decode():v.decode() for k,v in NAMES.items()},macro_ascii_lengths={k.decode():len(v) for k,v in NAMES.items()},
        macro_widths={k.decode():6*len(v) for k,v in NAMES.items()},fresh_logical_macro_alignments=160,default_measurement_alignments=4,
        all40_exact_source_current_sixbyte_preambles_andoriginal_dispatches_pass=True,source_selector00_ids=zero,
        selector00_native_actor_is_current_Rafael_captain=True,FE_original_null_actor_path_separate=True,
        original_getter_scratch_rings_restored_andall_unowned4MiB_input_output_canaries_ABI_exact=True,
        no_native_instructions_font_viewport_orROM_changes=True,no_target_pages_orB42_B43_gameplay_coverage_claim=True,
        wrapped_macros_native_pages_visual_storage_andrepresentative_tutorial_gameplay_pending=True,
        source_owned_dispatch_adapters={**adapters,'bind_current_catalog':catalog},source_owned_macro_body_adapter=body_adapter,
        source_owned_progressive_adapter=progressive_adapter,source_owned_FE_adapter=prior['source_owned_FE_adapter'],
        new_credit=0,guide_photos=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,MANUSCRIPT,PRECEDENT,RELEASE,STARTUP,Path(__file__)]}))
    print('40 full preambles/dispatches and164 default/logical macro alignment cases pass;Rafael6/Castor6/CastorCo.10 measured.')
