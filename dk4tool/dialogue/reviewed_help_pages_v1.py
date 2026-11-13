"""Plan complete source-bound Help articles with compiler-owned semantic pagination."""
import re
from copy import deepcopy
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.help_source_links import source_links
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_help_pages_v281 import wrap,encoded_line,WIDTH


def plan_articles(manuscript,clean,canonical,current,*,require_formatting=True):
    if manuscript.get('translation_policy')!='natural-dialogue-v2' or manuscript.get('target_locale')!='en-US':
        raise ValueError('Source-reviewed American English Help required')
    for key,raw in [('source_clean_HELP_sha256',clean),('source_canonical_HELP_sha256',canonical),('source_current_HELP_sha256',current)]:
        if manuscript[key]!=sha(raw):raise ValueError('Complete Help source lock differs:'+key)
    original,baseline,parent=[IlnkContainer.parse(raw).blocks for raw in [clean,canonical,current]]
    records=manuscript['records'];topics={r['topic_id'] for r in records}
    if len(topics)!=len(records) or len(original)!=202 or len(parent)!=211 or parent[203]!=b'\0':
        raise ValueError('Unique articles andcurrent211-topic/sentinel contract required')
    gates=['source','context','localization','naturalness']+(['formatting'] if require_formatting else [])
    pages=[];next_id=len(parent);owned=set(topics);article_proofs=[]
    for row in records:
        topic=row['topic_id']
        if not all(row.get('review',{}).get(g) is True for g in gates):raise ValueError('Per-article gates missing')
        for key,blocks in [('clean_source_hex',original),('canonical_source_hex',baseline),('current_source_hex',parent)]:
            if bytes.fromhex(row[key])!=blocks[topic]:raise ValueError('Exact article source differs')
        title,english=row['heading'],row['english']
        for value in [title,english]:
            if not value.isascii() or value!=value.strip() or any(ord(c)<32 for c in value) or '  ' in value or '{' in value or '}' in value:
                raise ValueError('Natural unpositioned ASCII prose required')
        sections=row.get('semantic_sections',[english])
        if not sections or ' '.join(sections)!=english:raise ValueError('Semantic sections change logical prose')
        if len(sections)>1:
            if topic not in [7,8,9] or len(sections)!=3 or not row.get('semantic_section_reason'):
                raise ValueError('Only the bound source biography/two-benefit lists aresectioned')
            Japanese=bytes.fromhex(row['clean_source_hex']).decode('cp932')
            if '［利点１］' not in Japanese or '［利点２］' not in Japanese:raise ValueError('Source benefit list missing')
        groups=[wrap(s) for s in sections];body=[line for group in groups for line in group]
        if len(wrap(title))+len(body)<=10:
            batches=[wrap(title)+body]
        else:
            queue=deepcopy(groups);batches=[]
            while queue:
                heading=wrap(title if not batches else title+' (continued)');content=list(heading)
                while queue and len(content)+len(queue[0])<=9:content.extend(queue.pop(0))
                if len(content)==len(heading) and queue:
                    take=9-len(content)
                    if take<=0:raise ValueError('Heading leaves no body space')
                    content.extend(queue[0][:take]);queue[0]=queue[0][take:]
                batches.append(content)
        ids=[topic]
        if topic==7:
            continuation=row.get('current_continuation')
            if continuation is None or continuation['topic_id']!=202 or bytes.fromhex(continuation['current_hex'])!=parent[202]:
                raise ValueError('Exact existing Rafael continuation202 required')
            if len(batches)!=2 or [l['topic_id'] for l in source_links(parent[7])].count(202)!=1 or [l['topic_id'] for l in source_links(parent[202])].count(7)!=1:
                raise ValueError('Preserve the two-page source-benefit structure andexisting forward/back navigation')
            ids.append(202);owned.add(202)
        else:
            for _ in batches[1:]:
                if next_id==203 or next_id>255:raise ValueError('Native one-byte continuation ID bounds exceeded')
                ids.append(next_id);owned.add(next_id);next_id+=1
        semantic=[];actual_links=[]
        for number,rows in enumerate(batches):
            header=wrap(title if number==0 else title+' (continued)')
            semantic.extend(encoded_line(tokens)[1] for tokens in rows[len(header):])
            if len(batches)>1:
                target=ids[number+1] if number+1<len(batches) else topic
                rows=rows+[[dict(label='Continue reading' if number+1<len(batches) else 'Back to article start',id=target,navigation=True)]]
            data=bytearray();visible=[];links=[]
            for line,tokens in enumerate(rows):
                encoded,text,selected=encoded_line(tokens);data.extend(encoded+b'\n');visible.append(text)
                links.extend({**link,'row':line} for link in selected)
            data.append(0)
            if len(rows)>10 or len(data)>=1024 or any(len(line)>WIDTH for line in visible):raise ValueError('Native Help row/buffer bounds exceeded')
            actual_links.extend(link['id'] for link in links if not link['navigation'])
            pages.append(dict(topic_id=ids[number],source_article_id=topic,page_number=number+1,page_count=len(batches),
                visible_lines=visible,links=links,bytes=len(data),encoded_hex=data.hex()))
        expected=[l['topic_id'] for l in source_links(original[topic])]
        if actual_links!=expected or row['original_link_IDs']!=expected:raise ValueError('Original binary links changed')
        plain=re.sub(r'\[\[[0-9]+\|([^\]]+)\]\]',r'\1',english)
        if ' '.join(semantic)!=plain:raise ValueError('Pagination loses orchanges prose')
        article_proofs.append(dict(topic_id=topic,page_ids=ids,all_complete_prose_andoriginal_links_exact=True,
            semantic_sections=len(sections),source_semantic_section_reason=row.get('semantic_section_reason')))
    if len({p['topic_id'] for p in pages})!=len(pages):raise ValueError('Overlapping planned page ownership')
    target=list(parent)
    for page in pages:
        while len(target)<=page['topic_id']:target.append(b'\0')
        target[page['topic_id']]=bytes.fromhex(page['encoded_hex'])
    if any(target[i]!=raw for i,raw in enumerate(parent) if i not in owned):raise ValueError('Unowned Help bytes changed')
    if target[203]!=parent[203] or any(target[i]!=parent[i] for i in range(204,211)):
        raise ValueError('Existing added articles/history sentinel changed')
    encoded=IlnkContainer(target).to_bytes();inverse=list(target[:len(parent)])
    for index in owned:
        if index<len(parent):inverse[index]=parent[index]
    if IlnkContainer(inverse).to_bytes()!=current:raise ValueError('Complete Help parent inverse differs')
    return encoded,dict(pages=pages,articles=article_proofs,planning_cells=41,native_width_px=252,native_height_px=120,native_rows=10,
        source_topic_count=len(original),parent_topic_count=len(parent),target_topic_count=len(target),owned_topic_ids=sorted(owned),
        source_HELP_sha256=sha(current),target_HELP_sha256=sha(encoded),
        all_unowned_bytes_sentinel_andexisting_appended_topics_except_owned202_exact=True,
        complete_parent_inverse_exact=True,all_original_links_andcomplete_logical_prose_exact=True,
        compiler_generated_navigation_pairs=[dict(article=p['topic_id'],page_ids=p['page_ids']) for p in article_proofs if len(p['page_ids'])>1],
        formatting_gate_required=require_formatting,native_glyphs_widgets_gameplay_andrelease_still_pending=True)
