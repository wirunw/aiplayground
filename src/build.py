"""สร้าง index.html จาก src/template.html โดยฝังข้อมูลจำลอง (01b/02b/03b) แทน __DATA__
ใช้: python3 src/build.py  (รันจากโฟลเดอร์หลักของ repo)"""
import json, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = root / 'data'
read = lambda pat: next(d.glob(pat)).read_text(encoding='utf-8').strip()
data = {'staff': read('01b_*.txt'), 'me': read('02b_*.txt'), 'stock': read('03b_*.txt')}
t = (root / 'src' / 'template.html').read_text(encoding='utf-8')
assert t.count('__DATA__') == 1
(root / 'index.html').write_text(t.replace('__DATA__', json.dumps(data, ensure_ascii=False)), encoding='utf-8')
print('สร้าง index.html แล้ว')
