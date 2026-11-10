"""Expose four exact native menu cases to the existing single-object live pixel analyzer."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

SOURCE=Path('work/analysis/Rafael255_reconstruction_inputs_v1_20261105/menu.json')
OUT=Path('work/analysis/Rafael255_menu_actual_inputs_v1_20261105')

if __name__=='__main__':
    assert not OUT.exists();full=load(SOURCE);docpath=Path(full['manuscript']);doc=load(docpath)
    assert sha(docpath.read_bytes())==full['manuscript_sha256'] and full['offline_visual_approved']
    assert len(full['menus'])==4 and len(full['records'])==48
    OUT.mkdir();projections=[]
    for item in full['menus']:
        block,offset=item['block'],item['source_command_offset'];rows=[r for r in doc['records'] if r['id'] in item['record_IDs']]
        assert len(rows)==3 and [r['source_index'] for r in rows]==[0,1,2]
        planes=[r for r in full['records'] if r['block']==block and r['command_offset']==offset]
        assert len(planes)==12
        manuscript=OUT/f'B{block}_C{offset}_caption_view.json'
        save(manuscript,dict(format='dk4-typed-choice-exact-projection-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',
            records=rows,typed_choice_objects=3,blocks=[block],subset_of=str(docpath),subset_of_sha256=sha(docpath.read_bytes()),
            no_prose_control_index_orreview_changes=True,new_credit=0))
        proof=deepcopy(full);proof.update(manuscript=str(manuscript),manuscript_sha256=sha(manuscript.read_bytes()),menus=[item],
            versions=item['versions'],records=planes,native_provider_alignments=6,bridged_modal_returns=24,
            complete_English_caption_style_planes=12,source_native_proof=str(SOURCE),source_native_proof_sha256=sha(SOURCE.read_bytes()),
            exact_subcase_projection_not_new_native_execution=True)
        target=OUT/f'B{block}_C{offset}_native_menu_view.json';save(target,proof)
        projections.append(dict(block=block,source_command_offset=offset,proof=str(target),proof_sha256=sha(target.read_bytes())))
    save(OUT/'projections.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),menus=projections,
        native_body_bytes_planes_aliases_indices_andruntime_exact=True,new_credit=0))
    print('Projected four exact complete native menu cases;no new tests orapproval claimed.')
