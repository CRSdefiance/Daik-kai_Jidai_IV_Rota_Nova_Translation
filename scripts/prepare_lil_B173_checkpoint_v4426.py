"""Prepare once-only B173 pending credit while preserving completed history."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_checkpoint_tools_v4426')
SOURCE=Path('scripts/checkpoint_lil_B172_v4379.py')
TARGET=Path('scripts/checkpoint_lil_B173_v4426.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    changes={'B172':'B173','v4379':'v4426','V4379':'V4426',
        'editorial_handoff_verification_v4363':'editorial_handoff_verification_v4409b',
        'native_approval_v4378':'native_approval_v4425',
        'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27':'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11',
        '[172]':'[173]','# Current editorial handoff - V4362':'# Current editorial handoff - V4408',
        'row_count_notes=13':'row_count_notes=5','all4_speech_sheets_viewed':'all2_speech_sheets_viewed',
        'unfinished_editorial_scope_v4357':'unfinished_editorial_scope_v4408',
        'remaining_B173_B180':'remaining_B174_B180','Latest V4353 and promoted V4303':'Latest V4404 and promoted V4353',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5762':'5789','5789':'5800','5792':'5803','5765':'5792','3909':'3936','3936':'3947',
        '4163':'4190','4190':'4201','3659':'3678','2103':'2111','27':'11','19':'8','8':'3','134':'123'}
    text=re.sub(r'(?<!\d)(?:'+'|'.join(numbers)+r')(?!\d)',lambda m:numbers[m[0]],text)
    assert 'encode_ledger(ledger)' in text and not re.search(r'B172|blocks=\[172\]|5762|5792\D*completed=5762',text)
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        pending_reviews_once=11,new_completion_credit=0,expected_fresh=5800,integrated=5789,source_prose=5803,
        full_goal_complete=False))
    print('Prepared B173 pending checkpoint:5800/5789/11,5803 source/prose;all prior completions and full scope preserved.')
