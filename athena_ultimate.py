#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   █████╗ ████████╗██╗  ██╗███████╗███╗   ██╗ █████╗                         ║
║  ██╔══██╗╚══██╔══╝██║  ██║██╔════╝████╗  ██║██╔══██╗                        ║
║  ███████║   ██║   ███████║█████╗  ██╔██╗ ██║███████║                        ║
║  ██╔══██║   ██║   ██╔══██║██╔══╝  ██║╚██╗██║██╔══██║                        ║
║  ██║  ██║   ██║   ██║  ██║███████╗██║ ╚████║██║  ██║                        ║
║  ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝                        ║
║                                                                              ║
║   ULTIMATE VULNERABILITY INTELLIGENCE PLATFORM                              ║
║   AI-Powered Defense Orchestrator + Real-time Dashboard                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import json
import re
import os
import requests
import hashlib
import threading
import webbrowser
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import Counter
from dataclasses import dataclass, asdict
from queue import Queue
import sys

# ==================== Dashboard Imports ====================
try:
    import dash
    from dash import dcc, html, Input, Output, callback_context
    import plotly.graph_objs as go
    import plotly.express as px
    import pandas as pd
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False
    print("⚠️ Dash not installed. Run: pip install dash plotly pandas")

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️ Redis not installed. Run: pip install redis")

# ==================== Configuration ====================
@dataclass
class Config:
    reports_dir: Path = Path("reports")
    cache_dir: Path = Path(".cache")
    cache_file: Path = cache_dir / "athena_ultimate_cache.json"
    llm_url: str = "http://localhost:11434/api/generate"
    llm_model: str = "llama3.1"
    llm_temp: float = 0.1
    redis_host: str = "localhost"
    redis_port: int = 6379
    dashboard_port: int = 8050
    dashboard_host: str = "0.0.0.0"
    auto_open_browser: bool = True
    max_history: int = 500

config = Config()

# ==================== Advanced Payload Analysis ====================
class PayloadAnalyzer:
    """Advanced payload analysis with MITRE ATT&CK mapping"""
    
    PATTERNS = {
        "SQL Injection": {
            "patterns": [r"union.*select", r"1' or '1'='1", r"benchmark", r"sleep", r"waitfor", r"information_schema", r"pg_sleep", r"or 1=1", r"'.*--"],
            "vectors": ["Union-based", "Time-based", "Error-based", "Boolean-based", "Stacked Queries"],
            "mitre_id": "T1190",
            "mitre_tactic": "Initial Access",
            "severity": "High"
        },
        "Cross-Site Scripting (XSS)": {
            "patterns": [r"<script", r"javascript:", r"on\w+=", r"eval\(", r"alert\(", r"prompt\(", r"confirm\(", r"document\.cookie"],
            "vectors": ["Reflected", "Stored", "DOM-based", "Blind"],
            "mitre_id": "T1059.007",
            "mitre_tactic": "Execution",
            "severity": "Medium"
        },
        "Command Injection": {
            "patterns": [r";\s*\w+", r"\|\s*\w+", r"\$\(", r"`.*`", r"whoami", r"id", r"ping", r"nc -e", r"bash -c", r"curl", r"wget"],
            "vectors": ["Direct Execution", "Blind", "Reverse Shell", "Out-of-band"],
            "mitre_id": "T1202",
            "mitre_tactic": "Execution",
            "severity": "Critical"
        },
        "Local File Inclusion (LFI)": {
            "patterns": [r"\.\./", r"\.\.%2f", r"php://", r"expect://", r"file://", r"/etc/passwd"],
            "vectors": ["Path Traversal", "Wrapper Bypass", "Null Byte Injection"],
            "mitre_id": "T1005",
            "mitre_tactic": "Collection",
            "severity": "High"
        },
        "Server-Side Request Forgery (SSRF)": {
            "patterns": [r"localhost", r"127\.0\.0\.1", r"169\.254\.169\.254", r"metadata\.google", r"api\.internal"],
            "vectors": ["Internal Pivot", "Cloud Metadata", "Port Scanning"],
            "mitre_id": "T1133",
            "mitre_tactic": "Discovery",
            "severity": "High"
        },
        "XML External Entity (XXE)": {
            "patterns": [r"<!DOCTYPE", r"<!ENTITY", r"xxe", r"xml.*external", r"SYSTEM"],
            "vectors": ["File Disclosure", "SSRF", "Denial of Service"],
            "mitre_id": "T1127",
            "mitre_tactic": "Defense Evasion",
            "severity": "High"
        },
        "Path Traversal": {
            "patterns": [r"\.\./", r"\.\.\\", r"%2e%2e", r"\.\.%2f"],
            "vectors": ["Absolute Path", "Relative Path", "Encoded"],
            "mitre_id": "T1006",
            "mitre_tactic": "Defense Evasion",
            "severity": "Medium"
        },
        "NoSQL Injection": {
            "patterns": [r"\$ne", r"\$gt", r"\$where", r"\$regex", r"sleep\("],
            "vectors": ["Operator Injection", "JavaScript Injection"],
            "mitre_id": "T1190",
            "mitre_tactic": "Initial Access",
            "severity": "High"
        }
    }
    
    @classmethod
    def analyze(cls, payload: str) -> Dict[str, Any]:
        if not payload:
            return {
                "type": "Unknown",
                "vectors": [],
                "mitre_id": "N/A",
                "mitre_tactic": "N/A",
                "severity": "Low",
                "confidence": 0
            }
        
        payload_lower = payload.lower()
        
        for vuln_type, info in cls.PATTERNS.items():
            for pattern in info["patterns"]:
                if re.search(pattern, payload_lower, re.I):
                    return {
                        "type": vuln_type,
                        "vectors": info["vectors"][:3],
                        "mitre_id": info["mitre_id"],
                        "mitre_tactic": info["mitre_tactic"],
                        "severity": info["severity"],
                        "confidence": 0.85
                    }
        
        return {
            "type": "Unknown",
            "vectors": ["Manual Analysis Required"],
            "mitre_id": "N/A",
            "mitre_tactic": "N/A",
            "severity": "Medium",
            "confidence": 0.3
        }

# ==================== Tech Stack Detector ====================
class TechStackDetector:
    """Advanced technology stack detection"""
    
    PATTERNS = {
        "PHP": [r"\.php", r"wp-content", r"X-Powered-By:\s*PHP", r"PHPSESSID"],
        "Node.js": [r":3000", r"express", r"node\.js", r"npm", r"X-Powered-By:\s*Express"],
        "ASP.NET": [r"\.aspx", r"ASP\.NET", r"X-AspNet-Version", r"__VIEWSTATE"],
        "Java": [r"\.jsp", r"tomcat", r"java", r"servlet", r"JSESSIONID"],
        "Python": [r"django", r"flask", r"python", r"gunicorn", r"wsgi"],
        "WordPress": [r"wp-content", r"wp-includes", r"wordpress", r"/wp-json/"],
        "Drupal": [r"drupal", r"sites/default"],
        "Joomla": [r"joomla", r"media/system"],
        "Ruby on Rails": [r"\.rb", r"rails", r"ruby"],
        "Go": [r"\.go", r"goroutine"],
        "Rust": [r"\.rs", r"cargo"],
    }
    
    @classmethod
    def detect(cls, data: Dict) -> List[str]:
        text = json.dumps(data).lower()
        detected = []
        
        for tech, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern.lower(), text, re.I):
                    detected.append(tech)
                    break
        
        return detected[:5] or ["Generic Web Application"]

# ==================== Athena Core Engine ====================
class AthenaUltimate:
    """The Ultimate Vulnerability Intelligence Engine"""
    
    def __init__(self):
        config.cache_dir.mkdir(exist_ok=True)
        config.reports_dir.mkdir(exist_ok=True)
        
        self.cache = self._load_cache()
        self.llm_queue = Queue()
        self.vulnerability_queue = Queue()
        self.stats = {
            "total_processed": 0,
            "cache_hits": 0,
            "llm_calls": 0,
            "start_time": datetime.now()
        }
        
        # Setup Redis broadcaster
        self.broadcaster = self._setup_broadcaster()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║  🦾 ATHENA ULTIMATE - Initialized                          ║
║  📡 LLM Engine: Ollama ({})                                ║
║  💾 Cache: {} entries                                       ║
║  📡 Broadcaster: {}                                        ║
╚══════════════════════════════════════════════════════════════╝
""".format(config.llm_model, len(self.cache), "Active" if self.broadcaster else "Disabled"))
    
    def _load_cache(self) -> Dict:
        if config.cache_file.exists():
            try:
                with open(config.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        with open(config.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, indent=2)
    
    def _setup_broadcaster(self):
        if REDIS_AVAILABLE:
            try:
                r = redis.Redis(host=config.redis_host, port=config.redis_port, decode_responses=True)
                r.ping()
                return r
            except:
                return None
        return None
    
    def _generate_cache_key(self, vuln_type: str, payload: str, tech: str) -> str:
        """Generate unique cache key for vulnerability"""
        payload_hash = hashlib.md5(payload.encode()).hexdigest()[:12]
        return f"{vuln_type}_{tech}_{payload_hash}"
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama LLM with retry logic"""
        payload = {
            "model": config.llm_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": config.llm_temp}
        }
        
        for attempt in range(3):
            try:
                resp = requests.post(config.llm_url, json=payload, timeout=120)
                return resp.json().get('response', '')
            except Exception as e:
                if attempt == 2:
                    return f"LLM Error: {e}"
                time.sleep(1)
        return "LLM Error: Max retries exceeded"
    
    def get_remediation(self, vuln: Dict, tech: str, analysis: Dict) -> Dict:
        """Get AI-powered remediation with caching"""
        
        vuln_type = vuln.get('vulnerability_type', vuln.get('type', 'Unknown'))
        payload = vuln.get('payload', '')
        cache_key = self._generate_cache_key(vuln_type, payload, tech)
        
        # Check cache
        if cache_key in self.cache:
            self.stats['cache_hits'] += 1
            return self.cache[cache_key]
        
        self.stats['llm_calls'] += 1
        
        # Build prompt for LLM
        prompt = f"""
You are a senior security expert. Provide remediation for this vulnerability:

VULNERABILITY DETAILS:
- Type: {vuln_type}
- Technology: {tech}
- Target: {vuln.get('target_url', vuln.get('endpoint', 'N/A'))}
- Payload: {payload[:500]}
- Attack Classification: {analysis['type']}
- MITRE ATT&CK: {analysis['mitre_id']} - {analysis['mitre_tactic']}

Provide a COMPLETE remediation plan in JSON format with:
{{
    "steps": ["step1", "step2", "step3", "step4"],
    "code_fix": "Complete code example in {tech} with proper security measures",
    "waf_rule": "ModSecurity/Cloudflare rule to block this attack",
    "monitoring": "SIEM query to detect similar attacks",
    "cvss_reduction": "CVSS score reduction (e.g., 8.5 → 4.2)",
    "mitre_mitigation": "MITRE ATT&CK mitigation technique ID"
}}

Make the code fix PRODUCTION-READY and specific to {tech}.
"""
        
        response = self._call_ollama(prompt)
        
        # Try to parse JSON from response
        try:
            # Extract JSON if wrapped in markdown
            response_clean = response.strip()
            if response_clean.startswith('```json'):
                response_clean = response_clean[7:]
            if response_clean.endswith('```'):
                response_clean = response_clean[:-3]
            fix = json.loads(response_clean)
        except:
            # Fallback remediation
            fix = {
                "steps": [
                    "Implement input validation using allowlist approach",
                    "Use parameterized queries/prepared statements",
                    f"Apply {tech}-specific security headers",
                    "Enable WAF rules for this attack pattern"
                ],
                "code_fix": f"# Implement proper security controls for {tech}",
                "waf_rule": "SecRule ARGS \"@validateSchema\" \"id:1001,phase:2,deny,status:403\"",
                "monitoring": 'index=* sourcetype=access_log "403" OR "500"',
                "cvss_reduction": "High → Medium",
                "mitre_mitigation": "M1038"
            }
        
        # Cache and return
        self.cache[cache_key] = fix
        self._save_cache()
        
        return fix
    
    def process_vulnerability(self, vuln: Dict, tech_stack: List[str]) -> Dict:
        """Process single vulnerability"""
        
        self.stats['total_processed'] += 1
        
        # Analyze payload
        payload = vuln.get('payload', '')
        analysis = PayloadAnalyzer.analyze(payload)
        
        # Determine severity
        severity = analysis.get('severity', vuln.get('severity', 'Medium'))
        
        # Get remediation
        tech = tech_stack[0] if tech_stack else "Generic"
        fix = self.get_remediation(vuln, tech, analysis)
        
        # Build result
        result = {
            "timestamp": datetime.now().isoformat(),
            "vulnerability_type": vuln.get('vulnerability_type', vuln.get('type', 'Unknown')),
            "severity": severity,
            "target": vuln.get('target_url', vuln.get('endpoint', 'Unknown')),
            "payload": payload[:200],
            "attack_type": analysis['type'],
            "attack_vectors": analysis['vectors'],
            "mitre_id": analysis['mitre_id'],
            "mitre_tactic": analysis['mitre_tactic'],
            "tech_stack": tech_stack,
            "remediation_steps": fix.get('steps', []),
            "code_fix": fix.get('code_fix', ''),
            "waf_rule": fix.get('waf_rule', ''),
            "monitoring": fix.get('monitoring', ''),
            "cache_hit": cache_key in self.cache if 'cache_key' in dir() else False
        }
        
        # Broadcast to dashboard
        if self.broadcaster:
            try:
                self.broadcaster.publish("athena:vulnerability", json.dumps(result))
                self.broadcaster.lpush("athena:history", json.dumps(result))
                self.broadcaster.ltrim("athena:history", 0, config.max_history)
            except:
                pass
        
        return result
    
    def process_report(self, report_path: Path) -> List[Dict]:
        """Process complete Ares report"""
        
        print(f"\n📄 Processing: {report_path.name}")
        
        with open(report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Detect tech stack
        tech_stack = TechStackDetector.detect(data)
        print(f"🔧 Tech Stack: {', '.join(tech_stack)}")
        
        # Get vulnerabilities
        findings = data.get('findings', data.get('vulnerabilities', []))
        if not findings:
            print("✅ No vulnerabilities found")
            return []
        
        print(f"🎯 Found {len(findings)} vulnerabilities")
        print("-" * 50)
        
        results = []
        for i, vuln in enumerate(findings, 1):
            print(f"  {i}. Processing {vuln.get('vulnerability_type', vuln.get('type', 'Unknown'))}...")
            result = self.process_vulnerability(vuln, tech_stack)
            results.append(result)
            
            # Show result
            status = "💾 Cached" if result.get('cache_hit') else "🧠 LLM"
            print(f"     → {result['attack_type']} [{result['severity']}] ({status})")
        
        print("-" * 50)
        print(f"✅ Processed {len(results)} vulnerabilities")
        print(f"💾 Cache hits: {self.stats['cache_hits']}")
        print(f"🧠 LLM calls: {self.stats['llm_calls']}")
        
        return results
    
    def get_latest_report(self) -> Optional[Path]:
        """Get most recent report from reports directory"""
        reports = list(config.reports_dir.glob("*.json"))
        if not reports:
            return None
        return max(reports, key=lambda p: p.stat().st_mtime)
    
    def generate_report(self, results: List[Dict], output_file: str = None) -> str:
        """Generate Markdown report"""
        
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"athena_report_{timestamp}.md"
        
        lines = []
        lines.append("# 🛡️ ATHENA ULTIMATE - Vulnerability Intelligence Report\n")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"**Vulnerabilities:** {len(results)}\n")
        lines.append(f"**Cache Efficiency:** {self.stats['cache_hits']}/{self.stats['total_processed']} ({self.stats['cache_hits']/max(1,self.stats['total_processed'])*100:.1f}%)\n")
        lines.append("---\n")
        
        # Statistics table
        severity_counts = Counter(r['severity'] for r in results)
        attack_counts = Counter(r['attack_type'] for r in results)
        
        lines.append("## 📊 Executive Summary\n")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Vulnerabilities | {len(results)} |")
        for sev, count in severity_counts.items():
            lines.append(f"| {sev} Severity | {count} |")
        lines.append(f"| Unique Attack Types | {len(attack_counts)} |")
        lines.append(f"| Cache Efficiency | {self.stats['cache_hits']/max(1,self.stats['total_processed'])*100:.1f}% |")
        lines.append("\n")
        
        # Attack types distribution
        lines.append("## 🎯 Attack Types Distribution\n")
        for attack, count in attack_counts.most_common():
            lines.append(f"- **{attack}**: {count}")
        lines.append("\n")
        
        # Detailed findings
        lines.append("## 🔍 Detailed Findings\n")
        
        for i, result in enumerate(results, 1):
            severity_icon = "🔴" if result['severity'] == "Critical" else "🟠" if result['severity'] == "High" else "🟡" if result['severity'] == "Medium" else "🟢"
            
            lines.append(f"### {severity_icon} {i}. {result['vulnerability_type']}\n")
            lines.append(f"| Field | Value |")
            lines.append(f"|-------|-------|")
            lines.append(f"| **Severity** | {result['severity']} |")
            lines.append(f"| **Target** | `{result['target']}` |")
            lines.append(f"| **Attack Type** | {result['attack_type']} |")
            lines.append(f"| **MITRE ATT&CK** | {result['mitre_id']} - {result['mitre_tactic']} |")
            lines.append(f"| **Payload** | `{result['payload'][:100]}...` |")
            lines.append(f"| **Cache** | {'✅ Hit' if result['cache_hit'] else '🧠 LLM Generated'} |")
            lines.append("\n")
            
            lines.append("#### 🔒 Remediation Steps\n")
            for step in result.get('remediation_steps', []):
                lines.append(f"{step}\n")
            
            if result.get('code_fix'):
                lines.append("#### 💻 Code Fix\n")
                lines.append(f"```{result['tech_stack'][0] if result['tech_stack'] else 'python'}\n{result['code_fix']}\n```\n")
            
            if result.get('waf_rule'):
                lines.append("#### 🛡️ WAF Rule\n")
                lines.append(f"```nginx\n{result['waf_rule']}\n```\n")
            
            lines.append("---\n")
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"\n📄 Report saved: {output_file}")
        return output_file
    
    def get_stats(self) -> Dict:
        """Get engine statistics"""
        runtime = (datetime.now() - self.stats['start_time']).total_seconds()
        return {
            "total_processed": self.stats['total_processed'],
            "cache_hits": self.stats['cache_hits'],
            "llm_calls": self.stats['llm_calls'],
            "cache_efficiency": self.stats['cache_hits'] / max(1, self.stats['total_processed']) * 100,
            "runtime_seconds": runtime,
            "vulnerabilities_per_second": self.stats['total_processed'] / max(1, runtime)
        }

# ==================== Dashboard ====================
class AthenaDashboard:
    """Real-time vulnerability dashboard"""
    
    def __init__(self, engine: AthenaUltimate):
        self.engine = engine
        self.vulnerabilities = []
        self.app = None
        
        if not DASH_AVAILABLE:
            print("❌ Dash not available. Install with: pip install dash plotly pandas")
            return
        
        self._setup_dashboard()
    
    def _setup_dashboard(self):
        """Setup Dash app"""
        
        self.app = dash.Dash(__name__, title="ATHENA Ultimate Dashboard")
        
        self.app.layout = html.Div([
            # Header
            html.Div([
                html.H1("🛡️ ATHENA ULTIMATE", style={
                    'fontSize': '48px', 'fontWeight': '800',
                    'background': 'linear-gradient(135deg, #00ff41, #00ccff)',
                    'WebkitBackgroundClip': 'text', 'WebkitTextFillColor': 'transparent',
                    'textAlign': 'center', 'marginBottom': '10px'
                }),
                html.P("AI-Powered Vulnerability Intelligence Platform", 
                       style={'textAlign': 'center', 'color': '#888'}),
                html.Div([
                    html.Span("●", style={'color': '#00ff41', 'marginRight': '5px'}),
                    html.Span("LIVE MONITORING ACTIVE", style={'color': '#00ff41', 'fontSize': '12px'})
                ], style={'textAlign': 'center', 'marginTop': '10px'})
            ], style={'padding': '30px', 'borderBottom': '1px solid #333'}),
            
            # Stats Row
            html.Div(id='stats-row', style={
                'display': 'grid', 'gridTemplateColumns': 'repeat(5, 1fr)',
                'gap': '20px', 'padding': '30px'
            }),
            
            # Charts Row
            html.Div([
                html.Div([
                    html.H3("Severity Distribution", style={'marginBottom': '20px'}),
                    dcc.Graph(id='severity-chart', config={'displayModeBar': False})
                ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '15px'}),
                
                html.Div([
                    html.H3("Top Attack Types", style={'marginBottom': '20px'}),
                    dcc.Graph(id='attack-chart', config={'displayModeBar': False})
                ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '15px'})
            ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px', 'padding': '0 30px 30px 30px'}),
            
            # Timeline
            html.Div([
                html.H3("Vulnerability Timeline", style={'marginBottom': '20px'}),
                dcc.Graph(id='timeline-chart', config={'displayModeBar': False})
            ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '15px', 'margin': '0 30px 30px 30px'}),
            
            # Live Table
            html.Div([
                html.H3("Recent Vulnerabilities", style={'marginBottom': '20px'}),
                html.Div(id='vuln-table')
            ], style={'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '15px', 'margin': '0 30px 30px 30px'}),
            
            dcc.Interval(id='interval', interval=1000)
        ], style={'backgroundColor': '#0a0a0a', 'color': '#fff', 'minHeight': '100vh'})
        
        # Callbacks
        @self.app.callback(
            [Output('stats-row', 'children'),
             Output('severity-chart', 'figure'),
             Output('attack-chart', 'figure'),
             Output('timeline-chart', 'figure'),
             Output('vuln-table', 'children')],
            Input('interval', 'n_intervals')
        )
        def update(n):
            # Get data from Redis if available
            if self.engine.broadcaster:
                try:
                    history = self.engine.broadcaster.lrange("athena:history", 0, 99)
                    self.vulnerabilities = [json.loads(h) for h in history]
                except:
                    pass
            
            if not self.vulnerabilities:
                return self._empty_stats(), self._empty_fig(), self._empty_fig(), self._empty_fig(), "No vulnerabilities detected"
            
            df = pd.DataFrame(self.vulnerabilities)
            
            # Stats
            total = len(df)
            critical = len(df[df['severity'] == 'Critical']) if 'severity' in df.columns else 0
            high = len(df[df['severity'] == 'High']) if 'severity' in df.columns else 0
            unique_targets = df['target'].nunique() if 'target' in df.columns else 0
            cache_hits = df['cache_hit'].sum() if 'cache_hit' in df.columns else 0
            
            stats = html.Div([
                self._stat_card("Total Vulnerabilities", str(total), "🔍"),
                self._stat_card("Critical", str(critical), "🔴", "#ff4444"),
                self._stat_card("High", str(high), "🟠", "#ffaa44"),
                self._stat_card("Unique Targets", str(unique_targets), "🌐"),
                self._stat_card("Cache Hits", f"{cache_hits}/{total}", "💾")
            ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(5, 1fr)', 'gap': '20px'})
            
            # Severity chart
            if 'severity' in df.columns:
                severity_counts = df['severity'].value_counts()
                severity_fig = go.Figure(data=[go.Pie(
                    labels=severity_counts.index, values=severity_counts.values,
                    hole=0.4, marker=dict(colors=['#ff4444', '#ffaa44', '#44ff44', '#888'])
                )])
                severity_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=350)
            else:
                severity_fig = self._empty_fig()
            
            # Attack chart
            if 'attack_type' in df.columns:
                attack_counts = df['attack_type'].value_counts().head(8)
                attack_fig = go.Figure(data=[go.Bar(
                    x=attack_counts.values, y=attack_counts.index, orientation='h',
                    marker=dict(color=attack_counts.values, colorscale='Viridis')
                )])
                attack_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=350)
            else:
                attack_fig = self._empty_fig()
            
            # Timeline
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df_sorted = df.sort_values('timestamp')
                timeline_fig = go.Figure()
                for sev in ['Critical', 'High', 'Medium', 'Low']:
                    sev_df = df_sorted[df_sorted['severity'] == sev]
                    if not sev_df.empty:
                        timeline_fig.add_trace(go.Scatter(
                            x=sev_df['timestamp'], y=range(len(sev_df)),
                            mode='lines+markers', name=sev
                        ))
                timeline_fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=350)
            else:
                timeline_fig = self._empty_fig()
            
            # Table
            table_rows = []
            for v in self.vulnerabilities[:20]:
                severity_color = '#ff4444' if v.get('severity') in ['Critical', 'High'] else '#ffaa44' if v.get('severity') == 'Medium' else '#44ff44'
                table_rows.append(html.Tr([
                    html.Td(v.get('timestamp', '')[-8:], style={'color': '#888'}),
                    html.Td(v.get('vulnerability_type', '')[:35]),
                    html.Td(v.get('severity', ''), style={'color': severity_color, 'fontWeight': 'bold'}),
                    html.Td(v.get('attack_type', '')[:25], style={'color': '#44aaff'}),
                    html.Td(v.get('target', '')[:45]),
                    html.Td('💾' if v.get('cache_hit') else '🧠')
                ]))
            
            vuln_table = html.Table([
                html.Thead(html.Tr([
                    html.Th("Time"), html.Th("Vulnerability"), html.Th("Severity"),
                    html.Th("Attack Type"), html.Th("Target"), html.Th("Cache")
                ])),
                html.Tbody(table_rows)
            ], style={'width': '100%', 'borderCollapse': 'collapse'})
            
            return stats, severity_fig, attack_fig, timeline_fig, vuln_table
        
    def _stat_card(self, label: str, value: str, icon: str, color: str = "#00ff41"):
        return html.Div([
            html.Div(icon, style={'fontSize': '30px', 'marginBottom': '10px'}),
            html.Div(value, style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color}),
            html.Div(label, style={'color': '#888', 'fontSize': '12px'})
        ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#1a1a1a', 'borderRadius': '15px'})
    
    def _empty_stats(self):
        return html.Div([
            self._stat_card("Total Vulnerabilities", "0", "🔍"),
            self._stat_card("Critical", "0", "🔴"),
            self._stat_card("High", "0", "🟠"),
            self._stat_card("Unique Targets", "0", "🌐"),
            self._stat_card("Cache Hits", "0/0", "💾")
        ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(5, 1fr)', 'gap': '20px'})
    
    def _empty_fig(self):
        fig = go.Figure()
        fig.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', height=350)
        fig.add_annotation(text="Waiting for data...", showarrow=False)
        return fig
    
    def run(self):
        if self.app:
            print(f"\n🌐 Dashboard: http://{config.dashboard_host}:{config.dashboard_port}")
            if config.auto_open_browser:
                webbrowser.open(f"http://localhost:{config.dashboard_port}")
            self.app.run(debug=False, host=config.dashboard_host, port=config.dashboard_port)

# ==================== Main Application ====================
class AthenaUltimateApp:
    """Complete Athena Ultimate Application"""
    
    def __init__(self):
        self.engine = AthenaUltimate()
        self.dashboard = None
        self.dashboard_thread = None
    
    def run_cli_mode(self, report_path: Path = None):
        """Run in CLI mode only"""
        
        # Get report
        if not report_path:
            report_path = self.engine.get_latest_report()
            if not report_path:
                print("❌ No reports found in 'reports/' directory")
                return
        
        # Process report
        results = self.engine.process_report(report_path)
        
        if results:
            # Generate report
            report_file = self.engine.generate_report(results)
            
            # Print stats
            stats = self.engine.get_stats()
            print("\n" + "="*50)
            print("📊 ATHENA ULTIMATE - Session Statistics")
            print("="*50)
            print(f"Total Processed: {stats['total_processed']}")
            print(f"Cache Hits: {stats['cache_hits']} ({stats['cache_efficiency']:.1f}%)")
            print(f"LLM Calls: {stats['llm_calls']}")
            print(f"Runtime: {stats['runtime_seconds']:.2f} seconds")
            print(f"Speed: {stats['vulnerabilities_per_second']:.2f} vulns/sec")
            print("="*50)
    
    def run_dashboard_mode(self, report_path: Path = None):
        """Run with dashboard"""
        
        # Start dashboard in thread
        self.dashboard = AthenaDashboard(self.engine)
        
        def start_dashboard():
            self.dashboard.run()
        
        self.dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
        self.dashboard_thread.start()
        
        print("\n🚀 ATHENA ULTIMATE is running...")
        print("📡 Dashboard will open automatically")
        print("⚡ Processing vulnerabilities...\n")
        
        # Process initial report
        if report_path:
            self.engine.process_report(report_path)
        else:
            # Watch for new reports
            print("🔍 Waiting for new reports in 'reports/' directory...")
            print("   Place JSON reports in the 'reports' folder and press Enter")
            
            while True:
                input("\n📁 Press Enter to check for new reports (or Ctrl+C to exit)...")
                report_path = self.engine.get_latest_report()
                if report_path:
                    self.engine.process_report(report_path)
                else:
                    print("   No reports found. Place JSON files in 'reports/'")
    
    def run_interactive(self):
        """Interactive mode"""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   🦾 ATHENA ULTIMATE - Vulnerability Intelligence Platform      ║
║                                                                  ║
║   Choose mode:                                                   ║
║     1. CLI Mode - Process report and save                       ║
║     2. Dashboard Mode - Live dashboard + real-time monitoring   ║
║     3. Watch Mode - Monitor reports folder for new files        ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
""")
        
        choice = input("Select mode (1/2/3): ").strip()
        
        if choice == "1":
            report_path = input("Enter report filename (or press Enter for latest): ").strip()
            if report_path:
                self.run_cli_mode(config.reports_dir / report_path)
            else:
                self.run_cli_mode()
        
        elif choice == "2":
            self.run_dashboard_mode()
        
        elif choice == "3":
            print("\n📁 Watching 'reports/' directory...")
            print("   Press Ctrl+C to stop\n")
            import time
            last_processed = None
            while True:
                try:
                    latest = self.engine.get_latest_report()
                    if latest and latest != last_processed:
                        print(f"\n📄 New report detected: {latest.name}")
                        self.engine.process_report(latest)
                        last_processed = latest
                    time.sleep(5)
                except KeyboardInterrupt:
                    print("\n\n👋 Shutting down...")
                    break
        
        else:
            print("Invalid choice")

# ==================== Entry Point ====================
if __name__ == "__main__":
    app = AthenaUltimateApp()
    app.run_interactive()