"""Bind the actual stored bodies to complete reviewed pages and relocated controls."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts.Hodram_FE_font_oracles_v8315 import bind
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_stored_v8729')
RELOCATION=Path('work/analysis/Hodram_B31_B53_relocation_v8728/reconstruction.json')
NATIVE=Path('work/analysis/Hodram_B31_B53_pages_v8726/compiled_native_pages.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v2.json')
CONTROL=Path('work/analysis/Hodram_B31_B53_source_controls_v8718/source_controls.json')
DISPLAY=Path('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json')
INPUT=Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();relocation,native,doc,control,display=map(read,[RELOCATION,NATIVE,DOC,CONTROL,DISPLAY])
    assert relocation['manuscript_sha256']==sha(DOC.read_bytes()) and sha(NATIVE.read_bytes())==doc['native_body_pages_sha256']
    assert native['manuscript_sha256']==doc['predecessor_manuscript_sha256']
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==relocation['candidate_sha256']
    arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT');archive=Path(relocation['target_archive']).read_bytes();assert sha(archive)==relocation['target_archive_sha256']
    bank=IlnkContainer.parse(archive).blocks;pixels,unused_factory,oracle=bind(image)
    pe={**original_pages.__globals__,'expected_pixels':pixels,'codes':codes};exec(compile(native['source_owned_target_page_adapter'],__file__+'::exact-native-pages','exec'),pe)
    prog=dict(progressive_expand.__globals__);exec(compile(native['source_owned_progressive_adapter'],__file__+'::exact-progressive','exec'),prog)
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for key,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+key,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image);exec(compile(display['source_owned_macro_body_adapter'],__file__+'::exact-body','exec'),ns)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');rows=[];fresh=[];reused=[];queries=[]
    for group in relocation['groups']:
        number=group['block'];target=Path(group['target_block']).read_bytes();assert sha(target)==group['target_block_sha256'] and bank[number]==target
        source=next(g for g in control['groups'] if g['block']==number)
        for ref in group['text_records']:
            row=next(r for r in doc['records'] if r['id']==ref['id']);old=next(r for r in native['records'] if r['id']==ref['id'])
            compiled,stored=bytes.fromhex(ref['compiled_hex']),bytes.fromhex(ref['target_hex']);at=ref['new_offset']
            assert compiled.hex()==row['compiled_hex']==old['compiled_hex'] and stored==compiled+(b' ' if ref['parity_space_added'] else b'')
            assert target[at:at+len(stored)+1]==stored+b'\0' and target[at-5:at+1].hex()==row['source_complete_preamble_hex']
            assert target[:at].count(b'\0')==ref['new_record_index'] and stored[0]==row['source_selector'];body=stored[1:]
            if stored==compiled:
                assert body.hex()==old['expanded_native_hex']
                for page in old['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                rendered=deepcopy(old);reused.append(row['id'])
            else:
                aligned=ctx.execute(prog['expand'],body,row['source_selector']);ctx.machines.pop()
                assert len(aligned['cases'])==4 and all(c['output_hex']==body.hex() for c in aligned['cases'])
                rendered=pe['pages'](arm,font,body);assert len(rendered['pages'])==len(old['pages'])==1 and rendered['complete_consumed_bytes']==len(body)
                for page,previous in zip(rendered['pages'],old['pages'],strict=True):
                    plane=bytes.fromhex(page.pop('native_plane_hex'));assert sha(plane)==previous['native_plane_sha256']==sha(Path(previous['native_plane']).read_bytes())
                    page.update(viewed_native_plane=previous['native_plane'],viewed_native_plane_sha256=sha(plane))
                rendered['native_alignment']=aligned;fresh.append(row['id'])
            result=ctx.execute(ns['dispatch'],stored[0],body);ctx.machines.pop()
            assert result['resolved_actor_ID']==stored[0] and result['source_voice_class']=={34:1,113:0}[stored[0]] and result['registered_catalog_match'] is None and not result['FE_original_null_actor_calls']
            boundary=next(b for b in result['boundaries'] if b['kind']=='unexecuted-progressive-body');assert boundary['text_hex']==body.hex()
            rows.append(dict(id=row['id'],file_path=row['file_path'],block=number,source_reference=row['source_reference'],current_reference=row['current_reference'],
                final_reference=dict(file_path='/data/SC1.DK4',block=number,offset=at,bytes=len(stored),header_offset=at-5,record_index=ref['new_record_index'],target_block_sha256=sha(target)),
                source_selector=stored[0],compiled_hex=compiled.hex(),stored_hex=stored.hex(),parity_space_added=ref['parity_space_added'],complete_native_page=rendered,original_dispatch=result))
        for command in group['all_target_commands']:
            if command['word']==0x8000:
                result=ctx.execute(probe,target,command);ctx.machines.pop();previous=source['source_raw_query_cases'][0]
                assert result['source_command_hex']==previous['source_command_hex'] and result['native_result']==previous['native_result'] and result['no_predicate_or_event_flag_forced']
                queries.append(dict(block=number,**result))
    assert len(rows)==3 and len(fresh)+len(reused)==3 and len(queries)==1 and not ctx.machines
    save(ROOT/'stored_pages_controls_andreferences.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),relocation=str(RELOCATION),relocation_sha256=sha(RELOCATION.read_bytes()),
        records=rows,fresh_parity_tail_records=fresh,exact_reused_compiled_records=reused,fresh_native_alignment_cases=4*len(fresh),exact_reused_alignment_cases=4*len(reused),fresh_target_query_cases=queries,
        complete3stored_first_internal_final_glyphs_independent_planes_bounds_consumption_andpagination_pass=True,
        all3_native_stored_dispatches_preambles_static_actors_andvoices_exact=True,
        four_relocated_relative_sites20_cases_reused_from_exact_reconstruction=True,
        original_full_normal_endwords_eight_opaque_controls_andall_unowned_command_bytes_exact_in18commandmaps=True,
        seeded_normal_end_semantics_reused_only_for_exact_original_fourbytewords_andcurrent_code=True,
        final_stored_offsets_NULrecordindices_andwhole_targetblocks_bound=True,target_font_oracle_binding=oracle,registered_catalogue_binding=catalogue,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        independent_reconstruction_references_loaders_fullname_actual_policy_atomic_andregistered_integration_pending=True,
        no_actual_native_effect_semantics_orwhole_script_activation_claim=True,no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [RELOCATION,NATIVE,DOC,CONTROL,DISPLAY,INPUT,Path(__file__)]}))
    print('Stored3speechplanes/dispatches/finalrefs pass;freshparitytails',len(fresh),'exactreused',len(reused),'unforcedtargetquery',queries[0]['native_result'],flush=True)
    print('All previous geometry/font/guards andwhole-block inverses preserved. Actual/names/independent/policy/release remain pending.',flush=True)
