"""Reject falsely unowned or unbound context before native object binding can output."""
from copy import deepcopy
import subprocess
import sys
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil382_residual_A_clean_20261110')


def main():
    out = ROOT/'credited_context_negatives_v1'
    assert not out.exists()
    packetpath = ROOT/'current_inputs_v1/source_packet.json'
    packet = load(packetpath)
    current = ROOT/'current_v1/current_effective.json'
    parent = Path('work/maria315_B286_B302_release_v1/registered_release_verification.json')
    protected = {str(p):digest(p) for p in [packetpath,current,parent,Path(load(parent)['candidate'])]}
    out.mkdir()
    results = []
    for label in ['uncredited-style-context','missing-exact-source-binding']:
        changed = deepcopy(packet)
        row = next(g for g in changed['groups'] if g['block']==115)['complete_clean_context_records'][0]
        assert row['covered'] and row['kind']=='physical-style-alternative'
        if label=='uncredited-style-context':
            row['covered'] = False
        else:
            row['exact_credited_source_bindings'] = []
        data = out/(label+'.json')
        target = out/(label+'_must_not_exist')
        save(data,changed)
        command = [sys.executable,'-m','scripts.bind_editorial_current_credited_objects_v1',
            '--current',str(current),'--styles',str(ROOT/'current_inputs_v1/styles_meanings.json'),
            '--choices',str(ROOT/'current_inputs_v1/choices_meanings.json'),'--out',str(target),
            '--captain','2','--source-packet',str(data),'--ledger','translations/editorial_review_current_v1.json',
            '--expected-credited-style-objects','1','--expected-credited-style-records','5']
        result = subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        assert result.returncode != 0 and 'AssertionError' in result.stderr and not target.exists()
        (out/(label+'.stderr.txt')).write_text(result.stderr,encoding='utf-8')
        results.append(dict(label=label,terminal_exit_code=result.returncode,rejected_before_output=True,
            mutated_packet=str(data),mutated_packet_sha256=digest(data),command=command))
    assert all(digest(p)==h for p,h in protected.items())
    save(out/'qualification.json',dict(rejections=results,original_source_current_andROM_preserved=True,
        protected=protected,producer=str(Path(__file__)),producer_sha256=digest(__file__),new_credit=0))
    print('PASS two credited-context scope rejections; original source/current/ROM unchanged.')


if __name__=='__main__':
    main()
