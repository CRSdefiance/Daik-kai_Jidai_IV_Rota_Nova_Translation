"""Give the appended-copy digest its accurate metadata field name."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('work/analysis/lil_B111_B119_source_v3217/complete150_reachable_Lil_clean_current_context.json')
ROOT=Path('work/analysis/lil_B111_B119_source_v3217b')
if __name__=='__main__':
    assert not ROOT.exists()
    doc=deepcopy(read(OLD));b=next(b for b in doc['blocks'] if b['block']==115)
    digest=b.pop('unowned_appended_copy_current_hex')
    assert len(digest)==64 and b.pop('unowned_copy_metadata_value_above_is_sha256_not_body_hex')
    b['unowned_appended_copy_current_sha256']=digest
    doc.update(previous_reconciled_source_packet=str(OLD),previous_reconciled_source_packet_sha256=sha(OLD.read_bytes()))
    doc['evidence'][str(OLD)]=sha(OLD.read_bytes());doc['evidence'][str(Path(__file__))]=sha(Path(__file__).read_bytes())
    ROOT.mkdir(parents=True);save(ROOT/'complete150_reachable_Lil_clean_current_context.json',doc)
    print('Appended-copy digest correctly namedSHA256;all150targets/source bytes/counts unchanged.')
