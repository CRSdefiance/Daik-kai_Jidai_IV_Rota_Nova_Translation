"""Source/runtime-locked speeches, aliased actor styles and three-option menus."""
import json
import struct
from itertools import pairwise
from pathlib import Path
from dk4tool.dialogue.lil_B111_B119_layout_v2 import encode_relocatable_dialogue, audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_B111_B119_profile import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B111_B119_editorial_release_v1.json'
HEADER=b'\0\x40\xff\xff\0'
BLOCKS=list(range(111,120))

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def _require(test,message):
    if not test:raise ValueError('Lil B111-B119 '+message)

def _mapped(patches,offset):
    delta=0
    for p in patches:
        if offset<p['start']:break
        _require(not p['start']<offset<p['end'],'unclassified interior reference')
        if offset==p['start']:return offset+delta
        delta+=len(p['value'])-(p['end']-p['start'])
    return offset+delta

def _compile(raw,row,profile,case):
    _require(all(raw.count(k.encode())==row['english'].count('{MACRO:'+k+'}') for k in ['FI','FA','FO']),
        'source macro count differs:'+row['id'])
    encoded=encode_relocatable_dialogue(raw,row['english'],profile)
    _require(encoded.encoded.hex()==row['compiled_hex']==case['encoded_hex'],'approved compiled prose differs:'+row['id'])
    for d in encoded.diagnostics:
        _require(d.severity!='error','formatting error:'+row['id'])
        if d.severity=='warning':
            _require(d.code in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'),'unreviewed encoder warning:'+row['id'])
    qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
    _require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not
        (i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))],
        'unapproved QA finding:'+row['id'])
    return encoded.encoded

def apply_release(image,baseline,config_path=CONFIG):
    config=load(config_path)
    _require(config.get('format')=='dk4-lil-B111-B119-editorial-release-v1','unknown release format')
    for p,digest in config['dependencies'].items():
        _require(sha(Path(p).read_bytes())==digest,'reviewed dependency differs:'+p)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin')
    _require(sha(arm)==config['required_runtime_arm9_sha256'],'native runtime differs')
    _require(sha(source)==config['source_SC2_sha256'] and sha(baseline.read_file(PATH))==config['canonical_SC2_sha256'],
        'current/canonical source differs')
    clean=Path(config['clean_ROM'])
    _require(sha(clean.read_bytes())==config['clean_ROM_sha256'],'clean ROM differs')
    japanese=NdsImage.open(clean).read_file(PATH)
    _require(sha(japanese)==config['clean_SC2_sha256'],'clean Japanese script differs')
    doc,voice=[load(config[k]) for k in ['manuscript','actor_styles']]
    mapping=load(config['reference_map'])
    for d in [doc,voice]:
        validate_natural_dialogue_batch(d)
        _require(d['translation_policy']=='natural-dialogue-v2' and d['target_locale']=='en-US'
            and d['encoder']=='dialogue-relocatable-v1' and d['formatting_review_pending'] is False,
            'source/native editorial contract differs')
        _require(d['reference_map']==config['reference_map'] and sha(Path(d['reference_map']).read_bytes())==d['reference_map_sha256'],
            'approved reference map differs')
    _require(doc['required_runtime_ARM9_sha256']==sha(arm),'reviewed runtime differs')
    _require(mapping.get('format')=='dk4-lil-B111-B119-source-relocation-map-v1'
        and mapping.get('external_references_complete') is True and mapping.get('entry_point_offset')==8
        and mapping.get('preserve_record_parity') is True and mapping.get('required_runtime_ARM9_sha256')==sha(arm)
        and mapping.get('source_SC2_sha256')==sha(source) and mapping.get('target_SC2_sha256')==config['target_SC2_sha256'],
        'complete source reference map required')
    for key in ['all305_physical_nested_command_boundaries_and64_relative_sites_verified',
        'all320_relocated_relative_skip_cases_preserve_original_targets',
        'all15_relocated_predicate_pairs_and_one_event319_query_preserve_source_operands_results_and_mapped_cursor',
        'all6_actor_style_objects48_slots34_strings_aliases_and_actual5_virtual_prefixes_verified',
        'unowned1886byte_copy_preserved_and_original_VM_return_before_copy_verified',
        'representative_shared_rules_approved']:
        _require(mapping.get(key) is True,'missing reference approval:'+key)
    _require(len(mapping['original_event_queries'])==1 and mapping['original_event_queries'][0]['event']==319,'event319 query contract required')
    _require(mapping.get('no_player_choice_objects') is True and mapping.get('all116_active_speech_targets_and148_physical_speeches_preserved') is True and mapping.get('canonical_Maria_SC3_B97_32_targets_still_pending_uncredited') is True,'active/physical/canonical scope contract differs')
    representative=load(doc['representative_proof'])
    _require(representative.get('no_open_translation_specific_display_or_control_finding') is True
        and representative.get('individual_selected_B111_B119_visits_not_required_for_reusable_rules') is True
        and representative.get('current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact') is True
        and representative.get('current4100_actual5_prefixes_all34_bodies_all48_aliases_and_all207_catalog_styles_bound') is True
        and representative.get('actual_selected_B111_B119_IDs')==[]
        and representative.get('new_emulator_runs')==0,'source-bound representative approval required')
    for key in ['historical_representative_sheet_review','prior_current_sheet_review']:
        sheet=load(doc[key])
        _require(sheet.get('viewed') is True and sha(Path(sheet['sheet']).read_bytes())==sheet['sha256'],
            'viewed representative sheet required')
    _require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B111_B119_layout_v2.py')
        and sha(Path(doc['native_formatter_module']).read_bytes())==doc['native_formatter_module_sha256'],
        'approved scoped formatter required')
    fonts={r['id']:r for r in load(doc['native_font_proof'])['cases']}
    FE=load(doc['native_FE_font_proof']);controls=load(doc['relocated_control_proof'])
    _require(len(FE['cases'])==1 and FE['ARM9_sha256']==sha(arm)
        and FE['all1_one_native_page_consumes_complete_target']
        and FE['all1_complete_native_independent_planes_all_glyphs_and_canaries_equal']
        and FE['one_source_unlabeled24000_gold_notice_preserved_without_invented_names_or_macros'],
        'complete distinct FE contract required')
    _require(controls['all15_predicate_and_one_query_current_relocated_results_and_source_operands_equal']
        and controls['all2484_pointer_cases_and_all_source_alias_groups_preserved']
        and controls['all150_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text'],
        'relocated predicate/style/dispatch approval required')
    copy=load(doc['unowned_copy_proof'])
    _require(sha(Path(doc['unowned_copy_proof']).read_bytes())==doc['unowned_copy_proof_sha256']==mapping['unowned_copy_proof_sha256']
        and copy.get('all32_unowned_copy_speeches_byte_exact_and_unreachable_from_ordinary_Lil_entry') is True
        and len(copy['original_VM_return_cases'])==2,'moved original return/copy proof required')
    _require(controls.get('original_query_r0_r1_r2_and_mapped_incidental_r3_cursor_exact') is True,'mapped query cursor approval required')
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    style_refs={r['id']:r for b in mapping['blocks'] for c in b['actor_style_commands'] for r in c['alternative_records']}
    _require(len(doc['records'])==len(refs)==116 and {r['id'] for r in doc['records']}==set(refs),'116speech coverage differs')
    _require(len(voice['records'])==len(style_refs)==34 and {r['id'] for r in voice['records']}==set(style_refs),'34style coverage differs')
    _require(len(fonts)==150 and set(fonts)==set(refs)|set(style_refs),'150complete native cases required')
    _require(sorted(b['block'] for b in mapping['blocks'])==BLOCKS,'nine exact blocks required')
    context=load(doc['source_context'])
    expected_commands={b['block']:len(b['all_current_native_commands']) for b in context['blocks']}
    _require(sum(expected_commands.values())==305,'source command census differs')
    container=IlnkContainer.parse(source);jp=IlnkContainer.parse(japanese);old_blocks=list(container.blocks)
    changes=[];reports=[];used_styles=set()
    for spec in mapping['blocks']:
        n=spec['block'];block=container.blocks[n];original=jp.blocks[n]
        _require(spec['external_references_complete'] and spec['entry_point_offset']==8,'block reference approval required')
        _require(sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block differs')
        end=8+struct.unpack_from('<H',block,4)[0]
        _require(end<=len(block) and not any(block[end:]),'source logical extent differs')
        profile=profile_for(arm,block);fe_profile=profile_for(arm,block,'FE-paper')
        patches=[]
        def bind_row(row):
            _require(row['file_path']==PATH,'wrong file identity')
            cr,sr=row['current_reference'],row['source_reference']
            at,source_at=cr['offset'],sr['offset']
            old=block[at:at+cr['bytes']];raw=original[source_at:source_at+sr['bytes']]
            _require(old.hex()==row['current_text_hex']==row['current_hex'] and raw.hex()==row['source_hex']
                and block[at+len(old)]==original[source_at+len(raw)]==0,'Japanese/current prose differs:'+row['id'])
            return at,source_at,old,raw
        for row in doc['records']:
            if row['block']!=n:continue
            ident=row['id'];ref=refs[ident];at,source_at,old,raw=bind_row(row)
            _require(at==ref['old_offset'] and len(old)==ref['old_length']
                and block[at-5:at]==original[source_at-5:source_at]==HEADER and old[:1]==raw[:1],
                'speech preamble/reference differs:'+ident)
            _require(raw[0] in {2,4,9,14,19,20,104,137,163,170,179,198,207,208,209,214,215,220,254},'unapproved speaker:'+ident)
            _require(row['native_display_consumer']==('original_FE_modal_5473C_mode1' if raw[0]==254 else 'original_progressive_54020')
                and (HEADER+raw[:1]).hex()==row['source_complete_preamble_hex'],'complete consumer/preamble differs:'+ident)
            _require(block[:at].count(b'\0')==row['record_index']==ref['record_index']
                and original[:source_at].count(b'\0')==row['source_record_index'],'NUL provenance differs:'+ident)
            value=_compile(raw,row,fe_profile if raw[0]==254 else profile,fonts[ident])
            pad=len(value)%2!=len(old)%2
            if pad:value+=b' '
            _require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and pad==ref['parity_space_added'],
                'approved final parity target differs:'+ident)
            patches.append(dict(start=at,end=at+len(old),old=old,value=value))
            changes.append(dict(id=ident,file_path=PATH,block=n,kind='speech',old_offset=at,
                old_bytes=len(old),new_bytes=len(value),parity_space_added=pad,new_offset=ref['new_offset']))
        for ref in spec['actor_style_commands']:
            at,length=ref['old_offset'],ref['old_length'];old=block[at:at+length]
            _require(old[:2]==original[at:at+2]==b'\0\x41' and old[18:20]==original[at+18:at+20] and old[18]==0 and old[19] in {208,209,214,215,220},
                'complete source 4100 selector/header differs')
            rows=sorted([r for r in voice['records'] if r['block']==n and r['command_offset']==at],
                key=lambda r:r['current_reference']['offset'])
            _require(rows and sum(len(r['style_indices']) for r in rows)==8,'all8style slots required')
            oldtable=list(struct.unpack_from('<8H',old,2));jptable=list(struct.unpack_from('<8H',original,at+2))
            _require(oldtable==ref['old_style_offsets']==jptable,'source/current alias table differs')
            table=[None]*8;chunks=[];cursor=0
            for row in rows:
                ident=row['id'];r=style_refs[ident];body_at,source_at,before,raw=bind_row(row)
                _require(ident not in used_styles and row['source_selector']==old[19] and row['virtual_formatter_prefix_hex']==format(old[19],'02x')
                    and row['virtual_formatter_prefix_is_not_part_of_stored_alternative_text'] is True
                    and row['native_display_consumer']=='original4100_actor_voice_selection_then2425C_progressive54020',
                    'actor-style identity/virtual prefix differs:'+ident)
                _require(body_at==r['old_offset'] and len(before)==r['old_length']
                    and row['style_indices']==r['style_indices']
                    and [i for i,v in enumerate(oldtable) if at+20+v==body_at]==row['style_indices']
                    and source_at==body_at,'source style aliases/reference differs:'+ident)
                used_styles.add(ident)
                value=_compile(bytes([old[19]])+raw,row,profile,fonts[ident])
                _require(value[:1]==bytes([old[19]]),'virtual style prefix differs')
                value=value[1:]
                _require(value.hex()==row['compiled_stored_alternative_hex']==r['target_hex']
                    and len(value)==r['new_length'] and 20+cursor==r['new_relative_offset'],
                    'stored alternative body/offset differs:'+ident)
                for i in row['style_indices']:
                    _require(table[i] is None,'overlapping style ownership');table[i]=cursor
                chunk=value+b'\0';chunk+=b'\0'*(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
                changes.append(dict(id=ident,file_path=PATH,block=n,kind='actor-style',actor_style_command_offset=at,
                    style_indices=row['style_indices'],old_offset=body_at,old_bytes=len(before),new_bytes=len(value),
                    new_offset=r['new_offset'],actual_virtual_prefix_excluded_from_stored_body=True))
            _require(table==ref['new_style_offsets'] and all((oldtable[i]==oldtable[j])==(table[i]==table[j])
                for i in range(8) for j in range(8)),'actor-style alias equivalence differs')
            value=old[:2]+struct.pack('<8H',*table)+old[18:20]+b''.join(chunks)
            _require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'],'complete approved 4100 object differs')
            patches.append(dict(start=at,end=at+length,old=old,value=value))
        _require(spec['choice_commands']==[],'unexpected player-choice object')
        patches.sort(key=lambda p:p['start'])
        _require(all(a['end']<=b['start'] for a,b in pairwise(patches)),'owned objects overlap')
        parts=[];last=0
        for p in patches:parts.extend([block[last:p['start']],p['value']]);last=p['end']
        parts.append(block[last:end]);logical=bytearray(b''.join(parts))
        _require(len(logical)==_mapped(patches,end) and len(logical)<0x2400,'cache or mapped extent differs')
        commands=spec['mapped_native_commands']
        _require(len(commands)==expected_commands[n] and len({c['old_offset'] for c in commands})==len(commands),
            'complete native census required')
        for c in commands:
            a,z=c['old_offset'],c['new_offset']
            _require(z==_mapped(patches,a) and c['new_native_extent']==_mapped(patches,a+c['old_native_extent'])-z
                and struct.unpack_from('<H',block,a)[0]==c['word']==struct.unpack_from('<H',logical,z)[0]
                and c['target_0100_ancestors']==[_mapped(patches,p) for p in c['source_0100_ancestors']],
                'mapped command/extent/ancestor differs')
            if c['word']==0x4000:_require(block[a:a+6]==logical[z:z+6],'complete speech header changed')
            elif c['word'] not in [0x100,0x200,0x300,0x400,0x4100,0x2200]:
                _require(block[a:a+c['old_native_extent']]==logical[z:z+c['new_native_extent']],'unowned opaque command changed')
        edges=spec['relative_skip_fixups']
        _require(len(edges)==sum(c['word'] in [0x100,0x200,0x300,0x400] for c in commands),'relative span census differs')
        boundaries={c['new_offset'] for c in commands}|{len(logical)}
        for edge in edges:
            a=_mapped(patches,edge['offset']);z=_mapped(patches,edge['matched_skip_target']);span=z-a-4
            _require(a==edge['new_offset'] and z==edge['new_matched_skip_target'] and a+4==edge['new_unmatched_next']
                and a+4 in boundaries and z in boundaries and 0<=span<=65535 and span%2==0 and span==edge['target_span']
                and struct.unpack_from('<H',block,edge['offset']+2)[0]==edge['source_span']
                and struct.unpack_from('<H',logical,a)[0]==edge['word'],'relative operand/destination differs')
            struct.pack_into('<H',logical,a+2,span)
        struct.pack_into('<H',logical,4,len(logical)-8);target=bytes(logical)+b'\0'*(-len(logical)%4)
        if n==115:
            unowned=spec['unowned_appended_copy'];a=unowned['old_offset'];z=unowned['new_offset'];size=unowned['bytes']
            _require(a==440 and size==1886 and z==_mapped(patches,a) and end-a==size
                and block[a:end]==target[z:z+size] and sha(target[z:z+size])==unowned['sha256']
                and target[z-4:z]==bytes(4) and copy['unowned_copy']==unowned
                and copy['conservative_relocated_prefix_graph']['reachable_return0_commands']==[z-4]
                and not any(p>=z for p in copy['conservative_relocated_prefix_graph']['reachable_commands']),
                'unowned copy or mapped original return changed')
        _require(sha(target)==spec['target_block_sha256'],'complete target block differs')
        for r in changes:
            if r['block']!=n:continue
            if r['kind']=='speech':
                _require(r['new_offset']==_mapped(patches,r['old_offset']) and target[r['new_offset']-5:r['new_offset']]==HEADER,'relocated speech header differs')
            elif r['kind']=='actor-style':
                a=_mapped(patches,r['actor_style_command_offset'])
                _require(all(r['new_offset']==a+20+struct.unpack_from('<H',target,a+2+2*i)[0] for i in r['style_indices']),
                    'relocated actor-style aliases differ')
            else:raise ValueError('Unexpected ownership kind')
        restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
        for edge in edges:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
        for p in reversed(patches):
            a=_mapped(patches,p['start']);restored[a:a+len(p['value'])]=p['old']
        _require(bytes(restored)==block[:end],'inverse restoration changed unowned bytes')
        container.blocks[n]=target
        reports.append(dict(block=n,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),
            target_bytes=len(target),growth_bytes=len(target)-len(block),relative_operands=len(edges),original_entry=8,
            actor_style_objects=len(spec['actor_style_commands']),three_option_menus=len(spec['choice_commands']),
            inverse_restores_every_original_logical_byte=True))
    _require(used_styles=={r['id'] for r in voice['records']}
        and len(changes)==len({r['id'] for r in changes})==150,'incomplete editorial coverage')
    result=container.to_bytes()
    _require(sha(result)==config['target_SC2_sha256'],'complete SC2 target differs')
    _require([n for n,(a,b) in enumerate(zip(old_blocks,container.blocks,strict=True)) if a!=b]==BLOCKS,'unrelated block changed')
    _require(image.read_file('/__arm9__.bin')==arm,'native runtime changed')
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=config['manuscript'],actor_styles=config['actor_styles'],reference_map=config['reference_map'],
        changed_records=changes,blocks=reports,only_SC2_selected_nine_blocks_changed=True,all327_other_SC2_blocks_unchanged=True,
        all116_speeches34_style_alternatives_no_choices64_relative_operands_verified=True,
        all48_style_slots_aliases_and_actual5_virtual_prefix_storage_verified=True,unowned1886byte_copy_preserved_and_canonicalMaria32_uncredited=True,
        native_code_and123040_staged_payload_unchanged=True)
