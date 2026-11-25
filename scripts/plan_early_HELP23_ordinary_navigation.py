"""Ordinary stylus/button navigation through all25 reviewed Help pages; no injected state."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
OUT=ROOT/'ordinary_navigation_plan_v1'
if __name__=='__main__':
    assert not OUT.exists()
    plan_path=ROOT/'automatic_plans_v1.json';plan=load(plan_path)
    pages={p['topic_id']:p for p in plan['pages']}
    blocks=IlnkContainer.parse(Path(plan['research_resource']).read_bytes()).blocks
    # One unchanged Data Guide page connects the reviewed Faction Info article.
    raw=blocks[143];pieces=[];cursor=0;links=[];visible=''
    for link in source_links(raw):
        visible+=raw[cursor:link['start']].decode('ascii')
        row=visible.count('\n');column=len(visible.rsplit('\n',1)[-1])
        links.append(dict(id=link['topic_id'],label=link['label'],row=row,column=column))
        visible+=link['label'];cursor=link['end']
    visible+=raw[cursor:].rstrip(b'\0').decode('ascii')
    pages[143]=dict(topic_id=143,visible_lines=visible.rstrip('\n').split('\n'),links=links,unchanged_connector_not_new_editorial_credit=True)
    entry=ROOT/'preview_qualification_v1/ordinary_Help_index_entry_inputs.json'
    inputs=load(entry);now=21400;current=0;history=[0];position=0;visits=[];frames={0:now};returns=[];captures={now}
    def key(button):
        global now,current,history,position
        inputs.append(dict(start=now+1,duration=8,buttons=[button]));now+=160
        if button=='X':current=0;history=[0];position=0
        elif button=='L':
            assert position>0;position-=1;current=history[position]
        elif button=='R':
            assert position+1<len(history);position+=1;current=history[position]
        captures.add(now)
    def click(target):
        global now,current,history,position
        page=pages[current];choices=[l for l in page['links'] if l['id']==target];assert len(choices)==1
        link=choices[0];label=link['label'].strip();text=page['visible_lines'][link['row']]
        assert text.count(label)==1
        x=(text.index(label)+len(label)//2)*6+2;y=24+(link['row']-1)*16+5
        assert 0<=x<252 and 0<=y<164 and link['row']>0
        inputs.append(dict(start=now+1,duration=8,buttons=[],touch=[x,y]));now+=160
        inputs.append(dict(start=now+1,duration=8,buttons=['A']));now+=160
        origin=current;current=target;history=history[:position+1]+[target];position+=1
        assert len(history)<=16
        frames.setdefault(target,now);captures.add(now)
        visits.append(dict(origin=origin,target=target,frame=now,touch=[x,y]))
    click(1);click(2);key('L');click(3);click(4);click(5);key('X')
    click(1);click(6);click(7);first=now;click(202);click(184);key('L');click(7)
    returns.append(dict(kind='Rafael_existing202_back_link',topic=7,frames=[first,now]));key('X')
    click(1);click(6);click(8);key('X')
    click(1);click(6);click(9);first=now;click(211);click(9)
    returns.append(dict(kind='Hodram_new211_back_link',topic=9,frames=[first,now]));key('X')
    click(11);click(12);click(13);key('L');click(14);key('L');click(15);key('L');click(16)
    for topic in [17,18,19,20]:
        click(topic)
        if topic!=20:key('L')
    key('X');click(1);click(10);key('X');click(143);click(181);click(184);first=now;key('L');key('R')
    returns.append(dict(kind='native_L_R_history',topic=184,frames=[first,now]))
    assert set(p['topic_id'] for p in plan['pages'])<=set(frames)
    OUT.mkdir();save(OUT/'inputs.json',inputs)
    save(OUT/'navigation_plan.json',dict(plan=str(plan_path),plan_sha256=sha(plan_path.read_bytes()),
        entry_schedule=str(entry),entry_schedule_sha256=sha(entry.read_bytes()),page_frames=frames,
        visited_links=visits,return_pairs=returns,capture_frames=sorted(captures),terminal_frame=now+1,
        all25_reviewed_pages_planned=True,unreviewed_connector_pages=[143],no_fixtures_orstate_injection=True,
        requested_controls_not_execution_receipts=True,actual_gameplay_proof_pending=True,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Ordinary25-page Help schedule:',len(visits),'link activations;terminal',now+1,'capture frames',len(captures))
