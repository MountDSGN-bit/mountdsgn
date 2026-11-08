import re, html
from pathlib import Path
E = html.escape
SITE = Path('/home/claude/site')
HERE = Path(__file__).parent

def u(css):
    return re.sub(r'(?<![\w.#-])(-?\d*\.?\d+)u\b', lambda m: f'calc(var(--u)*{m.group(1)})', css)

def ico(n, cls='', alt=''):
    return f'<img src="assets/icons/fx/{n}.svg" alt="{alt}" {cls}>'

CARDS = [
 ('winery','B2B SAAS · WEB + MOBILE','Платформа для винодельни','Система управления виноделием','fx-c-winery','l',(414,485,0,0),(102.27,-26.31,-2.27,160)),
 ('crm','B2B CRM · WEB','CRM для рабочей команды','Для банков и финансовых услуг','fx-c-crm','c',(420,474,0,0),(104.64,-27.18,-0.84,158.73)),
 ('tencore','САЙТ · FINTECH · ГОСЗАКУПКИ','Банковские услуги «Tencore»','Платформа госзакупок','fx-c-tencore','l',(425,476,-6,0),(99.9,-21.65,0.16,150.35)),
 ('webxile','САЙТ ДИЗАЙН-СТУДИИ · WEB','Дизайн-студия «WEBXILE»','Сайт дизайн-студии','fx-c-webxile','c',(414,487,0,5),(100.82,-26.34,-0.82,159.34)),
 ('tietly','MOBILE · SOCIAL + WEB3','Социальная сеть «TIETLY»','Соцсеть с крипто-кошельком','fx-c-tietly','w',(690,397,1,0),(116.08,-0.03,-11.67,100.06)),
 ('mount','MOBILE · КРИПТОКОШЕЛЁК','Крипто-кошелёк «MOUNT»','Приложение крипто-кошелька','fx-c-mount','w',(675,402,None,0),(117.74,-2.81,-12.48,105.19)),
]
MAN = None
def dims(n):
    from PIL import Image
    w,h = Image.open(SITE/f'assets/img/{n}.webp').size
    return w,h

def card(i,c):
    slug,lab,title,sub,im,kind,(iw,ih,il,it),(h,l,t,w) = c
    iw_,ih_ = dims(im)
    pos = f'left:calc(50% - {iw/2}u);' if il is None else f'left:{il}u;'
    return f'''<a class="fx-card" href="{slug}.html" data-reveal style="--i:{i%2}">
<div class="cbg"><img src="assets/img/fx-bg.webp" alt="" width="2400" height="1600" loading="lazy" decoding="async"></div>
<div class="clip {kind} {"kp" if kind=="w" else "kc"}"><div style="{pos}top:{it}u;width:{iw}u;height:{ih}u"><img src="assets/img/{im}.webp" alt="Обложка кейса: {E(title)}" width="{iw_}" height="{ih_}" loading="lazy" decoding="async" style="height:{h}%;left:{l}%;top:{t}%;width:{w}%"></div></div>
<div class="bar"><div class="in"><div class="txt"><span class="lab">{E(lab)}</span><div><h3>{E(title)}</h3><p class="sub" style="margin-top:8px">{E(sub)}</p></div></div><span class="ic" aria-hidden="true"><svg viewBox="0 0 76 76" fill="none"><path d="M56 38H55C55 47.3888 47.3888 55 38 55V56V57C48.4934 57 57 48.4934 57 38H56ZM38 56V55C28.6112 55 21 47.3888 21 38H20H19C19 48.4934 27.5066 57 38 57V56ZM20 38H21C21 28.6112 28.6112 21 38 21V20V19C27.5066 19 19 27.5066 19 38H20ZM38 20V21C47.3888 21 55 28.6112 55 38H56H57C57 27.5066 48.4934 19 38 19V20Z" fill="#000"/><path class="ar" d="M33.403 30.4415C32.853 30.3915 32.3666 30.7968 32.3166 31.3468C32.2666 31.8969 32.6719 32.3833 33.2219 32.4333L33.3125 31.4374L33.403 30.4415ZM43.625 32.3749L44.6209 32.2843C44.5772 31.8036 44.1963 31.4227 43.7156 31.379L43.625 32.3749ZM43.5667 42.778C43.6167 43.328 44.1031 43.7333 44.6531 43.6833C45.2031 43.6333 45.6084 43.1469 45.5584 42.5969L44.5625 42.6875L43.5667 42.778ZM31.6679 42.9179C31.2773 43.3084 31.2773 43.9415 31.6679 44.3321C32.0584 44.7226 32.6915 44.7226 33.0821 44.3321L32.375 43.625L31.6679 42.9179ZM33.3125 31.4374L33.2219 32.4333L43.5345 33.3708L43.625 32.3749L43.7156 31.379L33.403 30.4415L33.3125 31.4374ZM43.625 32.3749L42.6291 32.4654L43.5667 42.778L44.5625 42.6875L45.5584 42.5969L44.6209 32.2843L43.625 32.3749ZM43.625 32.3749L42.9179 31.6678L31.6679 42.9179L32.375 43.625L33.0821 44.3321L44.3321 33.082L43.625 32.3749Z" fill="#000"/></svg></span></div></div>
</a>'''

JOBS = [
 ('Крым Диджитал - Продуктовый дизайнер','Июль 2022 - сейчас',False,[
  'Спроектировал B2B SaaS-платформу для виноделен (web и мобильное приложение для поля): 60 модулей, внедрена на 3+ винодельнях, заменила бумажные журналы и Excel',
  'Создал и развиваю дизайн-систему: токены, компоненты, документация; время разработки новых экранов сократилось на 27%',
  'Внедрил дизайн-ревью реализованных интерфейсов: возвраты задач от разработки снизились на 29%',
  'Провёл UX-исследования и A/B-тесты: сократил ключевые флоу на 1–2 шага, доля успешно завершённых сценариев выросла с 66% до 83%, CTR ключевых элементов - на 16%',
  'Менторю дизайнеров, участвую в найме и онбординге: срок выхода новичка на полную продуктивность сократился на 20%',
  'Внедрил ИИ-инструменты и вайбкодинг интерактивных прототипов: цикл «гипотеза → прототип» сократился с 7 дней до 1']),
 ('Упрости-бизнес.рф (ранее WebXile) - UX/UI дизайнер','Май 2021 - Июль 2022',True,[
  'Спроектировал с нуля iOS-приложение соцсети Tietly (100+ экранов) за 4 месяца: UX-исследование, UX/UI-дизайн, материалы для питча инвесторам',
  'Сделал корпоративный сайт fintech-компании Tencore за 3 недели: информационная архитектура, калькулятор стоимости, единая навигация по 6 финансовым продуктам и 75 банкам-партнёрам',
  'Вёл дизайн CRM-системы с PM, аналитиками и разработкой - от исследования до дизайн-системы; на юзабилити-тестировании прототипа 7 из 8 пользователей прошли регистрацию без подсказок',
  'Построил Customer Journey Map (CJM), выявил барьеры в интерфейсах и устранил их: вовлечённость выросла на 13%']),
]

def build():
    css = u((HERE/'home.src.css').read_text()) + (HERE/'home.mobile.css').read_text() if (HERE/'home.mobile.css').exists() else u((HERE/'home.src.css').read_text())
    (SITE/'assets/css/home.css').write_text(css)
    dots = [(390,670),(584,670),(1516,670),(1322,670),(390,537),(1516,537),(390,403),(584,403),(1516,404),(1322,404)]
    nav = [('home','#top','Главная','c66f8',True),('rezume','assets/Alexey-Gora-CV.pdf','Резюме','8a767',False),('cases','#cases','Кейсы','7e65a',False),('work','#work','Опыт','dec72',False),('tg','https://t.me/mountdsgn1','Telegram','2484d',False)]
    navh = ''.join(f'<a href="{h}" data-label="{l}" aria-label="{l}"{" data-sec=\"%s\""%k if k in ("home","cases","work") else ""}{" aria-current=\"page\"" if cur else ""}{" download=\"Gora-Alexey-CV.pdf\"" if k=="rezume" else ""}{" target=\"_blank\" rel=\"noopener noreferrer\"" if k=="tg" else ""}><i class="ic" aria-hidden="true" style="-webkit-mask-image:url(assets/icons/fx/{i}.svg);mask-image:url(assets/icons/fx/{i}.svg)"></i></a>' for k,h,l,i,cur in nav)
    jobs = ''
    for j,(t,d,m,items) in enumerate(JOBS):
        jobs += f'''<article class="fx-job{" m" if m else ""}" data-reveal>
<h3 style="margin:0;font:inherit"><button class="name" type="button" aria-expanded="false" aria-controls="job{j}"><span class="tt"><b>{E(t)}</b><small><i></i>{E(d)}</small></span><span class="fx-chev">{ico('b8699','aria-hidden="true"')}</span></button></h3>
<div class="body" id="job{j}" hidden><div><ul>{''.join(f'<li>{ico("13100","aria-hidden=\"true\"")}<span>{E(x)}</span></li>' for x in items)}</ul></div></div>
</article>
'''
    page = f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Алексей Гора — продуктовый дизайнер</title>
<meta name="description" content="Портфолио продуктового дизайнера: B2B-платформы, мобильные продукты и финтех. Шесть кейсов.">
<meta name="theme-color" content="#ffffff">
<meta property="og:title" content="Алексей Гора — продуктовый дизайнер">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/Poppins-SemiBold.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="assets/fonts/MrDeHaviland.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/css/fonts.css">
<link rel="stylesheet" href="assets/css/home.css">
<script>document.documentElement.classList.add('js')</script>
</head>
<body class="home fx">
<a class="skip" href="#main">Перейти к содержимому</a>
<div class="page">
<section class="fx-hero" id="top" aria-label="Алексей, продуктовый дизайнер">
<img class="bg" src="assets/img/fx-bg.webp" width="2400" height="1600" alt="" fetchpriority="high">
<p class="hw yr y1" aria-hidden="true">20</p><p class="hw yr y2" aria-hidden="true">26</p>
<h1 class="sr">UX/UI Designer, Product Designer</h1>
<p class="hw t t-b" aria-hidden="true">Product Designer</p>
<p class="hw t t-a" aria-hidden="true">UX/UI Designer</p>
<header class="fx-head"><p class="who"><span>Алексей</span><a href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer">tg: @mountdsgn1</a></p><p class="aside">B2B-платформа на 3+ винодельнях, мобильные продукты и финтех: от первого MVP до аналитических систем</p></header>
<div class="fx-frame" aria-hidden="true"><img src="assets/img/fx-frame.webp" alt="" width="2254" height="534">{''.join(f'<i class="fx-dot" style="left:{x-397}u;top:{y-410}u"></i>' for x,y in dots)}</div>
<div class="fx-fig"><img src="assets/img/fx-figurine.webp" alt="3D-фигурка дизайнера" width="1024" height="808" fetchpriority="high"></div>
</section>
<main id="main">
<div class="fx-main">
<section class="fx-info" aria-label="Обо мне">
<p class="lead" data-reveal>Продуктовый дизайнер, 5+ лет в web и mobile. Проектирую сложные B2B-платформы: от исследования и логики до дизайн-системы и релиза. Ускоряю работу с ИИ: прототипы, автоматизация, вайбкодинг.</p>
<div class="right" data-reveal style="--i:1"><p>UX-исследования, user flow, прототипы, UI, дизайн-системы, дизайн-ревью. Работаю с PM, аналитиками и разработкой, менторю дизайнеров.</p>
<a class="fx-resume" href="assets/Alexey-Gora-CV.pdf" download="Gora-Alexey-CV.pdf" aria-label="Скачать резюме (PDF)"><span>Резюме</span>{ico('a6572','aria-hidden="true"')}</a></div>
</section>
<section class="fx-cases" id="cases" aria-labelledby="cases-h">
<div class="fx-sec-head" data-reveal><h2 id="cases-h">Кейсы</h2><p class="sec-p">Демонстрация моих <br>последних проектов</p></div>
<div class="fx-grid">
{chr(10).join(card(i,c) for i,c in enumerate(CARDS))}
</div>
</section>
</div>
<section class="fx-work" id="work" aria-labelledby="work-h"><div class="in">
<div class="fx-sec-head" data-reveal><h2 id="work-h">Опыт работы</h2><p>5+ лет в разработке продуктов</p></div>
<div class="fx-jobs">
{jobs}</div></div></section>
<section class="fx-foot" aria-labelledby="contact-h">
<div class="tx"><p class="up" data-reveal>Блок для связи.</p><h2 id="contact-h" style="margin:0;font:inherit"><span class="mid" style="position:absolute;left:0;top:28u;display:block" data-reveal>Поработаем вместе?</span><span class="down" style="position:absolute;left:0;top:121u;display:block" data-reveal>Напишите мне в телеграм</span></h2></div>
<div class="line"></div>
<dl data-reveal><div><dt>Email:</dt><dd><a href="mailto:mountdsgn@mail.ru">mountdsgn@mail.ru</a></dd></div><div><dt>Phone</dt><dd><a href="tel:+79183212635">+7 (918) 321-26-35</a></dd></div></dl>
<a class="fx-btn" href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer" aria-label="Написать в Telegram (откроется в новой вкладке)">{ico('c4553','class="a" aria-hidden="true"')}{ico('3c2a1','class="b" aria-hidden="true"')}<span class="t">Написать{ico('088e2','aria-hidden="true"')}</span></a>
</section>
</main>
</div>
<nav class="fx-nav" aria-label="Навигация">{navh}</nav>
<script src="assets/js/site.js" defer></script>
</body>
</html>
'''
    page = u_inline(page)
    (SITE/'index.html').write_text(page)

def u_inline(s):
    # inline style="...Nu" values
    return re.sub(r'style="([^"]*)"', lambda m: 'style="'+u(m.group(1))+'"', s)

if __name__=='__main__': build(); print('built')
