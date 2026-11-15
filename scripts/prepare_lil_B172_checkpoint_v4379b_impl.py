"""Prepare27 pending B172 reviews once, preserving one-space current-ledger storage."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B172_checkpoint_tools_v4379b')
OLD=Path('scripts/checkpoint_lil_B171_v4329.py')
NEW=Path('scripts/checkpoint_lil_B172_v4379.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    changes={
        'B171':'B172','lil_B171':'lil_B172','checkpoint_v4329':'checkpoint_v4379','checkpoint_text_v4329':'checkpoint_text_v4379',
        'editorial_handoff_verification_v4308b':'editorial_handoff_verification_v4363','native_approval_v4328':'native_approval_v4378',
        'editorial_manuscript_v4':'editorial_manuscript_v3',
        'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37':'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27',
        '[171]':'[172]','# Current editorial handoff - V4307':'# Current editorial handoff - V4362',
        'all5_speech_sheets_viewed':'all4_speech_sheets_viewed','unfinished_editorial_scope_v4307':'unfinished_editorial_scope_v4357',
        'remaining_B172_B180':'remaining_B173_B180','V4329':'V4379',
        'import json':'import json\nfrom scripts.editorial_ledger_storage_v1 import encode_ledger',
        r"(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8')":'encode_ledger(ledger)',
        'Latest V4303 and promoted V4251 unchanged':'Latest V4353 and promoted V4303 unchanged',
        "['lil_B171_v4329']":"['lil_B172_v4379']",'unfinished_editorial_scope_v4329':'unfinished_editorial_scope_v4379',
        'scope_reconciliation_v4329':'scope_reconciliation_v4379','fresh_context_review_checkpoint_v4329':'fresh_context_review_checkpoint_v4379',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m.group()],text)
    counts={'5725':'5762','5762':'5789','5728':'5765','5765':'5792','3872':'3909','3909':'3936','4163':'4190','4126':'4163',
        '37':'27','24':'19','13':'8','16':'13','3635':'3659','2090':'2103','161':'134'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(re.escape(k) for k in sorted(counts,key=len,reverse=True))+r')(?!\d)',lambda m:counts[m.group()],text)
    assert 'B171' not in text and '[171]' not in text and 'indent=2' not in text
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        expected_fresh=5789,expected_integrated=5762,expected_pending=27,expected_source_prose=5792,
        current_ledger_encoder='scripts.editorial_ledger_storage_v1.encode_ledger',no_completion_credit=True,full_goal_complete=False))
    print('Prepared B172 pending checkpoint;5789 rereads/5762 integrated/27 pending;5792 source/prose;one-space ledger retained.')
