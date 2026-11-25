"""Bind82 stored bodies; render only40 changed parity tails; preserve all source controls."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B31_B53_registered_route_context_v8781 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as original_FE_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_stored_v8811')
RELOCATION=Path('work/analysis/Hodram_B54_B60_relocation_v8809/reconstruction.json')
INDEPENDENT=Path('work/analysis/Hodram_B54_B60_independent_v8810/independent_reconstruction.json')
NATIVE=Path('work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
CONTROL=Path('work/analysis/Hodram_B54_B60_source_controls_v8791/source_controls.json')
DISPLAY=Path('work/analysis/Hodram_B54_B60_source_display_v8794/82_complete_source_dispatches_alignments_pages_andmacro_binding.json')
NAMES=Path('work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json')
INPUT=Path('work/analysis/current_V8778_Hodram_native_v8781/current_native_input.json')

def verify_viewed_files(display):
    if isinstance(display.get('pages'),list):
        for page in display['pages']:
            for key in ['native_plane','preview']:assert sha(Path(page[key]).read_bytes())==page[key+'_sha256']
    else:
        assert display['pages']==1
        for key in ['native_physical_plane','native_logical_plane','preview']:assert sha(Path(display[key]).read_bytes())==display[key+'_sha256']

if __name__=='__main__':
    assert not ROOT.exists();relocation,independent,native,doc,control,display,names=map(read,[RELOCATION,INDEPENDENT,NATIVE,DOC,CONTROL,DISPLAY,NAMES])
    assert relocation['manuscript_sha256']==independent['manuscript_sha256']==sha(DOC.read_bytes())
    assert sha(NATIVE.read_bytes())==doc['native_body_pages_sha256'] and native['manuscript_sha256']==doc['predecessor_manuscript_sha256']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==relocation['candidate_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
    archive=Path(relocation['target_archive']).read_bytes();assert sha(archive)==relocation['target_archive_sha256']==independent['target_archive_sha256']
    bank=IlnkContainer.parse(archive).blocks;pixels,factory,oracle=bind(image);paint,calibration=factory(image)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};exec(compile(native['source_owned_target_page_adapter'],__file__+'::complete-native-pages','exec'),pe)
    prog=dict(progressive_expand.__globals__);exec(compile(native['source_owned_progressive_adapter'],__file__+'::progressive-macros','exec'),prog)
    fe=dict(original_FE_expand.__globals__);exec(compile(native['source_owned_FE_adapter'],__file__+'::null-actor-FE-macros','exec'),fe)
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for key,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    exec(compile(display['source_owned_macro_body_adapter'],__file__+'::captain1-body','exec'),ns)
    voices={r['source_selector']:r['original_voice_class'] for r in names['ten_source_selector_voices']['rows']}
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[];fresh=[];reused=[];queries=[];fresh_pages=0
    for group in relocation['groups']:
        number=group['block'];target=Path(group['target_block']).read_bytes();assert sha(target)==group['target_block_sha256'] and bank[number]==target
        source=next(g for g in control['groups'] if g['block']==number)
        for ref in group['text_records']:
            row=next(r for r in doc['records'] if r['id']==ref['id']);old=next(r for r in native['records'] if r['id']==ref['id'])
            compiled,stored=bytes.fromhex(ref['compiled_hex']),bytes.fromhex(ref['target_hex']);at=ref['new_offset'];is_FE=stored[0]==254
            assert compiled.hex()==row['compiled_hex']==old['compiled_hex'] and stored==compiled+(b' ' if ref['parity_space_added'] else b'')
            assert target[at:at+len(stored)+1]==stored+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
            assert target[:at].count(b'\0')==ref['new_record_index'] and stored[0]==row['source_selector']
            body=stored[1:];expected=body.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            previous=old['complete_native_English_display'];verify_viewed_files(previous)
            assert expected==bytes.fromhex(old['expanded_native_hex'])+(b' ' if ref['parity_space_added'] else b'')
            if stored==compiled:
                proof=dict(exact_reused_compiled_native_record=deepcopy(old),reused_native_packet=str(NATIVE),reused_native_packet_sha256=sha(NATIVE.read_bytes()))
                reused.append(row['id'])
            else:
                aligned=ctx.execute(fe['expand'] if is_FE else prog['expand'],body,*(() if is_FE else (stored[0],)));ctx.machines.pop()
                assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
                if is_FE:
                    rendered=paint(expected);assert sha(rendered.pop('physical'))==previous['native_physical_plane_sha256'] and sha(rendered.pop('logical'))==previous['native_logical_plane_sha256']
                    proof=dict(native_alignment=aligned,original_FE_painter=rendered,complete_consumed_bytes=len(expected),full_logical_andphysical_planes_exact_to_viewed=previous)
                    fresh_pages+=1
                else:
                    rendered=pe['pages'](arm,font,expected)
                    assert len(rendered['pages'])==len(previous['pages'])==row['expected_native_pages'] and rendered['complete_consumed_bytes']==len(expected)
                    for page,earlier in zip(rendered['pages'],previous['pages'],strict=True):
                        plane=bytes.fromhex(page.pop('native_plane_hex'));assert sha(plane)==earlier['native_plane_sha256']
                        assert page['first_visible_origin']==earlier['first_visible_origin']
                        assert [e for e in page['events'] if e['code']!=32]==[e for e in earlier['events'] if e['code']!=32]
                        page.update(viewed_native_plane=earlier['native_plane'],viewed_native_plane_sha256=sha(plane))
                    fresh_pages+=len(rendered['pages']);proof=dict(native_alignment=aligned,**rendered)
                fresh.append(row['id'])
            result=ctx.execute(ns['dispatch'],stored[0],body);ctx.machines.pop()
            assert result['resolved_actor_ID']==(None if is_FE else stored[0]) and result['source_voice_class']==(None if is_FE else voices[stored[0]])
            assert result['registered_catalog_match'] is None and bool(result['FE_original_null_actor_calls'])==is_FE
            if is_FE:assert result['FE_original_null_actor_calls'][0]['args'][2]==0
            boundary=next(b for b in result['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
            assert boundary['text_hex']==expected.hex()
            rows.append(dict(id=row['id'],file_path=row['file_path'],block=number,source_reference=row['source_reference'],current_reference=row['current_reference'],
                final_reference=dict(file_path='/data/SC1.DK4',block=number,offset=at,bytes=len(stored),header_offset=at-5,record_index=ref['new_record_index'],target_block_sha256=sha(target)),
                source_selector=stored[0],kind=row['kind'],compiled_hex=compiled.hex(),stored_hex=stored.hex(),expanded_stored_hex=expected.hex(),parity_space_added=ref['parity_space_added'],
                complete_native_stored_proof=proof,complete_native_ink_exact_to_directly_viewed_pages=True,original_dispatch=result))
        for command in group['all_target_commands']:
            if command['word']!=0x8000:continue
            result=ctx.execute(probe,target,command);ctx.machines.pop()
            mapped=next(r for r in group['command_map'] if r['new_offset']==command['offset'])
            previous=next(r for r in source['source_raw_query_cases'] if r['offset']==mapped['old_offset'])
            assert result['source_command_hex']==previous['source_command_hex'] and result['native_result']==previous['native_result'] and result['no_predicate_or_event_flag_forced']
            queries.append(dict(block=number,source_offset=mapped['old_offset'],**result))
        save(ROOT/f'B{number}_completed_stored_rows.json',dict(records=[r for r in rows if r['block']==number],new_credit=0,actual_gameplay=False))
        print('Complete stored block',number,'rows',len([r for r in rows if r['block']==number]),'fresh parity records',len(fresh),flush=True)
    assert len(rows)==82 and len(fresh)==40 and len(reused)==42 and len(queries)==6 and fresh_pages==43 and not ctx.machines
    assert set(fresh)==set(relocation['parity_space_records'])
    save(ROOT/'stored_pages_controls_andreferences.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),independent_reconstruction=str(INDEPENDENT),independent_reconstruction_sha256=sha(INDEPENDENT.read_bytes()),
        records=rows,fresh_parity_tail_records=fresh,exact_reused_compiled_records=reused,fresh_native_alignment_cases=160,exact_reused_alignment_cases=168,
        fresh_native_stored_pages=43,exact_reused_compiled_pages=42,total_bound_stored_pages=85,fresh_stored_dispatches=82,fresh_target_query_cases=queries,
        all82_complete_leading_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass=True,
        all82_native_stored_dispatches_preambles_static_actors_voices_FE_null_anddefault_macros_exact=True,
        twentyfour_relocated_relative_sites120cases_reused_from_exact_reconstruction=True,
        all152commands33nonprose_controls7full_normal_endwords_andseparate_source_tails_exact_in_reconstruction=True,
        seeded_normal_end_semantics_reused_only_for_exact_original_fourbytewords_andown_current_code=True,
        original_end_control_proof=str(CONTROL),original_end_control_proof_sha256=sha(CONTROL.read_bytes()),
        final_stored_offsets_NULrecordindices_andwhole_targetblocks_bound=True,compiler_parity_tails_create_no_blank_oradditional_page=True,
        target_font_oracle_binding=oracle,FE_factory_calibration=calibration,registered_catalogue_binding=catalogue,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_actual_native_effect_semantics_orwhole_script_activation_claim=True,loaders_externalreferences_actual_fullname_policy_atomic_andregistered_integration_pending=True,
        no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RELOCATION,INDEPENDENT,NATIVE,DOC,CONTROL,DISPLAY,NAMES,INPUT,Path(__file__)]}))
    print('Stored82 pass:40paritytails/43freshpages/160alignments,42exactbodies/pages reused,82dispatches/6unforcedqueries;all85viewed planes exact.No ROM/credit.',flush=True)
