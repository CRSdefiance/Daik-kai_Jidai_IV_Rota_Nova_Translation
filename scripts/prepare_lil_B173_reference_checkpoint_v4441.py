"""Derive reference checkpoint with numeric tokens separate from UTF-8 literals."""
from pathlib import Path
import io,re,tokenize
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_reference_checkpoint_tools_v4441')
SOURCE=Path('scripts/checkpoint_lil_B172_references_v4400.py')
TARGET=Path('scripts/checkpoint_lil_B173_references_v4441.py')
if __name__=='__main__':
    assert not ROOT.exists() and not TARGET.exists()
    text=SOURCE.read_text(encoding='utf-8')
    changes={'B172':'B173','v4400':'v4441','V4400':'V4441',
        'Lil-B172-Julian-Mihwa-Silla-crown-conditional-date-independent-search27':'Lil-B173-Reika-crown-inquiry-uncertain-Julian-tomb-lead-competitive-search11',
        'reference_approval_v4399':'reference_approval_v4440',
        'promotion_v4392/promotion_receipt.json':'editorial_handoff_verification_v4427/verified_handoff.json',
        'focused_repeat_proof':'postscene_native_state_proof','v4379':'v4426',
        'display_fixture_v4389':'display_fixture_v4436','research_v4384':'research_v4431',
        "approval['new_emulator_runs'] == 4":"approval['new_emulator_runs'] == 2",'new_emulator_runs=4':'new_emulator_runs=2',
        'actual_new_cold_boot_runs=4':'actual_new_cold_boot_runs=2',
        'reviewed_sheets=5':'reviewed_sheets=2','actual panels/four boots':'actual panels/two boots',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    numbers={'5789':'5800','5762':'5789','5792':'5803','27':'11'}
    tokens=[]
    for token in tokenize.generate_tokens(io.StringIO(text).readline):
        if token.type==tokenize.NUMBER and token.string in numbers:token=token._replace(string=numbers[token.string])
        tokens.append(token)
    text=tokenize.untokenize(tokens)
    for old,new in [('5789 rereads/5762 integrated/27 pending','5800 rereads/5789 integrated/11 pending'),
        ('27-Lil-B173','11-Lil-B173'),('V4441:27 B173','V4441:11 B173'),('complete:27 reference-approved','complete:11 reference-approved'),
        ('27 actual panels','11 actual panels')]:
        assert old in text,old
        text=text.replace(old,new)
    assert 'encode_ledger(ledger)' in text and 'utf-8' in text and 'utf-3' not in text
    compile(text,str(TARGET),'exec');TARGET.write_text(text,encoding='utf-8',newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT/'derivation.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),target=str(TARGET),
        target_sha256=sha(TARGET.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),
        no_new_review_or_completion_credit=True,content_boots=2,full_goal_complete=False))
    print('Prepared B173 reference checkpoint:11 pending reviews,two content boots,no new source/completion credit.')
