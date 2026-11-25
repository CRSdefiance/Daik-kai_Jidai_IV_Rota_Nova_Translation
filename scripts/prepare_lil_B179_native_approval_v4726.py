"""Prepare B179 approval with the genuine Sailor/catalog Retainer distinction."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B179_native_approval_tools_v4726')
assert not ROOT.exists()
source=Path('scripts/approve_lil_B178_native_v4678.py')
text=source.read_text(encoding='utf-8')
start=text.index("            'review':'")
end=text.index("'})",start)+3
review="""            'review':'Viewed all fourteen final native panels across two sheets individually. Sailor92 is not used: source-bound roles are Barkeep92,Patron96,Sailor152; the separate catalog Retainer152 stays distinct. Preserve the rough challenge about an unspecified drink,defensive reply,concession,wine enthusiasm,repeated taste questions,personal hyperbole,decision to try one glass,casual service,three gulps,verdict,another-serving request and joining order. The impersonal Sao Jorge wine notice remains prospective. All eight revisions and six individually justified retentions remain coherent. Complete leading/internal/final characters,punctuation,bounds and single-page consumption pass. No invented drink type,brand,price,rank,relationship,drunkenness,medical claim,completed sale,active boom or earlier location. No new phrase exception,prose shortening,authored break or padding. Offline rendering;actual B179 gameplay remains pending.'})"""
old_names="    assert {r['actor_ID']:r['text'] for r in names}=={166:'Lady',167:'Lady',168:'Lady'}"
new_names="""    assert {(r['consumer'],r['actor_ID']):r['text'] for r in names}=={
        ('progressive-nameplate',92):'Barkeep',('progressive-nameplate',96):'Patron',('progressive-nameplate',152):'Sailor',
        ('full-catalogue',92):'Barkeep',('full-catalogue',96):'Patron',('full-catalogue',152):'Retainer'}
    controls=read(doc['source_effect_and_predicate_contract'])
    assert controls['source_has_no_C200_and_no_C200_probe_invented'] and controls['source_C200_pairs']==[]
    assert controls['source_declared_end_offsets']==[508]
    assert len(controls['all2_source_current_nonrelative_nonspeech_leaves'])==2
    assert Path(doc['separate_untranslated_city_alias_lead']).is_file()
    assert sha(Path(doc['separate_untranslated_city_alias_lead']).read_bytes())==doc['separate_untranslated_city_alias_lead_sha256']"""
tool=derive(source,'scripts/approve_lil_B179_native_v4726.py',{
    text[start:end]:review,old_names:new_names,
    'lil_B178_layout_v1':'lil_B179_layout_v1','lil_B178_profile':'lil_B179_profile',
    'lil_B178_native_approval_v4678':'lil_B179_native_approval_v4726',
    'lil_B178_editorial_manuscript_v2':'lil_B179_editorial_manuscript_v2',
    'lil_B178_editorial_manuscript_v3':'lil_B179_editorial_manuscript_v3',
    'lil_B178_fonts_v4677/all13_progressive_FE_native_planes_and104_alignment_cases':
        'lil_B179_fonts_v4724/all14_progressive_FE_native_planes_and112_alignment_cases',
    "len(font['cases'])==13 and font['current_original_macro_alignment_calls']==104":
        "len(font['cases'])==14 and font['current_original_macro_alignment_calls']==112",
    "(font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(12,1)":
        "(font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(13,1)",
    'blocks[178]':'blocks[179]','block=178':'block=179',
    "=={'revise':2,'retain-wording':11}":"=={'revise':8,'retain-wording':6}",
    "for r in doc['records'])==5":"for r in doc['records'])==4",
    "[166,167,168]":"[92,96,152]",
    "[('progressive',166),('FE-paper',254)]":"[('progressive',92),('FE-paper',254)]",
    'all13':'all14','current_original_macro_alignment_calls=104':'current_original_macro_alignment_calls=112',
    'progressive_planes=12':'progressive_planes=13','revised=2,retained=11':'revised=8,retained=6',
    'current_macro_alignment_cases=104':'current_macro_alignment_cases=112','narrow_row_count_notes=5':'narrow_row_count_notes=4',
    'source_one_A000_C200_single_end_preserved_without_guessed_operands':
        'source_one_A000_single_end_no_C200_preserved_without_guessed_operands',
    'actual_selected_B178_IDs':'actual_selected_B179_IDs','Seal the viewed B178':'Seal the viewed B179',
    'B178:13 five-gate reviews,2 revisions/11 retentions;12 progressive+1 FE planes,104 alignments and51 negatives.':
        'B179:14 five-gate reviews,8 revisions/6 retentions;13 progressive+1 FE planes,112 alignments and51 negatives.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,both_native_sheets_viewed_individually=True,
    source_Sailor152_and_separate_catalog_Retainer152_preserved=True,no_source_C200_invented=True,
    no_new_phrase_exception_or_prose_change=True,no_source_prose_credit_added_yet=True,full_goal_complete=False))
