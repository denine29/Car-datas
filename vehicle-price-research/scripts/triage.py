#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
站点可达性分诊（30 秒判断「这个站能不能采」）

按顺序探测，输出每个域的：
  - DNS 解析 IP
  - HTTP 状态（curl）
  - robots.txt 状态（用于判断是否整站封锁）
  - TCP 443 连通性
  - TLS 握手是否被 RST（SNI 级封锁的关键特征）
  - Playwright 无头/有头访问结果（可选）

用法：
    python3 triage.py <URL或域名> [更多URL...]
    python3 triage.py https://www.seat.be/fr https://org-eu-www.hyundai.com/eu/papi

结论速查：
    403 全站（含 robots.txt）      → 整站 IP 级封锁，无解，止损
    多市场域全 403                 → 同一 WAF 全球策略，无解
    TCP 通 + TLS read 0 bytes      → SNI 级封锁（浏览器表现为 ERR_CONNECTION_CLOSED）
    200                            → 可直连，继续找价格源
"""
import sys, socket, subprocess, argparse
from urllib.parse import urlparse

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def dns(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        try:
            return socket.getaddrinfo(host, 443, socket.AF_INET6)[0][4][0]
        except Exception:
            return None


def curl(url, timeout=20):
    r = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-A", UA,
         "-H", "Accept-Language: nl-BE,nl;q=0.9,en;q=0.8", url, "--max-time", str(timeout)],
        capture_output=True, text=True)
    return (r.stdout or "000").strip()


def tcp_ok(ip, port=443, timeout=8):
    try:
        s = socket.create_connection((ip, port), timeout=timeout)
        s.close()
        return True
    except Exception:
        return False


def tls_reset(host, port=443, timeout=12):
    """返回 (connected, reset)。TLS 立即 RST → read 0 bytes。"""
    r = subprocess.run(
        ["openssl", "s_client", "-connect", f"{host}:{port}", "-servername", host],
        input="", capture_output=True, text=True, timeout=timeout + 5)
    out = (r.stdout or "") + (r.stderr or "")
    connected = "CONNECTED" in out
    reset = ("read 0 bytes" in out) or ("unexpected eof" in out)
    return connected, reset


def playwright_probe(url, headed=False):
    """返回 (status, title)。headed 需 xvfb-run。"""
    js = r"""
const { chromium } = require('/root/.nvm/versions/node/v22.13.1/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ headless: %s, args:['--no-sandbox','--disable-dev-shm-usage'] });
  const c = await b.newContext({ userAgent: %s });
  const p = await c.newPage();
  try {
    const r = await p.goto(%s, { waitUntil:'domcontentloaded', timeout:40000 });
    console.log((r?r.status():'none') + ' | ' + (await p.title()));
  } catch(e) { console.log('ERR ' + e.message.split('\n')[0]); }
  await b.close();
})();
""" % ("false" if headed else "true", repr(UA), repr(url))
    cmd = ["node", "-e", js]
    if headed:
        cmd = ["xvfb-run", "-a", "--server-args=-screen 0 1600x1000x24"] + cmd
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return r.stdout.strip()
    except Exception as e:
        return "ERR " + str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--pw", action="store_true", help="额外跑 Playwright headless")
    ap.add_argument("--headed", action="store_true", help="额外跑 Playwright headed(xvfb)")
    a = ap.parse_args()

    for u in a.urls:
        if "://" not in u:
            u = "https://" + u
        p = urlparse(u)
        host = p.netloc
        print("=" * 72)
        print(f"URL  : {u}")
        ip = dns(host)
        print(f"DNS  : {ip or 'NXDOMAIN'}")
        if not ip:
            print("=> 结论: 域名不解析（NXDOMAIN），换个域名或确认拼写")
            continue
        http = curl(u)
        robots = curl(f"{p.scheme}://{host}/robots.txt")
        print(f"HTTP : {http}   robots.txt: {robots}")
        tcp = tcp_ok(ip) if ":" not in ip else None
        print(f"TCP 443: {'OK' if tcp else 'FAIL'}")
        conn, reset = tls_reset(host)
        print(f"TLS  : connected={conn}  reset={reset}")
        if a.pw:
            print("PW(headless):", playwright_probe(u, headed=False))
        if a.headed:
            print("PW(headed)  :", playwright_probe(u, headed=True))

        # 结论
        if http == "403" and robots == "403":
            print("=> 结论: 整站 IP 级封锁（连 robots.txt 都 403），无解，止损")
        elif http == "403":
            print("=> 结论: 应用层 WAF 403，可试 Playwright 真实浏览器/换路径")
        elif reset and not conn:
            print("=> 结论: TLS 被 RST —— SNI 级封锁，该 API 无解")
        elif reset:
            print("=> 结论: TLS 握手被断（read 0 bytes）—— SNI 级封锁")
        elif http in ("200", "301", "302"):
            print("=> 结论: 可直连，继续定位价格源")
        elif http == "000":
            print("=> 结论: 连接失败（TCP/SNI/超时），查上面 TCP 与 TLS 结果")
        else:
            print(f"=> 结论: HTTP {http}，人工判断")


if __name__ == "__main__":
    main()
