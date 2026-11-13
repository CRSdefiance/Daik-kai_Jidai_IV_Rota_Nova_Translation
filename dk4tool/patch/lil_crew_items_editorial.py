"""Source/runtime-bound fourteen-block Crew/Items prose and typed-choice layer."""
import json
import struct
from itertools import pairwise
from pathlib import Path

from dk4tool.dialogue.lil_crew_items_layout_v2 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_crew_items_profile import profile_for
from dk4tool.dialogue.review import REQUIRED_REVIEW_GATES, validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH='/data/SC2.DK4'
CONFIG='translations/lil_crew_items_editorial_release_v1.json'
HEADER=b'\0\x40\xff\xff\0'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def _require(test, message):
    if not test:
        raise ValueError('Lil Crew/Items '+message)


def _mapped(patches, offset):
    delta=0
    for patch in patches:
        if offset<patch['start']:
            break
        _require(not patch['start']<offset<patch['end'],'unclassified interior reference')
        if offset==patch['start']:
            return offset+delta
        delta+=len(patch['value'])-(patch['end']-patch['start'])
    return offset+delta


def apply_release(image, baseline, config_path=CONFIG):
    config=load(config_path)
    _require(config.get('format')=='dk4-lil-crew-items-editorial-release-v1','unknown release format')
    for name,digest in config['dependencies'].items():
        _require(sha(Path(name).read_bytes())==digest,'reviewed dependency differs:'+name)
    source=image.read_file(PATH);arm=image.read_file('/__arm9__.bin')
    _require(sha(arm)==config['required_runtime_arm9_sha256'],'requires the proven native runtime')
    _require(sha(source)==config['source_SC2_sha256'] and sha(baseline.read_file(PATH))==config['canonical_SC2_sha256'],
             'current/canonical source differs')
    clean_path=Path(config['clean_ROM'])
    _require(sha(clean_path.read_bytes())==config['clean_ROM_sha256'],'clean Japanese ROM differs')
    japanese=NdsImage.open(clean_path).read_file(PATH)
    _require(sha(japanese)==config['clean_SC2_sha256'],'clean Japanese script differs')
    doc=load(config['manuscript']);choices=load(config['choices']);mapping=load(config['reference_map'])
    validate_natural_dialogue_batch(doc)
    _require(doc['translation_policy']=='natural-dialogue-v2' and doc['target_locale']=='en-US'
        and doc['encoder']=='dialogue-relocatable-v1' and doc['dialogue_profile']=='lil-opening-editorial-native-v1'
        and doc['required_runtime_ARM9_sha256']==sha(arm) and doc['formatting_review_pending'] is False,
        'source/native review contract differs')
    _require(choices['translation_policy']=='natural-dialogue-v2' and choices['target_locale']=='en-US',
             'typed choice localization policy differs')
    validate_natural_dialogue_batch({**choices,'encoder':'dialogue-relocatable-v1','review_gates':sorted(REQUIRED_REVIEW_GATES)})
    _require(mapping.get('format')=='dk4-lil-crew-items-source-relocation-map-v1'
        and mapping.get('external_references_complete') is True and mapping.get('entry_point_offset')==8
        and mapping.get('preserve_record_parity') is True and mapping.get('required_runtime_ARM9_sha256')==sha(arm)
        and mapping.get('source_SC2_sha256')==sha(source),'complete source reference map required')
    _require(mapping['all268_nested_command_boundaries_and4_relative_sites_verified']
        and mapping['all20_relocated_relative_skip_cases_preserve_original_targets'],'complete branch contract required')
    representative=load(doc['representative_proof'])
    _require(representative.get('no_open_translation_specific_display_or_control_finding') is True
        and representative.get('individual_selected_Crew_Items_visits_not_required_for_reusable_rules') is True
        and representative.get('no_predicate_or_event_query_commands_in_selected_blocks') is True
        and representative.get('historical_actual_menu_and_FE_rules_reused_by_exact_consumer_font_and_object_geometry') is True
        and representative.get('actual_selected_Crew_Items_IDs')==[] and representative.get('new_emulator_runs')==0,
        'source-bound representative rules and relocated predicates required')
    for key in ['historical_representative_sheet_review','prior_current_sheet_review']:
        sheet=load(doc[key])
        _require(sheet.get('viewed') is True and sha(Path(sheet['sheet']).read_bytes())==sheet['sha256'],'viewed inherited representative sheet required')
    _require(mapping.get('no_predicate_or_event_query_commands_in_selected_blocks') is True,'relocated predicate approval required')
    _require(doc.get('native_formatter_module')=='dk4tool/dialogue/lil_crew_items_layout_v2.py'
        and sha(Path(doc['native_formatter_module']).read_bytes())==doc['native_formatter_module_sha256'],'approved scoped formatter required')
    menu_native=load(doc['native_choice_proof'])
    _require(menu_native['complete_current_and_reviewed_style_label_planes']==8 and menu_native['native_selection_cancel_cases']==6,'complete one-menu native proof required')
    menu_targets={}
    for native in menu_native['menus']:
        _require(sha(Path(native['proof']).read_bytes())==native['sha256'],'menu native proof hash differs')
        detail=load(native['proof']);target=next(c for c in detail['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
        menu_targets[(detail['block'],detail['original_command_offset'])]=target['object_hex']
    _require(len(menu_targets)==1,'one approved typed menu required')
    _require(mapping.get('representative_shared_rules_approved') is True
        and mapping.get('target_SC2_sha256')==config['target_SC2_sha256'], 'approved representative/map target required')
    fonts={r['id']:r for r in load(doc['native_font_proof'])['cases']}
    FE=load(doc['native_FE_font_proof'])
    _require(len(FE['cases'])==7 and FE['ARM9_sha256']==sha(arm)
        and FE['all7_one_native_page_consumes_complete_target']
        and FE['all7_complete_native_independent_planes_all_glyphs_and_canaries_equal']
        and len(FE['source_FI_null_actor_cases'])==2 and FE['all7_source_unlabeled_stat_notices_and_monkey_calls_preserved'] and FE['only2_source_FI_macros_preserved_no_invented_labels_or_kinship'],'complete distinct FE native contract required')
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    _require(len(doc['records'])==len(fonts)==len(refs)==198 and {r['id']for r in doc['records']}==set(fonts)==set(refs),
             'exhaustive198 speech coverage differs')
    _require(len(choices['records'])==len({r['id']for r in choices['records']})==2,'exhaustive two choice labels required')
    _require(sorted(b['block']for b in mapping['blocks'])==[81,82,83,84,86,88,91,92,93,94,95,96,99,100],'exact fourteen-block reference map required')
    container=IlnkContainer.parse(source);jp=IlnkContainer.parse(japanese);old_blocks=list(container.blocks)
    changes=[];block_reports=[];used_choices=set()
    for spec in mapping['blocks']:
        number=spec['block'];block=container.blocks[number];original=jp.blocks[number]
        profile=profile_for(arm,block)
        fe_profile=profile_for(arm,block,'FE-paper')
        _require(spec.get('external_references_complete') is True and spec.get('entry_point_offset')==8,
                 'complete block reference map required')
        _require(sha(block)==spec['source_block_sha256'] and block[:4]==b'CS\0\1','source block/header differs')
        end=8+struct.unpack_from('<H',block,4)[0]
        _require(end<=len(block) and not any(block[end:]),'source CS logical extent differs')
        parts=block.split(b'\0');original_parts=original.split(b'\0');patches=[];owned_changes=[]
        for row in doc['records']:
            if row['block']!=number:
                continue
            ident=row['id'];ref=refs[ident];case=fonts[ident];index=row['record_index']
            _require(row['file_path']==PATH and index==ref['record_index'],'speech identity differs:'+ident)
            at=sum(len(p)+1 for p in parts[:index]);source_at=sum(len(p)+1 for p in original_parts[:row['source_record_index']])
            old,raw=parts[index],original_parts[row['source_record_index']]
            _require(old.hex()==row['current_text_hex'] and raw.hex()==row['source_hex']
                and at==row['current_reference']['offset']==ref['old_offset']
                and source_at==row['source_reference']['offset'] and block[at-5:at]==original[source_at-5:source_at]==HEADER
                and old[:1]==raw[:1] and len(old)==ref['old_length'],'Japanese/current speech or speaker differs:'+ident)
            _require(raw[0] in {2,4,6,7,12,14,15,16,18,20,22,108,114,152,188,254},'unapproved original actor prefix:'+ident)
            _require(row.get('native_display_consumer')==('original_FE_modal_5473C_mode1' if raw[:1]==b'\xfe' else 'original_progressive_54020')
                and (HEADER+raw[:1]).hex()==row['source_complete_preamble_hex'], 'complete original display preamble differs:'+ident)
            _require(all(raw.count(k.encode('ascii'))==row['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO')),
                'source runtime substitution count differs:'+ident)
            compiled=encode_relocatable_dialogue(raw,row['english'],fe_profile if raw[:1]==b'\xfe' else profile)
            _require(compiled.encoded.hex()==row['compiled_hex']==case['encoded_hex'],
                     'complete reviewed native text differs:'+ident)
            for diagnostic in compiled.diagnostics:
                _require(diagnostic.severity!='error','native formatting error:'+ident)
                if diagnostic.severity=='warning':
                    _require(diagnostic.code in row.get('qa_waivers',[]) and bool(row.get('qa_waiver_reason')),
                             'unreviewed formatting warning:'+ident)
            qa=audit_relocatable_dialogue_record(raw,row['english'],fe_profile if raw[:1]==b'\xfe' else profile)
            _require(not [i for i in qa['issues'] if i['severity'] in ['warning','error'] and not (i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]) and row.get('qa_waiver_reason'))],'unapproved complete QA finding:'+ident)
            value=compiled.encoded;pad=len(value)%2!=len(old)%2
            if pad:
                value+=b' '
            _require(value.hex()==ref['target_hex'] and len(value)==ref['new_length'] and value[:1]==raw[:1]
                and b'\0' not in value and len(value)%2==len(old)%2 and pad==ref['parity_space_added'],
                'speaker, parity or approved target differs:'+ident)
            patches.append({'start':at,'end':at+len(old),'old':old,'value':value})
            change={'id':ident,'file_path':PATH,'block':number,'source_record_index':index,
                'old_offset':at,'old_bytes':len(old),'new_bytes':len(value),'body_changed':value!=old,
                'parity_space_added':pad,'original_speaker_header_and_macro_contracts_preserved':True}
            changes.append(change);owned_changes.append(change)
        for ref in spec['choice_commands']:
            at=ref['old_offset'];length=ref['old_length'];word=struct.unpack_from('<H',block,at)[0]
            _require(word==struct.unpack_from('<H',original,at)[0]==0x2100,'original two-label choice required')
            labels=sorted((r for r in choices['records'] if r['block']==number and r['command_offset']==at),key=lambda r:r['option_index'])
            _require([r['option_index']for r in labels]==[0,1],'complete two-label choice review required')
            values=[]
            for row in labels:
                ident=row['id'];option=row['option_index'];_require(ident not in used_choices,'choice identity overlaps')
                used_choices.add(ident)
                for data,key,hexkey in [(block,'current_reference','current_text_hex'),(original,'source_reference','source_hex')]:
                    label_at=at+6+struct.unpack_from('<H',data,at+2+option*2)[0]
                    old=data[label_at:data.index(b'\0',label_at)]
                    _require(label_at==row[key]['offset'] and old.hex()==row[hexkey],'original/current choice label differs:'+ident)
                value=row['english'].encode('ascii')
                _require(bool(value) and value.strip()==value and all(32<=c<=126 for c in value)
                    and b'{' not in value and b'}' not in value,'choice label must be reviewed plain ASCII:'+ident)
                values.append(value)
                changes.append({'id':ident,'file_path':PATH,'block':number,'choice_command_offset':at,
                    'option_index':option,'old_offset':row['current_reference']['offset'],
                    'old_bytes':len(bytes.fromhex(row['current_text_hex'])),'new_bytes':len(value),
                    'typed_choice_label_and_original_result_mapping_preserved':True})
            first=values[0]+b'\0';first+=b'\0'*(-len(first)%2)
            second=values[1]+b'\0';second+=b'\0'*(-len(second)%2)
            value=b'\0\x21\0\0'+struct.pack('<H',len(first))+first+second
            _require(value.hex()==ref['target_hex']==menu_targets[(number,at)] and len(value)==ref['new_length'],'approved typed choice object differs')
            patches.append({'start':at,'end':at+length,'old':block[at:at+length],'value':value})
        patches.sort(key=lambda p:p['start'])
        _require(all(a['end']<=b['start']for a,b in pairwise(patches)),'owned patches overlap')
        result=[];last=0
        for patch in patches:
            result.extend((block[last:patch['start']],patch['value']));last=patch['end']
        result.append(block[last:end]);logical=bytearray(b''.join(result))
        _require(len(logical)==_mapped(patches,end) and len(logical)<0x2400,'target exceeds original cache or mapped extent')
        mapped_commands=spec['mapped_native_commands']
        _require(len(mapped_commands)==({81:10,82:45,83:21,84:31,86:14,88:30,91:16,92:25,93:18,94:17,95:14,96:13,99:8,100:6}[number])
            and len({r['old_offset']for r in mapped_commands})==len(mapped_commands), 'complete typed command census required')
        for command in mapped_commands:
            old_at,new_at=command['old_offset'],command['new_offset']
            _require(new_at==_mapped(patches,old_at)
                and command['new_native_extent']==_mapped(patches,old_at+command['old_native_extent'])-new_at
                and struct.unpack_from('<H',block,old_at)[0]==command['word']
                and struct.unpack_from('<H',logical,new_at)[0]==command['word']
                and command['target_0100_ancestors']==[_mapped(patches,a)for a in command['source_0100_ancestors']],
                'complete mapped command/extent/ancestor differs')
            if command['word']==0x4000:
                _require(block[old_at:old_at+6]==logical[new_at:new_at+6], 'original complete speech preamble changed')
            elif command['word']not in(0x100,0x200,0x300,0x2100):
                _require(block[old_at:old_at+command['old_native_extent']]==logical[new_at:new_at+command['new_native_extent']],
                    'unowned opaque command changed')
        _require(len(spec['relative_skip_fixups'])==({81:0,82:4,83:0,84:0,86:0,88:0,91:0,92:0,93:0,94:0,95:0,96:0,99:0,100:0}[number]), 'complete relative span census required')
        boundaries={r['new_offset']for r in spec['mapped_native_commands']}|{len(logical)}
        for edge in spec['relative_skip_fixups']:
            at=_mapped(patches,edge['offset']);target=_mapped(patches,edge['matched_skip_target']);span=target-at-4
            _require(at==edge['new_offset'] and target==edge['new_matched_skip_target']
                and at+4==edge['new_unmatched_next'] and target in boundaries and at+4 in boundaries
                and 0<=span<=0xFFFF and span%2==0 and span==edge['target_span']
                and struct.unpack_from('<H',block,edge['offset']+2)[0]==edge['source_span']
                and struct.unpack_from('<H',logical,at)[0]==edge['word'],'relative operand or destination differs')
            struct.pack_into('<H',logical,at+2,span)
        struct.pack_into('<H',logical,4,len(logical)-8)
        target=bytes(logical)+b'\0'*(-len(logical)%4)
        _require(sha(target)==spec['target_block_sha256'],'complete target block differs from reference proof')
        for row in owned_changes:
            ref=refs[row['id']];at=_mapped(patches,row['old_offset']);row['new_offset']=at
            _require(at==ref['new_offset'] and target[at-5:at]==HEADER,'relocated speech header differs')
        for row in changes:
            if row['block']==number and 'option_index' in row:
                at=_mapped(patches,row['choice_command_offset']);option=row['option_index']
                row['new_offset']=at+6+struct.unpack_from('<H',target,at+2+option*2)[0]
        restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
        for edge in spec['relative_skip_fixups']:
            struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
        for patch in reversed(patches):
            at=_mapped(patches,patch['start']);restored[at:at+len(patch['value'])]=patch['old']
        _require(bytes(restored)==block[:end],'inverse restoration changed an unowned source byte')
        container.blocks[number]=target
        block_reports.append({'block':number,'source_sha256':sha(block),'target_sha256':sha(target),
            'source_bytes':len(block),'target_bytes':len(target),'growth_bytes':len(target)-len(block),
            'relative_operands':len(spec['relative_skip_fixups']),'original_entry':8,
            'inverse_restores_every_original_logical_byte':True})
    _require(used_choices=={r['id']for r in choices['records']} and len(changes)==200,'incomplete speech/choice coverage')
    result=container.to_bytes()
    _require(sha(result)==config['target_SC2_sha256'],'complete target SC2 differs')
    _require([n for n,(a,b)in enumerate(zip(old_blocks,container.blocks,strict=True))if a!=b]==[81,82,83,84,86,88,91,92,93,94,95,96,99,100],
             'changed an unrelated SC2 block')
    image.replace_file(PATH,result)
    _require(image.read_file('/__arm9__.bin')==arm,'changed native runtime code')
    return {'source_SC2_sha256':sha(source),'target_SC2_sha256':sha(result),'required_runtime_ARM9_sha256':sha(arm),
        'manuscript':config['manuscript'],'choices':config['choices'],'reference_map':config['reference_map'],
        'changed_records':changes,'blocks':block_reports,'only_SC2_selected_fourteen_blocks_changed':True,
        'all322_other_SC2_blocks_unchanged':True,'all198_speeches_two_choices_and4_relative_operands_verified':True,
        'compiler_owned_parity_padding_and_typed_choice_offsets_verified':True,
        'native_code_and123040_staged_payload_unchanged':True}
