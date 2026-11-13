"""Prepare exact twelve-panel native approval without inheriting a fur-scene exception."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_approval_preparation_v5156')
if __name__=='__main__':
    assert not ROOT.exists()
    row=derive('scripts/approve_lil_B185_native_v5104b.py','scripts/approve_lil_B186_native_v5156.py',{
        'B185':'B186','viewed8-panel':'viewed12-panel','native_approval_v5104b':'native_approval_v5156',
        'lil_B185_layout_v2':'lil_B186_layout_v4',
        'editorial_manuscript_v3':'editorial_manuscript_v4','editorial_manuscript_v4':'editorial_manuscript_v5',
        'fonts_v5102/all8_progressive_FE_native_planes_and64_alignment_cases':'fonts_v5154/all12_progressive_FE_native_planes_and96_alignment_cases',
        "len(font['cases'])==8":"len(font['cases'])==12",
        "font['current_original_macro_alignment_calls']==64":"font['current_original_macro_alignment_calls']==96",
        "==(7,1)":"==(11,1)",
        'blocks[185]':'blocks[186]',
        "len(font['review_sheets'])==1":"len(font['review_sheets'])==2",
        "row['source_record_index']==16":"row['source_record_index']==13",
        "len(qa.get('reviewed_ordinary_boundaries',[]))==1":"len(qa.get('reviewed_ordinary_boundaries',[]))==2",
        "{'revise':4,'retain-wording':4}":"{'revise':7,'retain-wording':5}",
        "('progressive',164)":"('progressive',174)",
        'all8_current_native_previews_viewed_on_one_sheet':'all12_current_native_previews_viewed_on_two_sheets',
        'wrap_comparison_v5103b/all8_unchanged_words_and_exact_R16_boundary':'wrap_comparison_v5155/all12_unchanged_words_and_exact_R13_boundaries',
        "['DK4_MES_B185_R0016'] and comparison['all8_words_controls_and_prose_unchanged']":"['DK4_MES_B186_R0013'] and comparison['all12_words_controls_and_prose_unchanged']",
        "R16 exact source/prose only:complete-word soft break after in keeps this cold and prices are going up intact in two safe rows. The exact approved shared warning is recorded on this record. All words,font,width,guards,phase and pagination remain checked. No global weak-ending exemption.":
        "R13 exact source/prose only:ordinary complete-word soft wraps after be and this use three flowing rows and keep the repeated sweet emphasis intact. Both exact approved warnings and reasons are recorded on this record. All words,font,width,guards,phase and pagination remain checked. No global weak-ending exemption.",
        'all8_source_prose_current_native_approval':'all12_source_prose_current_native_approval',
        'all8_complete_native_panels_read_as_one_exchange':'all12_complete_native_panels_read_as_one_exchange',
        'four_revisions_and_four_individually_justified_retentions':'seven_revisions_and_five_individually_justified_retentions',
        'source_reported_fur_sales_rising_prices_cold_coat_wish_and_tentative_notice_preserved':'source_Owner_Cook_comic_sweet_emphasis_self_authority_repeated_acknowledgments_and_tentative_notice_preserved',
        'all64_current_native_alignment_cases_and_complete_planes_pass':'all96_current_native_alignment_cases_and_complete_planes_pass',
        'All8 source/prose/current-native reviews approved:4 revisions/4 justified retentions,64 alignments':'All12 source/prose/current-native reviews approved:7 revisions/5 justified retentions,96 alignments',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_exact_native_approval.json',dict(derivation=row,new_review_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Prepared B186 twelve-panel approval with two exact R13 boundary reviews and unchanged native guards.')
