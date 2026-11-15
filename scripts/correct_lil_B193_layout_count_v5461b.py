"""Correct a transcription count while preserving the original viewed layout receipt."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
if __name__=='__main__':
    old=Path('work/analysis/lil_B193_relocation_tools_v5461/viewed_layout_retention_reasons.json')
    new=old.with_name('viewed_layout_retention_reasons_v2.json');assert not new.exists()
    d=read(old);doc=read('translations/lil_B193_editorial_manuscript_v3.json')
    r=next(r for r in doc['records'] if r['source_record_index']==25);count=len(r['english'].split('}',1)[1]);assert count==111
    item=next(r for r in d['retained_layouts'] if r['id']=='DK4_MES_B193_R0025');assert '109 ASCII' in item['reason']
    item['reason']=item['reason'].replace('109 ASCII','111 ASCII')
    d.update(previous_layout_receipt=str(old),previous_layout_receipt_sha256=sha(old.read_bytes()),
        exact_paragraph_ASCII_characters=111,three_row_maximum_cells=106,count_transcription_corrected_without_prose_layout_or_native_plane_change=True,
        correction_producer_sha256=sha(Path(__file__).read_bytes()))
    save(new,d);print('R25 receipt corrected109 to measured111 characters. Original receipt,all words and native planes preserved;four rows remain necessary.')
