from playwright.sync_api import sync_playwright
import subprocess
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();pg.goto('file:///home/claude/build/cv/cv.html');pg.wait_for_timeout(500)
    print('content h',pg.evaluate("document.body.scrollHeight"),'page',pg.evaluate("document.documentElement.clientHeight"))
    pg.pdf(path='/home/claude/build/cv/cv.pdf',width='210mm',height='297mm',print_background=True,prefer_css_page_size=True)
print(subprocess.run("pdfinfo /home/claude/build/cv/cv.pdf | grep Pages; pdftoppm -r 80 -png /home/claude/build/cv/cv.pdf /tmp/cvn",shell=True,capture_output=True,text=True).stdout)
