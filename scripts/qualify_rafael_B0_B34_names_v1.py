"""Review scoped labels and qualify three exclusive middle-name text repairs."""
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save
from scripts.bind_rafael_B0_B34_terms_v1 import OUT as TERMS
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT


BOUND = ROOT/'native_names_v1.json/names.json'
LABELS = Path('translations/rafael_B0_B34_scoped_names_review_v1.json')
OUT = ROOT/'owned_middle_fields_v1'
REASONS = {
 0:'Retain approved Rafael Castor; his battle orders, moral growth and offers of help consistently identify the protagonist.',
 4:'Retain Janus Pasar, matching the source name and his practical battle-stations and royal-report advice.',
 5:'Retain Claudio Manaus and source nickname Clau in dialogue; preserve his bluster, jokes and eagerness without changing identity.',
 6:'Retain Julio Erneco; the source identification and wry older-crew voice agree, without a new family claim.',
 7:'Retain Cristina Erneco, the established name used in the current progressive and full forms; her intervention belongs to Cristina.',
 8:'Retain Arcadius Eudoxios on the nameplate and Arcadius Eirene Eudoxios in the catalogue; the source itself distinguishes the optional middle component.',
 12:'Retain Yukihisa Shiraki and full Yukihisa Genjo Shiraki; the source supplies all components and his polite address to Al creates no Lord rank.',
 13:'Retain Cesare Tony as the established readable rendering of the clean name; his fearful pirate reaction remains his own.',
 16:'Retain Gerhard Adernkatz, preserving the source identity and the explicitly established former teacher of Vels.',
 17:'Retain Al Shin and full Al Ferid Shin, preserving the source components without adding a title to the polite Al address.',
 19:'Retain Carlo Sinat, the source-bound crew member delivering the readiness check.',
 20:'Retain Fernando Dias with the previously corrected ASCII initial; his swaggering response requires no new name adaptation.',
 23:'Retain Manuel Almeida, matching the source identity of the reflective sailor-poet rather than inventing an occupation label as his name.',
 25:'Retain Yifa Sol, the established phonetic rendering of the source name in both consumers.',
 27:'Retain Aziza Nurennahar, explicitly introduced in her retreat and used consistently through her recruitment; no romantic relationship is added.',
 30:'Retain Dinis Albuquerque and render the clean middle component デ as ASCII de in Dinis de Albuquerque. Preserve the full-name distinction rather than dropping the particle.',
 31:'Retain Pedro Valdes and full Pedro de Valdes, preserving the source particle and his explicit self-identification in the threat.',
 35:'Retain Fernan Silveira, including the already accepted ASCII initial; Rafael uses Fernan and other speakers use Silveira as in source.',
 36:'Retain Geronimo Espinosa and full Geronimo de Espinosa, preserving the source components of the hostile fleet leader.',
 37:'Retain Abraham Uddin and full Abraham Ibn Uddin; the source already supplies the middle component, without an invented father\'s identity or royal claim.',
 39:'Retain Duarte Pereira and full Duarte Lopes de Pereira. Source dialogue itself supports both Governor and Admiral addresses in their respective lines.',
 40:'Retain Antony Kuhn on the nameplate. Adapt clean フォン as von in the full Antony von Kuhn; the old Fong is a poor phonetic match and its full-width F is inconsistent. This is an editorial Latin rendering, not a claim of official Latin spelling or noble biography.',
 41:'Retain Sojin Kurushima, preserving the source name of the commander boasting about iron-armored ships.',
 48:'Retain Simon Linares, the established source-matching name of the officer ordering the attack on Portuguese rebels.',
 49:'Retain Alonso Rosa and full Alonso de Rosa, preserving the source particle and the officer\'s formation order.',
 59:'Retain Garcia Oviedo and render clean デ as ASCII de in Garcia de Oviedo; the untranslated particle is text in a player-facing full name.',
 61:'Retain Vels Granat and full Vels Wilhelm Granat, matching the source components of Gerhard\'s former pupil without inventing a new kinship.',
 62:'Retain Jacks Bloom, the established phonetic identity of the guild thief; do not simplify it to Jack or invent a different nationality.',
 63:'Retain Julian Vermeer, preserving the source traitor\'s distinct identity from both Julio and the separate Julian Lopes.',
 65:'Retain the approved Plett Perrault correction consistently in the labels and the newly reviewed arrest speech.',
 69:'Retain Peralonso Aguirre, matching the clean individual name rather than substituting an unrelated historical person.',
 70:'Retain approved Zaganos Bey, including the previous surname correction; preserve it in the challenge and arrest outcome.',
 71:'Retain William Clive, the established source-matching name, without diagnosing his shrill behavior or changing his identity.',
 151:'Retain Sailor for the clean progressive role 水夫 and Retainer for the separate catalogue 配下. Do not promote the subordinate to an invented naval rank.',
 153:'Retain Sailor on the nameplate and Retainer in the catalogue; Aziza\'s shouting crew are source subordinates, not a new named officer or an inferred nationality label.',
 176:'Retain Privateers for the source 私掠艦隊. Their pirate-like threat does not justify changing the explicit fleet category or adding a personal name.',
 183:'Retain Angel, explicitly called by Aziza before the maneuver and later leading the mutiny.',
 184:'Retain Snake, explicitly assigned command and later participating in the mutiny; do not turn the nickname into a new rank.',
 185:'Retain Dandy, explicitly addressed during gun readiness and speaking with a more formal register before the mutiny.',
}


def main():
    assert not OUT.exists() and not LABELS.exists()
    bound, terms = map(load,(BOUND,TERMS))
    runtime=bound['runtime']; assert terms['runtime']==runtime and bound['actors']==sorted(REASONS)
    fields={r['actor_ID']:r['source_andcurrent_fields'] for r in terms['scoped_actor_fields']}
    old={(r['actor_ID'],r['consumer']):r for r in bound['current_names']['rows']}
    source={(r['actor_ID'],r['consumer']):r for r in bound['clean_names']['rows']}
    changes={30:('デ','de'),40:('Ｆong','von'),59:('デ','de')}
    records=[]
    for actor,reason in REASONS.items():
        forms={consumer:old[actor,consumer]['text'] for consumer in ('progressive-nameplate','full-catalogue')}
        if actor in changes:
            before,after=changes[actor]
            assert forms['full-catalogue'].count(before)==1 and before not in forms['progressive-nameplate']
            forms['full-catalogue']=forms['full-catalogue'].replace(before,after)
        assert all(text.isascii() for text in forms.values())
        records.append(dict(actor_ID=actor,source_andcurrent_fields=fields[actor],
            source_consumers=[source[actor,c] for c in forms],current_consumers=[old[actor,c] for c in forms],
            approved_forms=forms,decision='revision' if actor in changes else 'retention',finding=reason,
            localization_note=reason,review=dict(source=True,context=True,localization=True,naturalness=True,formatting=False)))
    save(LABELS,dict(translation_policy='natural-dialogue-v2',target_locale='en-US',runtime=runtime,records=records,
        source_ARM9_sha256=bound['clean_ARM9_sha256'],name_revisions=3,justified_retentions=36,
        original_getters_bound=True,native_rendering_andvisual_review_pending=True,new_credit=0,
        publisher_name_corroboration=dict(url='https://www.gamecity.ne.jp/products/products/ee/new/dai4/dai4_06.htm',
            Japanese='アントニー・フォン・クーン',scope='Original publisher rival introduction confirms Japanese name and Dutch merchant context. It does not supply an official Latin spelling; von is a source-based editorial adaptation.'),
        evidence={str(p):digest(p) for p in (BOUND,TERMS,Path(__file__))}))
    arm=NdsImage.open(runtime['candidate']).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    sections=MainCodeFile(arm,BASE).sections
    payload=bytes(sections[3].data[:-48]); assert len(payload)==123264
    staged=arm.find(bytes(sections[3].data)); assert staged>=0
    table=struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE
    proposal=[]
    for actor,(_,target) in changes.items():
        component=next(r for r in fields[actor] if r['column']==8)
        current,jp=component['current'],component['source']
        pointer,field=current['pointer'],current['field_offset']; before=bytes.fromhex(current['hex'])
        at=staged+pointer-POOL if POOL<=pointer<POOL+len(payload) else pointer-BASE
        assert arm[at:at+len(before)+1]==before+b'\0' and len(target)<=len(before)
        owners=[]
        for ident in range(207):
            for column in (0,4,8):
                where=table+32*ident+column; p=struct.unpack_from('<I',arm,where)[0]
                if pointer<=p<pointer+len(before):
                    owners.append(dict(actor=ident,column=column,pointer=p,field_offset=where))
        refs=[dict(offset=i,pointer=struct.unpack_from('<I',arm,i)[0]) for i in range(0,len(arm)-3,4)
              if pointer<=struct.unpack_from('<I',arm,i)[0]<pointer+len(before)]
        assert owners==[dict(actor=actor,column=8,pointer=pointer,field_offset=field)]
        assert refs==[dict(offset=field,pointer=pointer)]
        reviewed=next(r for r in records if r['actor_ID']==actor)
        proposal.append(dict(actor=actor,column=8,table_field_offset=field,pointer=pointer,physical_offset=at,
            source_hex=before.hex(),target_hex=target.encode().ljust(len(before),b'\0').hex(),owned_bytes=len(before),
            current_text=current['text'],target_text=target,source_clean_component=dict(column=8,
                source_ARM9_field_offset=jp['field_offset'],pointer=jp['pointer'],offset=jp['pointer']-BASE,
                hex=jp['hex'],text=jp['text']),reason=reviewed['finding'],review=reviewed['review'],
            owners=owners,aligned_ARM9_references=refs,following16_hex=arm[at+len(before):at+len(before)+16].hex()))
    config=dict(format='dk4-owned-name-fields-proposal-v2',runtime=runtime,fields=proposal,
        clean_name_fields=str(LABELS),clean_name_fields_sha256=digest(LABELS),new_credit=0)
    target,proof=plan_arm9_name_fields(arm,config,clean)
    assert proof['complete_parent_inverse_exact'] and proof['all_unowned_ARM9_bytes_sections_pointer_tables_andallocations_exact']
    OUT.mkdir(); (OUT/'proposed_ARM9_RESEARCH_ONLY.bin').write_bytes(target)
    save(OUT/'proposal.json',config)
    save(OUT/'qualification.json',dict(**proof,proposal=str(OUT/'proposal.json'),proposal_sha256=digest(OUT/'proposal.json'),
        no_ROM_created=True,native_names_andglyphs_pending=True,new_credit=0))
    print('Reviewed 39 scoped names; qualified three exclusive middle fields:',proof['changed_bytes'],'changed bytes.')


if __name__=='__main__':
    main()
