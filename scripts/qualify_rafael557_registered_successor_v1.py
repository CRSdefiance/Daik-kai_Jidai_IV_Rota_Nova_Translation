"""Reject invalid source, runtime macro, storage and review evidence before a build."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/qualify_plain_SC0_registered_successor_v1.py').read_text(encoding='utf-8'),{
    "('changed-logical-prose','manuscript'),('wrong-control-only-membership',None)":
        "('changed-logical-prose','manuscript'),('changed-FU-macro','manuscript'),('changed-stored-target','manuscript'),('wrong-control-only-membership',None)",
    "set(config['blocks'])|{89}":"set(config['blocks'])|{140}",
    "doc['offline_only_source_speeches'] = 0":"doc['offline_only_speech_variants'] = 0",
    "            elif kind == 'changed-logical-prose':":"""            elif kind == 'changed-FU-macro':
                row=next(r for r in doc['records'] if '{MACRO:FU}' in r['english'])
                row['english']=row['english'].replace('{MACRO:FU}','{MACRO:FA}')
            elif kind == 'changed-stored-target':
                row=next(r for r in doc['records'] if r['id']=='DK4_MES_B154_R0084')
                row['planned_integrated_reference']['offset']+=2
            elif kind == 'changed-logical-prose':""",
    'assert len(rejections) == 8':'assert len(rejections) == 10',
    'eight semantic andordering rejections':'ten semantic and ordering rejections',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-pure-transaction-with-exact-FU-and-storage-rejections','exec'),globals())
