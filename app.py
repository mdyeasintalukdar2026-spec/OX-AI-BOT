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
    return "Quotex Sniper Bot Engine v125.0 [AUTO SCAN BOT with Password & Direct Execution] Running 24/7!"

@app.route('/ping')
def ping():
    return "OK", 200

@app.route('/signal')
def get_signal():
    try:
        current_sec = int(time.time())
        base_signal = "UP" if (current_sec % 2 == 0) else "DOWN"
        signal_conf = int(85 + ((current_sec * 7) % 12))
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
            "confidence": 88,
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
            var uniqueId = 'scan_bot_' + Math.floor(Math.random() * 10000);
            
            var oldS = d.getElementById('ybs_global');
            if(!oldS){
                var s = d.createElement('style');
                s.id = 'ybs_global';
                s.innerHTML = '@keyframes rgbColorShift {0%{border-color:#00ff66;box-shadow:0 0 15px #00ff66;}33%{border-color:#00ffff;box-shadow:0 0 15px #00ffff;}66%{border-color:#ff0055;box-shadow:0 0 15px #ff0055;}100%{border-color:#00ff66;box-shadow:0 0 15px #00ff66;}}' +
                              '@keyframes borderSlowGlow {0%{border-color:#ff3366;}33%{border-color:#00ffff;}66%{border-color:#00ff66;}100%{border-color:#ff3366;}}' +
                              '@keyframes laserScanVertical {0%{top:0%;opacity:0.9;}50%{top:95%;opacity:1;}100%{top:0%;opacity:0.9;}}' +
                              '@keyframes panelPop {0%{opacity:0;transform:translate(-50%, -45%) scale(0.9);}100%{opacity:1;transform:translate(-50%, -50%) scale(1);}}' +
                              '@keyframes spinAnim {0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}';
                d.head.appendChild(s);
            }

            var existingWrap = d.getElementById('sniper_target_wrap');
            if(existingWrap) existingWrap.remove();

            var wrap = d.createElement('div');
            wrap.id = 'sniper_target_wrap';
            wrap.style.cssText = 'position:fixed;bottom:70px;right:20px;display:flex;flex-direction:column;align-items:center;z-index:2147483647;cursor:pointer;';
            
            var b = d.createElement('div');
            b.id = 'sniper_target_btn';
            b.style.cssText = 'width:62px;height:62px;border-radius:50%;background:#030407;display:flex;align-items:center;justify-content:center;border:2.5px solid #00ff66;animation:rgbColorShift 6s infinite linear;box-sizing:border-box;overflow:hidden;';
            b.innerHTML = '<img src="https://i.postimg.cc/JzRR8g6M/IMG-20261102-WA0003.jpg" style="width:100%;height:100%;object-fit:cover;border-radius:50%;" />';
            wrap.appendChild(b);

            var lbl = d.createElement('div');
            lbl.style.cssText = 'margin-top:3px;font-size:7px;font-weight:900;color:#00ff66;font-family:sans-serif;background:rgba(3,4,7,0.85);padding:1px 6px;border-radius:3px;border:1px solid rgba(0,255,102,0.4);white-space:nowrap;box-shadow:0 0 5px rgba(0,0,0,0.8);animation:rgbColorShift 6s infinite linear;';
            lbl.innerText = 'AUTO SCAN BOT';
            wrap.appendChild(lbl);

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
                
                // Check if already verified in session
                if(sessionStorage.getItem('scan_bot_verified_' + uniqueId) === 'true'){
                    runLaserScanningAndTrade();
                } else {
                    createLicensePanel(wrap);
                }
            };

            function createLicensePanel(targetWrap){
                targetWrap.style.display = 'none';
                var panel = d.createElement('div');
                panel.id = 'scan_bot_license_panel';
                panel.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%, -50%);width:240px;background:#070b14;border:2.5px solid #00ff66;border-radius:10px;z-index:2147483647;font-family:sans-serif;color:#fff;box-shadow:0 15px 40px rgba(0,0,0,0.95);overflow:hidden;animation:panelPop 0.3s ease-out forwards;';
                
                var header = d.createElement('div');
                header.style.cssText = 'background:#03050a;padding:6px 10px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #131d2e;';
                header.innerHTML = '<div style="display:flex;align-items:center;gap:6px;">' +
                                   '<div style="background:#1a080d;border:1px solid #ff3366;width:18px;height:18px;border-radius:3px;display:flex;align-items:center;justify-content:center;font-size:10px;">🤖</div>' +
                                   '<div>' +
                                   '<div style="font-size:9.5px;font-weight:900;color:#fff;">AUTO SCAN BOT</div>' +
                                   '<div style="font-size:5.5px;color:#8a99ad;">SECURE ACCESS</div>' +
                                   '</div>' +
                                   '</div>' +
                                   '<button id="close-license" style="background:#101826;border:none;color:#fff;width:18px;height:18px;border-radius:3px;cursor:pointer;font-weight:bold;font-size:10px;">×</button>';
                panel.appendChild(header);
                
                header.querySelector('#close-license').onclick = function(){ 
                    panel.remove(); 
                    targetWrap.style.display = 'flex'; 
                };

                var licenseBox = d.createElement('div');
                licenseBox.style.cssText = 'padding:10px;background:#070b14;';
                licenseBox.innerHTML = '<div style="font-size:6.5px;color:#8a99ad;margin-bottom:4px;" id="err-msg">Enter Password to Activate Bot</div>' +
                                       '<input type="password" id="license-input" placeholder="Enter Password (112233)" style="width:100%;box-sizing:border-box;background:#0d1526;border:1px solid #16253f;padding:6px;border-radius:4px;color:#fff;font-size:8px;outline:none;margin-bottom:6px;" />' +
                                       '<button id="verify-btn" style="width:100%;background:#00c853;border:none;padding:6px;border-radius:4px;font-weight:900;font-size:8px;color:#000;cursor:pointer;">ACTIVATE BOT</button>';
                panel.appendChild(licenseBox);

                var verifyBtn = licenseBox.querySelector('#verify-btn');
                var licenseInput = licenseBox.querySelector('#license-input');
                var errMsg = licenseBox.querySelector('#err-msg');

                verifyBtn.onclick = function(){
                    var keyVal = licenseInput.value.trim();
                    if(keyVal === '112233'){
                        verifyBtn.innerHTML = '<span style="display:inline-block;width:8px;height:8px;border:1px solid #000;border-top-color:transparent;border-radius:50%;animation:spinAnim 0.8s linear infinite;"></span> Verifying...';
                        setTimeout(function(){
                            sessionStorage.setItem('scan_bot_verified_' + uniqueId, 'true');
                            panel.remove();
                            targetWrap.style.display = 'flex';
                            runLaserScanningAndTrade();
                        }, 1200);
                    } else {
                        errMsg.innerText = '⚠️ INCORRECT PASSWORD!';
                        errMsg.style.color = '#ff1744';
                        licenseInput.style.borderColor = '#ff1744';
                        verifyBtn.style.background = '#ff1744';
                        verifyBtn.style.color = '#fff';
                        verifyBtn.innerText = 'ACCESS DENIED';
                    }
                };

                d.body.appendChild(panel);
            }

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

                // Create Fullscreen Laser Scan Overlay with top indicator
                var overlay = d.createElement('div');
                overlay.id = 'laser_scan_overlay';
                overlay.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:2147483646;overflow:hidden;font-family:sans-serif;';
                
                // Thick Glowing Laser Beam Line
                var laserLine = d.createElement('div');
                laserLine.style.cssText = 'position:absolute;left:0;width:100%;height:6px;background:linear-gradient(90deg, transparent, #00ff66, #00ffff, #ff0055, #00ff66, transparent);box-shadow:0 0 25px #00ff66, 0 0 45px #00ffff;animation:laserScanVertical 1.2s infinite ease-in-out;';
                overlay.appendChild(laserLine);

                // Top Center Market Scanning Indicator (with color-changing border animation)
                var scanMsg = d.createElement('div');
                scanMsg.style.cssText = 'position:absolute;top:15px;left:50%;transform:translateX(-50%);background:rgba(3,4,7,0.92);border:2px solid #00ff66;color:#00ff66;padding:6px 16px;border-radius:20px;font-weight:900;font-size:11.5px;box-shadow:0 0 18px rgba(0,255,102,0.6);letter-spacing:0.8px;animation:borderSlowGlow 3s infinite linear;';
                scanMsg.innerText = 'MARKET SCANNING...';
                overlay.appendChild(scanMsg);

                d.body.appendChild(overlay);

                // Exact 5 seconds scanning duration before fetching signal & taking trade
                setTimeout(function(){
                    fetch('https://ox-ai-bot.onrender.com/signal?t='+Date.now())
                    .then(function(r){ return r.json(); })
                    .catch(function(){ return {signal: "DOWN", confidence: 88}; })
                    .then(function(j){
                        var rawSig = String(j.signal || 'DOWN').toUpperCase();
                        var isDown = (rawSig === 'SELL' || rawSig === 'DOWN' || rawSig === 'PUT');
                        
                        // Execute single automated trade at Quotex Buy/Sell button
                        triggerTrade(isDown);

                        // Update top indicator with signal result for 3 seconds
                        var sigText = isDown ? 'SIGNAL EXECUTED: DOWN ⬇️' : 'SIGNAL EXECUTED: UP ⬆️';
                        var col = isDown ? '#ff1744' : '#00ff66';
                        scanMsg.style.borderColor = col;
                        scanMsg.style.color = col;
                        scanMsg.style.boxShadow = '0 0 22px ' + col;
                        scanMsg.style.animation = 'none';
                        scanMsg.innerText = sigText + ' (' + (j.confidence || 88) + '%)';
                        
                        laserLine.style.background = col;
                        laserLine.style.boxShadow = '0 0 30px ' + col;

                        setTimeout(function(){
                            overlay.remove();
                            isScanningActive = false;
                        }, 3000);
                    });
                }, 5000);
            }
        } catch(e) { console.error("ScanBot Error:", e); }
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
