"""Prepare fresh complete native font/macro proofs for all 150 paragraphs."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B111_B119_font_tools_v3230')
PROGRESSIVE_OLD=Path('scripts/verify_lil_shrines_fonts_v3179.py')
PROGRESSIVE_NEW=Path('scripts/verify_lil_B111_B119_fonts_v3230b.py')
FE_OLD=Path('scripts/verify_lil_shrines_FE_v3180.py')
FE_NEW=Path('scripts/verify_lil_B111_B119_FE_v3231.py')
VOICES=Path('work/analysis/lil_B111_B119_voices_v3218/current207_catalog_eight_voices_and_CF_D0_D1_D6_D7_DC_roles.json')
def replace_all(text,changes):
    for old in changes:assert old in text,old
    return re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,PROGRESSIVE_NEW,FE_NEW])
    roles=read(VOICES)['dynamic_selectors']['rows']
    mapping={r['source_selector']:r['resolved_actor_ID'] for r in roles}
    assert set(mapping)=={207,208,209,214,215,220}
    text=replace_all(PROGRESSIVE_OLD.read_text(encoding='utf-8'),{
        'lil_Shrines_Temples_fonts_v3179':'lil_B111_B119_fonts_v3230b',
        'lil_shrines_temples_editorial_manuscript_v3.json':'lil_B111_B119_editorial_manuscript_v3.json',
        'lil_shrines_temples_actor_style_manuscript_v2.json':'lil_B111_B119_actor_style_manuscript_v2.json',
        'lil_shrines_temples_profile':'lil_B111_B119_profile',
        'lil_shrines_temples_layout_v1':'lil_B111_B119_layout_v1',
        '({207:2,208:151}.get(prefix,prefix))':'('+repr(mapping)+'.get(prefix,prefix))',
        "row['source_hex']='d0'+row['source_hex'];row['source_presentation_prefix_hex']='d0'":
        "row['source_hex']=row['virtual_formatter_prefix_hex']+row['source_hex'];row['source_presentation_prefix_hex']=row['virtual_formatter_prefix_hex']",
        "'D0 styles'+str(row['style_indices'])":"'selector'+row['source_presentation_prefix_hex']+' styles'+str(row['style_indices'])",
        'len(cases)==190 and len(qa_reports)==220 and macro_calls==1520':'len(cases)==149 and len(qa_reports)==150 and macro_calls==1192',
        'blocks[101]':'blocks[111]','blocks[100]':'blocks[110]',
        'selectors=[2,9,16,20,139,151,160,177,178,191,207,208]':
        'selectors=[2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220]',
        'len(negatives)==31':'len(negatives)==43',
        'all56_virtual_D0_prefixes_excluded_from_physical_alternative_body':'all34_actual_virtual_prefixes_excluded_from_physical_alternative_body',
        'all220_full_QA_reports':'all150_full_QA_reports',
        'current_original_macro_alignment_calls=1520':'current_original_macro_alignment_calls=1192',
        'all190_progressive_full_QA_and_complete_native_fonts_pass':'all149_progressive_full_QA_and_complete_native_fonts_pass',
        'all190_painted_consumers_original_progressive54020':'all149_painted_consumers_original_progressive54020',
        'thirty_FE_and_fifteen_three_option_choice_native_gates_separately_required':'one_FE_native_gate_separately_required_no_player_choices',
        'actual_selected_Shrines_Temples_IDs':'actual_selected_B111_B119_IDs',
        '190current progressive planes/1520macro alignments/220QA plans/31source-scope negatives pass;24sheets need visual review. ThirtyFE/fifteen three-choice labels/reference/release gates pending.':
        '149current progressive planes/1192macro alignments/150QA plans/43source-scope negatives pass;19sheets need visual review. OneFE/reference/release gates pending.'})
    text=text.replace('Current1520macro calls,190progressive planes andall220paragraph QA.',
        'Current1192macro calls,149progressive planes andall150paragraph QA.')
    PROGRESSIVE_NEW.write_text(text,encoding='utf-8')
    text=replace_all(FE_OLD.read_text(encoding='utf-8'),{
        'lil_Shrines_Temples_FE_v3180':'lil_B111_B119_FE_v3231',
        'lil_shrines_temples_editorial_manuscript_v3.json':'lil_B111_B119_editorial_manuscript_v3.json',
        'lil_shrines_temples_profile':'lil_B111_B119_profile',
        'lil_shrines_temples_layout_v1':'lil_B111_B119_layout_v1',
        'len(cases) == 30 and calls == 240 and len(staging) == 2':'len(cases) == 1 and calls == 8 and len(staging) == 0',
        'all30_one_native_page_consumes_complete_target':'all1_one_native_page_consumes_complete_target',
        'all30_complete_native_independent_planes_all_glyphs_and_canaries_equal':'all1_complete_native_independent_planes_all_glyphs_and_canaries_equal',
        'all30_source_unlabeled_panels_preserved_without_invented_names_or_macros':'one_source_unlabeled24000_gold_notice_preserved_without_invented_names_or_macros',
        'two_source_staging_cases_start_English_firstline_with_complete_glyphs':'no_source_leading_vertical_staging_in_gold_notice',
        'actual_selected_Shrines_Temples_IDs':'actual_selected_B111_B119_IDs',
        'Thirty complete FE planes/240null-actor macro cases andtwo source staging cases pass;four sheets need visual review. No gameplay or completion credit.':
        'One complete FE24000gold plane/8null-actor macro cases pass;one sheet needs visual review. No gameplay or completion credit.'})
    text=text.replace('Thirty FE records: complete native null-actor expansion, paper and pagination.',
        'One FE gold notice: complete native null-actor expansion,paper andpagination.')
    FE_NEW.write_text(text,encoding='utf-8')
    for p in [PROGRESSIVE_NEW,FE_NEW]:compile(p.read_text(encoding='utf-8'),str(p),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_font_tools_provenance.json',dict(
        previous={str(p):sha(p.read_bytes()) for p in [PROGRESSIVE_OLD,FE_OLD]},
        successors={str(p):sha(p.read_bytes()) for p in [PROGRESSIVE_NEW,FE_NEW]},
        exact_original_current_dynamic_selector_resolutions=mapping,
        virtual_prefixes_match_real_source_headers_not_assumed_D0=True,
        no_previous_producer_or_global_helper_modified=True,no_ROM_or_editorial_credit=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
