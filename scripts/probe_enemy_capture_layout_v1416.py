"""Research all capture voices and legal ship-name lengths on the original CPU path.

CPU-only original loader/selection/printf/macro/formatter execution,with existing
actors. Host file success and portrait UI construction are explicit boundaries.
No actor,role,RNG,result or emulator mutation. Findings never imply approval.
"""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.enemy_capture_native_plan_v1415 import compiled
from scripts.probe_battle_aftermath_fonts_v1256 import consumer
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/enemy_capture_layout_v1416')
PLAN = Path('work/analysis/enemy_capture_payload_v1415/native_payload_plan.json')
DOC = Path('translations/enemy_capture_editorial_manuscript_v1.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,doc = read(PLAN),read(DOC)
    assert sha(DOC.read_bytes())==plan['manuscript_sha256']
    context = read(doc['source_context'])
    assert sha(Path(doc['source_context']).read_bytes())==doc['source_context_sha256']
    observed = context['prior_actual_2082']
    raw = Path(observed['snapshot']).read_bytes()
    assert sha(raw)==observed['snapshot_sha256']
    arm,common = Path(plan['target_ARM9']).read_bytes(),Path(plan['target_COMMON']).read_bytes()
    assert sha(arm)==plan['target_ARM9_sha256'] and sha(common)==plan['target_COMMON_sha256']
    representatives = {}
    for source in context['all206_existing_actor_choices']:
        representatives.setdefault(source['source_voice'],source)
        if source['existing_actor_ID']==18:
            representatives[source['source_voice']] = source
    assert set(representatives)==set(range(8))
    names = [('actual-original-enemy',b'Hanse Cog')]
    names += [('legal-editor-byte-bound',b'F'+b'A'*(n-1)) for n in range(1,19)]
    names += [('macro-literal-regression',s.encode('cp932')) for s in
        ['FALCON','ICARUS','FIFOFOFU','Santa Maria',"F's Hope",'長崎丸'*3,'ＦＡＬＣＯＮ']]
    assert len(names)==26 and all(1<=len(n)<=18 for k,n in names)
    ROOT.mkdir(parents=True)
    cases,findings = [],[]
    for row in doc['records']:
        source = representatives[row['source_voice']]
        value = compiled(row)
        for index,(kind,name) in enumerate(names):
            native = consumer(arm,common,raw,plan,0x53F0C,source['actor_object'],context['source_table'],name)
            expected = value.replace(b'%s',name)
            assert native['input_hex']==expected.hex(),(row['message_id'],name,'printf')
            formatted = bytes.fromhex(native['formatted_hex'])
            lines = [v.decode('cp932') for v in formatted.split(b'\n')]
            readable = [v.strip() for v in lines]
            issues = []
            if ' '.join(readable)!=expected.decode('cp932'):
                issues.append('word-or-name-bytes-altered-or-split')
            if not 1<=len(lines)<=4 or any(len(v.encode('cp932'))>38 for v in lines):
                issues.append('native-lines-or-width-outside-view')
            margins = [len(v)-len(v.lstrip(' ')) for v in lines]
            if len(set(margins))>1:
                issues.append('unequal-native-leading-space-counts-requires-font-margin-check')
            if any('  ' in s for s in readable):
                issues.append('internal-padding')
            if len(lines)>1 and len(readable[-1].split())==1:
                issues.append('isolated-last-word')
            if readable[-1].rstrip('!.?').lower().split()[-1] in {'the','a','an','of','to','and','or','with','enemy','ship'}:
                issues.append('weak-final-fragment')
            case = {'message_ID':row['message_id'],'source_voice':source['source_voice'],
                'existing_actor_ID':source['existing_actor_ID'],'existing_actor_object':source['actor_object'],
                'variant':index,'name_kind':kind,'name':name.decode('cp932'),'name_hex':name.hex(),
                'expected_after_printf_hex':expected.hex(),'native_pipeline':native,
                'native_lines':lines,'native_leading_space_counts':margins,'findings':issues}
            cases.append(case)
            if issues:
                findings.append({k:case[k] for k in ['message_ID','variant','name','native_lines','findings']})
        print(row['message_id'],repr(row['english']),'26 native names inspected',flush=True)
    save(ROOT/'native_layout_research.json',{'manuscript':str(DOC),'manuscript_sha256':sha(DOC.read_bytes()),
        'plan':str(PLAN),'plan_sha256':sha(PLAN.read_bytes()),'cases':cases,'findings':findings,
        'all208_original_selection_printf_macro_layout_cases_executed':True,
        'all206_source_existing_actor_choices':context['all206_existing_actor_choices'],
        'no_identity_role_RNG_result_or_emulator_mutation':True,
        'original_direct_consumer_and_one_ship_name_argument_preserved':True,
        'full_font_planes_original_visible_gameplay_and_release_still_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('208 layouts recorded;findings:',len(findings),';no formatting/release/completion approval.',flush=True)
