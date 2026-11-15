"""Find retrospective wrap leads; bind live native storage without declaring defects."""
import re,inspect
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts import prove_lil_shrines_temples_controls_v3168c as catalogue
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/completed_contraction_wrap_leads_v7831')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7830/verified_handoff.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
ADAPTER=Path('work/analysis/maria_confrontation_effective_v7790/all16_effective_English_templates32_original_dispatches.json')
PATTERNS={
    'contracted-is-before-soft-break':r"\b(?:[Hh]e|[Ss]he|[Ii]t|[Tt]hat|[Tt]here|[Ww]ho|[Ww]hat|[Hh]ere)['’]s\s*\{LB\}",
    'contracted-am-are-before-soft-break':r"\b(?:[Ii]['’]m|[Yy]ou['’]re|[Ww]e['’]re|[Tt]hey['’]re)\s*\{LB\}",
    'split-negative-question-tag':r"\b(?:aren['’]t|isn['’]t|wasn['’]t|weren['’]t|don['’]t|doesn['’]t|didn['’]t|haven['’]t|hasn['’]t|won['’]t|wouldn['’]t|can['’]t|couldn['’]t)\s*\{LB\}\s*(?:you|he|she|it|we|they)\b[^.!?]*\?",
}

def raw_speeches(arm,blob,inventory):
    commands,speeches=inventory(arm,blob);rows=[]
    for speech in speeches:
        at=speech['offset']+5;end=blob.index(0,at+1);raw=blob[at:end]
        assert blob[at-5:at]==bytes.fromhex('0040ffff00')
        rows.append(dict(offset=at,record_index=blob[:at].count(b'\0'),raw_hex=raw.hex(),
            selector=raw[0],complete_preamble_hex=blob[at-5:at+1].hex(),
            native_extent=speech['native_extent'],ancestors=speech['ancestor_0100_offsets']))
    return commands,rows

if __name__=='__main__':
    assert not ROOT.exists()
    ledger,prior=map(read,[LEDGER,PRIOR]);assert sha(LEDGER.read_bytes())==prior['ledger_sha256']
    candidate=ledger['current_integrated_candidate'];rom_path=Path(candidate['path'])
    assert sha(rom_path.read_bytes())==candidate['sha256']==prior['candidate_sha256']
    image=NdsImage.open(rom_path);clean=NdsImage.open('work/clean.nds')
    current_arm=image.read_file('/__arm9__.bin');source_arm=clean.read_file('/__arm9__.bin')
    families=ledger['completed_editorial_families'];allrows=[(fi,ri,f,r) for fi,f in enumerate(families) for ri,r in enumerate(f['records'])]
    assert len(allrows)==ledger['records_editorially_completed']==6938
    available=Counter();leads=[]
    for fi,ri,f,r in allrows:
        for key in ['formatted_markup','formatted_lines','compiled_hex','source_hex','source_reference']:
            if r.get(key) is not None:available[key]+=1
        markup=r.get('formatted_markup')
        if not isinstance(markup,str):continue
        hits=[dict(pattern=name,match=m.group(),start=m.start(),end=m.end())
            for name,pattern in PATTERNS.items() for m in re.finditer(pattern,markup)]
        if hits:leads.append(dict(family_index=fi,record_index=ri,family=f,record=r,hits=hits))
    ROOT.mkdir(parents=True)
    current_input=ROOT/'current_ROM_binding.json';save(current_input,dict(current_ROM=str(rom_path),current_ROM_sha256=candidate['sha256']))
    adapter=read(ADAPTER)['source_owned_dispatch_adapters']['bind_current_catalog']
    lookups={};bindings=[]
    for route in sorted({int(x['record'].get('file_path',x['family'].get('file_path')).split('SC')[1][0]) for x in leads}):
        ns={**catalogue.__dict__,'SOURCE':current_input,'route':route,'route_mask':1<<route}
        exec(compile(adapter,__file__+'::unchanged-catalogue-binding','exec'),ns)
        lookups[route],binding=ns['bind_current_catalog'](image);bindings.append(binding)
    inventory,walker,invsource=scoped_inventory()
    groups={};rows=[];issues=[]
    for lead in leads:
        f,r=lead['family'],lead['record'];file=r.get('file_path',f.get('file_path'));block=r['block'];key=(file,block)
        if key not in groups:
            source_blob=IlnkContainer.parse(clean.read_file(file)).blocks[block]
            current_blob=IlnkContainer.parse(image.read_file(file)).blocks[block]
            sc,sr=raw_speeches(source_arm,source_blob,inventory);cc,cr=raw_speeches(current_arm,current_blob,inventory)
            groups[key]=dict(file_path=file,block=block,source_block_sha256=sha(source_blob),current_block_sha256=sha(current_blob),
                source_complete_native_commands=sc,current_complete_native_commands=cc,
                source_complete_native_speech_boundaries=sr,current_complete_native_speech_boundaries=cr)
        group=groups[key];compiled=bytes.fromhex(r['compiled_hex'])
        live=[x for x in group['current_complete_native_speech_boundaries'] if bytes.fromhex(x['raw_hex']) in [compiled,compiled+b' ']]
        source_index=int(r['id'].rsplit('_R',1)[1])
        sources=[x for x in group['source_complete_native_speech_boundaries'] if x['record_index']==source_index]
        entry=dict(id=r['id'],file_path=file,block=block,completed_family=f['id'],
            exact_ledger_record_reference=dict(path=str(LEDGER),sha256=sha(LEDGER.read_bytes()),
                JSON_pointer=f"/completed_editorial_families/{lead['family_index']}/records/{lead['record_index']}"),
            recorded_formatted_markup=r['formatted_markup'],recorded_compiled_hex=r['compiled_hex'],
            logical_English=r.get('logical_English',r.get('english',r.get('current_English'))),
            complete_historical_record=deepcopy(r),heuristic_matches=lead['hits'],
            current_native_boundary_matches=live,source_native_boundary_matches=sources,
            classification='pending-current-consumer-and-complete-exchange-editorial-review',
            no_automatic_defect_orretention_judgment=True,no_new_completion_credit=True)
        if len(live)==len(sources)==1:
            current,source=live[0],sources[0]
            assert current['complete_preamble_hex']==source['complete_preamble_hex']
            route=int(file.split('SC')[1][0]);raw=bytes.fromhex(current['raw_hex']);selected=lookups[route].get(raw[1:])
            entry.update(source_reference=dict(file_path=file,block=block,**source),
                current_reference=dict(file_path=file,block=block,**current),
                source_Japanese=bytes.fromhex(source['raw_hex'])[1:].decode('cp932'),
                compiled_equals_current_body_except_possible_one_zero_ink_storage_space=True,
                catalogue_match=None if selected is None else {k:(v.hex() if isinstance(v,bytes) else v) for k,v in selected.items()},
                current_raw_body_has_no_catalogue_override=selected is None,
                effective_body_native_dispatch_andnew_layout_changes_not_tested=True)
        else:
            issues.append(dict(id=r['id'],file_path=file,current_matches=len(live),source_matches=len(sources)))
        rows.append(entry)
    save(ROOT/'completed_layout_contraction_andquestion_tag_leads_with_live_storage_refs.json',dict(
        candidate=str(rom_path),candidate_sha256=candidate['sha256'],ledger=str(LEDGER),ledger_sha256=sha(LEDGER.read_bytes()),
        completed_record_rows_scanned=len(allrows),available_recorded_layout_metadata=dict(available),
        scan_scope='Only existing formatted_markup plans; missing markup is unscanned, and binary/COMMON text is not generically decoded.',
        patterns=PATTERNS,leads=rows,lead_count=len(rows),source_current_native_groups=list(groups.values()),binding_issues=issues,
        original_native_walker=walker,original_native_inventory=invsource,unchanged_catalogue_binding_adapter=adapter,
        offline_catalogue_bindings=bindings,
        all_source_current_references_are_offline_native_inventory_not_actual_scene_captures=True,
        existing_complete_exchange_reviews_preserved_not_freshly_claimed=True,
        ordinary_complete_word_wrapping_may_be_justified_case_by_case=True,
        no_global_keep_together_rule_width_change_authored_break_waiver_orautomatic_revision=True,
        next='Review coherent short predicates and question tags in full source/current exchanges; measure alternatives under the exact consumer and source controls. Retain ordinary wraps with reasons, and repair demonstrated early breaks without duplicate credit.',
        no_ROM_registry_ledger_orcounter_mutation=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,ADAPTER,Path(__file__)]},full_goal_complete=False))
    print('Recorded-layout rows',available['formatted_markup'],'of',len(allrows),';leads',len(rows),';native groups',len(groups),';binding issues',len(issues))
    for row in rows:print(row['file_path'],row['id'],'live',len(row['current_native_boundary_matches']),'source',len(row['source_native_boundary_matches']),'override',row.get('catalogue_match') is not None)
