"""Bind live room/skill aliases, complete installed Help pages and exact named-item fields."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.qualify_rafael351_item_and_UI_terms_v1 import string


def main():
    out=ROOT/'scoped_terms_reference_v1.json';assert not out.exists()
    currentpath=ROOT/'current_v1/current_effective.json';runtime=load(currentpath)['runtime']
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=3);assert ctx.receipt()==runtime
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    activepath=Path('work/analysis/HELP_active_skill_labels_20261105/active_terms_binding_v2.json');active=load(activepath)
    helppath=Path('translations/help_deck30_Coerce33_active_terms_final_review_v1.json');helpdoc=load(helppath)
    resource=ctx.image.read_file(helpdoc['file_path']);help_rows=[];rooms=[]
    specs=[(111,'個室','Cabin','Private Cabin'),(112,'娯楽室','Lounge','Recreation Room'),
        (113,'材木室','Lumber','Lumber Room'),(114,'診察室','Sickbay','Sickbay'),
        (115,'調理室','Galley','Galley'),(116,'飼育室','Nursery','Nursery'),
        (117,'礼拝室','Chapel','Chapel'),(121,'副官室','Mate',"First Mate's Office")]
    for topic,japanese,short,expanded in specs:
        old=next(r for r in active['active_room_references'] if r['source_label']['Japanese']==japanese)
        field=old['pointer_field'];sp,cp=struct.unpack_from('<I',clean,field)[0],struct.unpack_from('<I',ctx.arm,field)[0]
        before,after=string(clean,sp),string(ctx.raw,cp)
        assert before['text']==japanese and after['text']==old['current_text']==short and cp==old['current_pointer']
        row=next(r for r in helpdoc['records'] if r['topic_id']==topic)
        assert row['heading']==expanded and all(row['review'].values())
        refs=[]
        for ref in row['planned_stored_pages']:
            raw=bytes.fromhex(ref['exact_stored_hex']);at=struct.unpack_from('<I',resource,ref['offset_table_slot'])[0]
            assert resource[at:at+len(raw)]==raw
            refs.append(dict(offset_table_slot=ref['offset_table_slot'],current_archive_offset=at,exact_stored_hex=raw.hex(),current_page_byte_exact=True))
        rooms.append(dict(Japanese=japanese,pointer_field=field,source=before,current=after,short_label=short,prose_label=expanded,
            source_field_hex=clean[field:field+4].hex(),current_field_hex=ctx.arm[field:field+4].hex(),
            exact_existing_active_alias_rebound_to_own_current_RAM=True))
        help_rows.append(dict(id=row['id'],topic_id=topic,heading=expanded,english=row['english'],source_reference=row['source_reference'],
            source_hex=row['source_hex'],review=row['review'],current_stored_pages=refs))
    old=next(r for g in active['active_label_tables'] if g['group']=='Skills' for r in g['records'] if r['Japanese']=='説得力')
    field=old['pointer_field'];sp,cp=struct.unpack_from('<I',clean,field)[0],struct.unpack_from('<I',ctx.arm,field)[0]
    before,after=string(clean,sp),string(ctx.raw,cp)
    assert before['text']=='説得力' and after['text']==old['English']=='Speech' and cp==old['current_pointer']
    skill=dict(pointer_field=field,source=before,current=after,exact_active_native_label_not_inactive_Persuasion=True)
    itempath=Path('translations/all_item_names_arm9_v1.json');itemrow=next(r for r in load(itempath)['records'] if r['offset']==1175272)
    def bound(field,japanese,english):
        sp,cp=struct.unpack_from('<I',clean,field)[0],struct.unpack_from('<I',ctx.arm,field)[0]
        source,current=string(clean,sp),string(ctx.raw,cp)
        assert source['text']==japanese and current['text']==english
        return dict(pointer_field=field,source=source,current=current,source_field_hex=clean[field:field+4].hex(),
            current_field_hex=ctx.arm[field:field+4].hex(),static_reference_andown_RAM_not_new_widget_gameplay=True)
    assert itemrow['english']=='Silla Gold Crown'
    crown=bound(1175272,'新羅の金冠','Silla Gold Crown');crown['registered_item_record']=itemrow['id']
    ruinpath=Path('translations/hodram_B171_B190_scoped_names_andterms_v1.json')
    prior=next(r for r in load(ruinpath)['records'] if r['english']=='Tomb of King Muryeong')
    assert all(prior['review'][k] for k in ['source','context','localization','naturalness'])
    ruin=bound(prior['typed_field']['field_offset'],'武寧王陵','Tomb of King Muryeong')
    city=bound(1195828,'京城','Seoul')
    goods=[]
    for japanese,english in [('小麦','Wheat'),('バナナ','Bananas'),('トマト','Tomatoes')]:
        needle=japanese.encode('cp932')+b'\0';ats=[];start=0
        while (at:=clean.find(needle,start))>=0:ats.append(at);start=at+1
        assert len(ats)==1,(japanese,ats)
        pointer=struct.pack('<I',BASE+ats[0]);fields=[];start=0
        while (at:=clean.find(pointer,start))>=0:
            if at%4==0:fields.append(at)
            start=at+1
        assert len(fields)==1,(japanese,fields)
        goods.append(bound(fields[0],japanese,english))
    save(out,dict(runtime=runtime,room_labels=rooms,active_Speech_skill=skill,items=[crown],ruins=[ruin],cities=[city],goods=goods,
        HELP_file_path=helpdoc['file_path'],current_HELP_sha256=sha(resource),exact_current_HELP_pages=help_rows,
        HELP_archive_as_a_whole_not_claimed_unchanged=True,source_tutorial_effects_preserved_not_rewritten_from_different_Help_articles=True,
        exact_active_label_aliases_reused_without_replaying_historical_widget_gameplay=True,
        prior_26_actor_bindings_do_not_approve_names_orfonts=True,terms_reference_only_not_new_font_oractual_gameplay_approval=True,new_credit=0,
        evidence={str(p):digest(p) for p in [currentpath,activepath,helppath,itempath,ruinpath,Path(__file__)]}))
    print('Bound8 active room aliases/installed Help pages,Speech,Silla crown,Muryeong tomb,Seoul and3 commodity names;zero new gameplay orcredit.')


if __name__=='__main__':main()
