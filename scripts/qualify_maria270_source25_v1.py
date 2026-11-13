"""Bind the two relocated Abraham controls and verify malformed/nonleading rejection."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script import format_safety as legacy
from dk4tool.script.format_safety_relocated_v2 import reject_with_receipt
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/Maria_B37_B50_clean_20261109')
OUT=ROOT/'registered_source25_v1/qualification.json'
def main():
    assert not OUT.exists()
    rec_path=ROOT/'stored270_reconstruction_v1/reconstruction.json';rec=load(rec_path)
    final_path=Path('translations/maria_B37_B49_final_review_v1.json');doc=load(final_path)
    release_path=Path('work/market_goods_info_terminator_release_v1/registered_release_verification.json');release=load(release_path)
    manifest=load(release['manifest']);old=manifest['story_percent_contract']
    clean=NdsImage.open('work/clean.nds');target=NdsImage.open(rec['research_ROM'])
    assert digest(rec['research_ROM'])==rec['research_ROM_sha256']
    paths=[f'/data/SC{i}.DK4' for i in range(4)];path=paths[3]
    source={p:clean.read_file(p) for p in paths};current={p:target.read_file(p) for p in paths}
    bad=legacy.story_percent_findings(source[path],current[path])
    assert {(r['block'],r['record']) for r in bad}=={(38,43),(38,51)}
    rows={r['id']:r for r in doc['records']};selected=[]
    for group in rec['groups']:
        for row in group['text_records']:
            if (group['block'],row['new_record_index']) not in {(r['block'],r['record']) for r in bad}:continue
            d=rows[row['id']]
            assert d['source_selector']==37 and all(d['review'].values())
            assert d['source_reference']['offset']==row['old_offset'] and d['source_hex']==row['source_hex']
            assert d['planned_integrated_reference']['exact_stored_hex']==row['stored_hex']
            selected.append(dict(id=row['id'],block=group['block'],source_offset=row['old_offset'],target_offset=row['new_offset'],
                source_index=d['source_record_index'],target_index=row['new_record_index'],source_hex=row['source_hex'],
                target_hex=row['stored_hex'],complete_preamble_hex=d['source_complete_preamble_hex'],
                clean_block_sha256=group['clean_sha256'],target_block_sha256=group['target_sha256']))
    assert {r['id'] for r in selected}=={'DK4_MES_B38_R0044','DK4_MES_B38_R0052'}
    route=dict(file_path=path,clean_archive_sha256=sha(source[path]),block_count=303,relocated_source25_records=selected)
    receipt=dict(prior_receipt=old['exact_relocation_receipt'],additional_routes=[route],original_legacy_findings=bad)
    positive=reject_with_receipt(source,current,receipt)
    assert {k:v for k,v in positive.items() if k in old and k!='exact_relocation_receipt'}=={k:v for k,v in old.items() if k!='exact_relocation_receipt'}
    assert positive['additional_exact_source_bound_relocated_leading25_count']==2 and positive['total_exact_source_bound_relocated_leading25_count']==7
    negatives=[]
    for kind in ['wrong-clean-selector-offset','wrong-stored-preamble','wrong-target-index','introduced-valid-printf-in-unowned-record']:
        wrong=deepcopy(receipt);modified=dict(current);entry=wrong['additional_routes'][0]['relocated_source25_records'][0]
        if kind=='wrong-clean-selector-offset':entry['source_offset']+=2
        elif kind=='wrong-stored-preamble':entry['complete_preamble_hex']='0040ffff0024'
        elif kind=='wrong-target-index':entry['target_index']+=1
        else:
            blocks=list(IlnkContainer.parse(current[path]).blocks);raw=blocks[40]
            phrase=b'Meaning?';assert raw.count(phrase)==1
            blocks[40]=raw.replace(phrase,b'%s     ');assert len(blocks[40])==len(raw)
            modified[path]=IlnkContainer(blocks).to_bytes()
        try:reject_with_receipt(source,modified,wrong)
        except (AssertionError,ValueError) as error:
            if kind.startswith('introduced'):assert '%s' in str(error) and 'Introduced or invalid' in str(error)
            negatives.append(dict(case=kind,rejected=True,type=type(error).__name__))
        else:raise AssertionError('Accepted '+kind)
    receipt.update(positive=positive,negative_cases=negatives,original_failure_andall_rejections_verified=True,new_credit=0,
        evidence={str(p):digest(p) for p in [rec_path,final_path,release_path,Path(release['manifest']),Path(__file__),
            Path('dk4tool/script/format_safety.py'),Path('dk4tool/script/format_safety_relocated_v1.py'),Path('dk4tool/script/format_safety_relocated_v2.py')]})
    OUT.parent.mkdir();save(OUT,receipt)
    print('PASSexacttwo SC3 controls plusallfive prior SC0 controls;four original-format rejection cases;no ROM changes.')
if __name__=='__main__':main()
