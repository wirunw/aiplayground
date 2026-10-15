"""สร้างหน้าเว็บ 2 หน้าจาก src/template.html
  index.html       คลังคำสั่ง workshop (ใช้ SEGMENTS ที่อยู่ใน template)
  work/index.html  คลังคำสั่งสำหรับงานประจำ (แทน SEGMENTS ด้วย src/segments_work.js)
ฝังข้อมูลจำลอง (01b/02b/03b) แทน __DATA__ และรูป assets/avatar.webp แทน __AVATAR__
ใช้: python3 src/build.py  (รันจากโฟลเดอร์หลักของ repo)"""
import json, pathlib, base64
root = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://wirunw.github.io/aiplayground/'

LINK_TO_WORK = ('<a class="crosslink" href="' + SITE + 'work/"><span>คลังคำสั่งสำหรับงานประจำ'
                '<small>สรุปเอกสาร วางแผน QI วิเคราะห์ข้อมูล ใช้ต่อได้หลังวันอบรม</small></span><span class="arr" aria-hidden="true">→</span></a>')
LINK_TO_MAIN = ('<a class="crosslink" href="' + SITE + '"><span>คลังคำสั่ง workshop'
                '<small>โจทย์และกิจกรรมของวันอบรม AI Playground</small></span><span class="arr" aria-hidden="true">→</span></a>')

WORK_TEXT = [
    ('<title>คลังคำสั่ง AI Playground</title>', '<title>คลังคำสั่งงานประจำ</title>'),
    ('<h1>คลังคำสั่ง AI สำหรับทีมเภสัชกรรม</h1>', '<h1>คลังคำสั่งสำหรับงานประจำของฝ่ายเภสัชกรรม</h1>'),
    ('<p>เลือกกิจกรรม กรอกช่องว่าง แล้วกดคัดลอกไปวางใน Gemini ข้อมูลจำลองรวมอยู่ในคำสั่งแล้ว</p>',
     '<p>เลือกงาน กรอกช่องว่าง แล้วกดคัดลอกไปวางใน Gemini แต่ละคำสั่งมีวิธีตรวจคำตอบกำกับไว้</p>'),
    ('<div class="rule"><b>ส่งผลงานในกลุ่มแชตของห้องให้ครบ 3 อย่าง</b> ผลงาน (screenshot) · คำสั่งที่ใช้ · 1 จุดที่ AI ทำผิดหรือต้องแก้</div>',
     '<div class="rule"><b>แบ่ง 2 ระดับตามข้อมูลที่ต้องใช้</b> ระดับ 1 ไม่ต้องใช้ข้อมูลภายใน ใช้ได้เลย · ระดับ 2 ต้องใช้ข้อมูลของฝ่าย ตอนนี้ฝึกด้วยข้อมูลจำลองที่ฝังอยู่ในคำสั่ง</div>'),
    ('<b>ห้ามใส่ข้อมูลผู้ป่วยจริง</b> ข้อมูลทุกชุดในหน้านี้เป็นข้อมูลจำลอง ถ้าจะลองกับงานของตัวเอง ให้ตัดชื่อ HN เลขบัตร และรายละเอียดที่ระบุตัวบุคคลออกก่อนทุกครั้ง',
     '<b>ห้ามใส่ข้อมูลผู้ป่วยรายบุคคล</b> ระดับ 2 วางข้อมูลจริงได้เฉพาะข้อมูลสรุปที่ไม่ระบุตัวบุคคล และเมื่อฝ่ายมีแนวทางการใช้ข้อมูลกับ AI แล้วเท่านั้น'),
]

def render(kind):
    """คืน HTML ของหน้า (ยังไม่ครอบ doctype) kind = 'main' หรือ 'work'"""
    d = root / 'data'
    read = lambda pat: next(d.glob(pat)).read_text(encoding='utf-8').strip()
    data = {'staff': read('01b_*.txt'), 'me': read('02b_*.txt'), 'stock': read('03b_*.txt')}
    t = (root / 'src' / 'template.html').read_text(encoding='utf-8')
    if kind == 'work':
        seg = (root / 'src' / 'segments_work.js').read_text(encoding='utf-8')
        a = t.index('const SEGMENTS = [')
        b = t.index('];\n', t.index(" {id:'plan'")) + 3
        t = t[:a] + seg + t[b:]
        for x, y in WORK_TEXT:
            assert t.count(x) == 1, x[:60]
            t = t.replace(x, y)
    t = t.replace('__CROSSLINK__', LINK_TO_WORK if kind == 'main' else LINK_TO_MAIN)
    avatar = 'data:image/webp;base64,' + base64.b64encode((root / 'assets' / 'avatar.webp').read_bytes()).decode()
    assert t.count('__DATA__') == 1
    return t.replace('__DATA__', json.dumps(data, ensure_ascii=False)).replace('__AVATAR__', avatar)

def wrap(t):
    # GitHub Pages ไม่มีโครง HTML ครอบให้เหมือน Artifact จึงต้องใส่ doctype และ viewport เอง ไม่งั้นมือถือจะย่อหน้าแบบจอคอม
    return ('<!doctype html>\n<html lang="th">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="theme-color" content="#1D2D52">\n'
            + t.replace('<div class="wrap">', '</head>\n<body>\n<div class="wrap">', 1)
            + '\n</body>\n</html>\n')

if __name__ == '__main__':
    (root / 'index.html').write_text(wrap(render('main')), encoding='utf-8')
    (root / 'work').mkdir(exist_ok=True)
    (root / 'work' / 'index.html').write_text(wrap(render('work')), encoding='utf-8')
    print('สร้าง index.html และ work/index.html แล้ว')
