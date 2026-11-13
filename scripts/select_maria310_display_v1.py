"""Select distinct pagination, FE, glyph and transition risks; preserve full-review scope."""
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save

def main():
    out=ROOT/'display_selection_v1.json';assert not out.exists()
    native=load(ROOT/'storage_inputs_v1/native_pages.json');rows={r['id']:r for r in native['records']}
    def ids(block,numbers):return [f'DK4_MES_B{block}_R{n:04d}' for n in numbers]
    a=ids(51,[6,9,13,20,23,27,31,35,69,72,75,78,82,85])+ids(52,[11,17])+ids(53,[113,117,121,124,127,130])+ids(54,[491,495,499,502,507,511,515,523])
    b=ids(55,[4,8,12,16,91,98,124,133,141,148,155,162,165,172,179,187,191,201,208,211,215,219])+ids(56,[185,189])+ids(57,[17,27,126,129,136,143,166,169,176,194])
    fixtures=[]
    for name,selected,purpose in [
        ('Maria310_history_pages',a,'Progressive A/page returns, four distinct two-page layouts, two conditional town texts and complete repaired ending FE sequence including exact R507 storage alignment.'),
        ('Maria310_voices_glyphs',b,'Inline Bianca/Angelo FE voices and return to named portraits, three repaired dream FE rows, two other two-page layouts and normal ASCII I/F fixes; source-bound host exit/resupply/sailing.')]:
        assert len(selected)==len(set(selected)) and set(selected)<=set(rows)
        pages=sum(len(rows[k]['complete_native_English_display']['pages']) if rows[k]['kind']=='progressive' else 1 for k in selected)
        fixtures.append(dict(name=name,purpose=purpose,speech_ids=selected,frames=4001+pages*240+6000,
            capture_extra=[],extra_inputs=[],selection_source_utterances=len(selected),selection_expected_pages=pages))
    assert not set(a)&set(b)
    save(out,dict(fixtures=fixtures,source_utterances=len(a)+len(b),
        conditional_town_alternatives_not_claimed_as_naturally_consecutive=True,
        original_story_conditions_outcomes_chronology_full_routes_andhardware_unvisited=True,
        all310_whole_exchange_editorial_reviews_remain_required_andalready_saved=True,
        selected_display_cases_do_not_reduce_full_editorial_scope=True,guide_photos=False,new_credit=0))
    print([(f['name'],f['selection_source_utterances'],f['selection_expected_pages'],f['frames']) for f in fixtures])

if __name__=='__main__':main()
