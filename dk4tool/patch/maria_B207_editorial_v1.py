"""Reconstruct the sealed Maria exchange, then commit one staged file afterall guards."""
import json,struct
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.maria_B207_profile_v1 import contract,profile_for
from dk4tool.dialogue import maria_B207_layout_v1 as codec
from dk4tool.patch.maria_B207_atomic_support_v1 import audit_scope
from scripts.seal_Maria_B207_references_v7713 import FLAGS
CONFIG='translations/maria_B207_editorial_release_v1.json'
PATHS=('/data/SC3.DK4',)
def load(path):return json.loads(Path(path).read_bytes())
def require(value,label):
    if not value:raise ValueError('Maria B207 editorial contract: '+label)
def check_dependencies(conf):
    for p,h in conf['dependencies'].items():require(sha(Path(p).read_bytes())==h,'dependency:'+p)
def commit_files(image,files):
    image.rom.files=files
def apply_release(image,baseline,config=CONFIG):
    conf=load(config);check_dependencies(conf)
    require(conf['format']=='dk4-Maria-B207-editorial-release-v1' and len(conf['manuscripts'])==1,'single-file Maria release configuration')
    arm=image.read_file('/__arm9__.bin');require(sha(arm)==conf['required_runtime_arm9_sha256'] and sha(image.read_file('/COMMON/MESFILE.DK4'))==conf['required_runtime_common_sha256'],'exact current runtime')
    require(sha(baseline.source.read_bytes())==conf['canonical_ROM_sha256'],'canonical baseline')
    require(sha(Path(conf['clean_ROM']).read_bytes())==conf['clean_ROM_sha256'],'clean ROM')
    clean=NdsImage.open(conf['clean_ROM']);mapping,seal=[load(conf[k]) for k in ['reference_map','reference_approval']]
    require(conf['required_map_flags']==FLAGS and all(mapping[k] is True for k in FLAGS) and mapping['format']=='dk4-Maria-B207-source-relocation-map-v1','complete file-qualified map flags')
    require(seal['all18_five_gates_andexact_references_approved'] and seal['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and len(mapping['groups'])==1,'approval seal')
    audit_scope(image,clean,conf,mapping,seal,load,require)
    bindings=contract()['record_bindings'];p=conf['proofs'];packet=load(p['source_context']);font=load(p['native_font_proof']);stored=load(p['native_stored_proof']);control=load(p['relocated_control_proof']);actual=load(p['actual_proof'])
    require(sha(Path(conf['reference_ROM']).read_bytes())==conf['reference_ROM_sha256'],'exact research reference');reference=NdsImage.open(conf['reference_ROM'])
    prepared=[];changes=[]
    for path in conf['manuscripts']:
        route=3
        doc=load(path);spec=mapping['groups'][0];file=PATHS[0];n=207;source=image.read_file(file);original_archive=clean.read_file(file)
        require((spec['route'],spec['file_path'],spec['block'],spec['source_bytes'],spec['source_logical_end'],spec['source_tail_bytes'],spec['target_bytes'],spec['target_logical_end'],spec['target_tail_bytes'])==(route,file,n,1468,1468,0,1472,1470,2),'exact route/block/extents')
        require(sha(source)==spec['source_archive_sha256']==conf['archives'][0]['source_sha256'] and sha(baseline.read_file(file))==conf['archives'][0]['canonical_sha256'] and sha(original_archive)==conf['archives'][0]['clean_sha256'],'current/canonical/clean archives')
        require(all(not spec[k] for k in ['choice_commands','actor_style_commands','relative_skip_fixups','target_native_skip_cases','original_C200_map','original_630B_map']),'no invented typed controls/relatives')
        require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US' and doc['encoder']=='dialogue-relocatable-v1' and not doc['formatting_review_pending'],'reviewed v2 manuscript');validate_natural_dialogue_batch(doc)
        require(doc['reference_map_sha256']==sha(Path(conf['reference_map']).read_bytes()) and doc['reference_research_ROM_sha256']==conf['reference_ROM_sha256'],'manuscript map/reference binding')
        approved=load(doc['native_approved_manuscript']);require(approved['records']==doc['records'] and sha(Path(doc['native_approved_manuscript']).read_bytes())==doc['native_approved_manuscript_sha256']==spec['approved_manuscript_sha256'],'individually approved records')
        require(seal['manuscripts'][0]['path']==path and seal['manuscripts'][0]['sha256']==sha(Path(path).read_bytes()),'sealed manuscript')
        for key,value in p.items():require(doc[key]==value and doc[key+'_sha256']==sha(Path(value).read_bytes()),'exact proof link:'+key)
        rows=doc['records'];ids={r['id'] for r in rows};require(len(rows)==len(ids)==18 and Counter(r['editorial_decision'] for r in rows)=={'revise':13,'retain-wording':5} and Counter(r['source_selector'] for r in rows)=={19:9,104:9},'18 decisions/two actors')
        require(all(r['route_identity']=='Maria' and r['block']==n and r['file_path']==file and r['kind']=='progressive' and r['review']=={k:True for k in ['source','context','localization','naturalness','formatting']} and r['whole_English_exchange_cadence_andemotional_progression_reviewed'] and (r['editorial_decision']!='retain-wording' or r['retention_reason']) for r in rows),'individual route/context/gates')
        blocks=list(IlnkContainer.parse(source).blocks);block=blocks[n];japanese=IlnkContainer.parse(original_archive).blocks[n]
        require(len(blocks)==303 and sha(block)==spec['source_block_sha256'] and sha(japanese)==spec['clean_block_sha256'] and len(block)==1468 and block[:4]==b'CS\1\1' and 8+struct.unpack_from('<H',block,4)[0]==1468 and block[1464:]==bytes(4),'complete predecessor header/end/tail')
        source_rows={r['id']:r for r in packet['records']};refs={r['id']:r for r in spec['text_records']};allrefs={r['id']:r for r in spec['all_object_references']}
        fonts={r['id']:r for r in font['records']};stores={r['id']:r for r in stored['records']};dispatches={r['id']:r for r in control['dispatch_cases']}
        panels={r['id']:r for r in next(g for g in actual['groups'] if g['route']==route and g['version']=='English')['speech_observations']}
        require(set(source_rows)==set(refs)==set(allrefs)==set(fonts)==set(stores)==set(dispatches)==set(panels)==ids,'all individual proof sets')
        patches=[];record_changes=[];pads=0
        for row in rows:
            ident=row['id'];ref=refs[ident];b=bindings[ident];before=source_rows[ident];raw=bytes.fromhex(row['source_hex']);old=bytes.fromhex(row['current_hex']);at=row['current_reference']['offset'];ja=row['source_reference']['offset']
            require(ref==allrefs[ident] and row['source_reference']==before['source_reference']==ref['source_reference'] and row['current_reference']==before['current_reference']==ref['current_reference'] and row['source_hex']==before['source_hex'] and row['current_hex']==before['current_hex'],'complete source/current references:'+ident)
            require(row['source_meaning']==before['source_gloss'] and row['source_Japanese']==before['source_Japanese'] and row['context']==before['full_exchange_context'],'source gloss/context:'+ident)
            require((row['editorial_decision']=='retain-wording')==(' '.join(old[1:].decode('cp932').split())==row['english'].split('}',1)[1]),'individual retention comparison:'+ident)
            require(japanese[ja:ja+len(raw)+1]==raw+b'\0' and block[at:at+len(old)+1]==old+b'\0' and block[:at].count(b'\0')==row['current_record_index'],'literal records:'+ident)
            require(raw[0]==old[0]==row['source_selector']==b['source_selector']==ref['source_selector'] and row['source_voice_class']==ref['source_voice_class']=={19:7,104:0}[raw[0]] and block[at-5:at+1].hex()==row['source_complete_preamble_hex']==ref['source_preamble_hex'],'complete preamble/voice:'+ident)
            require(row['speaker']=={19:'Carlo Sinat',104:'Trader'}[raw[0]] and all(isinstance(row[k],str) and row[k].strip() for k in ['context','source_meaning','localization_note','editorial_finding']),'individual identity/reason:'+ident)
            prof=profile_for(arm,block,ident,file);encoded=codec.encode_relocatable_dialogue(raw,row['english'],prof);qa=codec.audit_relocatable_dialogue_record(raw,row['english'],prof)
            require(encoded.encoded.hex()==row['compiled_hex']==ref['compiled_hex']==fonts[ident]['compiled_hex'] and qa==row['base_QA_report'],'compiled native text/QA:'+ident)
            require(row['qa_waivers']==b['qa_waivers'] and row['qa_waiver_reason']==b['qa_waiver_reason'] and row['row_count_reason']==b['row_count_reason'] and row['reviewed_ordinary_boundaries']==b['ordinary_wrap_reasons'],'scoped row/wrap reasons:'+ident)
            value=encoded.encoded;pad=len(value)%2!=len(old)%2
            if pad:value+=b' '
            pads+=pad;require(value.hex()==ref['target_hex']==stores[ident]['final_target_hex']==dispatches[ident]['target_hex'] and ref['parity_space_added']==pad,'exact final stored bytes:'+ident)
            require(not any(m in raw[1:] or m in value[1:] for m in [b'FI',b'FA',b'FO']),'zero original/invented macros:'+ident)
            require(len(stores[ident]['native_pipeline']['cases'])==4 and all(c['output_hex']==value[1:].hex() for c in stores[ident]['native_pipeline']['cases']),'native final ABI:'+ident)
            require(len(fonts[ident]['pages'])==len(stores[ident]['complete_pages']['pages'])==row['native_page_count']==b['native_page_count']==1 and row['native_profile_maximum_total_rows']==row['original_physical_native_rows_per_page']==4,'bounded original page:'+ident)
            for a,z in zip(fonts[ident]['pages'],stores[ident]['complete_pages']['pages'],strict=True):require(Path(a['native_plane']).read_bytes()==Path(z['native_plane']).read_bytes() and sha(Path(z['native_plane']).read_bytes())==z['native_plane_sha256']==a['native_plane_sha256'],'complete native ink:'+ident)
            panel=panels[ident];require(row['actual_record_observed'] and panel['native_page_count']==1 and len(panel['complete_body_holds'])==row['actual_complete_body_holds'] and len(panel['complete_name_holds'])==row['actual_complete_name_holds'] and panel['complete_body_holds'] and panel['complete_name_holds'],'complete actual holds:'+ident)
            for h in panel['complete_body_holds']:require(h['complete_independent_native_body_mask_equal'] and h['gray_compared'] and h['body_shadow_RGB']==([197,198,197] if row['source_record_index']==4 else [98,97,98]) and sha(Path(h['capture']).read_bytes())==h['sha256'],'actual body/palette:'+ident)
            for h in panel['complete_name_holds']:require(h['actor_ID']==raw[0] and h['text']==row['speaker'] and h['complete_name_first_internal_final_glyphs_andblank_guards_equal'] and sha(Path(h['capture']).read_bytes())==h['sha256'],'actual name/header:'+ident)
            patches.append(dict(start=at,end=at+len(old),old=old,value=value,source_raw=raw))
            record_changes.append(dict(id=ident,file_path=file,block=n,old_offset=at,new_offset=ref['new_offset'],old_bytes=len(old),new_bytes=len(value)))
        require(pads==7,'seven zero-ink parity tails');patches.sort(key=lambda r:r['start']);require(all(a['end']<=b['start'] for a,b in zip(patches,patches[1:])),'disjoint replacements')
        def mapped(at):
            delta=0
            for r in patches:
                if at<r['start']:break
                require(not r['start']<at<r['end'],'unmapped interior reference')
                if at==r['start']:return at+delta
                delta+=len(r['value'])-len(r['old'])
            return at+delta
        parts=[];last=0
        for r in patches:parts.extend([block[last:r['start']],r['value']]);last=r['end']
        parts.append(block[last:1468]);logical=bytearray(b''.join(parts));require(len(logical)==mapped(1468)==1470,'target logical extent')
        struct.pack_into('<H',logical,4,1462);target=bytes(logical)+bytes(2);require(len(target)==1472 and sha(target)==spec['target_block_sha256'],'complete target block/tail')
        commands=packet['all_current_native_commands'];require(len(commands)==len(spec['command_map'])==20,'all20 native commands')
        for old,cm in zip(commands,spec['command_map'],strict=True):
            a,z=old['offset'],cm['new_offset'];require(a==cm['old_offset'] and mapped(a)==z and old['native_extent']==cm['old_extent'] and mapped(a+cm['old_extent'])==z+cm['new_extent'] and struct.unpack_from('<H',target,z)[0]==cm['word']==old['word'] and cm['source_0100_ancestors']==cm['target_0100_ancestors']==[],'complete command map')
            require(block[a:a+6]==target[z:z+6] if old['word']==0x4000 else bytes.fromhex(old['whole_command_hex'])==target[z:z+cm['new_extent']],'complete preamble/opaque command/end')
        require([(r['source_offset'],r['target_offset'],r['source_hex']) for r in spec['original_A000_map']]==[(1456,1458,'00a0ffff6a000110')] and [(r['source_offset'],r['target_offset'],r['source_hex']) for r in spec['complete_end_map']]==[(1464,1466,'00000000')] and target[1466:1470]==bytes(4) and target[1470:]==bytes(2),'A000/full normal end/separate storage tail')
        for ref in refs.values():require(mapped(ref['old_offset'])==ref['new_offset'] and target[ref['new_offset']:ref['new_offset']+ref['new_length']+1]==bytes.fromhex(ref['target_hex'])+b'\0' and target[:ref['new_offset']].count(b'\0')==ref['new_record_index'],'final stored reference')
        inverse=bytearray(target[:1470]);struct.pack_into('<H',inverse,4,1460)
        for r in reversed(patches):at=mapped(r['start']);inverse[at:at+len(r['value'])]=r['old']
        require(bytes(inverse)==block,'full1468 predecessor inverse')
        clean_inverse=bytearray(target[:1470]);struct.pack_into('<H',clean_inverse,4,1460)
        for r in reversed(patches):at=mapped(r['start']);clean_inverse[at:at+len(r['value'])]=r['source_raw']
        require(bytes(clean_inverse)==japanese,'full1468 clean source inverse')
        newblocks=list(blocks);newblocks[n]=target;result=IlnkContainer(newblocks).to_bytes()
        require(sha(result)==spec['target_archive_sha256']==conf['archives'][0]['target_sha256'] and result==reference.read_file(file),'exact approved target archive')
        prepared.append(dict(file_path=file,source_sha256=sha(source),target_sha256=sha(result),payload=result,changed_records=record_changes,block=n));changes.extend(record_changes)
    require(len(prepared)==1 and len(changes)==18,'one complete staged archive')
    files=list(image.rom.files);indices=image.path_map()
    for item in prepared:files[indices[item['file_path']]]=item['payload']
    require([i for i,(old,new) in enumerate(zip(image.rom.files,files,strict=True)) if old!=new]==[indices[p] for p in PATHS],'only the intended SC3 file slot')
    # All validation and complete source/predecessor reconstructions have finished; this is the sole mutation.
    commit_files(image,files)
    return dict(manuscripts=conf['manuscripts'],reference_map=conf['reference_map'],changed_records=changes,files=[{k:v for k,v in r.items() if k!='payload'} for r in prepared],one_files_list_commit_after_all_gates=True,full_clean_block_andpredecessor_archive_reversible=True,all18_actual_single_pages_andcomplete_headers_bound=True,all_measured_timing_RNG_components_RGB_andnatural_activation_limits_preserved=True,no_name_item_orother_file_component_change=True,full_goal_complete=False)
