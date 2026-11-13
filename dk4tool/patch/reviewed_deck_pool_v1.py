"""Plan the single reviewed Deck terminology change within the original owned pool."""
import struct
from dk4tool.patch.deck_explanation_release import format_paragraph
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.grand_race_menu_release import sha

def plan_pool(arm,clean,history,review,references):
    def require(ok,message):
        if not ok:raise ValueError('Reviewed Deck pool: '+message)
    start,end=history['source_span']
    require(end-start==540 and history['used_aligned_bytes']==536,'original complete allocation')
    old=history['moves'];refs=history['references']
    require(len(old)==len(refs)==31,'complete original ownership/reference set')
    require(len(review['records'])==4 and review['translation_policy']=='natural-dialogue-v2','complete four-panel review')
    byold={r['offset']:r for r in review['records']};require(len(byold)==4,'unique complete panel identities')
    prior=bytearray();planned=bytearray();moves=[]
    for item in old:
        original_at=item['old_offset'];current_at=item['new_offset'];text=item['complete_text']
        require(current_at==start+len(prior),'contiguous aligned current owners')
        raw=text.encode('cp932')+b'\0';prior.extend(raw);prior.extend(b'\0'*(-len(prior)%4))
        next_text=text
        if original_at in byold:
            row=byold[original_at];source=bytes.fromhex(row['source_hex'])
            require(clean[original_at:original_at+row['capacity']]==source,'exact clean Japanese panel')
            require(all(row['review'][k] is True for k in ['source','context','localization','naturalness']),'four individual prose gates')
            require(row['current_reference']['offset']==current_at and row['current_hex']==raw[:-1].hex(),'exact complete current panel')
            english=row['english'].removesuffix('{PAD}')
            require('{LB' not in english and '{ALIGN' not in english and '\n' not in english,'logical prose')
            next_text=format_paragraph(english)
            if row['decision']=='retention':require(next_text==text,'retained panel wraps unchanged')
        at=start+len(planned);encoded=next_text.encode('cp932')+b'\0'
        planned.extend(encoded);planned.extend(b'\0'*(-len(planned)%4))
        moves.append(dict(old_offset=original_at,current_offset=current_at,new_offset=at,complete_text=next_text,
            current_complete_text=text,bytes_including_nul=len(encoded),wording_changed=next_text!=text))
    require(len(prior)==536 and bytes(prior).ljust(540,b'\0')==arm[start:end],'complete current allocation andpadding exact')
    require(len(planned)==540,'reviewed complete text fits source-owned allocation')
    expected=[(r['component'],r['field_offset'],next(m['new_offset'] for m in old if m['old_offset']==r['owner_offset'])) for r in refs]
    require(references==expected,'all current component pointers including byte-position/interior inventory')
    target=bytearray(arm);target[start:end]=planned
    pointer_changes=[];by_source={m['old_offset']:m for m in moves}
    for ref in refs:
        field=ref['field_offset'];move=by_source[ref['owner_offset']]
        require(ref['component']=='arm9' and ref['interior_byte_offset']==0 and not start<=field<end,'original literal/table field ownership')
        require(struct.unpack_from('<I',arm,field)[0]==BASE+move['current_offset'],'current pointer targets complete owner')
        struct.pack_into('<I',target,field,BASE+move['new_offset'])
        pointer_changes.append(dict(field_offset=field,current_pointer=BASE+move['current_offset'],new_pointer=BASE+move['new_offset'],
            pc_relative_load_instructions=ref['pc_relative_load_instructions']))
    require(sum(m['wording_changed'] for m in moves)==1,'only First Mate paragraph changes')
    inverse=bytearray(target);inverse[start:end]=arm[start:end]
    for ref in refs:
        at=ref['field_offset'];inverse[at:at+4]=arm[at:at+4]
    require(bytes(inverse)==arm,'complete unowned ARM9 inverse')
    return bytes(target),dict(source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(target),source_span=[start,end],
        owned_labels=31,owned_pointer_fields=31,source_allocation_bytes=540,current_used_bytes=536,target_used_bytes=540,
        source_owned_allocation_not_grown=True,no_runtime_code_font_orlate_pool_change=True,moves=moves,pointer_changes=pointer_changes,
        all27_other_label_wordings_andthree_retained_panel_bytes_preserved=True,complete_parent_target_inverse_andall_unowned_ARM9_exact=True)
