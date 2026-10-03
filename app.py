from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

API_URL = "http://ip-api.com/json/"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP OSINT Tool</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg-primary: #0a0505;
            --bg-secondary: #140808;
            --bg-card: #1a0a0a;
            --bg-input: #1e0c0c;
            --border: #3d1414;
            --border-hover: #5a1e1e;
            --text-primary: #ffe8e8;
            --text-secondary: #b08080;
            --text-muted: #7a5555;
            --red-primary: #ef4444;
            --red-dark: #b91c1c;
            --red-light: #f87171;
            --red-glow: rgba(239, 68, 68, 0.4);
            --red-glow-strong: rgba(239, 68, 68, 0.6);
            --green: #10b981;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
            position: relative;
            overflow-x: hidden;
        }

        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(circle at 20% 20%, rgba(239, 68, 68, 0.18), transparent 45%),
                radial-gradient(circle at 80% 80%, rgba(185, 28, 28, 0.15), transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(120, 20, 20, 0.1), transparent 60%);
            z-index: -2;
            animation: pulse 6s ease-in-out infinite;
        }

        body::after {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(61, 20, 20, 0.4) 1px, transparent 1px),
                linear-gradient(90deg, rgba(61, 20, 20, 0.4) 1px, transparent 1px);
            background-size: 45px 45px;
            z-index: -1;
            mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
            -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 75%);
        }

        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.65; } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideIn { from { opacity: 0; transform: translateX(-10px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes slideDown { from { opacity: 0; transform: translateY(-20px); max-height: 0; } to { opacity: 1; transform: translateY(0); max-height: 200px; } }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes glowPulse { 0%, 100% { box-shadow: 0 0 25px var(--red-glow); } 50% { box-shadow: 0 0 45px var(--red-glow-strong); } }
        @keyframes markerPulse { 0% { transform: scale(1); opacity: 1; } 100% { transform: scale(3); opacity: 0; } }
        @keyframes alarmShake { 0%, 100% { transform: translateX(0); } 25% { transform: translateX(-3px); } 75% { transform: translateX(3px); } }
        @keyframes alarmGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.5), inset 0 0 20px rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.5); }
            50% { box-shadow: 0 0 40px rgba(239, 68, 68, 0.8), inset 0 0 30px rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.9); }
        }

        .container {
            width: 100%;
            max-width: 820px;
            background: rgba(20, 8, 8, 0.78);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 2.5rem;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), 0 0 60px rgba(239, 68, 68, 0.08), 0 0 0 1px rgba(255, 255, 255, 0.02) inset;
            animation: fadeInUp 0.6s ease-out;
            position: relative;
            overflow: hidden;
        }

        .container::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--red-primary), var(--red-light), transparent);
            opacity: 0.9;
            animation: glowPulse 3s ease-in-out infinite;
        }

        /* Uyarı banner */
        .alert-banner {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 1rem 1.25rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.18), rgba(185, 28, 28, 0.12));
            border: 1.5px solid rgba(239, 68, 68, 0.6);
            border-radius: 14px;
            animation: slideDown 0.5s ease-out, alarmGlow 2s ease-in-out infinite;
            position: relative;
            overflow: hidden;
        }

        .alert-banner::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.15), transparent);
            animation: shine 3s ease-in-out infinite;
        }

        @keyframes shine { 0% { left: -100%; } 100% { left: 100%; } }

        .alert-icon {
            width: 40px; height: 40px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--red-primary), var(--red-dark));
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            font-size: 1.3rem;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
            animation: alarmShake 0.6s ease-in-out 3;
        }

        .alert-text { flex: 1; }
        .alert-title { font-weight: 700; color: #fca5a5; font-size: 0.95rem; margin-bottom: 0.2rem; letter-spacing: 0.02em; }
        .alert-desc { font-size: 0.82rem; color: #d4a0a0; line-height: 1.4; }

        .alert-close {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            width: 28px; height: 28px;
            border-radius: 8px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            transition: all 0.2s;
            flex-shrink: 0;
        }

        .alert-close:hover { background: rgba(239, 68, 68, 0.3); color: #fff; }

        .header { display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; }

        .logo {
            width: 54px; height: 54px;
            border-radius: 14px;
            background: linear-gradient(135deg, var(--red-primary), var(--red-dark));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            box-shadow: 0 8px 24px var(--red-glow);
            flex-shrink: 0;
            position: relative;
        }

        .logo::after {
            content: '';
            position: absolute;
            inset: -2px;
            border-radius: 16px;
            background: linear-gradient(135deg, var(--red-primary), var(--red-dark));
            z-index: -1;
            filter: blur(14px);
            opacity: 0.7;
        }

        .header-text h1 {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #fff, #ff9999);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.15rem;
        }

        .header-text p { color: var(--text-secondary); font-size: 0.85rem; font-weight: 400; }

        .status-dot {
            display: inline-block;
            width: 6px; height: 6px;
            background: var(--red-primary);
            border-radius: 50%;
            margin-right: 6px;
            box-shadow: 0 0 8px var(--red-primary);
            animation: pulse 1.5s ease-in-out infinite;
            vertical-align: middle;
        }

        form { display: flex; gap: 0.75rem; margin-bottom: 1rem; }
        .input-wrapper { flex: 1; position: relative; }

        .input-wrapper svg {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            pointer-events: none;
            transition: color 0.2s;
        }

        input[type="text"] {
            width: 100%;
            padding: 0.95rem 1rem 0.95rem 2.85rem;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: var(--bg-input);
            color: var(--text-primary);
            font-size: 0.95rem;
            font-family: 'JetBrains Mono', monospace;
            outline: none;
            transition: all 0.25s ease;
        }

        input[type="text"]::placeholder { color: var(--text-muted); font-family: 'Inter', sans-serif; }

        input[type="text"]:focus {
            border-color: var(--red-primary);
            background: #260f0f;
            box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.12), 0 0 20px rgba(239, 68, 68, 0.15);
        }

        .input-wrapper:focus-within svg { color: var(--red-primary); }

        button[type="submit"] {
            padding: 0.95rem 1.6rem;
            border-radius: 12px;
            border: none;
            background: linear-gradient(135deg, var(--red-primary), var(--red-dark));
            color: #fff;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            white-space: nowrap;
            box-shadow: 0 4px 18px var(--red-glow);
            font-family: inherit;
        }

        button[type="submit"]:hover { transform: translateY(-2px); box-shadow: 0 8px 28px var(--red-glow-strong); }
        button[type="submit"]:active { transform: translateY(0); }
        button[type="submit"]:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

        .spinner {
            width: 16px; height: 16px;
            border: 2px solid rgba(255,255,255,0.3);
            border-top-color: #fff;
            border-radius: 50%;
            animation: spin 0.7s linear infinite;
            display: none;
        }

        .chips { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1rem; }

        .chip {
            padding: 0.4rem 0.85rem;
            border-radius: 999px;
            background: rgba(239, 68, 68, 0.08);
            border: 1px solid rgba(239, 68, 68, 0.22);
            color: var(--text-secondary);
            font-size: 0.78rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: 'JetBrains Mono', monospace;
        }

        .chip:hover {
            background: rgba(239, 68, 68, 0.18);
            border-color: var(--red-primary);
            color: var(--text-primary);
            transform: translateY(-1px);
            box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
        }

        /* Geçmiş */
        .history-section {
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            background: rgba(20, 8, 8, 0.5);
        }

        .history-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.75rem 1rem;
            background: rgba(239, 68, 68, 0.06);
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }

        .history-header:hover { background: rgba(239, 68, 68, 0.1); }

        .history-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .history-title svg { color: var(--red-primary); }

        .history-count {
            background: rgba(239, 68, 68, 0.2);
            color: var(--red-light);
            padding: 0.15rem 0.5rem;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 700;
            margin-left: 0.5rem;
        }

        .history-actions { display: flex; align-items: center; gap: 0.5rem; }

        .history-clear {
            background: transparent;
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #d4a0a0;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.7rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            font-family: inherit;
        }

        .history-clear:hover { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border-color: var(--red-primary); }

        .history-toggle { color: var(--text-muted); transition: transform 0.3s; display: flex; align-items: center; }
        .history-toggle.open { transform: rotate(180deg); }

        .history-list { max-height: 0; overflow: hidden; transition: max-height 0.3s ease-out; }
        .history-list.open { max-height: 300px; overflow-y: auto; }
        .history-list::-webkit-scrollbar { width: 6px; }
        .history-list::-webkit-scrollbar-track { background: var(--bg-secondary); }
        .history-list::-webkit-scrollbar-thumb { background: var(--border-hover); border-radius: 3px; }

        .history-item {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.7rem 1rem;
            border-top: 1px solid var(--border);
            cursor: pointer;
            transition: background 0.2s;
            animation: slideIn 0.3s ease-out;
        }

        .history-item:hover { background: rgba(239, 68, 68, 0.08); }

        .history-item-icon {
            width: 30px; height: 30px;
            border-radius: 8px;
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.25);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            flex-shrink: 0;
        }

        .history-item-content { flex: 1; min-width: 0; }
        .history-item-ip { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; font-weight: 600; color: var(--text-primary); margin-bottom: 0.1rem; }
        .history-item-meta { font-size: 0.7rem; color: var(--text-muted); display: flex; gap: 0.75rem; flex-wrap: wrap; }

        .history-item-delete {
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 0.3rem;
            border-radius: 6px;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            flex-shrink: 0;
        }

        .history-item-delete:hover { background: rgba(239, 68, 68, 0.15); color: var(--red-light); }

        /* Sonuç */
        .result {
            animation: fadeInUp 0.5s ease-out;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
            background: var(--bg-secondary);
            margin-top: 1.5rem;
        }

        .result-header {
            padding: 1rem 1.25rem;
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.12), rgba(185, 28, 28, 0.08));
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .result-header-title {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .result-header-title svg { color: var(--red-primary); }

        /* Sonuç aksiyon butonları */
        .result-actions {
            display: flex;
            gap: 0.4rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .action-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.4rem 0.75rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: rgba(239, 68, 68, 0.06);
            color: var(--text-secondary);
            font-size: 0.72rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            font-family: inherit;
            white-space: nowrap;
        }

        .action-btn:hover {
            background: rgba(239, 68, 68, 0.15);
            border-color: var(--red-primary);
            color: var(--text-primary);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.25);
        }

        .action-btn:active { transform: translateY(0); }
        .action-btn svg { width: 12px; height: 12px; }

        .action-btn.copied {
            background: rgba(16, 185, 129, 0.15);
            border-color: rgba(16, 185, 129, 0.5);
            color: #6ee7b7;
        }

        /* Toast */
        .toast {
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: linear-gradient(135deg, var(--red-primary), var(--red-dark));
            color: #fff;
            padding: 0.75rem 1.25rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            box-shadow: 0 8px 30px rgba(239, 68, 68, 0.5);
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 9999;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            pointer-events: none;
            max-width: 90vw;
        }

        .toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
        .toast svg { width: 16px; height: 16px; flex-shrink: 0; }

        .badge {
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .badge.success {
            background: rgba(239, 68, 68, 0.15);
            color: var(--red-light);
            border: 1px solid rgba(239, 68, 68, 0.35);
            box-shadow: 0 0 12px rgba(239, 68, 68, 0.2);
        }

        .badge.error {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.5);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
            gap: 1px;
            background: var(--border);
        }

        .grid-item {
            background: var(--bg-card);
            padding: 1rem 1.25rem;
            transition: background 0.2s;
            animation: slideIn 0.4s ease-out backwards;
        }

        .grid-item:hover { background: #250d0d; }

        .grid-item .label {
            display: flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.7rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            font-weight: 600;
            margin-bottom: 0.4rem;
        }

        .grid-item .label svg { width: 12px; height: 12px; color: var(--red-primary); }

        .grid-item .value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.92rem;
            color: var(--text-primary);
            font-weight: 500;
            word-break: break-word;
        }

        .grid-item.full { grid-column: 1 / -1; }

        .tag {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            padding: 0.22rem 0.65rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
        }

        .tag.danger { background: rgba(239, 68, 68, 0.18); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.4); }
        .tag.safe { background: rgba(180, 60, 60, 0.12); color: #d4a0a0; border: 1px solid rgba(180, 60, 60, 0.3); }

        .map-wrapper { position: relative; padding: 1rem; background: var(--bg-secondary); }

        .map-title {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }

        .map-title-left { display: flex; align-items: center; gap: 0.5rem; }
        .map-title svg { color: var(--red-primary); }

        .map-hint {
            font-size: 0.68rem;
            color: var(--text-muted);
            text-transform: none;
            letter-spacing: 0;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.3rem;
        }

        .map-hint kbd {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: 4px;
            padding: 0.1rem 0.35rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: var(--red-light);
        }

        #map {
            height: 380px;
            width: 100%;
            border-radius: 12px;
            border: 1px solid var(--border);
            background: #000;
            box-shadow: 0 0 30px rgba(239, 68, 68, 0.12);
        }

        .leaflet-container { background: #000 !important; font-family: 'Inter', sans-serif !important; }
        .leaflet-tile { filter: brightness(0.55) saturate(0.65) hue-rotate(-15deg); }
        .leaflet-control-attribution { background: rgba(20, 8, 8, 0.85) !important; color: #7a5555 !important; font-size: 10px !important; }
        .leaflet-control-attribution a { color: var(--red-light) !important; }
        .leaflet-bar { border: 1px solid var(--border) !important; box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important; }
        .leaflet-bar a { background: var(--bg-card) !important; color: var(--text-primary) !important; border-bottom: 1px solid var(--border) !important; }
        .leaflet-bar a:hover { background: var(--red-dark) !important; }

        .custom-marker { position: relative; }

        .marker-pin {
            width: 24px; height: 24px;
            border-radius: 50% 50% 50% 0;
            background: linear-gradient(135deg, var(--red-light), var(--red-dark));
            position: absolute;
            transform: rotate(-45deg);
            left: 50%; top: 50%;
            margin: -20px 0 0 -12px;
            box-shadow: 0 0 20px var(--red-primary), 0 0 40px rgba(239, 68, 68, 0.5);
            border: 2px solid #fff;
        }

        .marker-pin::after {
            content: '';
            width: 8px; height: 8px;
            border-radius: 50%;
            background: #fff;
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
        }

        .marker-pulse {
            position: absolute;
            width: 24px; height: 24px;
            border-radius: 50%;
            background: var(--red-primary);
            left: 50%; top: 50%;
            margin: -12px 0 0 -12px;
            animation: markerPulse 2s ease-out infinite;
        }

        .custom-popup .leaflet-popup-content-wrapper {
            background: var(--bg-card);
            color: var(--text-primary);
            border: 1px solid var(--red-primary);
            border-radius: 10px;
            box-shadow: 0 8px 24px rgba(239, 68, 68, 0.3);
        }

        .custom-popup .leaflet-popup-content {
            margin: 0.7rem 1rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            line-height: 1.5;
        }

        .custom-popup .leaflet-popup-tip { background: var(--red-primary); }

        .popup-title { font-weight: 700; color: var(--red-light); margin-bottom: 0.3rem; font-family: 'Inter', sans-serif; }

        .footer {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.72rem;
            color: var(--text-muted);
            letter-spacing: 0.03em;
        }

        .footer a { color: var(--red-light); text-decoration: none; }
        .footer a:hover { text-decoration: underline; }

        @media (max-width: 640px) {
            .container { padding: 1.5rem; border-radius: 18px; }
            form { flex-direction: column; }
            button[type="submit"] { justify-content: center; }
            .header-text h1 { font-size: 1.25rem; }
            #map { height: 280px; }
            .grid { grid-template-columns: 1fr 1fr; }
            .alert-banner { padding: 0.85rem 1rem; }
            .alert-icon { width: 34px; height: 34px; font-size: 1.1rem; }
            .result-header { padding: 0.85rem 1rem; }
            .action-btn { font-size: 0.68rem; padding: 0.35rem 0.6rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Uyarı Banner -->
        <div class="alert-banner" id="alertBanner" style="display: none;">
            <div class="alert-icon">⚠️</div>
            <div class="alert-text">
                <div class="alert-title" id="alertTitle">Proxy / VPN Tespit Edildi</div>
                <div class="alert-desc" id="alertDesc">Bu IP adresi bir proxy, VPN veya hosting servisine ait olabilir.</div>
            </div>
            <button class="alert-close" onclick="closeAlert()">✕</button>
        </div>

        <div class="header">
            <div class="logo">🎯</div>
            <div class="header-text">
                <h1>IP OSINT Tool</h1>
                <p><span class="status-dot"></span>Sistem aktif • ip-api.com</p>
            </div>
        </div>

        <form method="POST" id="queryForm">
            <div class="input-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="11" cy="11" r="8"></circle>
                    <path d="m21 21-4.3-4.3"></path>
                </svg>
                <input type="text" name="ip" id="ipInput" placeholder="IP adresi girin (boş = kendi IP'niz)" autocomplete="off" spellcheck="false">
            </div>
            <button type="submit" id="submitBtn">
                <span class="spinner" id="spinner"></span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                </svg>
                <span>Sorgula</span>
            </button>
        </form>

        <div class="chips">
            <span class="chip" onclick="setIP('8.8.8.8')">8.8.8.8 (Google)</span>
            <span class="chip" onclick="setIP('1.1.1.1')">1.1.1.1 (Cloudflare)</span>
            <span class="chip" onclick="setIP('')">Kendi IP'm</span>
        </div>

        <!-- Geçmiş -->
        <div class="history-section" id="historySection" style="display: none;">
            <div class="history-header" onclick="toggleHistory()">
                <div class="history-title">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>
                        <path d="M3 3v5h5"/>
                        <path d="M12 7v5l4 2"/>
                    </svg>
                    Sorgu Geçmişi
                    <span class="history-count" id="historyCount">0</span>
                </div>
                <div class="history-actions">
                    <button class="history-clear" onclick="event.stopPropagation(); clearHistory()">Temizle</button>
                    <span class="history-toggle" id="historyToggle">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="m6 9 6 6 6-6"/>
                        </svg>
                    </span>
                </div>
            </div>
            <div class="history-list" id="historyList"></div>
        </div>

        {% if result %}
            {% if result.success %}
            <div class="result">
                <div class="result-header">
                    <div class="result-header-title">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 6 9 17l-5-5"/>
                        </svg>
                        Sorgu Başarılı
                        <span class="badge success">{{ result.data.query }}</span>
                    </div>
                    <div class="result-actions">
                        <button class="action-btn" onclick="downloadJSON()" title="JSON olarak indir (Ctrl+S)">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                                <polyline points="7 10 12 15 17 10"/>
                                <line x1="12" y1="15" x2="12" y2="3"/>
                            </svg>
                            JSON
                        </button>
                        <button class="action-btn" id="copyBtn" onclick="copyResult()" title="Sonucu kopyala (Ctrl+C)">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"/>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
                            </svg>
                            Kopyala
                        </button>
                    </div>
                </div>

                <div class="grid">
                    <div class="grid-item">
                        <div class="label">🌍 Ülke</div>
                        <div class="value">{{ result.data.country }} ({{ result.data.countryCode }})</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">📍 Şehir</div>
                        <div class="value">{{ result.data.city or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">🗺️ Bölge</div>
                        <div class="value">{{ result.data.regionName or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">📮 Posta Kodu</div>
                        <div class="value">{{ result.data.zip or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">🛰️ ISP</div>
                        <div class="value">{{ result.data.isp or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">🏢 Organizasyon</div>
                        <div class="value">{{ result.data.org or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">🔢 AS</div>
                        <div class="value">{{ result.data.as_ or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">🕐 Zaman Dilimi</div>
                        <div class="value">{{ result.data.timezone or '—' }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">📡 Koordinatlar</div>
                        <div class="value">{{ result.data.lat }}, {{ result.data.lon }}</div>
                    </div>
                    <div class="grid-item">
                        <div class="label">📱 Mobil</div>
                        <div class="value">
                            {% if result.data.mobile %}<span class="tag danger">Evet</span>{% else %}<span class="tag safe">Hayır</span>{% endif %}
                        </div>
                    </div>
                    <div class="grid-item">
                        <div class="label">🛡️ Proxy / VPN</div>
                        <div class="value">
                            {% if result.data.proxy %}<span class="tag danger">Tespit Edildi</span>{% else %}<span class="tag safe">Temiz</span>{% endif %}
                        </div>
                    </div>
                    <div class="grid-item">
                        <div class="label">☁️ Hosting</div>
                        <div class="value">
                            {% if result.data.hosting %}<span class="tag danger">Evet</span>{% else %}<span class="tag safe">Hayır</span>{% endif %}
                        </div>
                    </div>
                </div>

                <div class="map-wrapper">
                    <div class="map-title">
                        <div class="map-title-left">
                            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                                <circle cx="12" cy="10" r="3"></circle>
                            </svg>
                            Konum Haritası
                        </div>
                        <div class="map-hint">
                            💡 İpucu: <kbd>Haritaya tıkla</kbd> → o bölgedeki IP'yi sorgula
                        </div>
                    </div>
                    <div id="map" data-lat="{{ result.data.lat }}" data-lon="{{ result.data.lon }}" data-ip="{{ result.data.query }}" data-city="{{ result.data.city or 'Bilinmiyor' }}" data-country="{{ result.data.country or 'Bilinmiyor' }}"></div>
                </div>
            </div>
            {% else %}
            <div class="result">
                <div class="result-header">
                    <div class="result-header-title">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"></circle>
                            <line x1="12" y1="8" x2="12" y2="12"></line>
                            <line x1="12" y1="16" x2="12.01" y2="16"></line>
                        </svg>
                        Sorgu Hatası
                    </div>
                    <span class="badge error">HATA</span>
                </div>
                <div style="padding: 1.25rem; color: #fca5a5; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;">
                    {{ result.error }}
                </div>
            </div>
            {% endif %}
        {% endif %}

        <div class="footer">
            Powered by <a href="https://ip-api.com" target="_blank">ip-api.com</a> • Harita: <a href="https://leafletjs.com" target="_blank">Leaflet</a> + <a href="https://carto.com" target="_blank">CARTO</a>
        </div>
    </div>

    <!-- Toast bildirimi -->
    <div class="toast" id="toast">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 6 9 17l-5-5"/>
        </svg>
        <span id="toastMsg">İşlem başarılı</span>
    </div>

    <script>
        /* ============================================
           1. YARDIMCI FONKSİYONLAR
           ============================================ */
        function setIP(ip) {
            document.getElementById('ipInput').value = ip;
            document.getElementById('ipInput').focus();
        }

        function closeAlert() {
            document.getElementById('alertBanner').style.display = 'none';
        }

        /* ============================================
           2. PROXY/VPN UYARI BANNER
           ============================================ */
        {% if result and result.success %}
            {% if result.data.proxy or result.data.hosting %}
            (function showAlert() {
                const banner = document.getElementById('alertBanner');
                const title = document.getElementById('alertTitle');
                const desc = document.getElementById('alertDesc');

                let alerts = [];
                if ({{ 'true' if result.data.proxy else 'false' }}) alerts.push('Proxy/VPN');
                if ({{ 'true' if result.data.hosting else 'false' }}) alerts.push('Hosting/Datacenter');

                if (alerts.length > 0) {
                    title.textContent = '⚠️ ' + alerts.join(' + ') + ' Tespit Edildi';
                    desc.textContent = 'Bu IP adresi ({{ result.data.query }}) ' +
                        (alerts.includes('Proxy/VPN') ? 'bir proxy/VPN servisi ' : '') +
                        (alerts.length > 1 ? 've ' : '') +
                        (alerts.includes('Hosting/Datacenter') ? 'bir hosting/datacenter altyapısı ' : '') +
                        'üzerinden geliyor olabilir. Gerçek kullanıcı konumu farklı olabilir.';
                    banner.style.display = 'flex';
                }
            })();
            {% endif %}
        {% endif %}

        /* ============================================
           3. SORGU GEÇMİŞİ (localStorage)
           ============================================ */
        const HISTORY_KEY = 'iposint_history';
        const MAX_HISTORY = 20;

        function getHistory() {
            try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); }
            catch (e) { return []; }
        }

        function saveHistory(h) { localStorage.setItem(HISTORY_KEY, JSON.stringify(h.slice(0, MAX_HISTORY))); }

        function addToHistory(entry) {
            const history = getHistory();
            const filtered = history.filter(h => h.ip !== entry.ip);
            filtered.unshift({ ...entry, timestamp: Date.now() });
            saveHistory(filtered);
            renderHistory();
        }

        function removeFromHistory(ip, event) {
            if (event) event.stopPropagation();
            const history = getHistory().filter(h => h.ip !== ip);
            saveHistory(history);
            renderHistory();
        }

        function clearHistory() {
            if (!confirm('Tüm sorgu geçmişi silinsin mi?')) return;
            localStorage.removeItem(HISTORY_KEY);
            renderHistory();
        }

        function toggleHistory() {
            document.getElementById('historyList').classList.toggle('open');
            document.getElementById('historyToggle').classList.toggle('open');
        }

        function timeAgo(ts) {
            const diff = Date.now() - ts;
            const sec = Math.floor(diff / 1000);
            const min = Math.floor(sec / 60);
            const hour = Math.floor(min / 60);
            const day = Math.floor(hour / 24);
            if (sec < 60) return 'şimdi';
            if (min < 60) return min + ' dk önce';
            if (hour < 24) return hour + ' saat önce';
            if (day < 7) return day + ' gün önce';
            return new Date(ts).toLocaleDateString('tr-TR');
        }

        function renderHistory() {
            const section = document.getElementById('historySection');
            const list = document.getElementById('historyList');
            const count = document.getElementById('historyCount');
            const history = getHistory();

            if (history.length === 0) { section.style.display = 'none'; return; }

            section.style.display = 'block';
            count.textContent = history.length;

            list.innerHTML = history.map(item => `
                <div class="history-item" onclick="loadFromHistory('${item.ip}')">
                    <div class="history-item-icon">🌐</div>
                    <div class="history-item-content">
                        <div class="history-item-ip">${item.ip}</div>
                        <div class="history-item-meta">
                            <span>📍 ${item.city || 'Bilinmiyor'}, ${item.country || '—'}</span>
                            <span>🕐 ${timeAgo(item.timestamp)}</span>
                        </div>
                    </div>
                    <button class="history-item-delete" onclick="removeFromHistory('${item.ip}', event)" title="Sil">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6h14z"/>
                        </svg>
                    </button>
                </div>
            `).join('');
        }

        function loadFromHistory(ip) {
            document.getElementById('ipInput').value = ip;
            document.getElementById('queryForm').submit();
        }

        window.addEventListener('DOMContentLoaded', renderHistory);

        {% if result and result.success %}
        addToHistory({
            ip: '{{ result.data.query }}',
            city: '{{ result.data.city or "" }}',
            country: '{{ result.data.country or "" }}'
        });
        {% endif %}

        /* ============================================
           4. HARİTA
           ============================================ */
        window.addEventListener('DOMContentLoaded', function() {
            const mapEl = document.getElementById('map');
            if (!mapEl) return;

            const lat = parseFloat(mapEl.dataset.lat);
            const lon = parseFloat(mapEl.dataset.lon);
            const ip = mapEl.dataset.ip;
            const city = mapEl.dataset.city;
            const country = mapEl.dataset.country;

            if (isNaN(lat) || isNaN(lon)) return;

            const map = L.map('map', { center: [lat, lon], zoom: 10, zoomControl: true });

            L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                attribution: '&copy; OpenStreetMap &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 20
            }).addTo(map);

            const redIcon = L.divIcon({
                className: 'custom-marker',
                html: '<div class="marker-pulse"></div><div class="marker-pin"></div>',
                iconSize: [24, 24],
                iconAnchor: [12, 24],
                popupAnchor: [0, -24]
            });

            const marker = L.marker([lat, lon], { icon: redIcon }).addTo(map);

            const popupContent = `
                <div class="popup-title">📍 ${city}, ${country}</div>
                <div>IP: ${ip}</div>
                <div>Lat: ${lat}</div>
                <div>Lon: ${lon}</div>
            `;

            marker.bindPopup(popupContent, { className: 'custom-popup' }).openPopup();

            L.circle([lat, lon], {
                color: '#ef4444', fillColor: '#ef4444', fillOpacity: 0.08,
                radius: 30000, weight: 1, dashArray: '5, 10'
            }).addTo(map);

            let clickMarker = null;
            map.on('click', function(e) {
                const clickLat = e.latlng.lat.toFixed(4);
                const clickLon = e.latlng.lng.toFixed(4);

                if (clickMarker) map.removeLayer(clickMarker);

                const clickIcon = L.divIcon({
                    className: 'custom-marker',
                    html: '<div style="width:18px;height:18px;border-radius:50%;background:linear-gradient(135deg,#f87171,#b91c1c);border:2px solid #fff;box-shadow:0 0 15px rgba(239,68,68,0.8);"></div>',
                    iconSize: [18, 18], iconAnchor: [9, 9]
                });

                clickMarker = L.marker([clickLat, clickLon], { icon: clickIcon }).addTo(map);

                const popupHtml = `
                    <div class="popup-title">🎯 Tıklanan Konum</div>
                    <div>Lat: ${clickLat}</div>
                    <div>Lon: ${clickLon}</div>
                    <div style="margin-top:0.5rem;padding-top:0.5rem;border-top:1px solid #3d1414;">
                        <button onclick="queryNearbyIP('${clickLat}', '${clickLon}')"
                            style="background:linear-gradient(135deg,#ef4444,#b91c1c);border:none;color:#fff;padding:0.4rem 0.8rem;border-radius:6px;cursor:pointer;font-family:inherit;font-size:0.78rem;font-weight:600;width:100%;">
                            🔍 Bu bölgeden IP sorgula
                        </button>
                    </div>
                `;

                clickMarker.bindPopup(popupHtml, { className: 'custom-popup' }).openPopup();
            });
        });

        async function queryNearbyIP(lat, lon) {
            const confirmed = confirm(
                'Seçilen konum: ' + lat + ', ' + lon + '\\n\\n' +
                '⚠️ Not: Belirli bir koordinattan IP bulmak için ücretli API gerekir.\\n\\n' +
                'Kendi IP\\'nizi sorgulamak için İptal\\'e basın.'
            );
            if (confirmed) {
                document.getElementById('ipInput').value = '';
                document.getElementById('queryForm').submit();
            }
        }

        /* ============================================
           5. FORM SUBMIT LOADING
           ============================================ */
        document.getElementById('queryForm').addEventListener('submit', function() {
            document.getElementById('spinner').style.display = 'block';
            const btn = document.getElementById('submitBtn');
            btn.disabled = true;
            btn.querySelector('span:last-child').textContent = 'Sorgulanıyor...';
        });

        /* ============================================
           6. JSON İNDİRME & KOPYALAMA
           ============================================ */
        const RESULT_DATA = {% if result and result.success %}{{ result.data | tojson }}{% else %}null{% endif %};

        function downloadJSON() {
            if (!RESULT_DATA) {
                showToast('İndirilecek veri yok', true);
                return;
            }

            const exportData = {
                _meta: {
                    tool: 'IP OSINT Tool',
                    version: '1.0',
                    exported_at: new Date().toISOString(),
                    source: 'ip-api.com'
                },
                ...RESULT_DATA
            };

            const jsonStr = JSON.stringify(exportData, null, 2);
            const blob = new Blob([jsonStr], { type: 'application/json;charset=utf-8' });
            const url = URL.createObjectURL(blob);

            const ipSafe = (RESULT_DATA.query || 'unknown').replace(/[^a-zA-Z0-9.]/g, '_');
            const date = new Date().toISOString().slice(0, 10);
            const filename = `iposint_${ipSafe}_${date}.json`;

            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            showToast('JSON indirildi: ' + filename);
        }

        function copyResult() {
            if (!RESULT_DATA) {
                showToast('Kopyalanacak veri yok', true);
                return;
            }
            const jsonStr = JSON.stringify(RESULT_DATA, null, 2);

            if (navigator.clipboard && window.isSecureContext) {
                navigator.clipboard.writeText(jsonStr).then(() => {
                    markCopied();
                    showToast('Sonuç kopyalandı');
                }).catch(() => fallbackCopy(jsonStr));
            } else {
                fallbackCopy(jsonStr);
            }
        }

        function fallbackCopy(text) {
            const textarea = document.createElement('textarea');
            textarea.value = text;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            try {
                document.execCommand('copy');
                markCopied();
                showToast('Sonuç kopyalandı');
            } catch (e) {
                showToast('Kopyalama başarısız', true);
            }
            document.body.removeChild(textarea);
        }

        function markCopied() {
            const btn = document.getElementById('copyBtn');
            if (!btn) return;
            const original = btn.innerHTML;
            btn.classList.add('copied');
            btn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M20 6 9 17l-5-5"/>
                </svg>
                Kopyalandı
            `;
            setTimeout(() => {
                btn.classList.remove('copied');
                btn.innerHTML = original;
            }, 2000);
        }

        let toastTimer = null;
        function showToast(msg, isError = false) {
            const toast = document.getElementById('toast');
            const toastMsg = document.getElementById('toastMsg');
            if (!toast) return;

            toastMsg.textContent = msg;

            const svg = toast.querySelector('svg');
            if (isError) {
                toast.style.background = 'linear-gradient(135deg, #ef4444, #7f1d1d)';
                svg.innerHTML = '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>';
            } else {
                toast.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                svg.innerHTML = '<path d="M20 6 9 17l-5-5"/>';
            }

            toast.classList.add('show');
            clearTimeout(toastTimer);
            toastTimer = setTimeout(() => toast.classList.remove('show'), 2500);
        }

        // Klavye kısayolları
        document.addEventListener('keydown', function(e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 's' && RESULT_DATA) {
                e.preventDefault();
                downloadJSON();
            }
            if ((e.ctrlKey || e.metaKey) && e.key === 'c' && RESULT_DATA && document.activeElement.tagName !== 'INPUT') {
                e.preventDefault();
                copyResult();
            }
        });
    </script>
</body>
</html>
"""

def query_ip(ip):
    """IP sorgusu yapar ve sonucu döner."""
    try:
        url = f"{API_URL}{ip}" if ip else API_URL
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get('status') == 'success':
            data['as_'] = data.get('as', '—')
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": data.get('message', 'Bilinmeyen bir hata oluştu.')}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "İstek zaman aşımına uğradı. Tekrar deneyin."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Bağlantı hatası. İnternet bağlantınızı kontrol edin."}
    except Exception as e:
        return {"success": False, "error": f"Beklenmeyen hata: {str(e)}"}


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        ip = request.form.get('ip', '').strip()
        result = query_ip(ip)

    return render_template_string(HTML_TEMPLATE, result=result)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  🎯  KADRBEQUIT IP OSINT TOOL ")
    print("="*60)
    print("  ✨ Özellikler:")
    print("     • Kırmızı tema + siyah harita")
    print("     • Sorgu geçmişi (localStorage)")
    print("     • Haritaya tıklayarak IP sorgulama")
    print("     • Proxy/VPN uyarı banner'ı")
    print("     • 📥 JSON indirme + kopyalama")
    print("     • ⌨️  Klavye kısayolları (Ctrl+S, Ctrl+C)")
    print("="*60)
    print("  🌐 Tarayıcıdan aç: http://127.0.0.1:5000")
    print("="*60 + "\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
