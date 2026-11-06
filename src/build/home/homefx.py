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
 ('winery','B2B SAAS · WEB + MOBILE','Цифровая платформа для винодельни','Комплексная система управления виноделием','fx-c-winery','l',(414,485,0,0),(102.27,-26.31,-2.27,160)),
 ('crm','B2B CRM · WEB','CRM: рабочее пространство для команды','Для компании, оказывающей клиентам банковские и финансовые услуги','fx-c-crm','c',(420,474,0,0),(104.64,-27.18,-0.84,158.73)),
 ('tencore','САЙТ · FINTECH · ГОСЗАКУПКИ','Банковские услуги «Tencore»','Платформа поставщиков госзакупок','fx-c-tencore','l',(425,476,-6,0),(99.9,-21.65,0.16,150.35)),
 ('webxile','САЙТ ДИЗАЙН-СТУДИИ · WEB','Дизайн-студия «WEBXILE»','Сайт дизайн-студии','fx-c-webxile','c',(414,487,0,5),(100.82,-26.34,-0.82,159.34)),
 ('tietly','MOBILE · SOCIAL + WEB3','Социальная сеть «TIETLY»','Мобильное приложение соцсети, объединенное с крипто-кошельком','fx-c-tietly','w',(690,397,1,0),(116.08,-0.03,-11.67,100.06)),
 ('mount','MOBILE · КРИПТОКОШЕЛЁК','Крипто-кошелек «MOUNT»','Мобильное приложение крипто-кошелька','fx-c-mount','w',(675,402,None,0),(117.74,-2.81,-12.48,105.19)),
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
<div class="clip {kind}"><div style="{pos}top:{it}u;width:{iw}u;height:{ih}u"><img src="assets/img/{im}.webp" alt="Обложка кейса: {E(title)}" width="{iw_}" height="{ih_}" loading="lazy" decoding="async" style="height:{h}%;left:{l}%;top:{t}%;width:{w}%"></div></div>
<div class="bar"><div class="in"><div class="txt"><span class="lab">{E(lab)}</span><div><h3>{E(title)}</h3><p class="sub" style="margin-top:8px">{E(sub)}</p></div></div>{ico('325c1','class="ic" aria-hidden="true"')}</div></div>
</a>'''

JOBS = [
 ('Крым Диджитал - Продуктовый дизайнер','Июль 2022 - сейчас',False,[
  'Проектирую B2B-платформу для винодельни: 60 модулей, web и мобильное приложение для поля. Продукт внедрён на 3–4 винодельнях',
  'Создал дизайн-систему: время разработки новых экранов сократилось на 25–30%',
  'Внедрил дизайн-ревью интерфейсов: возвраты задач от разработки снизились на ~30%',
  'Провёл UX-исследования и A/B-тесты: сократил ключевые флоу на 1–2 шага, успешное завершение сценариев ~85–90%',
  'Менторю дизайнеров и участвую в найме: срок выхода новичков на полную продуктивность сократился на 20%',
  'Применяю ИИ в работе: автоматизирую рутину, ускоряю прототипирование и вайбкодю интерактивные прототипы']),
 ('WebXile (дизайн-студия) - UX/UI дизайнер','Май 2021 - Июль 2022',True,[
  'Проектировал интерфейсы для B2B и B2C: от лендингов до многостраничных порталов',
  'Сделал мобильные приложения для iOS и Android: соцсеть Tietly и крипто-кошелёк Mount',
  'Проанализировал пользовательские пути (CJM), нашёл барьеры в интерфейсах и повысил вовлечённость аудитории']),
]

def build():
    css = u((HERE/'home.src.css').read_text()) + (HERE/'home.mobile.css').read_text() if (HERE/'home.mobile.css').exists() else u((HERE/'home.src.css').read_text())
    (SITE/'assets/css/home.css').write_text(css)
    dots = [(390,670),(584,670),(1516,670),(1322,670),(390,537),(1516,537),(390,403),(584,403),(1516,404),(1322,404)]
    nav = [('home','#top','Главная','c66f8',True),('rezume','assets/Alexey-Gora-CV.pdf','Резюме','8a767',False),('cases','#cases','Кейсы','7e65a',False),('work','#work','Опыт','dec72',False),('tg','https://t.me/mountdsgn1','Telegram','2484d',False)]
    navh = ''.join(f'<a href="{h}" data-label="{l}" aria-label="{l}"{" data-sec=\"%s\""%k if k in ("home","cases","work") else ""}{" aria-current=\"page\"" if cur else ""}{" download=\"Gora-Alexey-CV.pdf\"" if k=="rezume" else ""}{" target=\"_blank\" rel=\"noopener noreferrer\"" if k=="tg" else ""}>{ico(i,"aria-hidden=\"true\"")}</a>' for k,h,l,i,cur in nav)
    jobs = ''
    for j,(t,d,m,items) in enumerate(JOBS):
        jobs += f'''<article class="fx-job{" m" if m else ""}" data-reveal>
<h3 style="margin:0;font:inherit"><button class="name" type="button" aria-expanded="true" aria-controls="job{j}"><span class="tt"><b>{E(t)}</b><small><i></i>{E(d)}</small></span><span class="fx-chev">{ico('b8699','aria-hidden="true"')}</span></button></h3>
<div class="body" id="job{j}"><div><ul>{''.join(f'<li>{ico("13100","aria-hidden=\"true\"")}<span>{E(x)}</span></li>' for x in items)}</ul></div></div>
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
<link rel="stylesheet" href="assets/css/site.css">
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
<header class="fx-head"><p class="who"><span>Алексей</span><a href="https://t.me/mountdsgn1" target="_blank" rel="noopener noreferrer">tg: @mountdsgn1</a></p><p class="aside">B2B-платформа на 3–4 винодельнях, мобильные продукты и финтех: от первого MVP до аналитических систем</p></header>
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
