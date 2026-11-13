"""Original Deck-consumer QA for source manuscripts outside the story audit format."""

import argparse
from pathlib import Path
from shutil import copy2

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch import physical_wounds_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.physical_wounds_layout_v968b import layout,compiled
from scripts.verify_village_wrap_v608 import read,save


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--batch',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    assert not args.out.exists();doc=read(args.batch);validate_natural_dialogue_batch(doc)
    assert doc['consumer_layout_profile']=='deck-physical-wounds-visible-v1'
    source=Path(doc['current_ROM']);assert sha(source.read_bytes())==doc['current_ROM_sha256']
    rom=NdsImage.open(source);common,arm=rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin')
    target_common,target_arm,plan=owned.plan(common,arm,doc)
    context_path=Path(doc['native_context_proof']);assert sha(context_path.read_bytes())==doc['native_context_proof_sha256']
    context=read(context_path);assert context['candidate_sha256']==sha(source.read_bytes())
    assert len(context['all150_original_direct_main_battle_and_ordinary_wound_selections'])==150
    assert len(context['all25_healthy_direct_helper_no_message_controls'])==25 and context['job_role_and_mood_getters_not_called'] and len(context['all25_condition1_prior_fatigue_discriminating_controls'])==25
    fonts_path=Path(doc['native_font_proof']);assert sha(fonts_path.read_bytes())==doc['native_font_proof_sha256']
    fonts=read(fonts_path);research=Path(doc['reviewed_research_manuscript'])
    assert sha(research.read_bytes())==doc['reviewed_research_manuscript_sha256']==fonts['manuscript_sha256']
    assert fonts['producer_sha256']==sha(Path('scripts/probe_physical_wounds_fonts_v968b.py').read_bytes())
    assert fonts['layout_producer_sha256']==sha(Path('scripts/physical_wounds_layout_v968b.py').read_bytes())
    visual_path=Path(doc['visual_review_proof']);assert sha(visual_path.read_bytes())==doc['visual_review_proof_sha256']
    visual=read(visual_path);assert visual['all13_previews_visually_reviewed'] and not visual['visual_review_pending']
    assert len(doc['records'])==len(fonts['cases'])==13
    preview=args.out/'previews';preview.mkdir(parents=True)
    results=[]
    for row,case in zip(doc['records'],fonts['cases'],strict=True):
        n=row['message_id'];lines=layout(row['english'])
        assert n==case['message_id'] and case['physical_condition_IDs']==[2,3]
        assert lines==case['generated_native_lines'] and ' '.join(lines)==row['english']
        assert len(lines)<=3 and max(map(len,lines))<=36
        assert case['all_body_ink_inside_registered216x36_crop'] and case['all_four_original_selectors_full_canvas_and_words_equal']
        for variant in case['condition2_3_ordinary_and_battle_font_controls']:
            assert compiled(row).hex()==variant['text_hex']
            for gate in ('complete_native_copy_macro_draw_and_ABI','full252x96_native_and_independent_canvas_equal',
                'bitmap_and_input_guards_exact','independent_authored_words_at_x0_12px_rows_match_every_pixel','original_physical_selector_selected_condition2_3_message'):
                assert variant[gate]
        path=Path(case['preview']);assert sha(path.read_bytes())==case['preview_sha256']
        target=preview/path.name;copy2(path,target);assert target.read_bytes()==path.read_bytes()
        results.append({'message_id':n,'source_Japanese':row['source_Japanese'],'source_hex':row['source_hex'],
            'source_reference':row['source_reference'],'current_reference':row['current_reference'],
            'source_meaning':row['source_meaning'],'english':row['english'],'localization_note':row['localization_note'],
            'visible_lines':lines,'visible_widths':list(map(len,lines)),'compiled_hex':compiled(row).hex(),
            'preview':str(target),'preview_sha256':sha(target.read_bytes()),'complete_native_words_and_bounds_pass':True,
            'actual_gameplay_credit_added':0})
    report={'format':'dk4-native-work-comment-audit-v1','batch':str(args.batch),'batch_sha256':sha(args.batch.read_bytes()),
        'source_ROM':str(source),'source_ROM_sha256':sha(source.read_bytes()),'source_context_proof':str(context_path),
        'native_font_proof':str(fonts_path),'records':results,'native_repack_plan':plan,
        'target_COMMON_sha256':sha(target_common),'target_ARM9_sha256':sha(target_arm),
        'blocking_errors':0,'unwaived_warnings':0,'all13_native_previews_visually_reviewed':True,
        'standard_story_audit_format_not_supported':True,'actual_gameplay_registered_release_and_patch_pending':True,
        'scope':'Original Deck CDeckCabinInfoView36x3 source/native-word/font/guard audit;not a story-parser preview or actual gameplay claim.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(args.out/'audit.json',report)
    text=['# Physical wound native-consumer audit','',report['scope'],'',
        '13 records;zero blocking errors and zero unwaived warnings. Registered copies/patch and actual gameplay remain pending.','']
    for r in results:
        text.extend([f"## COMMON {r['message_id']}",'',r['source_Japanese'].replace('\n',' '),'',r['english'],'',
            r['source_meaning'],'',r['localization_note'],'',*[f'- {line}' for line in r['visible_lines']],''])
    (args.out/'summary.md').write_text('\n'.join(text),encoding='utf-8')
    print('Native wound audit:all13 source/word/font/guard/bounds gates pass;registered release and actual scenes pending.',flush=True)


if __name__=='__main__':main()
