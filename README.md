<p align="center">
  <img src="Boogie.svg" alt="BOOGIE Logo" width="300"/>
</p>

# 🔥 BOOGIE – Mobile Penetration Testing Framework

**BOOGIE** is an all‑in‑one mobile pentesting toolkit designed for **Termux** (Android) and other Linux environments. It combines reconnaissance, web attacks, payload generation, listeners, phishing, exploitation, and network utilities into a single, easy‑to‑use Python script.

> ⚠️ **IMPORTANT – LEGAL NOTICE**  
> This tool is intended for **authorized security assessments, educational purposes, and CTF competitions only**.  
> Unauthorized use against systems you do not own or have explicit permission to test is **illegal**.  
> The author (`anonymous-beta`) assumes no liability for misuse.

---

## ✨ Features

- **47+ modules**, **32+ payloads** – everything from recon to post‑exploitation
- **Reconnaissance** – DNS, subdomain brute‑force, certificate transparency, Wayback Machine, port scanning (Nmap/Python), directory brute‑force, technology fingerprinting, WHOIS, email/phone OSINT, social media search, Google dorks
- **Web Attacks** – SQLi scanner, XSS, LFI/RFI, command injection, header analysis, WAF detection, full web scan
- **Payload Generator** – Python, PHP, Bash, Perl, Ruby, Netcat, PowerShell, web shells (PHP/ASP), Android APK (msfvenom), Meterpreter staged payloads, custom builder
- **Listener** – Netcat, Python multi‑client, HTTP/HTTPS file server, PHP server
- **Phishing Kit** – Facebook, Google, Instagram, Twitter, LinkedIn, Microsoft, OTP/2FA pages; credential capture server; cloudflared tunnel for public URL
- **Exploitation** – privilege escalation checker, credential dumper, Linux/Windows enumeration scripts, SSH/FTP/HTTP brute‑force (Hydra), Metasploit integration
- **Network Attacks** – ARP scan, ping sweep, TCP scan, SYN scan (Nmap), packet capture, MAC changer, Slowloris stress test, Tor proxy chain

---

## 📱 Installation (Termux)

```bash
# Update packages and install git + python
pkg update && pkg upgrade -y
pkg install git python -y

# Clone the repository
git clone https://github.com/anonymous-beta/Boogie.git
cd Boogie

# Run Boogie (first run auto‑installs all dependencies)
python boogie.py
```

What happens on first run?

· Python modules (requests, scapy, dnspython, etc.) are installed via pip
· System packages (nmap, hydra, tor, etc.) are installed via pkg
· Wordlists (subdomains.txt, directories.txt) are generated
· sqlmap is cloned into the workspace

All data is stored in ~/boogie-workspace/ (logs, results, payloads, loot, etc.).

---

🕹️ Usage

Run python boogie.py and use the interactive menu:

1. Set a target (domain, IP, or URL) – most modules will use this target automatically.
2. Choose a module category: Recon / Web / Payload / Listener / Phishing / Exploit / Network.
3. Select a specific attack or scan.
4. Results are saved to ~/boogie-workspace/results/ as JSON or text files.

Example workflow:

```
$ python boogie.py
[?] Select option: 8
[?] Enter target: example.com
[+] Target set to: example.com

[?] Select option: 1   → Reconnaissance
[?] Select recon option: 2 → Subdomain brute‑force
```

---

🛠️ Requirements (auto‑installed)

· Python 3.8+
· Termux (recommended) or any Linux distribution with pkg/apt
· Internet connection for first‑run setup

---

🤝 Contributing

Issues, suggestions, and pull requests are welcome.
Please keep ethical considerations in mind.

---

📄 License

This project is licensed under the MIT License – see the LICENSE file for details.

---

⚡ Author

anonymous-beta – GitHub

Built with passion for security education and authorized testing.
