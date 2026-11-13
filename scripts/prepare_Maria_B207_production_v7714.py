"""Source-lock Maria reconstruction to18 sealed records before one final single-file commit."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_production_tools_v7714')
if __name__=='__main__':
    assert not ROOT.exists()
    tool=derive('dk4tool/patch/papal_trade_editorial_v1.py','dk4tool/patch/maria_B207_editorial_v1.py',{
        'Reconstruct both sealed exchanges, then commit the two staged files in one operation.':'Reconstruct the sealed Maria exchange, then commit one staged file afterall guards.',
        'papal_trade_profile_v1':'maria_B207_profile_v1','papal_trade_layout_v1':'maria_B207_layout_v1','papal_trade_atomic_support_v1':'maria_B207_atomic_support_v1',
        'scripts.seal_papal_trade_references_v7656':'scripts.seal_Maria_B207_references_v7713',
        'translations/papal_trade_editorial_release_v1.json':'translations/maria_B207_editorial_release_v1.json',
        "PATHS=('/data/SC0.DK4','/data/SC1.DK4')":"PATHS=('/data/SC3.DK4',)",
        'Papal trade editorial contract: ':'Maria B207 editorial contract: ',
        'dk4-papal-trade-editorial-release-v1':'dk4-Maria-B207-editorial-release-v1',
        "len(conf['manuscripts'])==2":"len(conf['manuscripts'])==1",
        'two-file release configuration':'single-file Maria release configuration',
        'dk4-papal-trade-source-relocation-map-v1':'dk4-Maria-B207-source-relocation-map-v1',
        "seal['all36_five_gates_andexact_references_approved']":"seal['all18_five_gates_andexact_references_approved']",
        "len(mapping['groups'])==2":"len(mapping['groups'])==1",
        "for route,path in enumerate(conf['manuscripts']):":"for path in conf['manuscripts']:\n        route=3",
        "mapping['groups'][route]":"mapping['groups'][0]",
        "file=PATHS[route];n=[246,237][route]":"file=PATHS[0];n=207",
        "conf['archives'][route]":"conf['archives'][0]",
        "seal['manuscripts'][route]":"seal['manuscripts'][0]",
        "r['route']==route":"r['route_identity']=='Maria'",
        "r['full_exchange_read_aloud_review']":"r['whole_English_exchange_cadence_andemotional_progression_reviewed']",
        "len(blocks)==[343,325][route]":"len(blocks)==303",
        r"block[:4]==b'CS\0\1'":r"block[:4]==b'CS\1\1'",
        "packet['groups'][route]['records']":"packet['records']",
        "packet['groups'][route]['all_current_native_commands']":"packet['all_current_native_commands']",
        "font['groups'][route]['records']":"font['records']",
        "stored['groups'][route]['records']":"stored['records']",
        "control['groups'][route]['dispatch_cases']":"control['dispatch_cases']",
        "source/current references:'+ident)":"source/current references:'+ident)\n            require(row['source_meaning']==before['source_gloss'] and row['source_Japanese']==before['source_Japanese'] and row['context']==before['full_exchange_context'],'source gloss/context:'+ident)\n            require((row['editorial_decision']=='retain-wording')==(' '.join(old[1:].decode('cp932').split())==row['english'].split('}',1)[1]),'individual retention comparison:'+ident)",
        "row['source_record_index']==5":"row['source_record_index']==4",
        'patches.append(dict(start=at,end=at+len(old),old=old,value=value))':'patches.append(dict(start=at,end=at+len(old),old=old,value=value,source_raw=raw))',
        "pads==8,'eight zero-ink parity tails perroute'":"pads==7,'seven zero-ink parity tails'",
        '1508':'1472','1506':'1470','1498':'1462','1494':'1458','1502':'1466',
        "require(bytes(inverse)==block,'full1468 predecessor inverse')":"require(bytes(inverse)==block,'full1468 predecessor inverse')\n        clean_inverse=bytearray(target[:1470]);struct.pack_into('<H',clean_inverse,4,1460)\n        for r in reversed(patches):at=mapped(r['start']);clean_inverse[at:at+len(r['value'])]=r['source_raw']\n        require(bytes(clean_inverse)==japanese,'full1468 clean source inverse')",
        "len(prepared)==2 and len(changes)==36,'two complete staged archives'":"len(prepared)==1 and len(changes)==18,'one complete staged archive'",
        'only two intended file slots':'only the intended SC3 file slot',
        'All validation and both reconstructions':'All validation and complete source/predecessor reconstructions',
        'both_full_predecessor_archives_reversible=True,all36_actual_single_pages_andcomplete_headers_bound=True':'full_clean_block_andpredecessor_archive_reversible=True,all18_actual_single_pages_andcomplete_headers_bound=True',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_atomic_reconstruction.json',dict(derivation=tool,all_native_high_constants_andmultiplicity_preserved=True,complete_clean_source_inverse_andindividual_retention_comparison_added=True,all_validations_precede_one_files_list_assignment=True,new_credit=0,full_goal_complete=False))
