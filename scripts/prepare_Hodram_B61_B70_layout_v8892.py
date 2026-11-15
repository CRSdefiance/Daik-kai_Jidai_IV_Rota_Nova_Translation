"""Qualify full-width planning with exact retained native literal bindings.

Only33 existing, individually retained clean/current bodies contain non-ASCII
characters. Their exact source/current references and complete logical body bind
each exception. This does not allow arbitrary Japanese or change global QA.
"""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B61_B70_layout_preparation_v8892')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=read('translations/hodram_B61_B70_editorial_manuscript_v1.json')
    literals=[r for r in doc['records'] if any(ord(c)>127 for c in r['english'])]
    assert len(literals)==33 and all(r['decision']=='retention' and r['english']==r['prior_macro_normalized_comparison'] for r in literals)
    old="""document=read(DOC)
REACTIONS={r['id']:dict(source_hex=r['source_hex'],logical_English=r['english']) for r in document['records'] if r['english'] in ['…','？']}
assert len(REACTIONS)==6

def source_bound_reaction(row,body):
    binding=REACTIONS.get(row['id'])
    return binding==dict(source_hex=row['source_hex'],logical_English=body) and bytes.fromhex(row['source_hex'])[1:].decode('cp932')==body
"""
    new="""document=read(DOC)
NATIVE_LITERALS={r['id']:dict(source_hex=r['source_hex'],current_hex=r['current_hex'],logical_English=r['english'],prior=r['prior_macro_normalized_comparison']) for r in document['records'] if any(ord(c)>127 for c in r['english'])}
assert len(NATIVE_LITERALS)==33 and all(v['logical_English']==v['prior'] for v in NATIVE_LITERALS.values())
assert all(r['decision']=='retention' for r in document['records'] if r['id'] in NATIVE_LITERALS)

def source_bound_existing_literal(row,body):
    binding=NATIVE_LITERALS.get(row['id'])
    return binding is not None and binding==dict(source_hex=row['source_hex'],current_hex=row['current_hex'],logical_English=body,prior=row['prior_macro_normalized_comparison']) and body==row['prior_macro_normalized_comparison']
"""
    changes={
        'Automatic full-width plans, with exact source-bound silent/question reactions.':
            'Automatic full-width plans, with exact retained clean/current native literal bodies.',
        'work/analysis/Hodram_B54_B60_layout_v8802d':'work/analysis/Hodram_B61_B70_layout_v8892',
        'translations/hodram_B54_B60_editorial_manuscript_v1.json':'translations/hodram_B61_B70_editorial_manuscript_v1.json',
        'work/analysis/Hodram_B54_B60_logical_v8801/logical_paragraphs.json':'work/analysis/Hodram_B61_B70_logical_v8891/logical_paragraphs.json',
        old:new,
        '[1,20,23,24,36,84,113,114,119,141]':'[1,2,3,9,10,16,17,18,20,23,24,38,78,105,116,154]',
        "c in '…？' and source_bound_reaction(row,body)":"c in '…？！○×Ｉ' and source_bound_existing_literal(row,body)",
        "'source_bound_reaction':source_bound_reaction":"'source_bound_existing_literal':source_bound_existing_literal",
        'Hodram B54-B60 plan:':'Hodram B61-B70 plan:',
        'Hodram-B54-B60-RESEARCH-ONLY:':'Hodram-B61-B70-RESEARCH-ONLY:',
        "'been','praying')}":"'been','praying'),('indian','ocean'),('king','of'),('the','seas'),('straight','face'),('spice','islands'),('li','family'),('li','clan'),('maria','huamei'),('huamei','li'),('in','time'),('world-class','standards'),('first','place'),('your','guard'),('guard','down'),('death','wish'),('no','one'),('will','object'),('for','now'),('right','now'),('once','again'),(\"aren't\",'you'),(\"isn't\",'it'),('you','will'),('don't','worry')}",
        "logical['fresh_native_alignment_cases']==328 and len(document['records'])==82":"logical['fresh_native_alignment_cases']==896 and len(document['records'])==224",
        'source_owned_reaction_predicate=inspect.getsource(source_bound_reaction),source_bound_reaction_bindings=REACTIONS':
            'source_owned_existing_literal_predicate=inspect.getsource(source_bound_existing_literal),exact_existing_native_literal_bindings=NATIVE_LITERALS',
        'all_words_punctuation_andFI3_FA4_FO0_preserved_without_shortening':'all_words_punctuation_andFI15_FA3_FO0_preserved_without_shortening',
        'original_FE_usable216_bitmap228_stride288_metrics6x12_physical16_distinction_preserved':
            'all_progressive216_bitmap_andusable_width_no_FE_source_panel',
        'len(rows)==82':'len(rows)==224'
    }
    # Encode the apostrophe as a valid Python string literal in the generated set.
    key="'been','praying')}";changes[key]=changes[key].replace("('don't','worry')",'(\"don\'t\",\'worry\')')
    receipt=derive('scripts/plan_Hodram_B54_B60_v8802d.py','scripts/plan_Hodram_B61_B70_v8892.py',changes)
    ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_derivation.json',dict(derivation=receipt,
        original216_width_native_font_pair_phase_guard_QA_no_manual_breaks_andword_preservation_guards_preserved=True,
        nonASCII_scope=dict(count=33,IDs=[r['id'] for r in literals],characters=sorted({c for r in literals for c in r['english'] if ord(c)>127})),
        native_literals_exact_existing_retained_bodies_not_arbitrary_multibyte_prose=True,
        opaque_unknown_language_source6_andexisting_punctuation_andtwo_fullwidth_I_bodies_require_native_glyph_checks=True,
        new_credit=0,full_goal_complete=False))
    print('Prepared224 full-width automatic plans;33 exact retained native literal bodies scoped; original QA andgeometry unchanged.')
