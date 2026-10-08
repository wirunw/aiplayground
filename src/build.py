"""สร้าง index.html จาก src/template.html โดยฝังข้อมูลจำลอง (01b/02b/03b) แทน __DATA__ และรูป assets/avatar.webp แทน __AVATAR__
ใช้: python3 src/build.py  (รันจากโฟลเดอร์หลักของ repo)"""
import json, pathlib, base64
root = pathlib.Path(__file__).resolve().parent.parent
d = root / 'data'
read = lambda pat: next(d.glob(pat)).read_text(encoding='utf-8').strip()
data = {'staff': read('01b_*.txt'), 'me': read('02b_*.txt'), 'stock': read('03b_*.txt')}
t = (root / 'src' / 'template.html').read_text(encoding='utf-8')
assert t.count('__DATA__') == 1
avatar = 'data:image/webp;base64,' + base64.b64encode((root / 'assets' / 'avatar.webp').read_bytes()).decode()
t = t.replace('__DATA__', json.dumps(data, ensure_ascii=False)).replace('__AVATAR__', avatar)
# GitHub Pages ไม่มีโครง HTML ครอบให้เหมือน Artifact จึงต้องใส่ doctype และ viewport เอง ไม่งั้นมือถือจะย่อหน้าแบบจอคอม
page = ('<!doctype html>\n<html lang="th">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<meta name="theme-color" content="#1D2D52">\n'
        + t.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1)
        + '\n</body>\n</html>\n')
(root / 'index.html').write_text(page, encoding='utf-8')
print('สร้าง index.html แล้ว')
