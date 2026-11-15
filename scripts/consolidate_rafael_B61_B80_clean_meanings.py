"""Bind all539 individual clean meanings andretain the zero-speech control block."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
NAMES=['B61_B63_77','B64_120','B65_B67_92','B69_B70_108','B71_B75_116','B76_B80_26']

if __name__=='__main__':
    output=ROOT/'all539_clean_meanings_v1.json';assert not output.exists()
    packet_path=ROOT/'clean_source_packet.json';packet=load(packet_path)
    paths=[ROOT/(name+'_clean_meanings_v1.json') for name in NAMES]
    rows=[r for p in paths for r in load(p)['records']]
    source=[r for g in packet['groups'] for r in g['records']]
    assert len(rows)==len(source)==packet['records']==539 and len({r['id'] for r in rows})==539
    byid={r['id']:r for r in rows}
    for original in source:
        reviewed=byid[original['id']]
        assert all(reviewed[k]==v for k,v in original.items())
        assert reviewed['source_meaning'] and reviewed['whole_exchange_context'] and reviewed['earlier_English_unconsulted']
    control=[g for g in packet['groups'] if not g['records']]
    assert len(control)==1 and control[0]['block']==68
    rows=[deepcopy(byid[r['id']]) for r in source]
    # Later complete exchanges provide context,not permission to rewrite earlier
    # frozen source receipts ordeclare a relationship the game never states.
    cross_context=[
        dict(blocks=[63,73],finding='B73 explicitly recalls the B63 quarrel/advice andadds Claudio jealousy subtext. Eirene womanhood is privately discussed;public Arcadius controls remain. No declared romance orfamily relationship.'),
        dict(blocks=[64,65,66,67,69],finding='Village arc moves from pity/dignity through investment,timber,corn seeds andself-conscious affection to successful production/celebration. Preserve actual progress andfuture promises at each stage,Romani identity andattributed prejudice.'),
        dict(blocks=[64,69,75],finding='Portugal threatened in the B64 recollection is explicitly annexed by B69/B75. Do not flatten these distinct source states into one timeline statement.'),
        dict(blocks=[70,71,72],finding='Maria key bargain,Kurushima defeat/directions andalternative handovers arecondition-linked,not one unconditional linear dialogue.'),
        dict(blocks=[74,75,77,78,80],finding='Final-battle warnings andValdes contempt coexist with an explicit direct-battle-loss supremacy alternative andPortuguese royal restoration/summons. Preserve each condition andthe source result.')]
    save(output,dict(source_packet=str(packet_path),source_packet_sha256=sha(packet_path.read_bytes()),records=rows,
        source_meaning_inputs={str(p):sha(p.read_bytes()) for p in paths},complete_source_blocks=list(range(61,81)),
        zero_speech_control_only_blocks=[dict(block=68,source_block_sha256=control[0]['clean_block_sha256'],commands=len(control[0]['all_source_commands']))],
        all539_clean_source_meanings_read_before_older_English=True,complete_exchange_cross_context=cross_context,
        FE_can_be_unlabeled_character_speech_not_automatically_system_narration=True,
        unresolved_context=['Exact source names/role labels/public-private alias anditem bindings','EV0/branch alternatives andoriginal entry membership',
            'B69 CG/staged gesture context;no kiss orother unstated action inferred','B77 sourceエシュタード approved term binding'],
        logical_English_drafts_current_comparisons_native_formatting_gameplay_andrelease_pending=True,
        all_five_editorial_gates_pending=True,source_gloss_not_final_English=True,new_credit=0,guide_photos=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('All539 source meanings sealed withwhole-exchange cross-context;B68 control-only preserved. Names/events/drafts/current English/formatting/release remain.',flush=True)
