"""Reconcile the five legacy percent findings with exact clean actor selectors."""
import re
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script import format_safety as legacy
from dk4tool.script.format_safety_relocated_v1 import reject_with_receipt
from scripts.audit_story_glyph_consistency import load,save

A=Path('work/analysis')
OUT=A/'Rafael557_story_percent_relocation_v1_20261105/qualification.json'
REBUILT=A/'Rafael557_reconstruction_v2_20261105/reconstruction.json'
PREP=A/'Rafael557_registered_preparation_v1_20261105/registered_preparation.json'
MANUSCRIPT=Path('translations/rafael_B141_B160_final_review_v1.json')

if __name__=='__main__':
    assert not OUT.exists()
    rec,prep,doc=map(load,[REBUILT,PREP,MANUSCRIPT]);rows={r['id']:r for r in doc['records']}
    planned=Path(prep['ordered_canonical_targets'][0]['path']);assert sha(planned.read_bytes())==prep['ordered_canonical_targets'][0]['sha256']
    paths=[f'/data/SC{i}.DK4' for i in range(4)];path=paths[0]
    clean_path=Path('work/clean.nds');assert sha(clean_path.read_bytes())=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    source,current=[{p:NdsImage.open(img).read_file(p) for p in paths} for img in [clean_path,planned]]
    assert sha(current[path])==rec['target_archive_sha256']
    bad=legacy.story_percent_findings(source[path],current[path])
    assert {(r['block'],r['record']) for r in bad}=={(146,i) for i in [48,56,64,71,88]}
    selected=[]
    for g in rec['groups']:
        for row in g['text_records']:
            if (g['block'],row['new_record_index']) not in {(x['block'],x['record']) for x in bad}:continue
            d=rows[row['id']]
            assert d['source_selector']==37 and all(d['review'].values())
            assert d['source_hex']==row['source_hex'] and d['source_reference']['offset']==row['old_offset']
            assert d['planned_integrated_reference']['exact_stored_hex']==row['stored_hex']
            selected.append(dict(id=row['id'],block=g['block'],source_offset=row['old_offset'],target_offset=row['new_offset'],
                source_index=d['source_record_index'],target_index=row['new_record_index'],source_hex=row['source_hex'],
                target_hex=row['stored_hex'],complete_preamble_hex=d['source_complete_preamble_hex'],
                clean_block_sha256=g['clean_sha256'],target_block_sha256=g['target_sha256']))
    assert len(selected)==5
    receipt=dict(clean_SC0_sha256=sha(source[path]),relocated_source25_records=selected,original_legacy_findings=bad)
    positive=reject_with_receipt(source,current,receipt)
    assert positive['exact_source_bound_relocated_leading25_count']==5 and positive['all_four_final_story_archives_checked']
    negatives=[]
    for kind in ['wrong-clean-selector-offset','wrong-stored-preamble','wrong-target-index','introduced-valid-printf-in-unowned-record']:
        wrong=deepcopy(receipt);modified=dict(current);entry=wrong['relocated_source25_records'][0]
        if kind=='wrong-clean-selector-offset':entry['source_offset']+=2
        elif kind=='wrong-stored-preamble':entry['complete_preamble_hex']='0040ffff0024'
        elif kind=='wrong-target-index':entry['target_index']+=1
        else:
            blocks=list(IlnkContainer.parse(current[path]).blocks)
            raw=blocks[143]
            assert raw.count(b'Not very well.')==1
            blocks[143]=raw.replace(b'Not very well.',b'Not very %s.  ')
            assert len(blocks[143])==len(raw)
            modified[path]=IlnkContainer(blocks).to_bytes()
        try:reject_with_receipt(source,modified,wrong)
        except (AssertionError,ValueError) as error:
            if kind.startswith('introduced'):assert '%s' in str(error) and 'Introduced or invalid' in str(error)
            negatives.append(dict(case=kind,rejected=True,type=type(error).__name__))
        else:raise AssertionError('Accepted '+kind)
    assert len(negatives)==4
    paths=[REBUILT,PREP,MANUSCRIPT,Path(__file__),Path('dk4tool/script/format_safety.py'),Path('dk4tool/script/format_safety_relocated_v1.py')]
    receipt.update(positive=positive,negative_cases=negatives,original_failure_andall_rejections_verified=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in paths})
    OUT.parent.mkdir(parents=True);save(OUT,receipt)
    print('Exact clean control bindings explain all five findings. Four-archive guard passes and all four negatives reject.')
