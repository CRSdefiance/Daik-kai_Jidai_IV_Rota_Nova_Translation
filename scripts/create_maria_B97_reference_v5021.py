"""Verify all final stored macro alignments and make the exact B97-only research reference."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts.prove_maria_B109_macro_profile_v3507 import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as FE_expand
from scripts.maria_B97_reference_paths_v5021 import PARENT,ROM,PLAN,DOC,STORED
from scripts.verify_village_wrap_v608 import read,save
ROOT=STORED.parent
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();doc,plan=read(DOC),read(PLAN);font=read(doc['native_font_proof']);approval=read('work/analysis/maria_B97_actual_approval_v5018/all32_native_actual_approval_and_remaining_release_gates.json')
    prior=read('work/analysis/editorial_handoff_verification_v5020/verified_handoff.json')
    assert sha(PARENT.read_bytes())==prior['candidate_sha256']==doc['current_ROM_sha256']==plan['parent_sha256']
    assert approval['manuscript_sha256']==sha(DOC.read_bytes()) and plan['font_proof_sha256']==sha(Path(doc['native_font_proof']).read_bytes())
    parent=NdsImage.open(PARENT);path='/data/SC3.DK4';container=IlnkContainer.parse(parent.read_file(path));old=container.blocks[97];target=Path(plan['target_block']).read_bytes()
    assert sha(target)==plan['target_block_sha256'] and len(target)==2048 and len(old)==1904
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B97_voices_v5000/current_native_input.json',read(doc['source_context'])['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};fonts={r['id']:r for r in font['cases']};cases=[];fresh=0;reused=0
    for text in plan['text_records']:
        row=rows[text['id']];case=fonts[text['id']];stored=bytes.fromhex(text['stored_text_hex']);encoded=bytes.fromhex(row['compiled_hex']);body=stored[1:]
        assert stored==encoded+(b' ' if text['parity_space_added'] else b'') and target[text['new_text_offset']:text['new_text_offset']+len(stored)+1]==stored+b'\0'
        if stored==encoded:
            result=next(p for p in case['current_native_macro_pipelines'] if p['kind']=='compiled-protected');reused+=4;method='four exact-byte compiled cases reused'
        else:
            result=ctx.execute(FE_expand if row['kind']=='system-FE' else progressive_expand,body,*(() if row['kind']=='system-FE' else (stored[0],)));ctx.machines.pop();fresh+=4;method='four fresh final-parity cases'
        expected=body.replace(b'FI',b'Maria').replace(b'FA',b'Li').replace(b'FO',b'Li Clan')
        assert len(result['cases'])==4 and all(bytes.fromhex(c['output_hex'])==expected for c in result['cases'])
        assert all(c['original_macro_ABI_input_output_canaries_and4MiB_exact'] if row['kind']=='system-FE' else c['original_macro_ABI_input_output_canaries_and_all4MiB_exact'] for c in result['cases'])
        if row['source_record_index']==72:
            actual=read(doc['actual_proof'])['source72_page_boundary'];assert expected.split(b'\n')[4].hex()==actual['continuation_input_hex'] and actual['original_continuation_first_row_indent_px']==6
        cases.append(dict(id=row['id'],stored_text_hex=stored.hex(),compiled_text_hex=encoded.hex(),parity_space_added=text['parity_space_added'],method=method,macro_alignment_cases=result,final_native_font_plane_sha256=text['final_font_plane_sha256'],font_matrix_equal_reviewed_proof=plan['all32_final_stored_font_matrices_equal_viewed_previews']))
    assert len(cases)==32 and fresh+reused==128 and not ctx.machines
    container.blocks[97]=target;image=NdsImage.open(PARENT);targetfile=container.to_bytes();image.replace_file(path,targetfile);image.save(ROM);result=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if result.read_file(p)!=v]==[path] and all(result.read_file(p)==v for p,v in parent.iter_components())
    before,after=[IlnkContainer.parse(im.read_file(path)).blocks for im in [parent,result]]
    assert len(before)==len(after)==303 and [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[97] and after[33]==before[33]
    targetpath=ROOT/'target_SC3.DK4';targetpath.write_bytes(targetfile)
    save(STORED,dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_plan=str(PLAN),source_plan_sha256=sha(PLAN.read_bytes()),source_SC3_sha256=sha(parent.read_file(path)),target_SC3=str(targetpath),target_SC3_sha256=sha(targetfile),target_block_sha256=sha(target),source_block_sha256=sha(old),final_stored_cases=cases,stored_alignment_cases=128,fresh_parity_alignment_cases=fresh,exact_byte_reused_alignment_cases=reused,all32_final_macro_outputs_and_source_selectors_exact=True,source72_actual_page_tail_guard_and_terminal_space_exact=True,all302_other_SC3_blocks_every_other_file_component_and_original_B33_exact=True,no_current_graphic_font_ARM9_or123040_pool_change=True,not_registered_candidate_or_playable_handoff=True,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(final_stored_records=32,alignments=128,fresh=fresh,reused=reused,only_changed_block=97,original_B33_preserved=True,credit=0))
