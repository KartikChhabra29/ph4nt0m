#!/usr/bin/env python3

import re
import sys
import json
import math
import asyncio
import argparse
import aiohttp
import urllib3
from collections import Counter
from urllib.parse import urljoin
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

urllib3.disable_warnings()

console = Console()

BANNER = r"""

██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝

      JavaScript Recon & Secret Intelligence Framework
"""

SECRET_PATTERNS = {
    "AWS": r"AKIA[0-9A-Z]{16}",
    "Google API": r"AIza[0-9A-Za-z\\-_]{35}",
    "GitHub": r"gh[pousr]_[A-Za-z0-9_]{30,}",
    "Stripe": r"sk_live_[0-9a-zA-Z]{24,}",
    "JWT": r"eyJ[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+",
    "Slack": r"xox[baprs]-[A-Za-z0-9\\-]+",
    "Discord": r"[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}",
    "Twilio": r"SK[0-9a-fA-F]{32}",
    "SendGrid": r"SG\\.[A-Za-z0-9_-]{22}\\.[A-Za-z0-9_-]{43}",
}

SEVERITY = {
    "AWS": "CRITICAL",
    "Stripe": "CRITICAL",
    "GitHub": "HIGH",
    "JWT": "MEDIUM",
}

ENDPOINT_REGEX = r'["\\\'](\\/api\\/[^"\\\']+)["\\\']'

TECH_SIGNATURES = {
    "React": "react",
    "Vue": "vue",
    "Angular": "angular",
    "NextJS": "_next",
    "Webpack": "webpack",
}

found_secrets = set()
found_endpoints = set()

stats = {
    "urls": 0,
    "secrets": 0,
    "endpoints": 0,
}

def entropy(data):
    if not data:
        return 0

    result = 0
    counter = Counter(data)

    for count in counter.values():
        p = count / len(data)
        result -= p * math.log2(p)

    return result

def detect_tech(content):
    tech = []

    for name, sig in TECH_SIGNATURES.items():
        if sig.lower() in content.lower():
            tech.append(name)

    return tech

def scan_entropy(content, url):
    strings = re.findall(r'[A-Za-z0-9+/=_-]{20,}', content)

    for s in strings:
        if entropy(s) > 4.5:
            console.print(
                f"[yellow][ENTROPY][/yellow] "
                f"[cyan]{url}[/cyan] "
                f"{s[:60]}"
            )

def scan_secrets(content, url):
    for name, pattern in SECRET_PATTERNS.items():
        matches = re.findall(pattern, content)

        for match in matches:
            key = f"{name}:{match}"

            if key in found_secrets:
                continue

            found_secrets.add(key)

            severity = SEVERITY.get(name, "LOW")

            console.print(
                f"[green][SECRET][/green] "
                f"[red][{severity}][/red] "
                f"[cyan]{url}[/cyan] "
                f"[yellow]{name}[/yellow] "
                f"{match}"
            )

            stats["secrets"] += 1

def scan_endpoints(content, url):
    matches = re.findall(ENDPOINT_REGEX, content)

    for endpoint in matches:
        if endpoint in found_endpoints:
            continue

        found_endpoints.add(endpoint)

        console.print(
            f"[blue][ENDPOINT][/blue] "
            f"[cyan]{url}[/cyan] "
            f"{endpoint}"
        )

        stats["endpoints"] += 1

async def fetch(session, url):
    try:
        async with session.get(url, ssl=False) as response:
            return await response.text()

    except Exception:
        return None

async def source_map_scan(session, url):
    map_url = f"{url}.map"

    content = await fetch(session, map_url)

    if content:
        console.print(
            f"[magenta][SOURCEMAP][/magenta] {map_url}"
        )

async def process(session, url, args):
    content = await fetch(session, url)

    if not content:
        return

    stats["urls"] += 1

    tech = detect_tech(content)

    if tech:
        console.print(
            f"[cyan][TECH][/cyan] "
            f"{url} "
            f"{', '.join(tech)}"
        )

    scan_secrets(content, url)
    scan_endpoints(content, url)

    if args.entropy:
        scan_entropy(content, url)

    if args.sourcemap:
        await source_map_scan(session, url)

async def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--entropy",
        action="store_true"
    )

    parser.add_argument(
        "--sourcemap",
        action="store_true"
    )

    parser.add_argument(
        "-o",
        "--output"
    )

    args = parser.parse_args()

    console.print(BANNER, style="bold red")

    urls = [line.strip() for line in sys.stdin if line.strip()]

    connector = aiohttp.TCPConnector(limit=100)

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = [
            process(session, url, args)
            for url in urls
        ]

        await asyncio.gather(*tasks)

    console.print(
        f"\n[green][✓][/green] URLs Scanned: {stats['urls']}"
    )

    console.print(
        f"[green][✓][/green] Secrets Found: {stats['secrets']}"
    )

    console.print(
        f"[green][✓][/green] Endpoints Found: {stats['endpoints']}"
    )

if __name__ == "__main__":
    asyncio.run(main())
