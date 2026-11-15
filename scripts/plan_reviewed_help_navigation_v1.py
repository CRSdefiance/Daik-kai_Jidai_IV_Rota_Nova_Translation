"""Reusable ordinary Help navigation planner;itinerary data replaces per-batch copied test code."""
import argparse
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['qualification','plan','itinerary','entry','out']:parser.add_argument('--'+key,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    qualification,plan,itinerary=map(load,[args.qualification,args.plan,args.itinerary])
    rom=Path(qualification['research_ROM']);assert sha(rom.read_bytes())==qualification['research_ROM_sha256']
    raw=NdsImage.open(rom).read_file('/COMMON/HELP.DK4');assert sha(raw)==plan['target_HELP_sha256']
    blocks=IlnkContainer.parse(raw).blocks;pages={}
    def page(topic):
        if topic in pages:return pages[topic]
        block=blocks[topic];cursor=0;visible='';links=[]
        for link in source_links(block):
            visible+=block[cursor:link['start']].decode('ascii')
            links.append(dict(id=link['topic_id'],label=link['label'],row=visible.count('\n'),column=len(visible.rsplit('\n',1)[-1])))
            visible+=link['label'];cursor=link['end']
        visible+=block[cursor:].rstrip(b'\0').decode('ascii')
        result=dict(topic_id=topic,visible_lines=visible.rstrip('\n').split('\n'),links=links)
        pages[topic]=result;return result
    inputs=load(args.entry);now=itinerary['start_frame'];current=0;history=[0];position=0
    assert inputs[-1]==dict(start=21001,duration=8,buttons=['X']) and now>=21400
    frames={0:now};captures={now};visits=[];remembered={};returns=[]
    for action in itinerary['actions']:
        if set(action)=={'remember'}:remembered[action['remember']]=(current,now);continue
        if set(action)=={'return_to'}:
            topic,frame=remembered[action['return_to']];assert current==topic
            returns.append(dict(kind=action['return_to'],topic=topic,frames=[frame,now]));continue
        if set(action)=={'key'}:
            button=action['key'];assert button in ['X','L','R']
            inputs.append(dict(start=now+1,duration=8,buttons=[button]));now+=160
            if button=='X':current=0;history=[0];position=0
            elif button=='L':assert position>0;position-=1;current=history[position]
            else:assert position+1<len(history);position+=1;current=history[position]
            captures.add(now);continue
        assert set(action)=={'open'};target=action['open'];p=page(current)
        choices=[l for l in p['links'] if l['id']==target];assert len(choices)==1,(current,target)
        link=choices[0];label=link['label'].strip();text=p['visible_lines'][link['row']];assert text.count(label)==1
        x=(text.index(label)+len(label)//2)*6+2;y=24+(link['row']-1)*16+5
        assert 0<=x<252 and 0<=y<164 and link['row']>0
        if p['links'][0]['id']!=target:inputs.append(dict(start=now+1,duration=8,buttons=[],touch=[x,y]));now+=160
        inputs.append(dict(start=now+1,duration=8,buttons=['A']));now+=160
        origin=current;current=target;history=history[:position+1]+[target];position+=1;assert len(history)<=16
        frames.setdefault(target,now);captures.add(now);visits.append(dict(origin=origin,target=target,frame=now,touch=[x,y]))
    assert set(itinerary['required_topics'])<=set(frames)
    new={p['topic_id'] for p in plan['pages']};observed=new&set(frames)
    args.out.mkdir();save(args.out/'inputs.json',inputs)
    save(args.out/'navigation_plan.json',dict(research_ROM=str(rom),research_ROM_sha256=qualification['research_ROM_sha256'],
        plan=str(args.plan),plan_sha256=sha(args.plan.read_bytes()),page_frames=frames,capture_frames=sorted(captures),
        return_pairs=returns,visited_links=visits,terminal_frame=now+1,observed_reviewed_topics=sorted(observed),offline_only_reviewed_topics=sorted(new-observed),
        controls_only_no_fixtures_state_injection_orbattery=True,requests_not_execution_receipts=True,actual_gameplay_proof_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [args.qualification,args.plan,args.itinerary,args.entry,Path(__file__)]}))
    print(dict(link_activations=len(visits),reviewed_pages_planned=len(observed),offline_only_pages=len(new-observed),terminal_frame=now+1))

if __name__=='__main__':main()
