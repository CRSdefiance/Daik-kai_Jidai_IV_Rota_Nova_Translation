"""Bridge a sealed source-first draft batch to the original guarded current-text binders."""
import argparse
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['drafts','meanings','packet','styles','choices','out']:p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();assert not a.out.exists()
    drafts,meanings,packet,styles,choices=map(load,[a.drafts,a.meanings,a.packet,a.styles,a.choices])
    n=len(drafts['records']);assert n==drafts['records_count']==meanings['records_count']
    assert drafts[f'all{n}_logical_drafts_written_before_current_ROM_story_English_intake']
    assert drafts['source_meanings_sha256']==digest(a.meanings) and drafts['current_English_comparisons']==0
    assert meanings['no_current_English_dialogue_consulted_for_eligible_records']
    source={r['id']:r for r in meanings['records']};assert len(source)==n
    for row in drafts['records']:
        original=source[row['id']]
        assert all(row[k]==original[k] for k in ['source_reference','source_hex','source_Japanese','source_meaning','exchange_context'])
        assert row['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert not any(t in row['english'] for t in ['{LB','{ALIGN','{PAD}','\n'])
        assert all(row['english'].count('{MACRO:'+m+'}')==row.get('source_macros',{}).get(m,0) for m in ['FI','FA','FO'])
    a.out.mkdir(parents=True);sealed=a.out/'sealed_drafts.json'
    save(sealed,{**drafts,'source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake':True,
        'original_drafts':str(a.drafts),'original_drafts_sha256':digest(a.drafts),
        'metadata_only_schema_bridge_all_drafts_unchanged':True})
    ordinary=[deepcopy(r) for r in drafts['records'] if 'source_complete_preamble_hex' in r]
    assert len(ordinary)==packet['records']
    for row in ordinary:row['current_ROM_English_unconsulted']=True
    save(a.out/'meanings.json',dict(source_packet=str(a.packet),source_packet_sha256=digest(a.packet),records=ordinary,
        meanings=len(ordinary),all_drafts_sealed=str(sealed),all_drafts_sha256=digest(sealed),
        no_blanket_prior_English_exposure_claim=True,new_credit=0))
    for kind,value in [('style',styles),('choice',choices)]:
        assert value['source_packet_sha256']==digest(a.packet)
        doc=deepcopy(value);doc.update(sealed_all_drafts=str(sealed),sealed_all_drafts_sha256=digest(sealed))
        save(a.out/f'{kind}_objects.json',doc)
    print(dict(sealed_drafts=n,ordinary_inputs=len(ordinary),style_inputs=len(styles['records']),caption_inputs=len(choices['records']),current_dialogue_intake=False))

if __name__=='__main__':main()
