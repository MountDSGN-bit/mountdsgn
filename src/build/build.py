#!/usr/bin/env python3
"""Static site generator for the portfolio. Run: python3 build/build.py"""
import json, re, html, sys, importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
sys.path.insert(0, str(Path(__file__).resolve().parent))
MAN = json.loads((SITE / 'assets/img/manifest.json').read_text())
E = html.escape

def icon(name):
    s = (SITE / f'assets/icons/{name}.svg').read_text()
    s = re.sub(r'stroke="(?!none)[^"]*"', 'stroke="currentColor"', s)
    s = re.sub(r'fill="(?!none)[^"]*"', 'fill="currentColor"', s)
    s = re.sub(r'\s(width|height)="\d+"', '', s, count=2)
    return s.replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1)

CIRC = '<svg class="circ" viewBox="0 0 40 40" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="20" cy="20" r="18"/><path d="M14 26L26 14M16 14h10v10"/></svg>'
CARR = '<svg viewBox="0 0 36 36" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="18" cy="18" r="16"/><path d="M12.5 23.5L23.5 12.5M14.5 12.5h9v9"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
CHEV = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

PROJECTS = [
    ('winery', 'Цифровая платформа для винодельни', 'Комплексная система управления виноделием', 'home-card-winery'),
    ('crm', 'CRM', 'Рабочее пространство для команды', 'home-card-crm'),
    ('tencore', 'Банковские услуги «Tencore»', 'Платформа поставщиков госзакупок', 'home-card-tencore'),
    ('webxile', 'Дизайн-студия «WEBXILE»', 'Сайт дизайн-студии', 'home-card-webxile'),
    ('tietly', 'Социальная сеть «TIETLY»', 'Мобильное приложение соцсети, объединенное с крипто-кошельком', 'home-card-tietly'),
    ('mount', 'Крипто-кошелек «MOUNT»', 'Мобильное приложение крипто-кошелька', 'home-card-mount'),
]
SOON = 'class="is-soon" href="#" data-soon aria-disabled="true"'

def img(name, alt='', eager=False, sizes=None):
    w, h = MAN[name]
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="assets/img/{name}.webp" width="{w}" height="{h}" alt="{E(alt)}" {loading}>'

def head(title, desc, body_cls, case=None):
    data = f' data-case="{case}"' if case else ''
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#ffffff">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/Poppins-Medium.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/css/site.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="{body_cls}"{data}>
<a class="skip" href="#main">Перейти к содержимому</a>
'''

def dock(current):
    items = [
        ('home', 'index.html' if current != 'home' else '#top', 'Главная', 'home', None),
        ('resume', None, 'Резюме', 'resume', None),
        ('cases', 'index.html#cases', 'Кейсы', 'cases', None),
        ('work', 'index.html#work', 'Опыт', 'work', None),
        ('tg', None, 'Telegram', 'tg', None),
    ]
    out = ['<nav class="dock" aria-label="Основная навигация">']
    for key, href, label, ic, _ in items:
        cur = ' aria-current="page"' if key == current else ''
        data_sec = f' data-sec="{key}"' if key in ('home', 'cases', 'work') else ''
        if key == 'tg':
            out.append(f'<a href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer" data-label="{label}" aria-label="Telegram (откроется в новой вкладке)">{icon(ic)}</a>')
        elif key == 'resume':
            out.append(f'<a href="assets/Alexey-Gora-CV.pdf" download="Gora-Alexey-CV.pdf" data-label="{label}" aria-label="Скачать резюме (PDF)">{icon(ic)}</a>')
        elif href is None:
            out.append(f'<a {SOON} data-label="{label}" aria-label="{label}">{icon(ic)}</a>')
        else:
            out.append(f'<a href="{href}" data-label="{label}" aria-label="{label}"{cur}{data_sec}>{icon(ic)}</a>')
    out.append('</nav>')
    return '\n'.join(out)

def pcard(p, small=False, i=0):
    slug, title, sub, im = p
    cls = 'pcard sm' if small else 'pcard'
    return f'''<a class="{cls}" href="{slug}.html" data-reveal style="--i:{i}">
<div class="img">{img(im, f'Обложка кейса: {title}')}</div>
<div class="meta"><div><h3>{E(title)}</h3><p>{E(sub)}</p></div><span class="arr">{CARR}</span></div>
</a>'''

def contact():
    return f'''<section class="contact" aria-labelledby="contact-h">
<div class="contact-in">
<p class="label" data-reveal>Блок для связи.</p>
<h2 id="contact-h" data-reveal style="--i:1">Поработаем вместе?<br>Напишите мне в телеграм</h2>
<div class="rule" data-reveal style="--i:2"><a class="tg-btn" href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer" aria-label="Написать в Telegram (откроется в новой вкладке)"><span>Написать {icon('tg')}</span></a></div>
<dl data-reveal style="--i:3"><div><dt>Email:</dt><dd>mountdsgn@mail.ru</dd></div><div><dt>Phone</dt><dd>+7 (918) 321-26-35</dd></div></dl>
</div>
</section>'''

def tail():
    return '<script src="assets/js/site.js" defer></script>\n</body>\n</html>\n'

# ---------------------------------------------------------------- home
JOBS = [
    ('Крым Диджитал - Продуктовый дизайнер', 'Июль 2023 - сейчас', [
        'Разрабатывал сложное и высоконагруженное техническое ПО для B2B сегмента, такое как «Цифровая платформа для винодельни»',
        'Создал и поддерживал дизайн-систему продукта, что сократило время разработки новых экранов на 25-30%',
        'Реализовал сложную логику фильтрации и поиска для объемных каталогов продукции, учитывающую профессиональную специфику',
        'Управлял процессом одновременной адаптации продукта под различные сценарии использования: от полевых условий (мобильный интерфейс для работы на виноградниках) до офисной аналитики и клиентских интерфейсов.',
        'Участвовал в формировании продуктовой стратегии и приоритизации задач совместно с менеджерами',
        'Проводил дизайн-ревью реализованных интерфейсов, что снизило количество возвратов задач от разработки на ~30%',
        'Проводил UX-аудит ключевых сценариев, выявлял узкие места и предлагал решения, повысившие конверсию и удобство интерфейсов',
        'Менторил начинающих дизайнеров, от лекций до составления PDP, используя основы коуч менеджмента',
        'Улучшение пользовательского опыта, редизайн интерфейсов, оптимизация сценариев мобильного приложения для чтения саммари книг',
        'Адаптировал дизайн под различные устройства и платформы, снизив количество UI-багов после релиза']),
    ('WebXile - UX/UI дизайнер', 'Май 2022 - Июль 2023', [
        'Проектировал и запускал комплексные интерфейсы для B2B и B2C сегментов: от высококонверсионных лендингов до многостраничных порталов',
        'Разрабатывал мобильные приложения с адаптацией под iOS и Android: социальная сеть, крипто-кошелек',
        'Проводил глубокую аналитику пользовательских путей (CJM), выявляя барьеры в интерфейсах, что привело к росту вовлеченности аудитории']),
]

def build_home():
    h = head('Алексей - продуктовый дизайнер', 'Портфолио продуктового дизайнера: B2B и B2C продукты, веб и мобильные интерфейсы, дизайн-системы. Шесть кейсов.', 'home')
    h += f'''<header class="site-header"><div class="who"><span>Алексей</span><a {SOON}>tg: @mountdsgn1</a></div>
<p class="aside">Проектировал B2B и B2C продукты для десятков тысяч пользователей от мобильных MVP до аналитических веб систем</p></header>
<main id="main">
<section class="hero" id="top" aria-label="Алексей, продуктовый дизайнер">
<img src="assets/img/home-bg.webp" width="{MAN['home-bg'][0]}" height="{MAN['home-bg'][1]}" alt="Алексей, продуктовый дизайнер" fetchpriority="high">
<h1><span class="sr">Product Designer, UX/UI Designer</span><span class="mq" aria-hidden="true"><span class="mq-t"><span class="mq-g"><span>Product Designer</span><i class="mq-x" aria-hidden="true">·</i><span class="mq-x">UX/UI Designer</span><i class="mq-x" aria-hidden="true">·</i></span><span class="mq-g mq-dup"><span>Product Designer</span><i class="mq-x" aria-hidden="true">·</i><span class="mq-x">UX/UI Designer</span><i class="mq-x" aria-hidden="true">·</i></span></span></span></h1>
</section>
<section class="intro wrap" aria-label="Обо мне">
<p class="lead" data-reveal>Алексей, 25 лет. Продуктовый дизайнер с 4+ годами опыта в web и mobile-продуктах. Работаю со всем циклом разработки: от анализа требований и UX-исследований до прототипирования, UI-реализации и передачи в разработку.</p>
<div class="side" data-reveal style="--i:1"><p>Комфортно взаимодействую с командой, участвовал в дизайн-ревью и онбординге дизайнеров. Ориентирован на понятные, масштабируемые интерфейсы.</p>
<a class="link-arrow" href="assets/Alexey-Gora-CV.pdf" download="Gora-Alexey-CV.pdf" aria-label="Скачать резюме (PDF)">Резюме {CIRC}</a></div>
</section>
<section class="cases wrap" id="cases" aria-labelledby="cases-h">
<div class="sec-head" data-reveal><h2 id="cases-h">Кейсы</h2><p>Демонстрация моих последних проектов</p></div>
<div class="case-grid">
{''.join(pcard(p, i=i % 2) for i, p in enumerate(PROJECTS))}
</div>
</section>
<section class="work wrap" id="work" aria-labelledby="work-h">
<div class="sec-head" data-reveal><h2 id="work-h">Опыт работы</h2><p>Более 4 лет опыта в разработке продуктов</p></div>
'''
    for j, (t, d, items) in enumerate(JOBS):
        h += f'''<article class="job" data-reveal>
<h3><button class="job-btn" type="button" aria-expanded="false" aria-controls="job{j}"><span><b>{E(t)}</b><small>{E(d)}</small></span><span class="chev">{CHEV}</span></button></h3>
<div class="job-body" id="job{j}" hidden><div><ul>{''.join(f'<li>{E(x)}</li>' for x in items)}</ul></div></div>
</article>
'''
    h += '</section>\n' + contact() + '\n</main>\n' + dock('home') + '\n' + tail()
    (SITE / 'index.html').write_text(h)

# ---------------------------------------------------------------- cases
def reveal(i=0): return f'data-reveal style="--i:{i % 4}"'

def r_shots(b, alt_base):
    n = b.get('n', len(b['items']))
    cls = f'shots n{n}' + (' mid' if b.get('mid') else '') + (' ph' if b.get('phone') else '')
    out = [f'<div class="{cls}">']
    for i, it in enumerate(b['items']):
        if isinstance(it, str): it = {'img': it}
        alt = it.get('alt') or f'{alt_base} - экран {i + 1}'
        cap = f'<figcaption>{E(it["cap"])}</figcaption>' if it.get('cap') else ''
        ph = ' phone' if b.get('phone') else ''
        out.append(f'<figure class="shot{ph}" {reveal(i)}><div class="fr">{img(it["img"], alt)}</div>{cap}</figure>')
    out.append('</div>')
    return '\n'.join(out)

def r_cards(b):
    cols = b.get('cols', 3)
    out = [f'<div class="cards c{cols}{" steps" if b.get("steps") else ""}">']
    for i, it in enumerate(b['items']):
        cls = 'card' + (' big' if b.get('big') else '') + (' step' if b.get('steps') else '') + (' dark' if it.get('dark') else '')
        s = [f'<div class="{cls}" {reveal(i)}>']
        if it.get('n'): s.append(f'<span class="n">{E(str(it["n"]))}</span>' if b.get('steps') else f'<span class="num">{E(str(it["n"]))}</span>')
        if it.get('st'): s.append(f'<span class="st{" done" if it.get("done") else ""}">{E(it["st"])}</span>')
        if it.get('k'): s.append(f'<p class="k{" a" if it.get("a", True) and not b.get("plainK") else ""}">{E(it["k"])}</p>')
        if it.get('h'): s.append(f'<h3>{E(it["h"])}</h3>')
        if it.get('p'): s.append(f'<p>{E(it["p"])}</p>')
        for k, t in it.get('rows', []):
            s.append(f'<div class="row"><p class="k">{E(k)}</p><p>{E(t)}</p></div>')
        if it.get('sw'): s.append('<div class="sw">' + ''.join(f'<span><i style="background:{c}"></i>{c}</span>' for c in it['sw']) + '</div>')
        if it.get('chips'): s.append(chips(it['chips']))
        if it.get('ul'): s.append('<ul>' + ''.join(f'<li>{E(x)}</li>' for x in it['ul']) + '</ul>')
        if it.get('go'): s.append(f'<div class="go"><p class="k">{E(it["go"][0])}</p><p>{E(it["go"][1])}</p></div>')
        s.append('</div>')
        out.append(''.join(s))
    out.append('</div>')
    return '\n'.join(out)

def r_stats(b):
    cols = b.get('cols', 4); size = b.get('size', '')
    out = [f'<div class="stats c{cols}">']
    for i, (n, t) in enumerate(b['items']):
        out.append(f'<div class="stat {size}" {reveal(i)}><b>{E(n)}</b><span>{E(t)}</span></div>')
    out.append('</div>')
    if b.get('fine'): out.append(f'<p class="fine">{E(b["fine"])}</p>')
    return '\n'.join(out)

def r_fl(b, alt_base):
    ratio = b.get('ratio', 'r58')
    fig = ''
    imgs = b['imgs'] if 'imgs' in b else [b['img']]
    figs = ''.join(f'<figure class="shot" {reveal(i)}><div class="fr">{img(n, (b.get("alt") or alt_base) + (f" - {i+1}" if len(imgs) > 1 else ""))}</div></figure>' for i, n in enumerate(imgs))
    fig = f'<div class="imgcol" style="display:grid;gap:clamp(12px,1.25vw,24px)">{figs}</div>' if len(imgs) > 1 else figs
    side = ''.join(f'<div class="blk" {reveal(i)}><h4>{E(k)}</h4><p>{E(t)}</p></div>' for i, (k, t) in enumerate(b['side']))
    if b.get('side_act'):
        a = b['side_act']
        side += f'<div class="blk" {reveal(3)}><h4>{E(a["label"])}</h4><ul class="plain" style="display:flex;flex-direction:column;gap:8px">' + ''.join(f'<li style="font:300 clamp(14px,.99vw,19px)/1.55 var(--f-head)">– {E(x)}</li>' for x in a['ul']) + '</ul>' + (chips(a.get('chips')) if a.get('chips') else '') + '</div>'
    return f'<div class="fl {ratio}">{fig}<div class="side">{side}</div></div>'

def chips(items):
    return '<div class="chips">' + ''.join(f'<span class="chip">{E(c)}</span>' for c in items) + '</div>' if items else ''

def r_act(b):
    return f'<div class="act" data-reveal><h4>{E(b.get("label", "Ключевые действия"))}</h4><div><ul>' + ''.join(f'<li>{E(x)}</li>' for x in b['ul']) + f'</ul>{chips(b.get("chips"))}</div></div>'

def r_sw(b):
    return '<div class="sw" data-reveal>' + ''.join(f'<span><i style="background:{c}"></i>{c}</span>' for c in b['colors']) + '</div>'

def r_text(b):
    return f'<p class="fine" style="max-width:70ch;font-size:clamp(14px,1.04vw,20px);color:var(--ink-2)" data-reveal>{E(b["p"])}</p>'

def r_sub(b):
    return f'<p class="eyebrow subh" data-reveal>{E(b["p"])}</p>'

def r_block(b, alt_base):
    t = b['t']
    return {'cards': lambda: r_cards(b), 'stats': lambda: r_stats(b), 'shots': lambda: r_shots(b, alt_base),
            'fl': lambda: r_fl(b, alt_base), 'act': lambda: r_act(b), 'sw': lambda: r_sw(b), 'text': lambda: r_text(b), 'sub': lambda: r_sub(b)}[t]()

def r_section(s):
    cls = 'sec' + (' key' if s.get('key') else '')
    sid = s['id']
    lead = f'<p class="lead">{E(s["lead"])}</p>' if s.get('lead') else ''
    out = [f'<section class="{cls}" id="{sid}" aria-labelledby="{sid}-h"><div class="wrap">',
           f'<div class="sec-h" data-reveal><p class="eyebrow">{E(s["num"])}</p><h2 id="{sid}-h">{E(s["title"])}</h2>{lead}</div>']
    for b in s['blocks']:
        out.append(r_block(b, s['title']))
    out.append('</div></section>')
    return '\n'.join(out)

def build_case(c):
    slug = c['slug']
    title = f'{c["title"]} | кейс · Алексей, продуктовый дизайнер'
    h = head(title, c['lead'], 'case', slug)
    h += '<div class="progress" aria-hidden="true"></div>\n'
    h += '<header class="site-header"><div class="who"><a href="index.html">Алексей</a><a ' + SOON + '>tg: @mountdsgn1</a></div><a class="back" href="index.html#cases"><span aria-hidden="true">←</span> Все кейсы</a></header>\n<main id="main">\n'
    tags = ''.join(f'<li class="tag">{E(t)}</li>' for t in c['tags'])
    st = f'<span class="pill st"><i></i>{E(c["status"])}</span>' if c.get('status') else ''
    nd = f'<span class="pill nda">{E(c["nda"])}</span>' if c.get('nda') else ''
    note = f'<div class="notes">{st}{nd}</div>' if (st or nd) else ''
    hero_imgs = ''.join(f'<figure class="shot"><div class="fr">{img(n, c["hero_alt"], eager=True)}</div></figure>' for n in c['hero'])
    h += f'''<section class="c-hero wrap" aria-labelledby="h1">
<p class="eyebrow">{E(c['eyebrow'])}</p>
<h1 id="h1">{E(c['title'])}</h1>
<p class="lead">{E(c['lead'])}</p>
<ul class="tags">{tags}</ul>
{note}
<div class="shots n{len(c['hero'])}" style="margin-top:clamp(28px,3.4vw,66px)">{hero_imgs}</div>
<dl class="facts">''' + ''.join(f'<div data-reveal style="--i:{i}"><dt>{E(k)}</dt><dd>{E(v)}</dd></div>' for i, (k, v) in enumerate(c['facts'])) + f'''</dl>
<div class="summary"><p class="eyebrow">Коротко о кейсе</p><p data-reveal>{E(c['summary'])}</p></div>
{r_stats({'items': c['summary_stats'], 'cols': 4, 'fine': c.get('summary_fine')})}
</section>
'''
    for s in c['sections']:
        h += r_section(s) + '\n'
    others = [p for p in PROJECTS if p[0] != slug]
    h += f'''<section class="more wrap" aria-labelledby="more-h">
<div class="sec-head" data-reveal><h2 id="more-h">Другие проекты</h2><p>Можете ознакомиться с моими другими проектами</p></div>
<div class="more-grid">
{''.join(pcard(p, small=i >= 2, i=i % 3) for i, p in enumerate(others))}
</div>
</section>
''' + contact() + '\n</main>\n' + dock('cases') + '\n' + tail()
    (SITE / f'{slug}.html').write_text(h)

def main():
    (SITE / 'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#28282A"/><path d="M10 23V9h6.2a4.4 4.4 0 010 8.8H10" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    build_home()
    for slug in ['winery', 'crm', 'tencore', 'webxile', 'tietly', 'mount']:
        try:
            mod = importlib.import_module(f'data.{slug}')
        except ModuleNotFoundError as e:
            print('skip', slug, e); continue
        build_case(mod.CASE)
        print('built', slug)

if __name__ == '__main__':
    main()
