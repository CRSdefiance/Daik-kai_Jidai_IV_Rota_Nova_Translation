"""Source/runtime-locked155 speeches,two two-option menus andtwo source pauses."""
import json
import struct
from itertools import pairwise
from pathlib import Path
from dk4tool.dialogue.lil_B122_B127_layout_v2 import encode_relocatable_dialogue, audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_B122_B127_profile_v2 import profile_for
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PATH='/data/SC2.DK4'
CONFIG='translations/lil_B122_B127_editorial_release_v1.json'
HEADER=b'\0\x40\xff\xff\0'
BLOCKS=list(range(122,128))

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def _require(test,message):
    if not test:raise ValueError('Lil B122-B127 '+message)

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
    _require(config.get('format')=='dk4-lil-B122-B127-editorial-release-v1','unknown release format')
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
    doc,menu=[load(config[k]) for k in ['manuscript','choices']]
    mapping=load(config['reference_map'])
    for d in [doc,menu]:
        validate_natural_dialogue_batch(d)
        _require(d['translation_policy']=='natural-dialogue-v2' and d['target_locale']=='en-US'
            and d['encoder']=='dialogue-relocatable-v1' and d['formatting_review_pending'] is False,
            'source/native editorial contract differs')
        _require(d['reference_map']==config['reference_map'] and sha(Path(d['reference_map']).read_bytes())==d['reference_map_sha256'],
            'approved reference map differs')
    _require(doc['required_runtime_ARM9_sha256']==sha(arm),'reviewed runtime differs')
    _require(mapping.get('format')=='dk4-lil-B122-B127-source-relocation-map-v1'
        and mapping.get('external_references_complete') is True and mapping.get('entry_point_offset')==8
        and mapping.get('preserve_record_parity') is True and mapping.get('required_runtime_ARM9_sha256')==sha(arm)
        and mapping.get('source_SC2_sha256')==sha(source) and mapping.get('target_SC2_sha256')==config['target_SC2_sha256'],
        'complete source reference map required')
    for key in ['all312_physical_nested_command_boundaries_and64_relative_sites_verified',
        'all320_relocated_relative_skip_cases_preserve_original_targets',
        'all14_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM',
        'all155_active_speech_targets_preserved','two2100_objects_four_labels_and_source_indices_0_1_cancel_verified',
        'two_original2000_pause_words_and_mapped_resume_boundaries_verified',
        'trade_choice0_tutorial_choice1_already_know_branch_and_return0_both_VM_modes_verified',
        'no_dynamic_selector_or4100_objects','representative_shared_rules_approved']:
        _require(mapping.get(key) is True,'missing reference approval:'+key)
    _require(mapping['original_event_queries']==[],'unexpected event query')
    representative=load(doc['representative_proof'])
    _require(representative.get('no_open_translation_specific_display_or_control_finding') is True
        and representative.get('individual_selected_B122_B127_visits_not_required_for_reusable_rules') is True
        and representative.get('current_ARM9_COMMON_EV2_font_and_shared_consumer_bytes_exact') is True
        and representative.get('two2100_menus_source_order_indices_geometry_complete_planes_and_selection_cancel_bound') is True
        and representative.get('both_mapped_pause_resumption_boundaries_exact') is True
        and representative.get('trade_tutorial_and_already_know_branch_native_paths_and_both_return_modes_bound') is True
        and representative.get('actual_selected_B122_B127_IDs')==[]
        and representative.get('new_emulator_runs')==0,'source-bound representative approval required')
    for key in ['historical_representative_sheet_review','prior_current_sheet_review']:
        sheet=load(doc[key])
        _require(sheet.get('viewed') is True and sha(Path(sheet['sheet']).read_bytes())==sheet['sha256'],
            'viewed representative sheet required')
    _require(Path(doc['native_formatter_module'])==Path('dk4tool/dialogue/lil_B122_B127_layout_v2.py')
        and sha(Path(doc['native_formatter_module']).read_bytes())==doc['native_formatter_module_sha256'],
        'approved scoped formatter required')
    fonts={r['id']:r for r in load(doc['native_font_proof'])['cases']}
    FE=load(doc['native_FE_font_proof']);controls=load(doc['relocated_control_proof'])
    _require(len(FE['cases'])==10 and FE['ARM9_sha256']==sha(arm)
        and FE['all10_one_native_page_consumes_complete_target']
        and FE['all10_complete_native_independent_planes_all_glyphs_and_canaries_equal']
        and len(FE['source_leading_vertical_staging_cases'])==7 and len(FE['source_FI_null_actor_cases'])==3,
        'complete distinct FE contract required')
    _require(controls['all14_predicate_current_relocated_results_and_source_operands_equal']
        and controls['all10_FE_preserve_original_null_actor_before_dynamic_fallback']
        and controls['all155_final_stored_paragraphs_reach_expected_original_consumer_and_exact_macro_text']
        and len(controls['relocated_predicate_pairs'])==14 and controls['original_event_queries']==[],
        'relocated predicate/FE/dispatch approval required')
    branch=load(doc['conditional_return_proof']);wait=load(doc['original2000_wait_proof'])
    _require(sha(Path(doc['conditional_return_proof']).read_bytes())==doc['conditional_return_proof_sha256']
        and branch['source_current_target_branch_endings_preserved']
        and branch['selection0_skips_already_know_return_and_reaches_tutorial']
        and branch['selection1_enters_already_know_branch_and_return0']
        and len(branch['conditional_native_paths'])==6 and len(branch['original_VM_return_cases'])==12,
        'original tutorial/already-know branch return proof required')
    _require(sha(Path(doc['original2000_wait_proof']).read_bytes())==doc['original2000_wait_proof_sha256']
        and wait['current_zero_argument_wait_contract_bound_by_exact_original_code_and_actual_Lil_pause_evidence']
        and wait['all3_historical_pause_captures_viewed'],'source2000 actual-rule binding required')
    menu_native=load(doc['native_choice_proof']);menu_targets={}
    _require(menu_native['complete_current_and_reviewed_style_label_planes']==16
        and menu_native['native_selection_cancel_cases']==12,'complete two-menu native proof required')
    for m in menu_native['menus']:
        _require(sha(Path(m['proof']).read_bytes())==m['sha256'],'menu proof hash differs')
        detail=load(m['proof']);target=next(c for c in detail['current_and_reviewed_VM_and_font_cases'] if c['version']=='reviewed-research')
        menu_targets[(detail['block'],detail['original_command_offset'])]=target['object_hex']
    _require(len(menu_targets)==2,'two approved two-option objects required')
    refs={r['id']:r for b in mapping['blocks'] for r in b['text_records']}
    _require(len(doc['records'])==len(refs)==155 and {r['id'] for r in doc['records']}==set(refs),'155speech coverage differs')
    _require(len(fonts)==155 and set(fonts)==set(refs),'155complete native cases required')
    _require(len(menu['records'])==len({r['id'] for r in menu['records']})==4,'four choice labels required')
    _require(sorted(b['block'] for b in mapping['blocks'])==BLOCKS,'six exact blocks required')
    context=load(doc['source_context'])
    expected_commands={b['block']:len(b['all_current_native_commands']) for b in context['blocks']}
    _require(sum(expected_commands.values())==312,'source command census differs')
    container=IlnkContainer.parse(source);jp=IlnkContainer.parse(japanese);old_blocks=list(container.blocks)
    changes=[];reports=[];used_choices=set()
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
            _require(raw[0] in {2,6,9,20,26,92,95,151,254},'unapproved speaker:'+ident)
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
        _require(spec['actor_style_commands']==[],'unexpected actor-style object')
        for ref in spec['choice_commands']:
            at,length=ref['old_offset'],ref['old_length']
            _require(block[at:at+2]==original[at:at+2]==b'\0\x21','source two-option opcode differs')
            rows=sorted([r for r in menu['records'] if r['block']==n and r['command_offset']==at],key=lambda r:r['option_index'])
            _require([r['option_index'] for r in rows]==[0,1],'all2 ordered choices required')
            chunks=[];offsets=[];cursor=0
            for row in rows:
                ident=row['id'];i=row['option_index'];body_at,source_at,before,raw=bind_row(row)
                _require(ident not in used_choices and body_at==at+6+struct.unpack_from('<H',block,at+2+2*i)[0]
                    and source_at==at+6+struct.unpack_from('<H',original,at+2+2*i)[0],'choice source/index differs:'+ident)
                used_choices.add(ident);value=row['english'].encode('ascii')
                _require(value and value.strip()==value and all(32<=c<=126 for c in value) and b'{' not in value and b'}' not in value
                    and value.hex()==row['compiled_hex'],'choice must be reviewed plain ASCII:'+ident)
                offsets.append(cursor);chunk=value+b'\0';chunk+=b'\0'*(-len(chunk)%2);chunks.append(chunk);cursor+=len(chunk)
                r=ref['label_references'][i]
                _require(r['id']==ident and r['option_index']==i and r['new_length']==len(value),'choice target reference differs')
                changes.append(dict(id=ident,file_path=PATH,block=n,kind='choice',choice_command_offset=at,
                    option_index=i,old_offset=body_at,old_bytes=len(before),new_bytes=len(value),new_offset=r['new_offset']))
            value=struct.pack('<3H',0x2100,*offsets)+b''.join(chunks)
            _require(value.hex()==ref['target_hex']==menu_targets[(n,at)] and len(value)==ref['new_length']
                and all(r['typed_target_object_hex']==value.hex() for r in rows),'approved two-option object differs')
            patches.append(dict(start=at,end=at+length,old=block[at:at+length],value=value))
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
            elif c['word'] not in [0x100,0x200,0x300,0x400,0x4100,0x2100]:
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
        _require(len(spec['original2000_pause_and_resume_maps'])==(2 if n==122 else 0),'source pause census differs')
        for p in spec['original2000_pause_and_resume_maps']:
            a,z=p['old_offset'],p['new_offset'];resume=p['target_resume']
            _require(block[a:a+2]==original[a:a+2]==target[z:z+2]==b'\0\x20'
                and z==_mapped(patches,a) and p['source_resume']==a+2
                and resume==z+2==_mapped(patches,a+2) and resume in boundaries,'source2000 pause/resume differs')
        if n==126:
            for a in [336,954]:
                z=_mapped(patches,a)
                _require(block[a:a+4]==original[a:a+4]==target[z:z+4]==bytes(4),'conditional/final return0 differs')
        _require(sha(target)==spec['target_block_sha256'],'complete target block differs')
        for r in changes:
            if r['block']!=n:continue
            if r['kind']=='speech':
                _require(r['new_offset']==_mapped(patches,r['old_offset']) and target[r['new_offset']-5:r['new_offset']]==HEADER,'relocated speech header differs')
            elif r['kind']=='choice':
                a=_mapped(patches,r['choice_command_offset'])
                _require(r['new_offset']==a+6+struct.unpack_from('<H',target,a+2+2*r['option_index'])[0],'relocated choice pointer differs')
            else:raise ValueError('Unexpected ownership kind')
        restored=bytearray(logical);struct.pack_into('<H',restored,4,end-8)
        for edge in edges:struct.pack_into('<H',restored,edge['new_offset']+2,edge['source_span'])
        for p in reversed(patches):
            a=_mapped(patches,p['start']);restored[a:a+len(p['value'])]=p['old']
        _require(bytes(restored)==block[:end],'inverse restoration changed unowned bytes')
        container.blocks[n]=target
        reports.append(dict(block=n,source_sha256=sha(block),target_sha256=sha(target),source_bytes=len(block),
            target_bytes=len(target),growth_bytes=len(target)-len(block),relative_operands=len(edges),original_entry=8,
            two_option_menus=len(spec['choice_commands']),original2000_pauses=len(spec['original2000_pause_and_resume_maps']),
            inverse_restores_every_original_logical_byte=True))
    _require(used_choices=={r['id'] for r in menu['records']} and len(changes)==len({r['id'] for r in changes})==159,'incomplete editorial coverage')
    result=container.to_bytes()
    _require(sha(result)==config['target_SC2_sha256'],'complete SC2 target differs')
    _require([n for n,(a,b) in enumerate(zip(old_blocks,container.blocks,strict=True)) if a!=b]==BLOCKS,'unrelated block changed')
    _require(image.read_file('/__arm9__.bin')==arm,'native runtime changed')
    image.replace_file(PATH,result)
    return dict(source_SC2_sha256=sha(source),target_SC2_sha256=sha(result),required_runtime_ARM9_sha256=sha(arm),
        manuscript=config['manuscript'],choices=config['choices'],reference_map=config['reference_map'],
        changed_records=changes,blocks=reports,only_SC2_selected_six_blocks_changed=True,all330_other_SC2_blocks_unchanged=True,
        all155_speeches_four_choice_labels64_relative_operands_verified=True,
        both2000_pause_resume_boundaries_and_trade_return0_verified=True,
        both2100_menu_counts_indices01_cancel_and_native_planes_verified=True,
        native_code_and123040_staged_payload_unchanged=True)
