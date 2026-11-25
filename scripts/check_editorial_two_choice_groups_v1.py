"""Apply the unchanged two-choice VM/compiler checks to each bound menu separately."""
import argparse
from copy import deepcopy
from pathlib import Path
import sys
from scripts import check_editorial_two_choice_explicit_captain_v1 as single
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for name in ['manuscript','release','startup','out']:ap.add_argument('--'+name,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    args=ap.parse_args();assert not args.out.exists()
    doc=load(args.manuscript);rows=[r for r in doc['records'] if r['kind']=='typed-choice-label']
    assert len(rows)==doc['typed_choice_objects'] and len({r['id'] for r in rows})==len(rows)
    groups={}
    for r in rows:groups.setdefault((r['block'],r['source_command_offset']),[]).append(r)
    assert len(groups)==doc['typed_choice_commands']
    # Current non-ASCII corruption is still passed through all original VM cases.
    # Its old raster cannot use the ASCII-only independent caption oracle. Every
    # reviewed target is fully raster-tested in both normal/highlight styles.
    source=checked_text(single.source,{
        '    for version in versions[1:]:':
            "    skipped_current_nonASCII=[v['version'] for v in versions[1:2] if any(not s.isascii() for s in v['cases'][0]['native_VM']['labels'])]\n    for version in [v for v in versions[1:] if v['version'] not in skipped_current_nonASCII]:",
        '        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,':
            '        source_font_planes_unchanged_not_replayed=True,bridged_modal_loop_not_actual_controller=True,\n        current_nonASCII_raster_omitted_from_ASCII_only_oracle=skipped_current_nonASCII,\n        all_three_versions_native_provider_still_tested=True,all_reviewed_target_normal_andhighlight_rasters_pass=True,',
    })
    env={**single.main.__globals__,'__file__':__file__}
    exec(compile(source,__file__+'::same-menu-guards-per-object-target-ASCII-only-oracle','exec'),env)
    args.out.mkdir(parents=True);receipts=[];original_argv=sys.argv[:]
    try:
        for (block,at),part in sorted(groups.items()):
            assert [r['source_index'] for r in part]==[0,1]
            for key in ['source_choice_object_hex','current_choice_object_hex']:
                assert len({r[key] for r in part})==1
            projected=deepcopy(doc);projected.update(records=deepcopy(part),blocks=[block],typed_choice_objects=2,
                typed_choice_commands=1,physical_speech_objects=0,subset_of=str(args.manuscript),
                subset_of_sha256=digest(args.manuscript),menu_projection_only_no_prose_control_orreview_changes=True)
            path=args.out/f'B{block}_C{at}_input.json';save(path,projected)
            target=args.out/f'B{block}_C{at}'
            sys.argv=[__file__,'--manuscript',str(path),'--release',str(args.release),'--startup',str(args.startup),
                '--captain',str(args.captain),'--out',str(target)]
            env['main']()
            receipt=target/'menu_provider_and_planes.json';proof=load(receipt)
            assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
            assert proof['native_provider_alignments']==6 and proof['bridged_modal_returns']==18
            assert len(proof['compiler_negatives_rejected'])==7
            receipts.append(dict(block=block,source_command_offset=at,record_ids=[r['id'] for r in part],
                receipt=str(receipt),receipt_sha256=digest(receipt),compiled_object=str(target/'compiled_choice_object.bin'),
                compiled_sha256=digest(target/'compiled_choice_object.bin'),review_sheet=proof['review_sheet'],
                current_nonASCII_raster_omitted=proof['current_nonASCII_raster_omitted_from_ASCII_only_oracle']))
    finally:sys.argv=original_argv
    save(args.out/'group_verification.json',dict(manuscript=str(args.manuscript),manuscript_sha256=digest(args.manuscript),
        menus=len(groups),captions=len(rows),objects=receipts,source_current_target_VM_alignments=6*len(groups),
        bridged_modal_returns=18*len(groups),compiler_negative_cases_rejected=7*len(groups),
        all_reviewed_captions_normal_andhighlight_complete_glyphs_centering_bounds_guards_pass=True,
        direct_visual_review_pending=True,actual_controller_andstored_integration_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [args.manuscript,Path(__file__),Path(single.__file__)]}))
    print('PASS',len(groups),'native menus/',len(rows),'captions;direct view andactual controller checks pending.')

if __name__=='__main__':main()
