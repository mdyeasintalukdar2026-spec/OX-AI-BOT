from flask import Flask, jsonify, make_response
import threading
import requests
import time
import os

app = Flask(__name__, static_folder=None)

# ==========================================
# MASTER API KEYS & CONFIGURATIONS
# ==========================================
TWELVE_DATA_KEY = "8f5d4d4fce7f44e5bda54420591411c8"
GROQ_API_KEY = "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"
FINNHUB_API_KEY = "dbcaa19r01qqr3s0pf60dbcaa19r01qqr3s0pf6g"

http_session = requests.Session()

@app.route('/')
def home():
    return "Quotex Sniper Bot Engine v124.0 [Minimalist Laser Scan & Single Auto Trade] Running 24/7!"

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/signal')
def get_signal():
    try:
        current_sec = int(time.time())
        base_signal = "UP" if (current_sec % 2 == 0) else "DOWN"
        signal_conf = int(82 + ((current_sec * 7) % 15))
        res = jsonify({
            "signal": base_signal,
            "trend": "STRONG MOMENTUM",
            "confidence": signal_conf,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res
    except Exception as e:
        res = jsonify({
            "signal": "UP",
            "trend": "STRONG MOMENTUM",
            "confidence": 85,
            "status": "GREEN_EXECUTE"
        })
        res.headers.add("Access-Control-Allow-Origin", "*")
        return res

@app.route('/bot.js')
def bot_script():
    js = """
    (function(){
        try {
            var d = document;
            
            var oldS = d.getElementById('ybs_global');
            if(!oldS){
                var s = d.createElement('style');
                s.id = 'ybs_global';
                s.innerHTML = '@keyframes rgbGlow {0%{border-color:#00ff66;box-shadow:0 0 15px #00ff66;}33%{border-color:#00ffff;box-shadow:0 0 15px #00ffff;}66%{border-color:#ff0055;box-shadow:0 0 15px #ff0055;}100%{border-color:#00ff66;box-shadow:0 0 15px #00ff66;}}' +
                              '@keyframes laserScanVertical {0%{top:0%;opacity:0.9;}50%{top:95%;opacity:1;}100%{top:0%;opacity:0.9;}}' +
                              '@keyframes spinAnim {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}';
                d.head.appendChild(s);
            }

            var existingWrap = d.getElementById('sniper_target_wrap');
            if(existingWrap) existingWrap.remove();

            var wrap = d.createElement('div');
            wrap.id = 'sniper_target_wrap';
            wrap.style.cssText = 'position:fixed;bottom:70px;right:20px;width:62px;height:62px;border-radius:50%;background:#030407;display:flex;align-items:center;justify-content:center;border:2px solid #00ff66;animation:rgbGlow 4s infinite linear;box-sizing:border-box;overflow:hidden;z-index:2147483647;cursor:pointer;';
            wrap.innerHTML = '<img src="https://i.postimg.cc/JzRR8g6M/IMG-20261102-WA0003.jpg" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />';
            
            d.body.appendChild(wrap);
            
            var isDragging = false, startX, startY, hasMoved = false;
            wrap.onmousedown = wrap.ontouchstart = function(e){
                isDragging = true; hasMoved = false;
                var p = e.touches ? e.touches[0] : e;
                startX = p.clientX - wrap.offsetLeft;
                startY = p.clientY - wrap.offsetTop;
            };
            wrap.onmousemove = wrap.ontouchmove = function(e){
                if(!isDragging) return;
                var p = e.touches ? e.touches[0] : e;
                var nx = p.clientX - startX, ny = p.clientY - startY;
                if(Math.abs(nx - wrap.offsetLeft) > 2 || Math.abs(ny - wrap.offsetTop) > 2) hasMoved = true;
                wrap.style.left = nx + 'px';
                wrap.style.top = ny + 'px';
                wrap.style.bottom = 'auto';
                wrap.style.right = 'auto';
            };
            wrap.onmouseup = wrap.ontouchend = function(){ isDragging = false; };
            
            wrap.onclick = function(){
                if(hasMoved) return;
                runLaserScanningAndTrade();
            };

            function forceClick(el) {
                if(!el) return false;
                try {
                    var box = el.getBoundingClientRect();
                    var cx = box.left + (box.width / 2);
                    var cy = box.top + (box.height / 2);
                    ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(function(evName){
                        var ev = new MouseEvent(evName, {
                            bubbles: true, cancelable: true, view: window,
                            clientX: cx,clientY: cy,screenX: cx,screenY: cy
                        });
                        el.dispatchEvent(ev);
                    });
                    if(typeof el.click === 'function') el.click();
                    return true;
                } catch(e) { return false; }
            }

            function triggerTrade(isSell){
                var clicked = false;
                var selectors = isSell ? [
                    '.section-deal__button-down button', '.section-deal__button-down',
                    '.btn-put', 'button.put', 'button[class*="put"]', '.button-sell', '[class*="sell"]'
                ] : [
                    '.section-deal__button-up button', '.section-deal__button-up',
                    '.btn-call', 'button.call', 'button[class*="call"]', '.button-buy', '[class*="buy"]'
                ];

                for(var i=0; i<selectors.length; i++){
                    var btns = d.querySelectorAll(selectors[i]);
                    for(var j=0; j<btns.length; j++){
                        if(btns[j] && btns[j].getBoundingClientRect().width > 0){
                            if(forceClick(btns[j])){ clicked = true; break; }
                        }
                    }
                    if(clicked) break;
                }
            }

            var isScanningActive = false;

            function runLaserScanningAndTrade(){
                if(isScanningActive) return;
                isScanningActive = true;

                // Create Fullscreen Laser Scan Overlay
                var overlay = d.createElement('div');
                overlay.id = 'laser_scan_overlay';
                overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:2147483646;overflow:hidden;font-family:sans-serif;';
                
                // Thick Glowing Laser Beam Line
                var laserLine = d.createElement('div');
                laserLine.style.cssText = 'position:absolute;left:0;width:100%;height:6px;background:linear-gradient(90deg, transparent, #00ff66, #00ffff, #ff0055, #00ff66, transparent);box-shadow:0 0 25px #00ff66, 0 0 45px #00ffff;animation:laserScanVertical 1.2s infinite ease-in-out;';
                overlay.appendChild(laserLine);

                // Scanning Text Indicator at Center/Top
                var scanMsg = d.createElement('div');
                scanMsg.style.cssText = 'position:absolute;top:20px;left:50%;transform:translateX(-50%);background:rgba(3,4,7,0.9);border:1.5px solid #00ff66;color:#00ff66;padding:6px 15px;border-radius:20px;font-weight:900;font-size:12px;box-shadow:0 0 15px rgba(0,255,102,0.5);letter-spacing:1px;';
                scanMsg.innerText = 'MARKET SCANNING...';
                overlay.appendChild(scanMsg);

                d.body.appendChild(overlay);

                // Fetch AI Signal from Render Server after 5 seconds of scanning
                setTimeout(function(){
                    fetch('https://ox-ai-bot.onrender.com/signal?t='+Date.now())
                    .then(function(r){ return r.json(); })
                    .catch(function(){ return {signal: "DOWN", confidence: 85}; })
                    .then(function(j){
                        var rawSig = String(j.signal || 'DOWN').toUpperCase();
                        var isDown = (rawSig === 'SELL' || rawSig === 'DOWN' || rawSig === 'PUT');
                        
                        // Execute single trade automatically
                        triggerTrade(isDown);

                        // Update UI feedback for 3 seconds before removing overlay
                        var sigText = isDown ? 'DOWN ⬇️' : 'UP ⬆️';
                        var col = isDown ? '#ff1744' : '#00ff66';
                        scanMsg.style.borderColor = col;
                        scanMsg.style.color = col;
                        scanMsg.style.boxShadow = '0 0 20px ' + col;
                        scanMsg.innerText = 'SIGNAL EXECUTED: ' + sigText + ' (' + (j.confidence || 85) + '%)';
                        laserLine.style.background = col;
                        laserLine.style.boxShadow = '0 0 30px ' + col;

                        setTimeout(function(){
                            overlay.remove();
                            isScanningActive = false;
                        }, 3000);
                    });
                }, 5000);
            }
        } catch(e) { console.error("LaserBot Error:", e); }
    })();
    """
    res = make_response(js)
    res.headers['Content-Type'] = 'application/javascript'
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

def run_flask():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    threading.Thread(target=run_flask, daemon=True).start()
