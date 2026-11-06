import sys, asyncio
from playwright.async_api import async_playwright
OUT='/tmp/claude-0/-home-claude/ccd58704-1ea8-52ce-b622-fa9320287125/scratchpad/shots'
async def main(pages, widths, full=True):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in widths:
            ctx = await b.new_context(viewport={'width':w,'height':1080 if w>800 else 844}, reduced_motion='reduce', device_scale_factor=1)
            pg = await ctx.new_page()
            logs=[]
            pg.on('console', lambda m: logs.append(m.type+': '+m.text) if m.type in ('error','warning') else None)
            pg.on('pageerror', lambda e: logs.append('pageerror: '+str(e)))
            pg.on('requestfailed', lambda r: logs.append('reqfail: '+r.url))
            for name in pages:
                await pg.goto(f'http://127.0.0.1:8765/{name}.html' if name!='index' else 'http://127.0.0.1:8765/index.html', wait_until='networkidle')
                await pg.wait_for_timeout(300)
                # force-load lazy images
                await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')")
                H0 = await pg.evaluate('document.documentElement.scrollHeight')
                for y in range(0, H0, 700):
                    await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(60)
                await pg.evaluate('window.scrollTo(0,0)')
                await pg.wait_for_function("[...document.images].every(i=>!i.getAttribute('src')||(i.complete && i.naturalWidth>0))", timeout=30000)
                await pg.wait_for_timeout(300)
                ov = await pg.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                h = await pg.evaluate("document.documentElement.scrollHeight")
                print(name, w, 'overflowX', ov, 'height', h, logs[:5])
                await pg.screenshot(path=f'{OUT}/{name}-{w}.png', full_page=full)
            await ctx.close()
        await b.close()
pages = sys.argv[1].split(',')
widths = [int(x) for x in sys.argv[2].split(',')]
asyncio.run(main(pages, widths))
