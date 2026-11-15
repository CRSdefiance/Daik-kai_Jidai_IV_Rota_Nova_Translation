"""Versioned Market-through-Square planner;preserve the registered first23 compiler unchanged."""
import inspect
from dk4tool.dialogue import reviewed_help_pages_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(inspect.getsource(previous.plan_articles),{
    "len(topics)!=len(records) or len(original)!=202 or len(parent)!=211 or parent[203]!=b'\\0'":
        "len(topics)!=len(records) or topics!=set(range(21,44)) or len(original)!=202 or len(parent)!=212 or parent[203]!=b'\\0'",
    'Unique articles andcurrent211-topic/sentinel contract required':'Exact23 town articles andcurrent212-topic/sentinel contract required',
    "            if topic not in [7,8,9] or len(sections)!=3 or not row.get('semantic_section_reason'):":
        "            if topic!=37 or len(sections)!=2 or not row.get('semantic_section_reason'):",
    'Only the bound source biography/two-benefit lists aresectioned':'Only the bound source military-investment cost/outcome paragraphs aresectioned',
    "            if '［利点１］' not in Japanese or '［利点２］' not in Japanese:raise ValueError('Source benefit list missing')":
        "            if '１口につき' not in Japanese or '投資すると武装度が上がります' not in Japanese:raise ValueError('Source military cost/outcome paragraphs missing')",
    "        if topic==7:\n            continuation=row.get('current_continuation')\n            if continuation is None or continuation['topic_id']!=202 or bytes.fromhex(continuation['current_hex'])!=parent[202]:\n                raise ValueError('Exact existing Rafael continuation202 required')\n            if len(batches)!=2 or [l['topic_id'] for l in source_links(parent[7])].count(202)!=1 or [l['topic_id'] for l in source_links(parent[202])].count(7)!=1:\n                raise ValueError('Preserve the two-page source-benefit structure andexisting forward/back navigation')\n            ids.append(202);owned.add(202)\n        else:\n            for _ in batches[1:]:\n                if next_id==203 or next_id>255:raise ValueError('Native one-byte continuation ID bounds exceeded')\n                ids.append(next_id);owned.add(next_id);next_id+=1":
        """        if topic==37:
            declared=row.get('current_continuations')
            if declared is None or [r['topic_id'] for r in declared]!=[204,205]:
                raise ValueError('Both exact existing Military37 continuations required')
            if any(bytes.fromhex(r['current_hex'])!=parent[r['topic_id']] for r in declared):
                raise ValueError('Existing Military37 continuation bytes differ')
            if any([l['topic_id'] for l in source_links(parent[a])].count(b)!=1 for a,b in [(37,204),(204,205),(205,37)]):
                raise ValueError('Original three-page Military37 navigation ownership differs')
            for index,block in enumerate(parent):
                if index not in [37,204,205] and any(l['topic_id'] in [204,205] for l in source_links(block)):
                    raise ValueError('Another article owns a Military37 continuation entry')
            for continuation in declared[:len(batches)-1]:
                ids.append(continuation['topic_id']);owned.add(continuation['topic_id'])
        for _ in batches[len(ids):]:
            if next_id==203 or next_id>255:raise ValueError('Native one-byte continuation ID bounds exceeded')
            ids.append(next_id);owned.add(next_id);next_id+=1""",
    "any(target[i]!=parent[i] for i in range(204,211))":
        "any(target[i]!=parent[i] for i in range(202,len(parent)) if i not in owned)",
    'all_unowned_bytes_sentinel_andexisting_appended_topics_except_owned202_exact':
        'all_unowned_bytes_sentinel_andexisting_appended_topics_except_owned_military_continuations_exact',
})
env={**previous.plan_articles.__globals__,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-native-width-font-links-andinverse-with-scoped-Military37-ownership','exec'),env)
plan_articles=env['plan_articles']
