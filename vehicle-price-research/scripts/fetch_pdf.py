#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绕过 Akamai/Cloudflare 对 PDF 直链的 403 封锁，下载 PDF 到本地。

原理：在 Playwright 真实浏览器页面内做同源 fetch（带 cookies），
     把二进制转 base64 回传 Python 落盘。

用法：
    python3 fetch_pdf.py <pdf_url> <输出路径> [--locale es-ES] [--referer https://...]

示例：
    python3 fetch_pdf.py \
      "https://www.dsautomobiles.es/content/dam/ds/spain/pdf/caracteristicas-tecnicas/CT_DS3.pdf" \
      /tmp/CT_DS3.pdf --locale es-ES

注意：直链 403 的站点，必须先访问同域的一个正常页面建立会话（本脚本已内置）。
"""
import sys, os, base64, argparse

def fetch_pdf(url, out, locale='es-ES', referer=None, wait=3000):
    from playwright.sync_api import sync_playwright

    # 从 URL 推导同源首页，用于建立会话
    from urllib.parse import urlparse
    p = urlparse(url)
    home = f'{p.scheme}://{p.netloc}/'

    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
        ctx = br.new_context(
            locale=locale,
            user_agent=('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'),
            viewport={'width': 1440, 'height': 1000})
        pg = ctx.new_page()

        # 1) 先访问首页建立会话/cookie
        try:
            pg.goto(referer or home, wait_until='domcontentloaded', timeout=60000)
            pg.wait_for_timeout(wait)
        except Exception as e:
            print(f'[warn] 建立会话失败（继续尝试）: {e}')

        # 2) 页面内同源 fetch
        res = pg.evaluate("""async (u)=>{
          try{
            const r = await fetch(u,{credentials:'include'});
            const b = await r.arrayBuffer();
            const bytes = new Uint8Array(b);
            let s='';
            for(let i=0;i<bytes.length;i++) s+=String.fromCharCode(bytes[i]);
            return {ok:r.ok, status:r.status,
                    ct:r.headers.get('content-type'), len:bytes.length, b64:btoa(s)};
          }catch(e){return {err:String(e)}}
        }""", url)
        br.close()

    if res.get('err'):
        print(f'[FAIL] fetch 异常: {res["err"]}')
        return False
    if not res.get('ok'):
        print(f'[FAIL] HTTP {res.get("status")}')
        return False

    data = base64.b64decode(res['b64'])
    # 简单校验是否为 PDF
    head = data[:5]
    if head != b'%PDF-':
        print(f'[warn] 返回内容非 PDF（头部={head!r}, ct={res.get("ct")}）')

    os.makedirs(os.path.dirname(os.path.abspath(out)) or '.', exist_ok=True)
    with open(out, 'wb') as f:
        f.write(data)
    print(f'[OK] {len(data)} 字节 -> {out}  (ct={res.get("ct")})')
    return True


def main():
    ap = argparse.ArgumentParser(description='破 Akamai/Cloudflare PDF 403 并下载')
    ap.add_argument('url')
    ap.add_argument('out')
    ap.add_argument('--locale', default='es-ES')
    ap.add_argument('--referer', default=None)
    ap.add_argument('--wait', type=int, default=3000)
    a = ap.parse_args()
    ok = fetch_pdf(a.url, a.out, a.locale, a.referer, a.wait)
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
