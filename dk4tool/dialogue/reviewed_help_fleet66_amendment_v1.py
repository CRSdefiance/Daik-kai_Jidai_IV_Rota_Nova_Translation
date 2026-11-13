"""Reformat one source-bound stat-name correction, preserving its existing two-page ownership."""
from dk4tool.dialogue import reviewed_help_pages_v5 as previous
from scripts.source_locked_derivation_v5118 import checked_text

SOURCE = checked_text(previous.SOURCE, {
    "topics!=set(range(44,81)) or len(original)!=202 or len(parent)!=216":
        "topics!={66} or len(original)!=202 or len(parent)!=217",
    'Exact37 shipyard-to-ruins articles andcurrent216-topic/sentinel contract required':
        'Exact Fleet66 amendment and current217-topic/sentinel contract required',
    "        if topic==37:": "        if topic==66:\n            if len(batches)!=2:raise ValueError('Retain existing two-page Fleet66 structure')",
    "[r['topic_id'] for r in declared]!=[204,205]": "[r['topic_id'] for r in declared]!=[216]",
    'Both exact existing Military37 continuations required': 'Exact existing Fleet66 continuation required',
    'Existing Military37 continuation bytes differ': 'Existing Fleet66 continuation bytes differ',
    '[(37,204),(204,205),(205,37)]': '[(66,216),(216,66)]',
    'Original three-page Military37 navigation ownership differs': 'Original two-page Fleet66 navigation ownership differs',
    "index not in [37,204,205] and any(l['topic_id'] in [204,205]":
        "index not in [66,216] and any(l['topic_id'] in [216]",
    'Another article owns a Military37 continuation entry': 'Another article owns a Fleet66 continuation entry',
    "        sections=row.get('semantic_sections',[english])":
        "        if 'Command of at least 150.' not in english or 'Leadership' in english:\n            raise ValueError('Bound native Command stat and unchanged threshold required')\n        sections=row.get('semantic_sections',[english])",
})
env = {**previous.plan_articles.__globals__, '__file__': __file__}
exec(compile(SOURCE, __file__ + '::same-source-links-parser-bounds-and-inverse-with-existing66-216-ownership', 'exec'), env)
plan_articles = env['plan_articles']
