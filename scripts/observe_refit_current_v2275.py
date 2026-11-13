"""Extend the read-only observer to exact direct Refit help payloads."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.town_trade_port_contextual_reference_v1 import current_entries
source=Path('scripts/observe_town_yard_context_v2156.py').read_text()
source=source.replace("ROOT=Path('work/analysis/town_yard_actual_v2156')","ROOT=Path('work/analysis/refit_actual_v2276')").replace('all_routes_combined_v2143_candidate.nds','all_routes_combined_v2171_candidate.nds')
old="  self.core,self.folder=core,Path(folder);self.folder.mkdir(parents=True,exist_ok=True)"
new=old+"\n  rom=NdsImage.open(ROM);entries=current_entries(rom.read_file('/COMMON/MESFILE.DK4'),rom.read_file('/__arm9__.bin'));self.help_payloads={entries[n].text:n for n in (*range(1247,1256),*range(1268,1290))};assert len(self.help_payloads)==31"
assert source.count(old)==1;source=source.replace(old,new)
start="    if not self.last or not 0<=self.last['ID']<3668:return"
end="    if modal and text!=b\"You can't sell any more ships!\":return"
a,b=source.index(start),source.index(end)+len(end)
replacement='''    if not 0x02000000<=v[5]<0x023FFE00:return
    ctx=v[4];assert 0x02000000<=ctx<0x023FFF80
    context=ct.string_at(self.wram+ctx-0x02000000,128);bounds=list(struct.unpack_from('<4I',context,4));candidate_text=ct.string_at(self.wram+v[5]-0x02000000,512).split(bytes(1))[0]
    direct_help=bounds[2]==168 and bounds[3]in(84,108)and candidate_text in self.help_payloads
    if direct_help:
     source_request=dict(frame=frame,ID=self.help_payloads[candidate_text],source='exact-current-direct-help-payload-and168pixel-context',original_last_request=self.last)
     modal=False;body=v[5];text=candidate_text
    else:
     if not self.last or not 0<=self.last['ID']<3668:return
     source_request=dict(self.last);modal=self.last['ID']==267
     if not modal and v[5]not in(0x0228E5A8,0x0228E5AA):return
     body=v[5]if modal else 0x0228E5A8;text=ct.string_at(self.wram+body-0x02000000,512).split(bytes(1))[0]
     if modal and text!=b"You can't sell any more ships!":return'''
source=source[:a]+replacement+source[b:]
source=source.replace("key=self.last['ID'],v[18],context[:32],text","key=source_request['ID'],v[18],context[:32],text").replace('self.last["ID"]','source_request["ID"]').replace('source_request=dict(self.last),PC=pc','source_request=source_request,direct_help_payload_match=direct_help,PC=pc')
exec(compile(source,__file__,'exec'),globals())
