"""Prepare six original-scene samples with one disclosed mood byte, preserving health."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/mood_comments_v982')
CASES={'CamillePositive':(9,2),'SeraPositive':(24,2),'CarloDejected':(19,2),
       'CaptainSilent':(1,2),'CaptainPanic':(1,2),'SeraPanic':(24,2)}
MOODS={'CamillePositive':0,'SeraPositive':0,'CarloDejected':4,'CaptainSilent':4,'CaptainPanic':5,'SeraPanic':5}

def main():
    prepared=[]
    names=['native_illness_critical_room_v976','native_illness_critical_fixture_v976',
           'run_illness_critical_adapter_v976','native_illness_critical_standoff_v976',
           'run_illness_critical_live_v976','navigate_illness_critical_v976','illness_critical_flags_v976']
    for name in names:
        s=Path('scripts')/(name+'.py');t=Path('scripts')/(name.replace('illness_critical','mood_comments').replace('v976','v982')+'.py')
        assert not t.exists();raw=s.read_bytes();text=raw.decode('utf-8')
        text=text.replace('illness_critical','mood_comments').replace('v976','v982').replace('v975','v981').replace('V976','V982').replace('V975','V981')
        if name.startswith('native_illness_critical_room'):
            lo=text.index('CASES=');hi=text.index('\n',lo);text=text[:lo]+'CASES='+repr(CASES)+text[hi:]
            text=text.replace('illness/near-death-panel','mood-panel')
        elif name.startswith('native_illness_critical_fixture'):
            lo=text.index('CONDITIONS=');hi=text.index('\n',lo);text=text[:lo]+'MOODS='+repr(MOODS)+text[hi:]
            text=text.replace('late_condition_only','late_mood_only').replace('status=CONDITIONS[label]','status=MOODS[label]')
            text=text.replace("assert arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')","assert arm[0x7E100:0x7E108]==bytes.fromhex('0600d0e51eff2fe1')\n    assert arm[0x7E0B4:0x7E0BC]==bytes.fromhex('0700d0e51eff2fe1')")
            text=text.replace('condition=get(0x7E100,obj);assert condition==0','physical=get(0x7E100,obj);mood=get(0x7E0B4,obj);assert physical==0 and mood in (1,2,3)')
            text=text.replace('obj-BASE+6','obj-BASE+7').replace('obj+6','obj+7').replace("'before':condition","'before':mood")
            text=text.replace('before[:6]+bytes([status])+before[7:]','before[:7]+bytes([status])+before[8:]')
            text=text.replace('verify(0x7E100,obj)==status','verify(0x7E0B4,obj)==status and verify(0x7E100,obj)==0')
            text=text.replace('late_condition_fixture','late_mood_fixture').replace("'source_condition':condition,'fixture_condition':status,'condition_address'","'source_mood':mood,'fixture_mood':status,'mood_address'")
            text=text.replace('only_condition_byte6_changes_all_other4MiB_exact','only_mood_byte7_changes_all_other4MiB_including_physical_condition_exact')
            text=text.replace('no_earned_mood_comments_condition_or_recovery_claim','no_earned_mood_or_recovery_claim')
            text=text.replace('late condition tag','late mood tag')
        elif name.startswith('run_illness_critical_adapter'):
            text=text.replace('illness-critical','mood-comments').replace('declared illness/near-death condition4/5','declared mood0/4/5')
            text=text.replace('physical-condition bytes','mood bytes;physical health remains unchanged')
        elif name.startswith('run_illness_critical_live'):
            text=text.replace('illness-critical','mood-comments').replace('late_condition4_5','late_mood0_4_5')
        elif name.startswith('navigate_illness_critical'):
            text=text.replace('late_condition_only','late_mood_only').replace('room_or_condition_fixture','room_or_mood_fixture')
        elif name=='illness_critical_flags_v976':
            text=text.replace('mood_comments_layout_v974','mood_comments_layout_v980')
        ast.parse(text,filename=str(t));prepared.append((s,t,raw,text))
    ROOT.mkdir(parents=True,exist_ok=True);records=[]
    for s,t,raw,text in prepared:
        with t.open('x',encoding='utf-8') as f:f.write(text)
        assert s.read_bytes()==raw
        records.append({'source':str(s),'source_sha256':sha(raw),'source_after_sha256':sha(s.read_bytes()),'successor':str(t),'successor_sha256':sha(t.read_bytes()),'source_unchanged':True})
    save(ROOT/'actual_tools_provenance.json',{'files':records,'all_replacements_and_syntax_preflighted_before_output':True,
        'physical_condition_zero_preserved_only_mood_byte7_changes_after_Deck_opens':True,
        'cases':CASES,'moods':MOODS,'actual_gameplay_pending':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('Seven historical tools unchanged;six disclosed mood0/4/5 samples prepared.')

if __name__=='__main__':main()
