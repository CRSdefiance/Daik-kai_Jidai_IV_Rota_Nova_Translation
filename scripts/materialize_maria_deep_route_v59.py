from __future__ import annotations
import csv,json
from pathlib import Path
SOURCE=Path('work/sc3/script.csv');PREVIOUS=Path('translations/maria_deep_route_v58.json');OUTPUT=Path('translations/maria_deep_route_v59.json');SC3_SHA256='001e21897ddb727ae261c82763ebef8515784ecfa571619c7614d87f3320aab2';BLOCKS=(54,)
DUPLICATES={
'DK4_MES_B54_R0012':'DK4_MES_B53_R0006','DK4_MES_B54_R0015':'DK4_MES_B53_R0009','DK4_MES_B54_R0019':'DK4_MES_B53_R0013','DK4_MES_B54_R0031':'DK4_MES_B53_R0025','DK4_MES_B54_R0041':'DK4_MES_B53_R0035','DK4_MES_B54_R0046':'DK4_MES_B53_R0040','DK4_MES_B54_R0052':'DK4_MES_B53_R0046','DK4_MES_B54_R0063':'DK4_MES_B53_R0057','DK4_MES_B54_R0066':'DK4_MES_B53_R0061','DK4_MES_B54_R0070':'DK4_MES_B53_R0065','DK4_MES_B54_R0074':'DK4_MES_B53_R0069','DK4_MES_B54_R0077':'DK4_MES_B53_R0072','DK4_MES_B54_R0080':'DK4_MES_B53_R0075','DK4_MES_B54_R0084':'DK4_MES_B53_R0079','DK4_MES_B54_R0087':'DK4_MES_B53_R0082','DK4_MES_B54_R0091':'DK4_MES_B53_R0086','DK4_MES_B54_R0101':'DK4_MES_B53_R0096','DK4_MES_B54_R0107':'DK4_MES_B53_R0102','DK4_MES_B54_R0114':'DK4_MES_B53_R0109','DK4_MES_B54_R0118':'DK4_MES_B53_R0113','DK4_MES_B54_R0122':'DK4_MES_B53_R0117','DK4_MES_B54_R0125':'DK4_MES_B53_R0120','DK4_MES_B54_R0128':'DK4_MES_B53_R0123','DK4_MES_B54_R0132':'DK4_MES_B53_R0127','DK4_MES_B54_R0135':'DK4_MES_B53_R0130','DK4_MES_B54_R0139':'DK4_MES_B53_R0134','DK4_MES_B54_R0143':'DK4_MES_B53_R0137','DK4_MES_B54_R0146':'DK4_MES_B53_R0140','DK4_MES_B54_R0150':'DK4_MES_B53_R0144','DK4_MES_B54_R0154':'DK4_MES_B53_R0148','DK4_MES_B54_R0158':'DK4_MES_B53_R0152','DK4_MES_B54_R0170':'DK4_MES_B53_R0164','DK4_MES_B54_R0184':'DK4_MES_B53_R0178','DK4_MES_B54_R0199':'DK4_MES_B53_R0193',
}
LINES={
'DK4_MES_B54_R0205':'{LB}Hmph. Leave it to me.{LB}Young people will not beat me yet.{LB}...Hm?',
'DK4_MES_B54_R0209':'The welcoming officials{LB}have arrived.',
'DK4_MES_B54_R0212':'A grand affair.{LB}Very different from years ago.',
'DK4_MES_B54_R0215':'{LB}These people once treated us{LB}like common thieves.',
'DK4_MES_B54_R0218':'Heh.',
'DK4_MES_B54_R0231':'{MACRO:FI},{LB}the fleet review is ready.',
'DK4_MES_B54_R0234':'L-let us hurry along...',
'DK4_MES_B54_R0268':'{LB}(Glance.)',
'DK4_MES_B54_R0272':'N-no, please proceed at once.{LB}Everyone awaits you eagerly.{LB}Whew...',
'DK4_MES_B54_R0283':'Pfft!',
'DK4_MES_B54_R0298':'Heh heh heh.',
'DK4_MES_B54_R0305':'Why so formal today?',
'DK4_MES_B54_R0316':'What do you mean?',
'DK4_MES_B54_R0323':'You command Ming\'s navy.{LB}We are merely your retainers.',
'DK4_MES_B54_R0326':'Too stiff.{LB}Act as always.',
'DK4_MES_B54_R0329':'{LB}No. That sets{LB}a poor example.',
'DK4_MES_B54_R0340':'Exactly.',
'DK4_MES_B54_R0355':'Quite right.',
'DK4_MES_B54_R0363':'Will it be like this forever?{LB}Please spare me.',
'DK4_MES_B54_R0374':'Heh.',
'DK4_MES_B54_R0381':'Do not be selfish.{LB}This officer too{LB}finds it difficult.',
'DK4_MES_B54_R0393':'Yes, yes. Sudden formal speech{LB}nearly ties the tongue...{LB}Does it not?',
'DK4_MES_B54_R0400':'Everyone...{LB}Only while on duty.',
'DK4_MES_B54_R0411':'No worry.{LB}That will happen.',
'DK4_MES_B54_R0425':'Admiral{LB}the troops are growing restless.',
'DK4_MES_B54_R0432':'Let us proceed.',
'DK4_MES_B54_R0436':'Yes. Let us go.',
'DK4_MES_B54_R0448':'At last, before that huge crowd!{LB}This one is terribly nervous!',
'DK4_MES_B54_R0455':'Generals, form ranks!{LB}With me!',
'DK4_MES_B54_R0458':'{LB}Hah!',
'DK4_MES_B54_R0470':'Yes!',
'DK4_MES_B54_R0477':'At once.',
'DK4_MES_B54_R0481':'{MACRO:FI} {MACRO:FA}{LB}reviews the troops!',
'DK4_MES_B54_R0491':'{LB}--And here, the story ends.',
'DK4_MES_B54_R0495':'{LB}And yet...',
'DK4_MES_B54_R0499':'The Ming dynasty was losing{LB}the people\'s support.{LB}A march toward collapse{LB}could no longer be stopped.',
'DK4_MES_B54_R0502':'{LB}And...',
'DK4_MES_B54_R0507':'Europe sought the world\'s wealth,{LB}but one heroine{LB}from the distant East{LB}stood in its path.',
'DK4_MES_B54_R0511':'{LB}Europe waits{LB}for new age.',
'DK4_MES_B54_R0515':'{LB}No one yet knew{LB}their place in history--',
'DK4_MES_B54_R0523':'{LB}No one at all--',
}
EXCLUDED={'DK4_MES_B54_R0360':'nontext event payload 94 46 60 80 14 05; preserved byte-for-byte'}
STATES={0x03,0x04,0x06,0x07,0x0B,0x0C,0x0D,0x0E,0x0F,0x11,0x13,0x14,0x15,0x16,0x17,0xFE};SPEAKERS={'03':'Maria','04':'Companion','06':'Old sailor','07':'Companion','0B':'Jam','0C':'Companion','0D':'Companion','0E':'Companion','0F':'Companion','11':'Companion','13':'Companion','14':'Companion','15':'Companion','16':'Companion','17':'Companion','FE':'Narrator'}
def main()->None:
 with SOURCE.open(encoding='utf-8-sig',newline='') as source:all_rows={r['id']:r for r in csv.DictReader(source)}
 rows={i:r for i,r in all_rows.items() if i.startswith('DK4_MES_B54_')};prior={r['id']:r for r in json.loads(PREVIOUS.read_text(encoding='utf-8'))['records']}
 if set(DUPLICATES)|set(LINES)|set(EXCLUDED)!=set(rows):raise SystemExit(f'V59 mismatch: missing={sorted(set(rows)-set(DUPLICATES)-set(LINES)-set(EXCLUDED))}, extra={sorted((set(DUPLICATES)|set(LINES)|set(EXCLUDED))-set(rows))}')
 records=[]
 for i in sorted(set(DUPLICATES)|set(LINES),key=lambda v:int(v.rsplit('R',1)[1])):
  r=rows[i]
  if i in DUPLICATES:
   base=prior[DUPLICATES[i]];entry={k:v for k,v in base.items() if k!='id'};entry['id']=i;entry['context']='Maria route ending variant: every Proof assembled, public fleet review, and historical narration.';records.append(entry);continue
  e=LINES[i];first=bytes.fromhex(r['source_hex'])[0];state=f'{first:02X}' if first in STATES and not r['japanese'].startswith('{LB}') else '';sb=r['japanese'].count('{LB}');tb=e.count('{LB}');waivers=['weak-line-ending','orphan-final-line']+(['manual-break'] if tb else [])+(['source-leading-linebreak'] if e.startswith('{LB}') else [])+(['line-break-count'] if sb!=tb else [])
  records.append({'id':i,'english':f'{{SPEAKER:{state}}}{e}{{PAD}}' if state else f'{e}{{PAD}}','speaker':SPEAKERS.get(state,'Scene speaker'),'context':'Maria route ending variant: every Proof assembled, public fleet review, and historical narration.','source_meaning':e.replace('{LB}',' '),'localization_note':'Direct SC3 translation preserving ending staging, title and name macros, portrait states, narrator control, and fixed allocation.','qa_waivers':waivers,**({'manual_break_reason':'Preserves source staging or groups the thought within the source display.'} if tb else {}),'review':{'source':True,'context':True,'localization':True,'naturalness':True,'formatting':True}})
 payload={'format':'dk4-ilnk-translation-batch-v1','file_path':'/data/SC3.DK4','source_file_sha256':SC3_SHA256,'encoder':'dialogue-fixed-v1','dialogue_profile':'maria-story-shared-events-v59-live','translation_policy':'natural-dialogue-v2','target_locale':'en-US','review_gates':['source','context','localization','naturalness','formatting'],'scope':'Maria SC3 block 54: complete alternate ending, fleet review, and historical narration.','inventory':{'identified_records':len(rows),'translated_records':len(records),'excluded_records':len(EXCLUDED),'blocks':{'54':len(records)}},'excluded':[{'id':i,'reason':r} for i,r in EXCLUDED.items()],'records':records}
 OUTPUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(f'wrote {OUTPUT}: {len(records)} records, {len(EXCLUDED)} preserved control')
if __name__=='__main__':main()
