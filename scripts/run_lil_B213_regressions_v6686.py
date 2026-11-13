"""Run the repository's pytest regressions;preserve the wrong-runner diagnostic."""
from pathlib import Path
import subprocess,sys
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B213_regressions_v6686')
if __name__=='__main__':
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    names=['test_integrated_release','test_release_translation_integrity','test_dialogue_review','test_dialogue_tool',
        'test_dialogue_balanced_wrap','test_dialogue_pair_phase','test_dialogue_relocation','test_lil_editorial_literal_guard']
    command=[sys.executable,'-m','pytest','-q',*['tests/'+n+'.py' for n in names]]
    log=ROOT/'release_dialogue_regressions.log'
    with log.open('w',encoding='utf-8') as stream:r=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT,check=False)
    output=log.read_text(encoding='utf-8')
    save(ROOT/'terminal.json',dict(terminal=True,returncode=r.returncode,command=command,log=str(log),log_sha256=sha(log.read_bytes()),
        no_ROM_or_ledger_mutation_by_runner=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(output[-2200:],flush=True);raise SystemExit(r.returncode)
