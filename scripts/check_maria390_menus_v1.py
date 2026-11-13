"""Check the eight complete source/current/target menu objects without speech encoding."""
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import runpy
import sys
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B152_B175_clean_20261109')


def main():
    docpath = ROOT/'formatting_v1/formatting_input.json'
    doc = load(docpath)
    out = ROOT/'menu_native_v1'
    assert not out.exists()
    groups = defaultdict(list)
    for row in doc['records']:
        if row['kind']=='typed-choice-label':
            groups[(row['block'],row['source_command_offset'])].append(row)
    assert len(groups)==8 and sum(map(len,groups.values()))==17
    out.mkdir()
    outputs=[]
    for (block, offset), rows in groups.items():
        count=len(rows)
        assert count in (2,3) and [r['source_index'] for r in rows]==list(range(count))
        assert all(r['file_path']==doc['file_path']=='/data/SC3.DK4' for r in rows)
        projected=deepcopy(doc)
        projected.update(records=rows, typed_choice_objects=count,
            complete_exchange_projection_source=str(docpath),complete_exchange_projection_source_sha256=digest(docpath),
            only_this_menu_object_checked_not_other_body_orstyle_records=True,new_credit=0)
        path=out/f'B{block}_C{offset}_input.json'
        save(path,projected)
        directory=out/f'B{block}_C{offset}'
        module='scripts.check_editorial_two_choice_explicit_route_v1' if count==2 else 'scripts.check_maria390_three_choice_v1'
        before=sys.argv[:]
        try:
            sys.argv=[module,'--manuscript',str(path),'--release',doc['runtime']['release_proof'],
                '--startup',doc['runtime']['startup_proof'],'--out',str(directory)]
            if count==2:sys.argv+=['--captain','3']
            runpy.run_module(module,run_name='__main__')
        finally:
            sys.argv=before
        proofpath=directory/'menu_provider_and_planes.json'
        proof=load(proofpath)
        assert proof['runtime']==doc['runtime'] and proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
        assert proof['native_provider_alignments']==6 and proof['bridged_modal_returns']==(18 if count==2 else 24)
        assert proof['complete_English_caption_style_planes']==4*count
        if count==2:
            target=proof['native_choice_object_hex']; sheets=[proof['review_sheet']]
            assert len(proof['compiler_negatives_rejected'])==7
        else:
            assert len(proof['menus'])==1
            target=proof['menus'][0]['target_object_hex'];sheets=proof['review_sheets']
            assert len(proof['compiler_negatives_rejected'][0]['rejected'])==8
        outputs.append(dict(block=block,source_command_offset=offset,current_command_offset=rows[0]['current_reference']['command_offset'],
            source_object_hex=rows[0]['source_choice_object_hex'],current_object_hex=rows[0]['current_choice_object_hex'],
            target_object_hex=target,record_ids=[r['id'] for r in rows],caption_count=count,
            proof=str(proofpath),proof_sha256=digest(proofpath),review_sheets=sheets))
    save(out/'group_verification.json',dict(runtime=doc['runtime'],objects=outputs,
        menus=8,captions=17,native_provider_alignments=48,bridged_modal_returns=150,
        current_andtarget_normal_highlight_planes=68,target_normal_highlight_planes=34,
        compiler_negatives=57,all_complete_caption_controls_indices_pixels_centering_bounds_andcanaries_pass=True,
        no_speech_encoder_used=True,direct_visual_review_pending=True,
        actual_controller_paths_stored_integration_andall_fifth_gates_pending=True,new_credit=0,actual_gameplay=False,
        evidence={str(p):digest(p) for p in [docpath,Path(__file__),Path('scripts/check_maria390_three_choice_v1.py')]}))
    print('PASS8 menus/17 captions/48 alignments/150 bridged returns/68 planes;direct review andactual controller pending.')


if __name__=='__main__':main()
