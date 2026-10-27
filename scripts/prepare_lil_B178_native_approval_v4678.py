"""Prepare offline B178 native approval after both complete sheets were viewed."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B178_native_approval_tools_v4678')
assert not ROOT.exists()
source=Path('scripts/approve_lil_B177_native_v4622.py');text=source.read_text(encoding='utf-8')
start=text.index('    for labels,index in ');end=text.index('    names=read',start)
old_review=text[text.index("            'review':'"):text.index("'})",text.index("            'review':'"))+3]
new_review="""            'review':'Viewed all thirteen final native panels across two sheets individually. Three Lady speakers retain home-baking enthusiasm,the explicit second-speaker husband reference,curiosity,the bakery boast,encouragement,teaching offer,pleased reply,shopping plan and ingredient question. The revised offer uses the speaker\'s own help;the wheat reply restores first. The impersonal Amsterdam forecast remains prospective. All eleven retentions remain coherent;all leading/internal/final characters,punctuation,bounds and single-page consumption pass. No extra names,rank,kinship,recipe,flour,quantity,price,completed purchase or earned boom. No new phrase exception,prose shortening,authored break or padding. Offline rendering;actual B178 gameplay remains pending.'})"""
# The generated single-quoted literal needs an escaped apostrophe.
new_review=new_review.replace("speaker's", "speaker\\'s")
tool=derive(source,'scripts/approve_lil_B178_native_v4678.py',{
    old_review:new_review,text[start:end]:'',
    'lil_B177_layout_v3':'lil_B178_layout_v1','lil_B177_profile':'lil_B178_profile',
    'lil_B177_native_approval_v4622':'lil_B178_native_approval_v4678',
    'lil_B177_editorial_manuscript_v4':'lil_B178_editorial_manuscript_v2',
    'lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
    'lil_B177_fonts_v4621/all10_progressive_FE_native_planes_and80_alignment_cases':
        'lil_B178_fonts_v4677/all13_progressive_FE_native_planes_and104_alignment_cases',
    "len(font['cases'])==10 and font['current_original_macro_alignment_calls']==80":
        "len(font['cases'])==13 and font['current_original_macro_alignment_calls']==104",
    "(font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(9,1)":
        "(font['complete_progressive_planes'],font['complete_FE_logical_and_physical_planes'])==(12,1)",
    "len(font['negative_controls'])==18":"len(font['negative_controls'])==20",
    'blocks[177]':'blocks[178]','block=177':'block=178',
    "=={'revise':5,'retain-wording':5}":"=={'revise':2,'retain-wording':11}",
    'native_four_consumer_cases':'native_six_consumer_cases','len(names)==4':'len(names)==6',
    "[174,175]":"[166,167,168]","{174:'Owner',175:'Cook'}":"{166:'Lady',167:'Lady',168:'Lady'}",
    "[('progressive',174),('FE-paper',254)]":"[('progressive',166),('FE-paper',254)]",
    'all10':'all13','two_static_selectors':'three_static_selectors',
    'current_original_macro_alignment_calls=80':'current_original_macro_alignment_calls=104',
    'progressive_planes=9':'progressive_planes=12','revised=5,retained=5':'revised=2,retained=11',
    'current_macro_alignment_cases=80,source_consumer_negatives=18':'current_macro_alignment_cases=104,source_consumer_negatives=20',
    'actual_selected_B177_IDs':'actual_selected_B178_IDs','Seal the viewed B177':'Seal the viewed B178',
    'B177:10 five-gate reviews,5 revisions/5 retentions;9 progressive+1 FE planes,80 alignments and49 negatives.':
        'B178:13 five-gate reviews,2 revisions/11 retentions;12 progressive+1 FE planes,104 alignments and51 negatives.',
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,both_native_sheets_viewed_individually=True,
    no_new_phrase_exception_or_prose_change=True,no_source_prose_credit_added_yet=True,full_goal_complete=False))
