"""Mark the one retained FI substitution explicitly before native encoding."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_macro_markup_v5786')
INPUT=Path('translations/lil_B199_editorial_manuscript_v1.json')
OUTPUT=Path('translations/lil_B199_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists()
    old=read(INPUT);new=deepcopy(old);changes=[]
    for a,b in zip(old['records'],new['records'],strict=True):
        count=bytes.fromhex(a['source_hex'])[1:].count(b'FI')
        if count:
            assert a['source_record_index']==37 and count==1
            assert a['english']=='{SPEAKER:09}FI! Stop throwing things! Ow!'
            b['english']=a['english'].replace('FI','{MACRO:FI}')
            assert b['english'].replace('{MACRO:FI}','FI')==a['english']
            changes.append(a['id'])
    assert changes==['DK4_MES_B199_R0037']
    new.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),
        one_source_FI_explicitly_marked_before_native_encoding=True,no_localized_wording_or_other_record_changed=True)
    save(OUTPUT,new);ROOT.mkdir(parents=True)
    save(ROOT/'one_exact_runtime_macro_markup_no_prose_change.json',dict(input=str(INPUT),input_sha256=sha(INPUT.read_bytes()),
        output=str(OUTPUT),output_sha256=sha(OUTPUT.read_bytes()),changed_records=changes,
        source_FI_kept_as_runtime_macro_not_literal_fixed_name=True,all31_logical_words_and_speakers_unchanged=True,
        no_ROM_or_emulator_or_review_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('One FI explicitly marked;all31 localized wordings unchanged. No formatting or release approval.')
