"""Recover only fully sealed blocks from a terminal native run; never replay their CPU work."""
import argparse
import importlib
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('run','manuscript','plan','producer','out'):p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    doc,plan=map(load,(a.manuscript,a.plan))
    assert plan['manuscript_sha256']==sha(a.manuscript.read_bytes()) and not plan['failures']
    assert not any(i['severity'] in ('warning','error') for r in plan['records'] for i in r['base_QA']['issues'])
    runtime=doc['runtime'];image=NdsImage.open(runtime['candidate'])
    assert sha(Path(runtime['candidate']).read_bytes())==runtime['candidate_sha256']
    assert sha(image.read_file('/__arm9__.bin'))==runtime['ARM9_sha256']
    assert sha(Path(runtime['snapshot']['path']).read_bytes())==runtime['snapshot']['sha256']
    module=importlib.import_module('.'.join(a.producer.with_suffix('').parts))
    code=module.source
    assert "save(args.out/f'B{block}_checked.json'" in code
    assert code.index("save(args.out/f'B{block}_checked.json'")>code.index('complete_native_English_display=rendered))')
    byid={r['id']:r for r in doc['records']};planned={r['id']:r for r in plan['records']}
    records=[];inputs={};blocks=[]
    for block in doc['blocks']:
        path=a.run/f'B{block}_checked.json'
        if not path.exists():continue
        value=load(path)
        expected={r['id'] for r in doc['records'] if r['block']==block and r['kind']!='typed-choice-label'}
        assert len(value['records'])==len(expected) and {r['id'] for r in value['records']}==expected
        for row in value['records']:
            source,target=byid[row['id']],planned[row['id']]
            assert row['block']==block and row['kind']==source['kind']
            assert row['source_reference']==source['source_reference'] and row['current_reference']==source['current_reference']
            assert row['compiled_hex']==target['encoded_hex'] and row['logical_English']==source['english']==target['logical_English']
            cases=row['native_alignment']['cases'];assert len(cases)==4
            key='original_macro_ABI_input_output_canaries_and4MiB_exact' if row['kind']=='system-FE' else 'original_macro_ABI_input_output_canaries_and_all_unowned4MiB_exact'
            assert all(c[key] and c['output_hex']==row['expanded_native_hex'] for c in cases)
            display=row['complete_native_English_display']
            if row['kind']=='system-FE':
                assert display['all_first_internal_final_ASCII_CP932_codes_andindependent_logical_plane_exact']
                assert display['planned_native_row_comparison']['complete_glyph_row_membership_exact']
                pages=[display]
            else:
                assert display['all_visible_first_internal_final_characters_in_order'] and display['no_blank_or_overlap_page']
                assert display['complete_consumed_bytes']==len(bytes.fromhex(row['expanded_native_hex']))
                pages=display['pages']
            assert len(pages)==target['expected_native_pages']
            for page in pages:
                assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                assert sha(Path(page['preview']).read_bytes())==page['preview_sha256']
            records.append(row)
        inputs[str(path)]=sha(path.read_bytes());blocks.append(block)
    assert records and len(records)==len({r['id'] for r in records})
    save(a.out,dict(manuscript=str(a.manuscript),manuscript_sha256=sha(a.manuscript.read_bytes()),plan=str(a.plan),plan_sha256=sha(a.plan.read_bytes()),
        runtime=runtime,font_sha256=sha(image.read_file('/GRP/KANJI.FNT')),records=records,
        pages=sum(planned[r['id']]['expected_native_pages'] for r in records),completed_blocks=blocks,
        original_run_terminal_exit_code=1,unsealed_partial_block_rows_not_recovered=True,
        completed_native_assertions_recovered_not_reexecuted=True,no_new_native_execution_orformatting_credit=True,
        direct_visual_review_pending=True,actual_gameplay=False,new_credit=0,
        producer=str(a.producer),producer_sha256=sha(a.producer.read_bytes()),executed_source_sha256=sha(code.encode()),
        completed_block_checkpoints=inputs,
        evidence={str(p):sha(p.read_bytes()) for p in (a.manuscript,a.plan,a.producer,Path(__file__))}))
    print(dict(recovered_records=len(records),completed_blocks=blocks,native_execution_repeated=False))


if __name__=='__main__':main()
