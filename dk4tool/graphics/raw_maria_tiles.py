"""Source-locked decorative Maria headings; covered backing estimates are explicit."""

import hashlib
import struct
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BLOCK_SHA = 'c95b9d4b968638d488158c8971c03f4116ac6e6ceb8a6863a4de5a1b05b54464'
FRAME_BYTES = 153600
BOXES = {11: [137, 138, 314, 205], 12: [192, 14, 311, 220]}
LAYOUTS = {
    11: [('Ma', [149,153,190,193], 19, 0, 0),
         ('ri', [182,141,213,186], 26, 11164, 0),
         ('a', [211,164,237,194], 24, 18314, 0),
         ('Mode', [241,153,313,187], 20, 0, 0)],
    12: [('Ma', [260,17,309,63], 24, 3191, 0),
         ('ri', [231,50,258,93], 27, 32767, 0),
         ('a', [264,105,290,135], 25, 32767, 0),
         ('Mode', [205,108,247,216], 25, 0, -90)],
}


def channels(word):
    return [(word >> (c * 5)) & 31 for c in range(3)]


def inside(x, y, box):
    return box[0] <= x < box[2] and box[1] <= y < box[3]


def render_maria_tiles(row, source_region, batch, source_block):
    f = row.get('image_index')
    if (f not in BOXES or row.get('box') != BOXES[f] or row.get('english') != 'Maria Mode'
            or row.get('source_text') != 'まりあもーど'
            or source_block is None or hashlib.sha256(source_block).hexdigest() != BLOCK_SHA):
        raise ValueError('Maria tiles require the exact reviewed source heading')
    font_path = Path(batch['font_file_path'])
    if hashlib.sha256(font_path.read_bytes()).hexdigest() != batch['font_sha256']:
        raise ValueError('Maria tile font identity differs')
    x0,y0,x1,y1 = row['box'];w,h=x1-x0,y1-y0
    if len(source_region) != w*h*2:
        raise ValueError('Maria tile plane extent differs')
    original = [v for v, in struct.iter_unpack('<H',source_region)]
    frame = source_block[f*FRAME_BYTES:(f+1)*FRAME_BYTES]
    frame_words = [v for v, in struct.iter_unpack('<H',frame)]

    def old_at(x,y):
        return frame_words[y*320+x]

    white_a_component=set()
    white_ri_component=set()
    if f == 12:
        pending=deque([(273,106)])
        white_a_component.add((273,106))
        while pending:
            x,y=pending.popleft()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                xx,yy=x+dx,y+dy
                if (248<=xx<310 and 92<=yy<147 and (xx,yy) not in white_a_component
                        and old_at(xx,yy)==32767):
                    white_a_component.add((xx,yy));pending.append((xx,yy))
        if len(white_a_component)!=317:
            raise ValueError('Original tilted-tile white letter component differs')
        candidates=[(x,y) for y in range(51,91) for x in range(230,258) if old_at(x,y)==32767]
        seed=min(candidates,key=lambda p:(p[1],p[0]));pending=deque([seed]);white_ri_component.add(seed)
        while pending:
            x,y=pending.popleft()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                xx,yy=x+dx,y+dy
                if (228<=xx<272 and 48<=yy<95 and (xx,yy) not in white_ri_component
                        and old_at(xx,yy)==32767):
                    white_ri_component.add((xx,yy));pending.append((xx,yy))
    red_plate_rows={}
    if f == 11:
        for y in range(138,205):
            xs=[]
            for x in range(137,199):
                r,g,b=channels(old_at(x,y))
                if r-g>=8 and r-b>=8:xs.append(x)
            if xs:red_plate_rows[y]=(min(xs),max(xs))

    def backing(x,y):
        if f == 11:
            if y in red_plate_rows and red_plate_rows[y][0]<=x<=red_plate_rows[y][1]:
                return 4246
            if y >= 188 and x >= 158:
                return old_at(300,y)
            return 32767
        if inside(x,y,[259,16,310,64]):
            return 0
        if inside(x,y,[228,48,271,94]):
            return 3191
        if inside(x,y,[252,92,309,147]):
            return 26430
        # The monochrome shape here is the Japanese label's own drop shadow.
        # Remove it with that lettering and generate an English label shadow.
        return 32767

    seeds=set()
    plate_borders=set()
    if f == 12:
        plate_borders={(x,y) for y in range(16,64) for x in range(259,310)
                       if x in (259,309) or y in (16,63)}
    for i,v in enumerate(original):
        x,y=x0+i%w,y0+i//w;r,g,b=channels(v)
        if f == 11:
            black=(inside(x,y,[146,150,196,196]) or inside(x,y,[241,153,313,186])) and max(r,g,b)<=8
            yellow=inside(x,y,[179,139,220,190]) and min(r,g)>=20 and min(r,g)-b>=7
            green=inside(x,y,[208,162,238,196]) and g-r>=7 and g-b>=5
            if black or yellow or green:seeds.add(i)
        else:
            red=inside(x,y,[260,17,309,63]) and r>=g+8 and r>=b+8
            white_ri=(x,y) in white_ri_component
            # This separate 317-pixel white source component is the letter あ.
            white_a=(x,y) in white_a_component
            black=inside(x,y,[193,101,250,220]) and max(r,g,b)-min(r,g,b)<=1 and min(r,g,b)<31
            if red or white_ri or white_a or black:seeds.add(i)
    mask=set(seeds)
    for i in seeds:
        sx,sy=i%w,i//w
        for dy in range(-2,3):
            for dx in range(-2,3):
                xx,yy=sx+dx,sy+dy
                if not 0<=xx<w or not 0<=yy<h:continue
                j=yy*w+xx;x,y=x0+xx,y0+yy;v=original[j]
                if f == 12 and inside(x,y,[192,99,252,220]):
                    # Exact neutral source letter/shadow pixels already seed the
                    # mask; do not grow into neighboring pink tile edge artwork.
                    continue
                bg=backing(x,y)
                # Source background is left untouched. The growth is bounded by
                # original seeds, never a recursively expanding foreground fill.
                if v!=bg:mask.add(j)
    restored=list(original)
    mask={i for i in mask if (x0+i%w,y0+i//w) not in plate_borders}
    for i in mask:
        restored[i]=(original[i]&0x8000)|backing(x0+i%w,y0+i//w)
    output=list(restored);glyphs=[];painted=set();parts=[]
    for text,box,size,ink,rotation in LAYOUTS[f]:
        ax,ay,bx,by=box;pw,ph=bx-ax,by-ay
        tw,th=(ph,pw) if rotation else (pw,ph)
        font=ImageFont.truetype(str(font_path),size);bounds=font.getbbox(text)
        if bounds[2]-bounds[0]>tw-2 or bounds[3]-bounds[1]>th-2:
            raise ValueError('Complete Maria tile segment does not fit')
        left=(tw-(bounds[2]-bounds[0]))//2-bounds[0]
        top=(th-(bounds[3]-bounds[1]))//2-bounds[1]
        plane=Image.new('L',(tw,th));ImageDraw.Draw(plane).text((left,top),text,font=font,fill=255)
        for k,ch in enumerate(text):
            gx=left+font.getlength(text[:k]);gb=font.getbbox(ch)
            if gx+gb[0]<0 or gx+gb[2]>tw or top+gb[1]<0 or top+gb[3]>th:
                raise ValueError('Individual Maria tile letter clipped')
            gm=Image.new('L',(tw,th));ImageDraw.Draw(gm).text((gx,top),ch,font=font,fill=255)
            if rotation:gm=gm.transpose(Image.Transpose.ROTATE_270)
            q=gm.getbbox()
            if q is None:raise ValueError('Blank Maria tile letter')
            glyphs.append({'character':ch,'bbox':[q[0]+ax-x0,q[1]+ay-y0,q[2]+ax-x0,q[3]+ay-y0]})
        if rotation:plane=plane.transpose(Image.Transpose.ROTATE_270)
        if f == 12 and text == 'Mode':
            shadow_ink=24311
            for j,alpha in enumerate(plane.tobytes()):
                if not alpha:continue
                x,y=ax+j%pw-3,ay+j//pw+2
                if not inside(x,y,row['box']):raise ValueError('English title shadow escapes ownership')
                i=(y-y0)*w+x-x0;bg=output[i]
                output[i]=(original[i]&0x8000)|sum(round((((bg>>(c*5))&31)*(255-alpha)+((shadow_ink>>(c*5))&31)*alpha)/255)<<(c*5) for c in range(3))
        for j,alpha in enumerate(plane.tobytes()):
            if not alpha:continue
            x,y=ax+j%pw,ay+j//pw;i=(y-y0)*w+x-x0
            if not inside(x,y,row['box']) or i in painted:
                raise ValueError('Maria tile letters overlap or escape ownership')
            if (x,y) in plate_borders:
                raise ValueError('Maria letters cover original tile border')
            painted.add(i);bg=output[i]
            output[i]=(original[i]&0x8000)|sum(round((((bg>>(c*5))&31)*(255-alpha)+((ink>>(c*5))&31)*alpha)/255)<<(c*5) for c in range(3))
        parts.append({'text':text,'font_size':size,'box':box,'ink_word':ink,'rotation':rotation})
    if ''.join(g['character'] for g in glyphs)!='MariaMode':
        raise ValueError('Incomplete Maria Mode logical heading')
    return struct.pack(f'<{len(output)}H',*output), {
        'visible_characters':glyphs,'segments':parts,'source_glyph_mask_indices':sorted(mask),
        'source_seed_indices':sorted(seeds),'fringe_radius':2,
        'hidden_backing_recovery_is_exact':False,'actual_native_display_verified':False,
        'english_drop_shadow_replaces_source_letter_shadow':f==12,
        'full_payload_sha256':hashlib.sha256(struct.pack(f'<{len(output)}H',*output)).hexdigest(),
    }


def restore_maria_bubble(row, source_region, source_block):
    if (row.get('image_index')!=11 or row.get('box')!=[141,22,313,74]
            or source_block is None or hashlib.sha256(source_block).hexdigest()!=BLOCK_SHA):
        raise ValueError('Maria speech bubble requires exact reviewed source')
    words=[v for v, in struct.iter_unpack('<H',source_region)]
    width=172;height=52
    if len(words)!=width*height:
        raise ValueError('Maria speech plane extent differs')
    seeds=set()
    for i,v in enumerate(words):
        r,g,b=channels(v)
        if r-g>=2 and r-b>=2:seeds.add(i)
    mask=set(seeds)
    for i in seeds:
        x,y=i%width,i//width
        for dy in range(-2,3):
            for dx in range(-2,3):
                xx,yy=x+dx,y+dy
                if 0<=xx<width and 0<=yy<height:
                    j=yy*width+xx;r,g,b=channels(words[j])
                    if r>g and r>b:mask.add(j)
    restored=[(v&0x8000)|32767 if i in mask else v for i,v in enumerate(words)]
    border={i for i,v in enumerate(words) if i not in mask and v!=32767}
    return restored, {'source_glyph_mask_indices':sorted(mask),'protected_border_indices':sorted(border),
                      'fringe_radius':2,'background_is_original_white_plane':True,
                      'actual_native_display_verified':False}


def render_maria_speech(row, source_region, batch, source_block):
    if (row.get('layout_profile')!='maria-speech-source-ellipse-v1' or row.get('size')!=9
            or row.get('background')!=32767 or row.get('ink_word')!=6359
            or row.get('text_box') is not None):
        raise ValueError('Maria dialogue requires reviewed ellipse layout')
    restored,proof=restore_maria_bubble(row,source_region,source_block)
    font_path=Path(batch['font_file_path'])
    if hashlib.sha256(font_path.read_bytes()).hexdigest()!=batch['font_sha256']:
        raise ValueError('Maria dialogue font identity differs')
    font=ImageFont.truetype(str(font_path),9)
    # Shape lanes describe the original bubble; words are still wrapped from a
    # single logical paragraph. No translated line boundaries are authored.
    plans=[[[174,27,287,36],[149,38,309,47],[151,49,309,58],[174,60,293,69]]]
    words=row['english'].split()
    for lanes in plans:
        lines=[];position=0
        for box in lanes:
            line='';width=box[2]-box[0]-2
            while position<len(words):
                trial=(line+' '+words[position]).strip()
                if font.getbbox(trial)[2]-font.getbbox(trial)[0]>width:break
                line=trial;position+=1
            lines.append(line)
        if position==len(words):break
    else:
        raise ValueError('Complete visiting dialogue does not fit original bubble at9px')
    mask=Image.new('L',(172,52));glyphs=[]
    for line,box in zip(lines,lanes,strict=True):
        if not line:continue
        b=font.getbbox(line);left=(box[2]-box[0]-(b[2]-b[0]))//2+box[0]-b[0]
        top=(box[3]-box[1]-(b[3]-b[1]))//2+box[1]-b[1]
        if b[3]-b[1]>box[3]-box[1]:raise ValueError('Visiting dialogue line height escapes lane')
        ImageDraw.Draw(mask).text((left-141,top-22),line,font=font,fill=255)
        for k,ch in enumerate(line):
            if ch==' ':continue
            gx=left-141+font.getlength(line[:k]);gy=top-22;gb=font.getbbox(ch)
            if gx+gb[0]<0 or gx+gb[2]>172 or gy+gb[1]<0 or gy+gb[3]>52:
                raise ValueError('Individual visiting-dialogue character clipped')
            gm=Image.new('L',(172,52));ImageDraw.Draw(gm).text((gx,gy),ch,font=font,fill=255)
            q=gm.getbbox()
            if q is None:raise ValueError('Blank visiting-dialogue character')
            glyphs.append({'character':ch,'bbox':q})
    out=[];protected=set(proof['protected_border_indices']);ink=6359
    for i,(v,alpha) in enumerate(zip(restored,mask.tobytes(),strict=True)):
        if alpha and i in protected:
            raise ValueError(f'Visiting-dialogue lane touches original border at{141+i%172},{22+i//172}')
        out.append((v&0x8000)|sum(round((((v>>(c*5))&31)*(255-alpha)+((ink>>(c*5))&31)*alpha)/255)<<(c*5) for c in range(3)))
    return struct.pack(f'<{len(out)}H',*out), {'font_size':9,'automatic_lines':[line for line in lines if line],
        'shape_lanes':lanes[:sum(bool(line) for line in lines)],'visible_characters':glyphs,'restoration':proof,
        'full_mask_sha256':hashlib.sha256(mask.tobytes()).hexdigest()}
