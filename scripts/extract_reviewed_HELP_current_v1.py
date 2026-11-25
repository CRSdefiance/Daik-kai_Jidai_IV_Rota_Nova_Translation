"""Bind sealed clean Help drafts to a verified current release,including owned continuation pages."""
import argparse
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import readable_source,source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['draft','release','out']:parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--headings',nargs='*',type=int,default=[])
    args=parser.parse_args();assert not args.out.exists()
    draft,release=map(load,[args.draft,args.release]);rom=Path(release['candidate'])
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert sha(rom.read_bytes())==release['candidate_sha256']
    image=NdsImage.open(rom);file='/COMMON/HELP.DK4';raw=image.read_file(file)
    assert sha(raw)==release['target_HELP_sha256']
    clean_path=Path('work/clean.nds');assert sha(clean_path.read_bytes())==release['clean_input_sha256']
    original=IlnkContainer.parse(NdsImage.open(clean_path).read_file(file)).blocks
    blocks=IlnkContainer.parse(raw).blocks;assert len(original)==202 and IlnkContainer(blocks).to_bytes()==raw
    links=[source_links(block)for block in blocks]
    def reference(n):
        at=int.from_bytes(raw[8+4*n:12+4*n],'little');assert raw[at:at+len(blocks[n])]==blocks[n]
        return dict(file_path=file,block=n,archive_offset=at,bytes=len(blocks[n]),offset_table_slot=8+4*n)
    def view(n):
        return dict(topic_id=n,current_reference=reference(n),current_hex=blocks[n].hex(),current_sha256=sha(blocks[n]),
          current_English_with_link_IDs=readable_source(blocks[n]),current_links=links[n],current_link_IDs=[l['topic_id']for l in links[n]])
    rows=[];selected=set()
    for row in draft['records']:
        n=row['topic_id'];assert n not in selected and n<len(original) and original[n].hex()==row['source_hex'];selected.add(n)
        continuations=[];seen={n};queue=[l['topic_id']for l in links[n]if l['topic_id']>=len(original)]
        while queue:
            child=queue.pop(0)
            if child in seen:continue
            assert child<len(blocks) and child!=203 and blocks[child].strip(b'\0'),(n,child)
            seen.add(child);continuations.append(view(child))
            queue.extend(l['topic_id']for l in links[child]if l['topic_id']>=len(original))
        foreign=[dict(origin=i,target=l['topic_id'])for i,ls in enumerate(links)if i not in seen for l in ls if l['topic_id']in seen-{n}]
        rows.append(dict(id=row['id'],source_reference=row['source_reference'],source_hex=row['source_hex'],**view(n),
          complete_current_continuations=continuations,continuation_foreign_incoming_links=foreign,
          continuation_ownership_requires_review=bool(foreign),continuation_discovery_is_offline_not_a_gameplay_visit=True))
    headings=[dict(topic_id=n,current_heading=readable_source(blocks[n]).split('\n',1)[0],current_block_sha256=sha(blocks[n]),only_heading_consulted_not_unselected_body=True)for n in args.headings]
    save(args.out,dict(file_path=file,current_ROM=str(rom),current_ROM_sha256=release['candidate_sha256'],current_archive_sha256=sha(raw),
      current_topic_count=len(blocks),original_clean_topic_count=len(original),records=rows,UI_heading_bindings=headings,
      sealed_draft=str(args.draft),sealed_draft_sha256=sha(args.draft.read_bytes()),draft_precedes_this_fresh_current_extraction=True,
      prior_English_andgeneral_consumer_exposure_retained_as_disclosed_in_sealed_draft=True,no_blanket_unconsulted_English_claim=True,
      verified_parent_release=str(args.release),verified_parent_release_sha256=sha(args.release.read_bytes()),
      actual_gameplay=False,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    for row in rows:
        print(row['topic_id'],row['current_English_with_link_IDs'])
        for child in row['complete_current_continuations']:print('CONTINUATION',child['topic_id'],child['current_English_with_link_IDs'])
        if row['continuation_foreign_incoming_links']:print('FOREIGN INCOMING',row['continuation_foreign_incoming_links'])
    print('HEADINGS',headings)

if __name__=='__main__':main()
