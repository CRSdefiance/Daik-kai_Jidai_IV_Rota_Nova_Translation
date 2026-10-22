"""Source-faithful notice refinement and repeat of the prospective layout matrix."""

from copy import deepcopy
from pathlib import Path
from types import FunctionType

from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_ceremony_layout_v807 as probe
from scripts.verify_village_wrap_v608 import read,save

MANUSCRIPT=Path('translations/ceremony_editorial_manuscript_v2.json')
ROOT=Path('work/analysis/ceremony_layout_v807_v2')


def main():
    old=read(probe.MANUSCRIPT);new=deepcopy(old)
    row=next(r for r in new['records'] if r['message_id']==290)
    assert row['japanese']=='%sたちは\n未知なる精神世界にいざなわれるという\n貴重な体験をしました'
    row['english']='%s and the others were drawn into an unfamiliar spiritual world. It was a remarkable experience.{PAD}'
    row['localization_note']='Restore the source experience of being drawn into an unknown spiritual world,which the old English replaced with unrelated trade-good instructions. Two ordinary English sentences preserve the group,experience and spiritual-world meaning without inserting a manual break;complete native formatting is rechecked for all four original given names and a23-character custom name.'
    new['supersedes']=str(probe.MANUSCRIPT)
    new['superseded_manuscript_sha256']=sha(probe.MANUSCRIPT.read_bytes())
    new['refinement_reason']='ID290 V1 leaves an article at a line end with a23-character supplied custom name. V2 uses a complete,source-faithful two-sentence paragraph. All51 other records and every formatting gate remain unchanged.'
    assert [r for r in old['records'] if r['message_id']!=290]==[r for r in new['records'] if r['message_id']!=290]
    assert all(not r['review']['formatting'] for r in new['records'])
    if MANUSCRIPT.exists():assert read(MANUSCRIPT)==new
    else:save(MANUSCRIPT,new)
    env={**probe.main.__globals__,'ROOT':ROOT,'MANUSCRIPT':MANUSCRIPT}
    FunctionType(probe.main.__code__,env)()
    report=read(ROOT/'research_report.json')
    report['adapter_producer_sha256']=sha(Path(__file__).read_bytes())
    report['superseded_initial_research']='work/analysis/ceremony_layout_v807/research_report.json'
    save(ROOT/'research_report.json',report)
    assert report['layouts']==92 and report['findings']==0
    print('V2 all92 prospective layouts and full fonts pass. Actual production contracts and scenes remain pending.',flush=True)


if __name__=='__main__':main()
