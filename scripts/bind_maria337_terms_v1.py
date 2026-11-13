"""Bind two item labels and unchanged installed Help/story terminology."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.meaning_maria337_clean_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string

def main():
    out=ROOT/'scoped_terms_reference_v1.json'; assert not out.exists()
    currentpath=ROOT/'current_v1/current_effective.json'; runtime=load(currentpath)['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3); assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    itempath=Path('translations/all_item_names_arm9_v1.json')
    labels={r['offset']:r for r in load(itempath)['records'] if 'english' in r}; items=[]
    for offset,japanese,english in [(1176304,'儀式用の小刀','Ceremonial Knife'),(1176472,'太陽紋の鞘','Sun-Crest Sheath')]:
        before=string(clean,struct.unpack_from('<I',clean,offset)[0]); after=string(ctx.raw,struct.unpack_from('<I',ctx.arm,offset)[0])
        assert before['text']==japanese and after['text']==labels[offset]['english']==english
        items.append(dict(pointer_field_offset=offset,source=before,current=after,registered_record=labels[offset]['id'],
            source_field_hex=clean[offset:offset+4].hex(),current_field_hex=ctx.arm[offset:offset+4].hex()))
    helppath=Path('translations/help_shipyard_sea59_integrated_final_review_v1.json'); helpdoc=load(helppath)
    assert helpdoc['all59_individual_five_gates_pass']; resource=ctx.image.read_file(helpdoc['file_path']); helprows=[]
    for number in [59,66,83]:
        row=next(r for r in helpdoc['records'] if r['topic_id']==number); assert all(row['review'].values())
        refs=[]
        for old in row['planned_stored_pages']:
            raw=bytes.fromhex(old['exact_stored_hex']); at=struct.unpack_from('<I',resource,old['offset_table_slot'])[0]
            assert resource[at:at+len(raw)]==raw,(number,at)
            refs.append(dict(block=old['block'],offset_table_slot=old['offset_table_slot'],current_archive_offset=at,
                exact_stored_hex=raw.hex(),prior_reference=old,current_page_byte_exact=True))
        helprows.append(dict(id=row['id'],source_reference=row['source_reference'],source_hex=row['source_hex'],
            source_Japanese=row['source_Japanese_with_link_IDs'],english=row['english'],review=row['review'],current_stored_pages=refs))
    storypath=Path('work/Maria_B96_B124_clean_20261109/registered_story_terms_reference_v1.json'); story=load(storypath)
    anchor=next(r for r in story['anchors'] if r['term']=='Proofs of Conquest')
    assert all(anchor['review'].values()); blocks=IlnkContainer.parse(ctx.image.read_file('/data/SC3.DK4')).blocks
    ref=anchor['current_stored_reference']; raw=bytes.fromhex(ref['exact_stored_hex']); block=blocks[ref['block']]
    assert sha(block)==anchor['exact_current_complete_block_sha256'] and block[ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0'
    assert sha(ctx.arm)==story['runtime']['ARM9_sha256'] and sha(ctx.common)==story['runtime']['COMMON_sha256']
    prior153path=Path('translations/maria_B73_B95_scoped_names_final_v1.json'); prior153=next(r for r in load(prior153path)['records'] if r['actor_ID']==153)
    assert all(prior153['review'].values()) and prior153['english']=='Sailor'
    save(out,dict(runtime=runtime,items=items,HELP_file_path=helpdoc['file_path'],current_HELP_sha256=sha(resource),
        exact_current_HELP_pages=helprows,HELP_archive_as_a_whole_not_claimed_unchanged=True,
        prose_UI_terms={'海兵詰所':'Quarters','武装砲台':'Battery','砲台':'Battery','積荷倉庫':'Cargo','物資倉庫':'Supplies',
            '地方艦隊':'regional fleet','操帆手':'Sail Handler'},full_Proof_term=story['full_Proof_term'],
        full_Proof_exact_current_anchor=anchor,prior_linguistic_andnative_lookup_proof_reused_not_fresh_gameplay=True,
        role153_prior_scoped_review=dict(path=str(prior153path),sha256=digest(prior153path),id=prior153['id'],
            english=prior153['english'],localization_note=prior153['localization_note'],
            actual_consumers_remain_Sailor_andRetainer_not_interchangeable=True),
        terms_andprior_alias_reference_only_not_new_font_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [currentpath,itempath,helppath,storypath,prior153path,Path(__file__)]}))
    print('Bound Ceremonial Knife,Sun-Crest Sheath,three byte-exact installed Help articles,Proof anchor andprior Sailor/Retainer distinction.')

if __name__=='__main__':main()
