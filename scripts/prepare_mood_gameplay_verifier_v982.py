"""Prepare exact mood, silence, symbol and alignment checks from the preserved verifier."""
import ast
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

def main():
    s=Path('scripts/verify_illness_critical_gameplay_v976b.py');raw=s.read_bytes();text=s.read_text(encoding='utf-8')
    t=Path('scripts/verify_mood_comments_gameplay_v982.py');assert not t.exists()
    text=text.replace('illness_critical','mood_comments').replace('v976','v982').replace('v975','v981').replace('mood_comments_layout_v974','mood_comments_layout_v980')
    a=text.index('SPECS=');b=text.index('\n\n',a)
    specs={'CamillePositive':(1835,9,False,0),'SeraPositive':(1845,24,False,0),'CarloDejected':(1853,19,False,4),
           'CaptainSilent':(1855,1,True,4),'CaptainPanic':(1868,1,True,5),'SeraPanic':(1871,24,False,5)}
    text=text[:a]+'SPECS='+repr(specs)+text[b:]
    text=text.replace('late_condition_fixture','late_mood_fixture')
    text=text.replace("late['fixture_condition']==status and late['source_condition']==0","late['fixture_mood']==status and late['source_mood'] in (1,2,3)")
    text=text.replace('only_condition_byte6_changes_all_other4MiB_exact','only_mood_byte7_changes_all_other4MiB_including_physical_condition_exact')
    text=text.replace('room_or_condition_fixture','room_or_mood_fixture')
    text=text.replace('assert get(0x7E100,obj)==status','assert get(0x7E0B4,obj)==status and get(0x7E100,obj)==0')
    text=text.replace('actual_physical_condition_ID=status','actual_physical_condition_ID=0,actual_mood_ID=status')
    text=text.replace('condition_is_disclosed_fixture_not_earned_acquisition','mood_is_disclosed_fixture_not_earned_acquisition')
    a=text.index('        extras=');b=text.index('        for line,column,name',a)
    extras={'CamillePositive':[(1,0,'delete-complete-I-continuation')],
        'SeraPositive':[(0,24,'delete-now-final-w')],
        'CarloDejected':[(1,0,'delete-aligned-Oh-after19cell-row'),(1,30,'delete-myself-final-f')],
        'CaptainSilent':[(0,1,'delete-middle-silence-dot')],
        'CaptainPanic':[(1,0,'delete-complete-at-continuation')],
        'SeraPanic':[(0,2,'delete-comic-dollar'),(0,3,'delete-comic-star')]}
    text=text[:a]+'        extras='+repr(extras)+'\n'+text[b:]
    a=text.index('    assert len(holds)==12');b=text.index('    sheet=Image.new',a)
    text=text[:a]+'''    assert len(holds)==12 and len(returns)==6 and len(controls)==26
    assert layout(rows[1835]['english'])==["I'm in top form!","I feel like I can do anything!"]
    assert layout(rows[1845]['english'])==['I feel fantastic right now!']
    assert layout(rows[1853]['english'])==['"Mutter, mutter..."','Oh, I was just talking to myself...']
    assert list(map(len,layout(rows[1853]['english'])))==[19,35]
    assert layout(rows[1855]['english'])==['...'] and rows[1855]['nonverbal_only']
    assert layout(rows[1868]['english'])==['No! I have to stay calm','at a time like this!']
    assert layout(rows[1871]['english'])==['@#$*!!'] and rows[1871]['nonverbal_only']
'''+text[b:]
    text=text.replace('ASCII_I1810_three_row36cell1811_personal_captain1816_complete1822_retained1825_and_Sera1832_pass',
        'complete_I1835_ASCII_I1845_quoted19_and35cell1853_pure_silence1855_self_calming1868_comic1871_pass')
    a=text.index("        'scope':'Six separate");b=text.index("\n        'producer_sha256'",a)
    text=text[:a]+"        'scope':'Six separate V981 fresh cold boots:mood0 Camille9 ID1835 and Sera24 ASCII-I1845;mood4 Carlo19 quoted self-talk1853 (19cell quote,35cell aligned reply) and genuine captain1 pure silence1855;mood5 genuine captain1 personal self-calming1868 and Sera24 six comic symbols1871. Two complete native bitmap/actual RGB holds and normal return per case. Disclosed room assignment follows observed original combat0/1;one mood byte7 is inserted after Deck opens with physical health0 and all other RAM exact. Two coordinate approaches remain. No savestate,actor/captain identity or battle-mode/outcome/text/code injection,earned mood/recruitment/refit,full-route or hardware claim. Other33 entries have complete source/native font evidence,not individual actual visits.',"+text[b:]
    text=text.replace('Six targeted condition4/5 scenes','Six targeted mood0/4/5 scenes').replace('Twelve complete illness/near-death holds','Twelve complete mood/panic holds')
    ast.parse(text)
    with t.open('x',encoding='utf-8') as f:f.write(text)
    assert s.read_bytes()==raw
    save('work/analysis/mood_comments_v982/gameplay_verifier_provenance.json',{'source':str(s),'source_sha256':sha(raw),
        'source_after_sha256':sha(s.read_bytes()),'successor':str(t),'successor_sha256':sha(t.read_bytes()),'source_unchanged':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'actual_gameplay_pending':True})
    print('Mood actual verifier prepared;six cases,twelve holds,26 negative controls.')

if __name__=='__main__':main()
