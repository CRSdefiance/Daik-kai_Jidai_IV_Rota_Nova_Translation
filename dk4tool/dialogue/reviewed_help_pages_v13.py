"""Remaining67 Help articles with source paragraphs and exclusive reuse of five existing continuations."""
from dk4tool.dialogue import reviewed_help_pages_v12 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE=checked_text(previous.SOURCE,{
    "topics!=({33}|set(range(103,133))) or len(original)!=202 or len(parent)!=217":
        "topics!=(set(range(133,202))-{181,184}) or len(original)!=202 or len(parent)!=217",
    'Exact Deck30 plus Coerce33 amendment andcurrent217-topic/sentinel contract required':
        'Exact remaining67 Help articles andcurrent217-topic/sentinel contract required',
    "            if topic!=66 or len(sections)!=2 or not row.get('semantic_section_reason'):":
        "            if topic not in {133:16,139:2,150:3,151:2,168:2} or len(sections)!={133:16,139:2,150:3,151:2,168:2}[topic] or not row.get('semantic_section_reason'):",
    'Only the source-bound regional-fleet definition andoperating-funds paragraphs aresectioned':
        'Only the source16-entry table andreviewed crew/share/exclusive/HP paragraphs aresectioned',
    "            markers={66:['委任方針','運用資金','金貨10万枚']}":
        "            markers={133:['必要能力一覧','マスト','主計室'],139:['旗艦重視','平均化','必要最小'],150:['最初の１％','本拠地ポイント'],151:['100％','他の勢力'],168:['ＨＰ','生命力','徐々に回復']}",
    "        if topic==37:\n            declared=row.get('current_continuations')\n            if declared is None or [r['topic_id'] for r in declared]!=[204,205]:\n                raise ValueError('Both exact existing Military37 continuations required')\n            if any(bytes.fromhex(r['current_hex'])!=parent[r['topic_id']] for r in declared):\n                raise ValueError('Existing Military37 continuation bytes differ')\n            if any([l['topic_id'] for l in source_links(parent[a])].count(b)!=1 for a,b in [(37,204),(204,205),(205,37)]):\n                raise ValueError('Original three-page Military37 navigation ownership differs')\n            for index,block in enumerate(parent):\n                if index not in [37,204,205] and any(l['topic_id'] in [204,205] for l in source_links(block)):\n                    raise ValueError('Another article owns a Military37 continuation entry')\n            for continuation in declared[:len(batches)-1]:\n                ids.append(continuation['topic_id']);owned.add(continuation['topic_id'])":
    """        existing={133:209,139:210,150:206,151:207,168:208}
        if topic in existing:
            declared=row.get('current_continuations');child=existing[topic]
            if declared is None or [r['topic_id'] for r in declared]!=[child]:
                raise ValueError('Exact existing owned article continuation required')
            if bytes.fromhex(declared[0]['current_hex'])!=parent[child]:
                raise ValueError('Existing owned continuation bytes differ')
            if any([l['topic_id'] for l in source_links(parent[a])].count(b)!=1 for a,b in [(topic,child),(child,topic)]):
                raise ValueError('Original continuation forward/back ownership differs')
            for index,block in enumerate(parent):
                if index not in [topic,child] and any(l['topic_id']==child for l in source_links(block)):
                    raise ValueError('Another article owns this continuation')
            if len(batches)>1:ids.append(child);owned.add(child)""",
})

env={**previous.plan_articles.__globals__,'__file__':__file__}
exec(compile(SOURCE,__file__+'::same-native-pages-all-links-inverse-andsource-locked-five-continuation-owners','exec'),env)
plan_articles=env['plan_articles']
