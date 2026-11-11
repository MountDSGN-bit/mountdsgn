import re, html, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent/'home'))
import homefx
from homefx import u, ico, E, SITE
HERE = Path(__file__).parent

def dims(n):
    from PIL import Image
    return Image.open(SITE/f'assets/img/{n}.webp').size

def image(name, alt='', style='', cls='', eager=False):
    w,h = dims(name)
    ld = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="assets/img/{name}.webp" width="{w}" height="{h}" alt="{E(alt)}" {ld} style="{style}" class="{cls}">'

# ---- other-projects cards ----
PROJ = {
 'winery':('B2B SAAS · WEB + MOBILE','Платформа для винодельни','Система управления виноделием','fx-c-winery','c',(102.01,-26.31,-2.01,160)),
 'crm':('B2B CRM · WEB','CRM для рабочей команды','Для банков и финансовых услуг','fx-c-crm','c',(104.64,-27.18,-0.84,158.73)),
 'tencore':('САЙТ · FINTECH · ГОСЗАКУПКИ','Банковские услуги «Tencore»','Платформа госзакупок','fx-c-tencore','c',(99.9,-21.65,0.16,150.35)),
 'webxile':('САЙТ ДИЗАЙН-СТУДИИ · WEB','Дизайн-студия «WEBXILE»','Сайт дизайн-студии','fx-c-webxile','c',(100.82,-26.34,-0.82,159.34)),
 'tietly':('MOBILE · SOCIAL + WEB3','Социальная сеть «TIETLY»','Соцсеть с крипто-кошельком','fx-c-tietly','p',(116.08,-0.03,-11.67,100.06)),
 'mount':('MOBILE · КРИПТОКОШЕЛЁК','Крипто-кошелек «MOUNT»','Приложение крипто-кошелька','fx-c-mount','p',(117.74,-2.81,-12.48,105.19)),
}
def pcard(slug, wide, i=0):
    lab,title,sub,im,kind,(h,l,t,w) = PROJ[slug]
    W = 825 if wide else 530
    if kind=='c':
        if wide: clip='left:calc(50% - .5px);transform:translateX(-50%);top:11.11u;width:414u;height:370u'; inner='left:34u;top:0;width:346u;height:391u'
        else:    clip='left:calc(50% - 1px);transform:translateX(-50%);top:16.11u;width:414u;height:294u'; inner='left:31u;top:-.11u;width:352u;height:414u'
    else:
        if wide: clip='left:50%;transform:translateX(-50%);top:-60u;width:693u;height:397u'; inner='left:calc(50% - 337.5u);top:0;width:675u;height:402u'
        else:    clip='left:calc(50% + .5px);transform:translateX(-50%);top:0;width:531u;height:303u'; inner='left:8u;top:17u;width:517u;height:297u'
    iw,ih = dims(im)
    if not wide and slug=='tietly': sub='Соцсеть с крипто-кошельком'
    info_w = 745 if wide else 450
    return f'''<a class="fx-card" href="{slug}.html" data-reveal style="--i:{i};width:{W}u">
<div class="cbg"><img src="assets/img/fx-bg.webp" alt="" width="2400" height="1600" loading="lazy" decoding="async"></div>
<div class="clip {"kc" if kind=="c" else "kp"}" style="{clip}"><div style="{inner}"><img src="assets/img/{im}.webp" alt="Обложка кейса: {E(title)}" width="{iw}" height="{ih}" loading="lazy" decoding="async" style="height:{h}%;left:{l}%;top:{t}%;width:{w}%"></div></div>
<div class="bar" style="width:100%"><div class="in" style="width:{info_w}u"><div class="txt" style="width:auto"><span class="lab">{E(lab)}</span><div><h3>{E(title)}</h3><p class="sub" style="margin-top:8px">{E(sub)}</p></div></div>{ico('325c1','class="ic" aria-hidden="true"')}</div></div>
</a>'''

def others(slugs):
    top, bot = slugs[:2], slugs[2:]
    r1 = ''.join(pcard(s, True, i) for i,s in enumerate(top))
    r2 = ''.join(pcard(s, False, i) for i,s in enumerate(bot))
    return f'''<section class="cs-oth" aria-labelledby="oth-h"><div class="in">
<div class="hd" data-reveal><h2 id="oth-h">Другие проекты</h2><p>Можете ознакомиться с моими другими проектами</p></div>
<div class="g"><div class="r">{r1}</div><div class="r n">{r2}</div></div></div></section>'''

def footer():
    return f'''<section class="fx-foot" aria-labelledby="contact-h">
<div class="tx"><p class="up" data-reveal>Блок для связи.</p><h2 id="contact-h" style="margin:0;font:inherit"><span class="mid" style="position:absolute;left:0;top:28u;display:block" data-reveal>Поработаем вместе?</span><span class="down" style="position:absolute;left:0;top:121u;display:block" data-reveal>Напишите мне в телеграм</span></h2></div>
<div class="line"></div>
<dl data-reveal><div><dt>Email:</dt><dd><a href="mailto:goraakk2@mail.ru">goraakk2@mail.ru</a></dd></div><div><dt>Phone</dt><dd><a href="tel:+79183212635">+7 (918) 321-26-35</a></dd></div></dl>
<a class="fx-btn" href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer" aria-label="Написать в Telegram (откроется в новой вкладке)">{ico('c4553','class="a" aria-hidden="true"')}{ico('3c2a1','class="b" aria-hidden="true"')}<span class="t">Написать{ico('088e2','aria-hidden="true"')}</span></a>
</section>'''

# ---- sections ----
def MH(d): return f' style="--mh:{d["hero_mh"]}px"' if d.get('hero_mh') else ''

def hero(d):
    if d.get('hero_phones'):
        ph=''.join(f'<div class="ph">{image(n,"Экран приложения","width:100%;height:100%;object-fit:contain",eager=True)}</div>' for n in d['hero_phones'])
        shots=f'<div class="phones">{ph}</div>'
        return f'''<section class="cs-hero"><div class="card"{MH(d)}>
<div class="bgi"><img src="assets/img/fx-bg.webp" alt="" width="2400" height="1600" fetchpriority="high"></div>
<div class="in"><p class="k">{E(d['kicker'])}</p><h1>{E(d['title'])}</h1><p class="d"{(' style="width:%su"'%d['lead_w']) if d.get('lead_w') else ''}>{E(d['lead'])}</p>{shots}</div>
<div class="shine"></div></div></section>'''
    if d.get('hero_pair'):
        im=''.join(f'<div class="hp" style="left:{t[2]}u;top:{t[3]}u">{image(t[0],t[1],"width:100%;height:auto;display:block",eager=True)}</div>' for t in d['hero_pair'])
        return f'''<section class="cs-hero"><div class="card"{MH(d)}>
<div class="bgi"><img src="assets/img/fx-bg.webp" alt="" width="2400" height="1600" fetchpriority="high"></div>
<div class="in"><p class="k">{E(d['kicker'])}</p><h1>{E(d['title'])}</h1><p class="d"{(' style="width:%su"'%d['lead_w']) if d.get('lead_w') else ''}>{E(d['lead'])}</p></div>
<div class="hpr">{im}</div>
<div class="shine"></div></div></section>'''
    if d.get('hero_img'):
        return f'''<section class="cs-hero"><div class="card"{MH(d)}>
<div class="bgi"><img src="assets/img/fx-bg.webp" alt="" width="2400" height="1600" fetchpriority="high"></div>
<div class="in"><p class="k">{E(d['kicker'])}</p><h1>{E(d['title'])}</h1><p class="d"{(' style="width:%su"'%d['lead_w']) if d.get('lead_w') else ''}>{E(d['lead'])}</p></div>
<div class="himg">{image(d['hero_img'], d.get('hero_alt',''), 'width:100%;height:100%;object-fit:cover', eager=True)}</div>
<div class="shine"></div></div></section>'''
    shots = ''
    for s in d['hero_shots']:
        if s['kind']=='aspect':
            w,h = dims(s['img'])
            shots += f'<div class="shot" style="height:396u"><div class="im" style="aspect-ratio:{w}/{h}">{image(s["img"], s.get("alt",""), "inset:0;width:100%;height:100%;object-fit:cover", eager=True)}</div></div>'
        else:
            shots += f'<div class="shot"><div class="im" style="height:375u">{image(s["img"], s.get("alt",""), f"left:0;width:100%;height:{s["h"]}%;top:{s["t"]}%")}</div></div>'
    return f'''<section class="cs-hero"><div class="card"{MH(d)}>
<div class="bgi"><img src="assets/img/fx-bg.webp" alt="" width="2400" height="1600" fetchpriority="high"></div>
<div class="in"><p class="k">{E(d['kicker'])}</p><h1>{E(d['title'])}</h1><p class="d"{(' style="width:%su"'%d['lead_w']) if d.get('lead_w') else ''}>{E(d['lead'])}</p><div class="shots">{shots}</div></div>
<div class="shine"></div></div></section>'''

def meta(d):
    cells = ''.join(f'<div><span class="k">{E(t[0])}</span><span class="v"{" style=\"white-space:nowrap\"" if len(t)>2 else ""}>{E(t[1])}</span></div>' for t in d['meta'])
    return f'<section class="cs-meta"><div class="ln"></div><div class="row" data-reveal>{cells}</div></section>'

def summary(d):
    tags = ''.join(f'<span class="tag">{E(t)}</span>' for t in d['tags'])
    nums = ''.join(f'<div><b>{E(t[0])}</b><span{" style=\"white-space:nowrap\"" if len(t)>2 else ""}>{E(t[1])}</span></div>' for t in d['nums'])
    return f'''<section class="cs-sum"><div class="r2">
<div class="col" data-reveal><h2 class="geo">МОЯ РОЛЬ</h2><p style="width:733u">{E(d['role'])}</p><div class="tags">{tags}</div></div>
<div class="col" data-reveal style="--i:1"><h2 class="geo">КОРОТКО О КЕЙСЕ</h2><p style="width:634u">{E(d['about'])}</p></div></div>
<div class="nums" data-reveal>{nums}</div></section>'''

def figsec(cls, lab, h, p, img, alt):
    w,hh = dims(img)
    return f'''<section class="cs-fig {cls}" aria-labelledby="{cls}-h"><div class="sr"><span>{E(lab)}</span><h2 id="{cls}-h">{E(h)}</h2><p>{E(p)}</p></div><div class="fgi" data-reveal role="img" aria-label="{E(alt)}" tabindex="0"><img src="assets/img/{img}.webp" width="{w}" height="{hh}" alt="{E(alt)}" loading="lazy" decoding="async"></div></section>'''

def context(d):
    if d['ctx'].get('img'):
        c=d['ctx']; return figsec('ctxf',c['lab'],c['h'],c['p'],c['img'],c['alt'])
    c = d['ctx']
    BR=lambda x: E(x).replace(chr(10),' <br>')
    dk = ''.join(f'<div><b>{E(t[0])}</b><span{((" style=\"white-space:nowrap\"" if t[2]=="n" else " style=\"max-width:%su\""%t[2])) if len(t)>2 else ""}>{E(t[1])}</span></div>' for t in c['dark'])
    def tn(rows): return '<div class="tn">'+''.join(f'<div><b>{E(t[0])}</b><span{(" style=\"max-width:%su\""%t[2]) if len(t)>2 else ""}>{E(t[1])}</span></div>' for t in rows)+'</div>'
    users = ''
    for col in c['users']:
        users += '<div>'
        for sub,name,items in col:
            qs=''.join(f'<div class="q"><i>{E(a)}</i><span style="color:#000">{BR(b)}</span></div>' for a,b in items)
            users += f'<div class="u"><div class="h"><span>{E(sub)}</span><b>{E(name)}</b></div>{qs}</div>'
        users += '</div>'
    HL=lambda x: re.sub(r'\{(.+?)\}',r'<i>\1</i>',E(x))
    def pcard(p):
        at=''.join(f'<div><span>{E(a)}</span><b>{E(b)}</b></div>' for a,b in p['at'])
        js=''.join(f'<li>{HL(j)}</li>' for j in p['js'])
        return f'<article class="pc"><div class="pt"><img src="assets/img/{p["img"]}.webp" width="180" height="180" alt="{E(p["name"])}" loading="lazy" decoding="async"><div><h3>{E(p["name"])}</h3><dl>{at}</dl></div></div><p>{E(p["bio"])}</p><ul>{js}</ul></article>'
    def pimg(n,a): return f'<div class="pi" style="aspect-ratio:{dims(n)[0]}/{dims(n)[1]}">{image(n, a, "width:100%;height:100%;object-fit:cover")}</div>'
    pers = ''.join(pcard(p) if isinstance(p,dict) else pimg(*p) for p in c.get('personas',[]))
    return f'''<section class="cs-ctx{' fq' if c.get('fixq') else ''}{' sm' if c.get('sm') else ''}"{(' style="padding-left:%su;padding-right:%su"'%(c['pad'],c['pad'])) if c.get('pad') else ''}><div class="row">
<div class="l" data-reveal><span class="eb">{E(c.get('lab','01 · КОНТЕКСТ'))}</span><div class="body">
<div class="intro"><h2 class="geo up">{E(c['h'])}</h2><p{(' style="width:%su"'%c['pw']) if c.get('pw') else ''}>{BR(c['p'])}</p></div>
<div class="mid"><div class="sub"><span class="eb">{E(c['dark_lab'])}</span><div class="dk">{dk}</div></div>{tn(c['tn'][0])}{tn(c['tn'][1])}</div>
</div></div>
<div class="us{' pe' if c.get('personas') else ''}" data-reveal style="--i:1">{pers if c.get('personas') else users}</div></div></section>'''

def research(d):
    r = d['res']
    cards = ''
    for i,cd in enumerate(r['cards']):
        tw=None
        if len(cd)==5: lab,a,b,c,tw = cd
        elif len(cd)==4 and isinstance(cd[3],int): a,b,c,tw = cd; lab=f"{r.get('cl','ВЫВОД')} {i+1}"
        elif len(cd)==4: lab,a,b,c = cd
        else: a,b,c = cd; lab=f"{r.get('cl','ВЫВОД')} {i+1}"
        cards += f'<div data-reveal style="--i:{i}"><div class="t"><span>{E(lab)}</span><b{(' style="max-width:%su"'%tw) if tw else ''}>{E(a).replace(chr(10),' <br>')}</b><p>{E(b)}</p></div><div class="sol"><span>→ {E(r.get('sl','РЕШЕНИЕ'))}</span><p>{E(c)}</p></div></div>'
    pst=(' style="width:%su"'%r['pw']) if r.get('pw') else ''
    paras=''.join(f'<p class="t"{pst}>{E(x)}</p>' for x in r['p'].split(chr(10)))
    return f'''<section class="cs-res"><div class="hd" data-reveal><span class="eb">{E(r['lab'])}</span><h2 class="geo">{E(r['h'])}</h2>{paras}</div><div class="cards">{cards}</div></section>'''

def arch(d):
    a=d.get('arch')
    if not a: return ''
    if not a.get('cap'):
        return figsec('archf',a['lab'],a['h'],a['p'],a['img'],a['alt'])
    w,hh=dims(a['img'])
    return f'''<section class="cs-arch"><div class="hd" data-reveal><span class="eb">{E(a['lab'])}</span><h2 class="geo up">{E(a['h'])}</h2><p class="t"{(' style="width:%su"'%a['pw']) if a.get('pw') else ''}>{E(a['p']).replace(chr(10),' <br>')}</p></div><div class="sch" data-reveal><span class="eb">{E(a['cap'])}</span><div class="fgi" role="img" aria-label="{E(a['alt'])}" tabindex="0"><img src="assets/img/{a['img']}.webp" width="{w}" height="{hh}" alt="{E(a['alt'])}" loading="lazy" decoding="async"></div></div></section>'''

def solutions(d):
    s = d['sol']
    if s.get('kind')=='rows':
        n=len(s['rows']); rows=''
        for r in s['rows']:
            sw,sh=dims(r['scr']); cw,ch=dims(r['sch'])
            rows+=f'''<div class="rwx" data-reveal><div class="rt"><div class="rl"><span class="eb">РЕШЕНИЕ {r['n']} / {n}</span><h3{' class="nw"' if r.get('nw') else ''}>{E(r['t'])}</h3><p{(' style="max-width:%su"'%r['dw']) if r.get('dw') else ''}>{E(r['d'])}</p><div class="rcd"><span>РЕШЕНИЕ</span><p>{E(r['sol'])}</p></div><div class="rcd ef"><span>ЭФФЕКТ</span><p>{E(r['eff'])}</p></div></div><div class="rr"><div class="fgi" role="img" aria-label="Экраны: {E(r['t'])}" tabindex="0" style="width:{sw/2:g}u"><img src="assets/img/{r['scr']}.webp" width="{sw}" height="{sh}" alt="Экраны: {E(r['t'])}" loading="lazy" decoding="async"></div></div></div><div class="rb"><span class="eb">{E(r['cap'])}</span><div class="fgi" role="img" aria-label="Схема сценариев: {E(r['t'])}" tabindex="0"><img src="assets/img/{r['sch']}.webp" width="{cw}" height="{ch}" alt="Схема сценариев: {E(r['t'])}" loading="lazy" decoding="async"></div></div></div>'''
        return f'''<section class="cs-sol rows"><div class="hd" data-reveal><span class="eb">{E(s['lab'])}</span><h2 class="geo up">{E(s['h'])}</h2><p class="t">{E(s['p'])}</p></div><div class="rwg">{rows}</div></section>'''
    if s.get('kind')=='cards':
        n=len(s['items']); rows=''
        for r0 in range(0,n,4):
            cs=''
            for i,(a,b,imgs) in enumerate(s['items'][r0:r0+4],r0):
                im=''.join(f'<div class="sc">{image(x,"Экран приложения","width:100%;height:100%;object-fit:contain")}</div>' for x in imgs)
                cs+=f'<div data-reveal style="--i:{i%4}"><span>РЕШЕНИЕ {i+1} / {n}</span><b>{E(a)}</b><p>{E(b)}</p><div class="scs">{im}</div></div>'
            rows+=f'<div class="scr">{cs}</div>'
        return f'''<section class="cs-sol"><div class="hd" data-reveal><span class="eb">{E(s['lab'])}</span><h2 class="geo up">{E(s['h'])}</h2><p class="t">{E(s['p'])}</p></div><div class="scg">{rows}</div></section>'''
    n = len(s['items'])
    sums = ''.join(f'<div data-reveal style="--i:{i%3}"><span>РЕШЕНИЕ {i+1} / {n}</span><b>{E(a)}</b><p>{E(b)}</p></div>' for i,(a,b) in enumerate(s['items']))
    rects = ''
    for (x,y,w,h,img,ih,it) in s['board']['rects']:
        rects += f'<div class="rc" style="left:{x}u;top:{y}u;width:{w}u;height:{h}u;--ar:{w:.3f}/{h:.3f}">{image(img, "Экран из кейса", f"height:{ih}%;top:{it}%")}</div>'
    return f'''<section class="cs-sol"><div class="hd" data-reveal><span class="eb">{E(s['lab'])}</span><h2 class="geo up">{E(s['h'])}</h2><p class="t">{E(s['p'])}</p></div>
<div class="sum">{sums}</div><div class="board" style="height:{s['board']['h']}u">{rects}</div></section>'''

def results(d):
    o = d['out']
    g = ''.join(f'<div data-reveal style="--i:{i%3}"><b>{E(a)}</b><span>{E(b)}</span></div>' for i,(a,b) in enumerate(o['grid']))
    return f'''<section class="cs-out"><div class="hd" data-reveal><span class="eb">{E(o['lab'])}</span><h2>{E(o['h'])}</h2><p class="t"{(' style="width:%su"'%o['pw']) if o.get('pw') else ''}>{E(o['p'])}</p></div><div class="grid">{g}</div></section>'''

def reflection(d):
    r = d['ref']
    c = ''.join(f'<div data-reveal style="--i:{i}{";align-self:flex-start" if (i==0 and r.get("hug0")) else ""}"><span>{E(a)}</span><p>{E(b)}</p></div>' for i,(a,b) in enumerate(r['cards']))
    return f'''<section class="cs-ref"><div class="hd" data-reveal><span class="eb">{E(r['lab'])}</span><h2>{E(r['h'])}</h2></div><div class="cards">{c}</div></section>'''

def dsblock(d, key='ds'):
    a=d.get(key)
    if not a: return ''
    figs=''
    for f in a['figs']:
        w,hh=dims(f['img'])
        figs+=f'''<div class="sch" data-reveal><span class="eb">{E(f['cap'])}</span><div class="fgi" role="img" aria-label="{E(f['alt'])}" tabindex="0"><img src="assets/img/{f['img']}.webp" width="{w}" height="{hh}" alt="{E(f['alt'])}" loading="lazy" decoding="async"></div></div>'''
    sd=''
    if a.get('side'):
        w,hh=dims(a['side']); sd=f'''<div class="sd" data-reveal><img src="assets/img/{a['side']}.webp" width="{w}" height="{hh}" alt="{E(a.get('side_alt',''))}" loading="lazy" decoding="async"></div>'''
    hd=f'''<div class="hd" data-reveal><span class="eb">{E(a['lab'])}</span><h2 class="geo up">{E(a['h'])}</h2><p class="t"{(' style="width:%su"'%a['pw']) if a.get('pw') else ''}>{E(a['p']).replace(chr(10),'<br><br>')}</p></div>'''
    top=f'<div class="dsh">{hd}{sd}</div>' if sd else hd
    return f'''<section class="cs-arch cs-ds">{top}{figs}</section>'''

def build(slug, d):
    pal = d['pal']
    style = ';'.join(f'--{k}:{v}' for k,v in pal.items())
    css = u((HERE/'case.src.css').read_text())
    mob = (HERE/'case.mobile.css').read_text() if (HERE/'case.mobile.css').exists() else ''
    (SITE/'assets/css/case.css').write_text(css+mob)
    page = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(d['title'])} — Алексей Гора</title>
<meta name="description" content="{E(d['lead'])}">
<meta name="theme-color" content="#ffffff">
<meta property="og:title" content="{E(d['title'])}">
<meta property="og:description" content="{E(d['lead'])}">
<meta property="og:type" content="article">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/Poppins-Medium.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/home.css">
<link rel="stylesheet" href="assets/css/case.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="cs fx{' wide' if d.get('wide') else ''}{' mf' if d.get('meta_flex') else ''}" style="{style}">
<a class="skip" href="#main">Перейти к содержимому</a>
<div class="pg">
<header class="cs-top"><p class="who"><a href="index.html">Алексей</a><a href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer">tg: @mountdsgn1</a></p><a class="cs-back" href="index.html#cases">{ico('arrow-down','aria-hidden="true"')}<span>Все кейсы</span></a></header>
<main id="main">
{hero(d)}{meta(d)}{summary(d)}{context(d)}{research(d)}{arch(d)}{solutions(d)}{dsblock(d)}{dsblock(d,'ai')}{results(d)}{reflection(d)}{others(d['others'])}
</main>
{footer()}
</div>
<button type="button" class="totop" aria-label="Наверх"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button>
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''
    page = homefx.u_inline(page)
    (SITE/f'{slug}.html').write_text(page)
