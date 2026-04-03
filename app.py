# app.py (الملف الرئيسي)
from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import json
import uuid
import os
from pathlib import Path

app = Flask(__name__)

# مجلد للتقارير
REPORTS_DIR = Path('/home/yourusername/reports')
REPORTS_DIR.mkdir(exist_ok=True)

# تخزين حالة الفحوصات
scans = {}

def run_both_scanners(target_url, scan_id):
    """تشغيل nu_ares ثم athena"""
    try:
        scans[scan_id]['status'] = 'running_nu_ares'
        
        # تشغيل Nu Ares Scanner
        cmd = ['python3', '/home/yourusername/nu_ares.py', '-u', target_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        scans[scan_id]['status'] = 'running_athena'
        
        # البحث عن أحدث تقرير من Nu Ares
        reports = list(Path('/home/yourusername/reports').glob('*.json'))
        if reports:
            latest = max(reports, key=lambda p: p.stat().st_mtime)
            
            # تشغيل Athena Ultimate
            athena_cmd = ['python3', '/home/yourusername/athena_ultimate.py', '--cli', str(latest)]
            athena_result = subprocess.run(athena_cmd, capture_output=True, text=True)
            
            # قراءة النتيجة
            with open(latest, 'r') as f:
                report_data = json.load(f)
            
            scans[scan_id] = {
                'status': 'complete',
                'result': report_data,
                'report_file': str(latest)
            }
        else:
            scans[scan_id]['status'] = 'error'
            scans[scan_id]['message'] = 'No report generated'
            
    except Exception as e:
        scans[scan_id]['status'] = 'error'
        scans[scan_id]['message'] = str(e)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Nu Ares + Athena - Security Scanner</title>
        <style>
            body {
                background: linear-gradient(135deg, #0a0a0a, #1a1a2e);
                font-family: Arial, sans-serif;
                color: white;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 20px;
            }
            input, button {
                width: 100%;
                padding: 15px;
                margin: 10px 0;
                border-radius: 10px;
                border: none;
                font-size: 16px;
            }
            input {
                background: rgba(0,0,0,0.5);
                color: white;
                border: 1px solid #00ff88;
            }
            button {
                background: linear-gradient(90deg, #00ff88, #00ccff);
                color: black;
                font-weight: bold;
                cursor: pointer;
            }
            .status {
                margin-top: 20px;
                padding: 15px;
                background: rgba(0,0,0,0.5);
                border-radius: 10px;
            }
            .vuln {
                border-left: 4px solid #ff4444;
                padding: 10px;
                margin: 10px 0;
                background: rgba(255,68,68,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛡️ Nu Ares + Athena Ultimate</h1>
            <p>AI-Powered Web Security Scanner</p>
            
            <input type="text" id="target" placeholder="Enter target URL (e.g., https://testphp.vulnweb.com)">
            <button onclick="startScan()">🚀 Start Scan</button>
            
            <div id="status" class="status" style="display:none;">
                <div id="status-text">Starting...</div>
                <div id="progress">⏳</div>
            </div>
            
            <div id="results"></div>
        </div>
        
        <script>
            let scanId = null;
            
            async function startScan() {
                const target = document.getElementById('target').value;
                if (!target) {
                    alert('Please enter a URL');
                    return;
                }
                
                document.getElementById('status').style.display = 'block';
                document.getElementById('results').innerHTML = '';
                
                const response = await fetch('/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target})
                });
                
                const data = await response.json();
                scanId = data.scan_id;
                checkStatus();
            }
            
            async function checkStatus() {
                const response = await fetch(`/status/${scanId}`);
                const data = await response.json();
                
                if (data.status === 'running_nu_ares') {
                    document.getElementById('status-text').innerHTML = '🔍 Scanning with Nu Ares...';
                    document.getElementById('progress').innerHTML = '⏳ This may take a few minutes';
                } else if (data.status === 'running_athena') {
                    document.getElementById('status-text').innerHTML = '🧠 Analyzing with Athena AI...';
                } else if (data.status === 'complete') {
                    document.getElementById('status-text').innerHTML = '✅ Scan Complete!';
                    document.getElementById('progress').innerHTML = '🎉';
                    showResults(data.result);
                    return;
                } else if (data.status === 'error') {
                    document.getElementById('status-text').innerHTML = '❌ Error: ' + data.message;
                    return;
                }
                
                setTimeout(checkStatus, 2000);
            }
            
            function showResults(report) {
                let html = '<h2>📊 Scan Results</h2>';
                const vulns = report.vulnerabilities || report.findings || [];
                
                if (vulns.length === 0) {
                    html += '<p>✅ No vulnerabilities found!</p>';
                } else {
                    html += `<p>Found ${vulns.length} vulnerabilities:</p>`;
                    for (const v of vulns) {
                        html += `
                            <div class="vuln">
                                <strong>${v.vulnerability_type || v.type || 'Unknown'}</strong><br>
                                📍 ${v.target_url || v.url}<br>
                                🔧 Parameter: ${v.parameter || 'N/A'}<br>
                                ⚠️ Severity: ${v.severity || 'Medium'}
                            </div>
                        `;
                    }
                }
                
                document.getElementById('results').innerHTML = html;
            }
        </script>
    </body>
    </html>
    '''

@app.route('/scan', methods=['POST'])
def start_scan():
    data = request.json
    scan_id = str(uuid.uuid4())[:8]
    scans[scan_id] = {'status': 'starting'}
    
    thread = threading.Thread(target=run_both_scanners, args=(data['target'], scan_id))
    thread.start()
    
    return jsonify({'scan_id': scan_id})

@app.route('/status/<scan_id>')
def get_status(scan_id):
    return jsonify(scans.get(scan_id, {'status': 'unknown'}))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)