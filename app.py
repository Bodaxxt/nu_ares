from flask import Flask, request, jsonify, render_template_string
import json
import time

app = Flask(__name__)

# الصفحة الرئيسية كاملة
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nu Ares Security Scanner</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #0f0f23 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            min-height: 100vh;
            color: #fff;
        }
        
        .container {
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .header h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, #00ff88, #00ccff, #0066ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }
        
        .header p {
            color: #888;
            font-size: 1.1rem;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 30px;
        }
        
        .input-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #00ff88;
            font-weight: 500;
        }
        
        input, select {
            width: 100%;
            padding: 14px 16px;
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            color: white;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #00ff88;
            box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
        }
        
        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(90deg, #00ff88, #00ccff);
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: bold;
            color: #0a0a0a;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0, 255, 136, 0.3);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .status-card {
            display: none;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
            text-align: center;
        }
        
        .loader {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 3px solid rgba(0, 255, 136, 0.3);
            border-top-color: #00ff88;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 15px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .results-card {
            margin-top: 30px;
        }
        
        .vuln-item {
            background: rgba(0, 0, 0, 0.3);
            border-left: 4px solid #ff4444;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 12px;
            transition: all 0.3s;
        }
        
        .vuln-item:hover {
            background: rgba(0, 0, 0, 0.5);
            transform: translateX(5px);
        }
        
        .vuln-title {
            font-size: 1.1rem;
            font-weight: bold;
            margin-bottom: 8px;
        }
        
        .vuln-detail {
            font-size: 0.85rem;
            color: #aaa;
            margin-top: 5px;
        }
        
        .severity-critical { border-left-color: #ff0044; }
        .severity-high { border-left-color: #ff6644; }
        .severity-medium { border-left-color: #ffcc44; }
        .severity-low { border-left-color: #44ff44; }
        
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-left: 10px;
        }
        
        .badge-critical { background: #ff0044; color: white; }
        .badge-high { background: #ff6644; color: white; }
        .badge-medium { background: #ffcc44; color: black; }
        .badge-low { background: #44ff44; color: black; }
        
        .note {
            background: rgba(255, 255, 0, 0.1);
            border-radius: 10px;
            padding: 15px;
            font-size: 0.85rem;
            color: #ffcc44;
            text-align: center;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            color: #666;
            font-size: 0.8rem;
        }
        
        @media (max-width: 600px) {
            .container { padding: 20px 15px; }
            .header h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ Nu Ares Scanner</h1>
            <p>Enterprise Web Application Security Scanner</p>
        </div>
        
        <div class="card">
            <div class="input-group">
                <label>🎯 Target URL</label>
                <input type="text" id="target" placeholder="https://example.com" value="http://testphp.vulnweb.com">
            </div>
            
            <div class="input-group">
                <label>⚡ Scan Speed</label>
                <select id="threads">
                    <option value="10">🐢 Slow (10 threads) - More thorough</option>
                    <option value="30" selected>⚡ Normal (30 threads)</option>
                    <option value="50">🚀 Fast (50 threads) - Quick scan</option>
                </select>
            </div>
            
            <button onclick="startScan()">🚀 Start Security Scan</button>
        </div>
        
        <div id="statusCard" class="status-card">
            <div class="loader"></div>
            <div id="statusText">Initializing scan...</div>
        </div>
        
        <div id="resultsCard" class="results-card"></div>
        
        <div class="note">
            ⚠️ <strong>Important:</strong> Use this tool only on websites you own or have explicit permission to test.
            Unauthorized scanning may be illegal. For educational purposes only.
        </div>
        
        <div class="footer">
            Nu Ares v37.0 | AI-Powered Security Scanner | Made with 🛡️ for security researchers
        </div>
    </div>
    
    <script>
        let scanId = null;
        
        async function startScan() {
            const target = document.getElementById('target').value;
            const threads = document.getElementById('threads').value;
            
            if (!target) {
                alert('Please enter a target URL');
                return;
            }
            
            // Show status card
            const statusCard = document.getElementById('statusCard');
            const resultsCard = document.getElementById('resultsCard');
            statusCard.style.display = 'block';
            resultsCard.innerHTML = '';
            document.getElementById('statusText').innerHTML = '🚀 Starting scan on ' + target + '...';
            
            try {
                const response = await fetch('/api/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        target: target, 
                        threads: parseInt(threads) 
                    })
                });
                
                const data = await response.json();
                scanId = data.scan_id;
                
                checkStatus();
            } catch (error) {
                document.getElementById('statusText').innerHTML = '❌ Error: ' + error.message;
            }
        }
        
        async function checkStatus() {
            try {
                const response = await fetch('/api/status/' + scanId);
                const data = await response.json();
                
                if (data.status === 'running') {
                    document.getElementById('statusText').innerHTML = '🔍 Scanning... ' + (data.progress || 0) + '% - Please wait, this may take 1-2 minutes';
                    setTimeout(checkStatus, 2000);
                } else if (data.status === 'complete') {
                    document.getElementById('statusText').innerHTML = '✅ Scan Complete!';
                    displayResults(data.result);
                } else if (data.status === 'error') {
                    document.getElementById('statusText').innerHTML = '❌ Error: ' + data.message;
                } else {
                    document.getElementById('statusText').innerHTML = '⏳ Waiting for scan to start...';
                    setTimeout(checkStatus, 2000);
                }
            } catch (error) {
                document.getElementById('statusText').innerHTML = '❌ Status error: ' + error.message;
            }
        }
        
        function displayResults(data) {
            const resultsCard = document.getElementById('resultsCard');
            let html = '<div class="card"><h2>📊 Scan Results</h2>';
            
            if (data.vulnerabilities && data.vulnerabilities.length > 0) {
                html += `<p style="margin-bottom: 15px;">🔍 Found ${data.vulnerabilities.length} potential vulnerabilities:</p>`;
                
                for (const v of data.vulnerabilities) {
                    let severityClass = 'severity-medium';
                    let badgeClass = 'badge-medium';
                    let severityText = v.severity || 'Medium';
                    
                    if (severityText.toLowerCase() === 'critical') {
                        severityClass = 'severity-critical';
                        badgeClass = 'badge-critical';
                    } else if (severityText.toLowerCase() === 'high') {
                        severityClass = 'severity-high';
                        badgeClass = 'badge-high';
                    } else if (severityText.toLowerCase() === 'low') {
                        severityClass = 'severity-low';
                        badgeClass = 'badge-low';
                    }
                    
                    html += `
                        <div class="vuln-item ${severityClass}">
                            <div class="vuln-title">
                                ${v.type || v.vulnerability_type || 'Unknown'}
                                <span class="badge ${badgeClass}">${severityText}</span>
                            </div>
                            <div class="vuln-detail">📍 ${v.url || v.target_url || 'N/A'}</div>
                            <div class="vuln-detail">🔧 Parameter: ${v.parameter || 'N/A'}</div>
                            <div class="vuln-detail">📊 Confidence: ${((v.confidence || 0.7) * 100).toFixed(0)}%</div>
                        </div>
                    `;
                }
            } else {
                html += '<p>✅ No vulnerabilities found! The target appears secure.</p>';
            }
            
            html += `<div class="note" style="margin-top: 20px;">
                📄 Report generated at ${new Date().toLocaleString()}<br>
                🛡️ Scan completed successfully
            </div>`;
            
            html += '</div>';
            resultsCard.innerHTML = html;
        }
    </script>
</body>
</html>
'''

# تخزين الفحوصات
scans = {}

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/scan', methods=['POST'])
def start_scan():
    try:
        data = request.get_json()
        target = data.get('target', '')
        scan_id = str(int(time.time()))
        
        # تقرير تجريبي للعرض
        scans[scan_id] = {
            'status': 'complete',
            'progress': 100,
            'result': {
                'vulnerabilities': [
                    {
                        'type': 'SQL Injection',
                        'url': target,
                        'parameter': 'id',
                        'severity': 'High',
                        'payload': "' OR '1'='1",
                        'confidence': 0.92
                    },
                    {
                        'type': 'Cross-Site Scripting (XSS)',
                        'url': target,
                        'parameter': 'search',
                        'severity': 'Medium',
                        'payload': '<script>alert(1)</script>',
                        'confidence': 0.85
                    },
                    {
                        'type': 'Local File Inclusion (LFI)',
                        'url': target,
                        'parameter': 'page',
                        'severity': 'High',
                        'payload': '../../etc/passwd',
                        'confidence': 0.78
                    },
                    {
                        'type': 'Command Injection',
                        'url': target,
                        'parameter': 'cmd',
                        'severity': 'Critical',
                        'payload': '; whoami',
                        'confidence': 0.71
                    }
                ],
                'total': 4,
                'scan_time': time.time()
            }
        }
        
        return jsonify({'scan_id': scan_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<scan_id>')
def get_status(scan_id):
    scan = scans.get(scan_id, {'status': 'running', 'progress': 50})
    return jsonify(scan)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
