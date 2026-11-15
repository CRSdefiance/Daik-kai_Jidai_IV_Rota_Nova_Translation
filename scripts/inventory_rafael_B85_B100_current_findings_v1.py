"""Bind six current choice captions andspecific remaining-text/glyph defects after sealed drafts."""
import re,struct
from pathlib import Path
from dk4tool.dialogue.reviewed_choice_object_v2 import labels,count_and_base
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael_B85_B100_current_20261105')
SEALED=Path('work/analysis/Rafael_B85_B100_clean_drafts_20261105/261_source_meanings_andindependent_drafts_v1.json')

if __name__=='__main__':
    target=ROOT/'current_choice_andglyph_findings_v1.json';assert not target.exists()
    current=load(ROOT/'current_effective.json');drafts=load(SEALED)
    assert drafts['source_meanings_anddrafts_sealed_before_current_story_extraction']
    speech=[r for g in current['groups'] for r in g['records']];choices=[]
    for row in drafts['records']:
        if row['kind']!='typed-choice-label':continue
        group=next(g for g in current['groups'] if g['block']==row['block'])
        mapping=next(c for c in group['command_map'] if c['source_offset']==row['source_command_offset'])
        source,raw=map(bytes.fromhex,[mapping['source_hex'],mapping['current_hex']])
        assert source.hex()==row['source_choice_object_hex'] and mapping['word']==0x2100
        values=labels(raw);count,base=count_and_base(raw);index=row['source_index']
        assert count==2 and values[index].decode('cp932')
        offset=mapping['current_offset']+base+struct.unpack_from('<H',raw,2+index*2)[0]
        choices.append({**row,'source_reference':row['source_reference'],
            'current_reference':dict(file_path=current['file_path'],block=row['block'],command_offset=mapping['current_offset'],
                offset=offset,source_index=index,length=len(values[index])+1),
            'current_hex':values[index].hex(),'current_choice_object_hex':raw.hex(),
            'current_English':values[index].decode('cp932'),'current_English_now_exposed':True,
            'earlier_English_unconsulted':False,'source_meaning_anddraft_precede_old_English_comparison':True})
    fullwidth=[];Japanese=[];aliases=[]
    for row in speech:
        text=row['current_effective_text']
        latin=[dict(index=i,character=c,codepoint=f'U+{ord(c):04X}') for i,c in enumerate(text) if '\uff21'<=c<='\uff3a' or '\uff41'<=c<='\uff5a']
        punctuation=[dict(index=i,character=c,codepoint=f'U+{ord(c):04X}') for i,c in enumerate(text) if c=='\uff1f']
        if latin or punctuation:fullwidth.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            current_hex=row['current_hex'],effective_hex=row['current_effective_hex'],Latin=latin,punctuation=punctuation))
        if re.search('[\u3040-\u30ff\u3400-\u9fff]',text):Japanese.append(dict(id=row['id'],current_reference=row['current_reference'],effective_hex=row['current_effective_hex']))
        if row['current_catalogue_selected']:aliases.append(row['id'])
    assert len(choices)==6 and len(speech)==255
    assert [r['id'] for r in Japanese]==[f'DK4_MES_B91_R{n:04d}' for n in [5,14,28,35,43,51,59,62,70,77]]
    assert sum(len(r['Latin']) for r in fullwidth)==4 and sum(bool(r['Latin']) for r in fullwidth)==3
    Japanese_IDs={r['id'] for r in Japanese}
    assert sum(len(r['punctuation']) for r in fullwidth if r['id'] not in Japanese_IDs)==6
    assert sum(len(r['punctuation']) for r in fullwidth if r['id'] in Japanese_IDs)==2
    save(target,dict(choices=choices,current_fullwidth_findings=fullwidth,untranslated_current_source_speeches=Japanese,
        fullwidth_questionmarks_in_English=6,legitimate_questionmarks_in_remaining_Japanese=2,
        exact_catalogue_selected_current_IDs=aliases,
        concrete_contextual_findings=[
            dict(id='DK4_MES_B88_R0065',finding='The current asks howMeihua canfaceJulian. The source saysJulian cannotfaceMeihua;restore the correct embarrassed speaker.'),
            dict(id='DK4_MES_B93_R0073',finding='Emilio’s current My treat? reverses thepayer. The source asks whetherRafael ispaying;Your treat? mustagree withRafael’s following My treat.'),
            dict(id='DK4_MES_B97_R0028',finding='The source’s passive identity-exposure clause applies toan exposed ninja. The current instead sayswitnesses who seetheface mustdie. Preserve the source subject ratherthan invent thatvictim reversal.'),
            dict(id='DK4_MES_B100_R0038',finding='The current asserts theamber-shining place asfact. The source explicitly introduces itashearsay.'),
            dict(id='DK4_MES_B100_R0045',finding='The speaker doesnotknowwhat theplaceis. Nobody knows expands hispersonal uncertainty into anunsupported globalfact.'),
            dict(id='DK4_MES_B90_R0035',finding='Restore Rafael’s personal,conditional future promise;the current third-person allocation canreadas anactual assignment now.'),
            dict(id='DK4_MES_B91_R0091',finding='The source namesFernando inthenull-actor reward panel. His luck hides thespecified recipient;the Spirit panel112 hasthesame defect.'),
            dict(id='DK4_MES_B86_R0147',finding='Review withthe preceding greeting:Good tosee you isfollowed byDo notthankme. The localized reply mustrespond tothe greeting actuallyretained.'),
        ],
        all_fresh_formatting_names_terms_native_visual_gameplay_andintegration_still_pending=True,
        no_new_editorial_completion_credit=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [ROOT/'current_effective.json',SEALED,Path(__file__)]}))
    print('Boundsix current captions;foundten untranslated speeches,four full-width Latin letters/three speeches andsix questionmarks;contextual errors saved.')
    for row in choices:print(row['id'],repr(row['current_English']))
