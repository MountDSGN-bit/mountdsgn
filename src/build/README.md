# Сборка

- `home/homefx.py` — генерирует `index.html` и `assets/css/home.css`.
- `case/run.py <slug…>` — генерирует страницы кейсов из `case/data_<slug>.py` (шаблон `casefx.py`, стили `case.src.css` + `case.mobile.css`).
- `build.py` и `data/` — устаревший генератор, страницы кейсов им больше не собираются.

Размеры в `*.src.css` записаны в «дизайн-пикселях» (`Nu`), они превращаются в `calc(var(--u)*N)`.
