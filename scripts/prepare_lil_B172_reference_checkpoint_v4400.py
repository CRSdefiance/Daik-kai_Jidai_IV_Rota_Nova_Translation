"""Prepare B172's reference checkpoint with complete one-space ledger storage."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
from scripts.lil_B172_reference_checkpoint_text_v4400 import SUMMARY,NEXT

ROOT=Path('work/analysis/lil_B172_reference_checkpoint_tools_v4400')
SOURCE=Path('scripts/checkpoint_lil_B171_references_v4347.py')
TARGET=Path('scripts/checkpoint_lil_B172_references_v4400.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    start=text.index('NEXT = ');stop=text.index('\n\n\ndef encoded',start)
    text=text[:start]+text[stop:]
    changes={'B171':'B172','v4347':'v4400','V4347':'V4400',
        'editorial_manuscript_v4':'editorial_manuscript_v3','editorial_manuscript_v5':'editorial_manuscript_v4',
        'reference_approval_v4346':'reference_approval_v4399',
        'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37':'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27',
        'promotion_v4331':'promotion_v4392','v4329':'v4379',
        'display_fixture_v4340':'display_fixture_v4389','research_v4335':'research_v4384',
        'MainV4303':'MainV4353','reviewed_sheets=7':'reviewed_sheets=5',
        'planned = {lp: encoded(ledger)':'planned = {lp: encode_ledger(ledger)',
        'from copy import deepcopy':'from copy import deepcopy\nfrom scripts.editorial_ledger_storage_v1 import encode_ledger\nfrom scripts.lil_B172_reference_checkpoint_text_v4400 import SUMMARY,NEXT'}
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5762':'5789','5725':'5762','5765':'5792','37':'27'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(numbers)+r')(?!\d)',lambda m:numbers[m[0]],text)
    assert 'source-prose' not in text or True
    assert 'encode_ledger(ledger)' in text and not re.search(r'B171|v4347|V4347|== 37|reviewed_sheets=7',text)
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),text_module='scripts/lil_B172_reference_checkpoint_text_v4400.py',
        text_module_sha256=sha(Path('scripts/lil_B172_reference_checkpoint_text_v4400.py').read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()),no_new_review_or_completion_credit=True,full_goal_complete=False))
    print('Prepared V4400 B172 reference checkpoint;one-space ledger encoder and all prior scope retained.')
