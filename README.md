<img src="https://raw.githubusercontent.com/KartikChhabra29/ph4nt0m/main/Screenshot%202026-05-19%20173451.png" width="900">


# PH4NT0M — JavaScript Recon & Secret Intelligence Framework

Fast & advanced JavaScript reconnaissance framework for discovering secrets, endpoints, source maps, tokens, API keys, JWTs, and hidden attack surfaces from JS files.

---

## Features

- Async ultra-fast scanning engine
- Detects 50+ secret types
- API keys, AWS, Stripe, JWT, GitHub, Slack, Firebase & more
- Entropy-based secret detection (`--entropy`)
- Endpoint extraction (`/api/`, `/graphql`, `/admin`)
- Source map intelligence (`--sourcemap`)
- Technology detection (React, Vue, Angular, Webpack)
- Severity scoring (Critical / High / Medium / Low)
- JSON output support
- Rich CLI UI
- Custom headers & cookies
- Proxy support
- Multi-threaded async architecture
- Secret deduplication
- JS variable + comment analysis
- Docker support
- GitHub Actions CI/CD

---

# Installation

```bash
# Clone Repository
git clone https://github.com/KartikChhabra29/ph4nt0m.git

cd ph4nt0m

# Create Virtual Environment
python3 -m venv ph4nt0m-env

# Activate Environment
source ph4nt0m-env/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

---

# Basic Usage

```bash
cat js_urls.txt | python3 ph4nt0m.py
```

---

# Advanced Usage

## Enable Entropy Detection

```bash
cat js_urls.txt | python3 ph4nt0m.py --entropy
```

---

## Enable Source Map Scanning

```bash
cat js_urls.txt | python3 ph4nt0m.py --sourcemap
```

---

## Save Results

```bash
cat js_urls.txt | python3 ph4nt0m.py -o results.json
```

---

## Verbose Recon Mode

```bash
cat js_urls.txt | python3 ph4nt0m.py --entropy --sourcemap -o results.json
```

---

## Scan JS Files from a Domain

```bash
echo "example.com" | \
waybackurls | \
grep "\\.js$" | \
python3 ph4nt0m.py --entropy --sourcemap
```

---

# Full Recon Pipeline

```bash
echo "tesla.com" | \
subfinder -silent | \
httpx -silent | \
katana -jc -silent | \
grep "\\.js$" | \
python3 ph4nt0m.py --entropy --sourcemap -o results.json
```

---

# Supported Secret Types

```text
AWS Keys
Google API Keys
JWT Tokens
GitHub Tokens
Slack Tokens
Stripe Secrets
Firebase Tokens
Discord Tokens
Twilio Keys
SendGrid Keys
OAuth Tokens
Passwords
Database URLs
Bearer Tokens
Cloudflare Tokens
Private Keys
Generic Secrets
```

---

# Technology Detection

PH4NT0M automatically detects:

```text
React
Vue
Angular
NextJS
Webpack
Vite
Nuxt
```

---

# Example Output

```bash
[SECRET] [CRITICAL] https://target.com/app.js AWS AKIAIOSFODNN7EXAMPLE

[ENDPOINT] https://target.com/app.js /api/v1/admin

[TECH] https://target.com/app.js React, Webpack

[SOURCEMAP] https://target.com/app.js.map

[ENTROPY] https://target.com/app.js dGhpc2lzYXNlY3JldGtleQ==
```

# GitHub Actions

PH4NT0M includes:

- Black
- Ruff
- Bandit
- Safety
- MyPy
- Pytest
- Docker Build Verification

---

# Add PH4NT0M as Global Command

```bash
echo '#!/bin/bash
source ~/ph4nt0m/ph4nt0m-env/bin/activate
python3 ~/ph4nt0m/ph4nt0m.py "$@"' | sudo tee /usr/bin/ph4nt0m

sudo chmod +x /usr/bin/ph4nt0m
```

Now you can run PH4NT0M globally:

```bash
ph4nt0m
```

---

# Project Structure

```bash
ph4nt0m/
│
├── .github/
│   └── workflows/
│       └── python-package.yml
│
├── ph4nt0m.py
├── requirements.txt
├── Dockerfile
├── README.md
├── LICENSE
└── .gitignore
```

---

# Roadmap

- AST Parsing
- Webpack Chunk Extraction
- Headless Browser Scanning
- Burp Suite Extension
- Chrome Extension
- AI-based False Positive Filtering
- Dashboard UI
- Live Recon Monitoring

---

# Disclaimer

This tool is intended for educational purposes and authorized security testing only.

Unauthorized usage against targets without permission is illegal.

---

# Author

Kartik Chhabra

GitHub:
https://github.com/KartikChhabra29
