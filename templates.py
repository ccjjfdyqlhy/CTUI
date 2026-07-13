import json


CSS = r""":root{--terminal-font-family:'LanaPixel',sans-serif;--terminal-font-size:16px}
*{margin:0;padding:0;box-sizing:border-box;user-select:none;-webkit-user-select:none}
body{margin:0;padding:0;background:#000;color:#fff;height:100vh;display:flex;justify-content:center;align-items:center;overflow:hidden;font-family:var(--terminal-font-family)}
#terminal{width:100vw;height:100vh;display:flex;justify-content:center;align-items:center}
.terminal-content{width:80%;max-width:700px;background:rgba(0,0,0,.9);padding:20px;position:relative;min-height:300px}
.panel{display:none}.panel.active{display:block}
.component-container{position:relative;display:inline-flex;flex-direction:column;gap:10px;align-items:flex-start;width:100%}
.component-row{display:flex;flex-direction:row;align-items:center;gap:15px;width:100%;flex-wrap:wrap}
.cursor-highlight{position:absolute;background:rgba(255,255,255,.35);pointer-events:none;transition:top .15s cubic-bezier(.4,0,.2,1),left .15s cubic-bezier(.4,0,.2,1),height .15s cubic-bezier(.4,0,.2,1),width .15s cubic-bezier(.4,0,.2,1),opacity .3s ease;z-index:10}
.cursor-highlight.activated{background:#fff!important}
.cursor-highlight.editing-special{background:rgba(255,255,255,.7)}
.terminal-component{background:transparent;border:none;color:#fff;position:relative;width:auto;min-width:0;padding:10px;font-size:var(--terminal-font-size);transition:all .3s ease;pointer-events:none;white-space:nowrap;font-family:var(--terminal-font-family)}
.terminal-component[data-type="text"]{opacity:.7;font-size:calc(var(--terminal-font-size)*.9);padding:2px 4px;cursor:default}
.terminal-component[data-type="html"]{opacity:1;padding:2px 4px;white-space:normal;pointer-events:none}
button.terminal-component{text-align:left;padding:2px 4px;font-size:calc(var(--terminal-font-size)*1.1);cursor:pointer;pointer-events:all;font-family:var(--terminal-font-family)}
button.terminal-component:hover{background:rgba(255,255,255,.5)}
input.terminal-component{outline:none;padding:2px 4px;font-size:calc(var(--terminal-font-size)*.9);font-family:var(--terminal-font-family);color:#fff;background:transparent;border:1px solid rgba(255,255,255,.3);pointer-events:all;caret-color:#fff}
input.terminal-component:focus{background:rgba(255,255,255,.5)}
.terminal-component[data-type="long-press"]{position:relative;overflow:hidden;z-index:1;pointer-events:all}
.terminal-component[data-type="long-press"] .charge-bar{position:absolute;bottom:0;left:0;width:100%;height:0%;background:#2a9d8f;pointer-events:none;z-index:-1}
.terminal-component[data-type="switch"]{pointer-events:all}
.terminal-component[data-type="toggle"]{pointer-events:all}
.terminal-component[data-type="toggle"][data-checked="true"]{background:rgba(42,157,143,.3)}
.terminal-component[data-type="toggle"][data-checked="true"]::after{content:' ✓'}
.digit-string-component{display:flex;gap:10px;padding:2px 4px;font-size:calc(var(--terminal-font-size)*1.3);letter-spacing:5px;pointer-events:all}
.digit-string-component.error{background:rgba(255,0,0,.5);animation:shake .5s cubic-bezier(.36,.07,.19,.97) both}
.digit-char{position:relative;padding:0 5px;transition:background-color .2s,color .2s;color:#fff}
.digit-string-component.editing .digit-char.selected{background:#fff;color:#000}
.digit-string-component.editing .digit-char.selected::before,.digit-string-component.editing .digit-char.selected::after{content:'';position:absolute;left:50%;transform:translateX(-50%);width:0;height:0;border-left:6px solid transparent;border-right:6px solid transparent}
.digit-string-component.editing .digit-char.selected::before{top:-10px;border-bottom:8px solid #fff}
.digit-string-component.editing .digit-char.selected::after{bottom:-10px;border-top:8px solid #fff}

.terminal-component[data-type="slider"]{display:flex;align-items:center;gap:8px;padding:2px 4px;pointer-events:all;white-space:nowrap}
.slider-label{opacity:.7;font-size:calc(var(--terminal-font-size)*.9)}
.slider-value{min-width:3em;text-align:right;font-size:calc(var(--terminal-font-size)*1.1)}
.slider-track{position:relative;width:120px;height:4px;background:rgba(255,255,255,.2);overflow:hidden}
.slider-fill{position:absolute;top:0;left:0;height:100%;background:var(--bar-color,#fff);transition:width .1s linear}
.slider-btn{background:transparent;border:1px solid rgba(255,255,255,.4);color:#fff;width:24px;height:24px;cursor:pointer;pointer-events:all;font-family:var(--terminal-font-family);font-size:14px;display:flex;align-items:center;justify-content:center;transition:background .2s}
.slider-btn:hover{background:rgba(255,255,255,.3)}
.slider-btn:active{background:rgba(255,255,255,.5)}

.terminal-component[data-type="progress"]{display:flex;align-items:center;gap:10px;padding:4px;pointer-events:none;width:100%}
.progress-label{opacity:.7;font-size:calc(var(--terminal-font-size)*.8);min-width:60px}
.progress-track{flex:1;height:4px;background:rgba(255,255,255,.15);overflow:hidden;position:relative}
.progress-fill{position:absolute;top:0;left:0;height:100%;background:var(--bar-color,#2a9d8f);transition:width .3s ease}
.progress-text{font-size:calc(var(--terminal-font-size)*.8);min-width:3em;text-align:right;opacity:.8}

.terminal-component[data-type="dragbar"]{display:flex;align-items:center;gap:10px;padding:4px;pointer-events:none;width:100%}
.dragbar-label{opacity:.7;font-size:calc(var(--terminal-font-size)*.8);min-width:60px}
.dragbar-track{flex:1;height:4px;background:rgba(255,255,255,.15);overflow:hidden;position:relative}
.dragbar-fill{position:absolute;top:0;left:0;height:100%;background:var(--bar-color,#2a9d8f);transition:width .05s linear}
.dragbar-thumb{position:absolute;top:50%;transform:translate(-50%,-50%);width:12px;height:12px;background:#fff;pointer-events:none;transition:left .05s linear}
.dragbar-value{font-size:calc(var(--terminal-font-size)*.8);min-width:3em;text-align:right;opacity:.8}

.terminal-component[data-type="scroll-view"]{pointer-events:all;width:100%;overflow:hidden;border:1px solid rgba(255,255,255,.2);padding:0}
.scroll-content{width:100%;height:100%;overflow-y:auto;padding:8px;white-space:pre-wrap;word-break:break-all;font-family:var(--terminal-font-family);font-size:calc(var(--terminal-font-size)*.85);color:rgba(255,255,255,.85);pointer-events:all;cursor:text;user-select:text;-webkit-user-select:text}
.scroll-content::-webkit-scrollbar{width:6px}
.scroll-content::-webkit-scrollbar-track{background:rgba(255,255,255,.05)}
.scroll-content::-webkit-scrollbar-thumb{background:rgba(255,255,255,.3);border-radius:3px}

.terminal-component[data-type="image"]{padding:4px;pointer-events:none}
.terminal-image{max-width:100%;image-rendering:pixelated;border:1px solid rgba(255,255,255,.2)}

.terminal-component[data-type="table"]{padding:2px;pointer-events:none;width:100%;overflow-x:auto}
.terminal-component[data-type="table"] table{width:100%;border-collapse:collapse;font-size:calc(var(--terminal-font-size)*.85)}
.terminal-component[data-type="table"] th,.terminal-component[data-type="table"] td{border:1px solid rgba(255,255,255,.2);padding:4px 8px;text-align:left}
.terminal-component[data-type="table"] th{background:rgba(255,255,255,.1);font-weight:400;opacity:.9}
.terminal-component[data-type="table"] td{opacity:.75}

.dialog-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1000;display:none;pointer-events:none}
.dialog-overlay[data-visible="true"]{display:flex;align-items:center;justify-content:center;pointer-events:all}
.dialog-backdrop{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.7)}
.dialog-box{position:relative;background:#111;border:1px solid rgba(255,255,255,.3);padding:24px;min-width:280px;max-width:500px;text-align:center}
.dialog-title{font-size:calc(var(--terminal-font-size)*1.2);margin-bottom:12px;opacity:.9}
.dialog-message{font-size:calc(var(--terminal-font-size)*.9);margin-bottom:20px;opacity:.7;line-height:1.5}
.dialog-confirm{display:inline-block;padding:6px 20px;cursor:pointer;pointer-events:all;border:1px solid rgba(255,255,255,.4);transition:background .2s}
.dialog-confirm:hover{background:rgba(255,255,255,.3)}

.terminal-component[data-type="spinner"]{display:inline-flex;align-items:center;gap:8px;padding:2px 4px;pointer-events:none}
.spinner-anim{display:inline-block;animation:spin 1s steps(4) infinite}
@keyframes spin{0%{opacity:1}25%{opacity:.5}50%{opacity:.2}75%{opacity:.5}100%{opacity:1}}

.countdown-large-text{line-height:1.2;opacity:1;text-align:center;width:100%;padding:20px 0 !important;pointer-events:none}
.countdown-large-text span{display:block;font-size:.4em;letter-spacing:2px}

#typewriter-large-char-display{position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);font-family:'LanaPixel',sans-serif;font-size:80vh;color:#fff;opacity:0;visibility:hidden;transition:opacity .5s ease-out;line-height:1;z-index:100;pointer-events:none;image-rendering:pixelated;-webkit-font-smoothing:none;font-smooth:never}
#typewriter-large-char-display.visible{opacity:1;visibility:visible;transition:opacity .1s ease-in}
.typewriter-message{position:fixed;bottom:15%;left:50%;transform:translateX(-50%);font-size:var(--terminal-font-size);color:rgba(255,255,255,.7);transition:opacity .3s ease;opacity:1;visibility:visible;text-align:center;z-index:100;pointer-events:none}
.typewriter-message.hidden{opacity:0;visibility:hidden}

@keyframes shake{10%,90%{transform:translate3d(-1px,0,0)}20%,80%{transform:translate3d(2px,0,0)}30%,50%,70%{transform:translate3d(-4px,0,0)}40%,60%{transform:translate3d(4px,0,0)}}

.terminal-component[data-type="status"]{display:inline-flex;align-items:center;gap:6px;padding:2px 4px;pointer-events:none}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;animation:pulse-dot 2s infinite}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.4}}

.terminal-component[data-type="code"]{background:rgba(255,255,255,.05);padding:10px;font-size:calc(var(--terminal-font-size)*.85);line-height:1.4;white-space:pre-wrap;word-break:break-all;width:100%;font-family:'Courier New',monospace;pointer-events:none}

.terminal-component[data-type="log"]{width:100%;max-height:300px;overflow-y:auto;background:rgba(255,255,255,.03);padding:8px;font-size:calc(var(--terminal-font-size)*.8);line-height:1.3;font-family:'Courier New',monospace;pointer-events:all}
.terminal-component[data-type="log"] pre{white-space:pre-wrap;word-break:break-all;pointer-events:none}

.terminal-component[data-type="keypad"]{display:flex;flex-direction:column;gap:4px;padding:4px;pointer-events:all}
.keypad-row{display:flex;gap:4px;justify-content:center}
.keypad-key{width:40px;height:40px;background:transparent;border:1px solid rgba(255,255,255,.3);color:#fff;font-size:calc(var(--terminal-font-size)*1.1);font-family:var(--terminal-font-family);cursor:pointer;transition:background .2s;pointer-events:all}
.keypad-key:hover{background:rgba(255,255,255,.5)}
.keypad-key.active-key{background:rgba(255,255,255,.5)}

.terminal-component[data-type="separator"]{opacity:.3;font-size:calc(var(--terminal-font-size)*.7);letter-spacing:2px;width:100%;text-align:center;padding:4px 0;pointer-events:none}

.terminal-component[data-type="checkbox"]{pointer-events:all}
.terminal-component[data-type="checkbox"][data-checked="true"]{color:#2a9d8f}

.terminal-component[data-type="dropdown"]{pointer-events:all}

.modal-overlay{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1000;display:none;pointer-events:none}
.modal-overlay[data-visible="true"]{display:flex;align-items:center;justify-content:center;pointer-events:all}
.modal-backdrop{position:absolute;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.8)}
.modal-box{position:relative;background:#111;border:1px solid rgba(255,255,255,.3);padding:20px;min-width:300px;max-width:80%;text-align:center}
.modal-title{font-size:calc(var(--terminal-font-size)*1.2);margin-bottom:15px;opacity:.9}
.modal-body{font-size:calc(var(--terminal-font-size)*.9);margin-bottom:15px;opacity:.7;line-height:1.5}
.modal-confirm{display:inline-block;padding:6px 20px;cursor:pointer;pointer-events:all;border:1px solid rgba(255,255,255,.4);transition:background .2s}
.modal-confirm:hover{background:rgba(255,255,255,.3)}

#terminal-cursor{position:fixed;pointer-events:none;z-index:9999;background:rgba(255,255,255,.25);width:0;height:0;transition:width .12s ease,height .12s ease,top .12s ease,left .12s ease,background .15s,opacity .1s linear;display:none;opacity:1}
#terminal-cursor.fading{opacity:0!important;transition:opacity .4s linear!important}
#terminal-cursor.snapped{background:rgba(255,255,255,.35)}
#terminal-cursor.clicked{background:#fff!important;transition:width .08s,height .08s,top .08s,left .08s,background 0s}
.keyboard-cursor{opacity:1}
*{cursor:none!important}
:hover{cursor:none!important}
.terminal-component.hover{background:rgba(255,255,255,.3)}

.terminal-component[data-type="log-gen"]{width:100%;height:200px;overflow-y:auto;background:rgba(255,255,255,.03);padding:8px;font-size:calc(var(--terminal-font-size)*.8);line-height:1.3;font-family:'Courier New',monospace;pointer-events:none;position:relative}
.log-gen-line{white-space:pre-wrap;word-break:break-all;opacity:.85}

.terminal-component[data-type="choice-group"]{display:flex;flex-direction:column;gap:8px;padding:8px;width:100%;pointer-events:all}
.choice-btn{padding:8px 16px;text-align:left;background:transparent;border:1px solid rgba(255,255,255,.25);color:#fff;font-family:var(--terminal-font-family);font-size:calc(var(--terminal-font-size)*.95);cursor:pointer;pointer-events:all;transition:all .2s ease;opacity:0;animation:choice-in .3s ease forwards}
.choice-btn:nth-child(1){animation-delay:0s}
.choice-btn:nth-child(2){animation-delay:.1s}
.choice-btn:nth-child(3){animation-delay:.2s}
.choice-btn:nth-child(4){animation-delay:.3s}
.choice-btn:nth-child(5){animation-delay:.4s}
.choice-btn:hover{background:rgba(255,255,255,.9);color:#000;transform:translateX(8px)}
.choice-btn:active{background:#fff;color:#000}
.choice-btn.active-choice{background:rgba(255,255,255,.9);color:#000;transform:translateX(8px)}
@keyframes choice-in{0%{opacity:0;transform:translateY(10px)}100%{opacity:1;transform:translateY(0)}}

.terminal-component[data-type="audio-toggle"]{pointer-events:all;font-size:calc(var(--terminal-font-size)*1.1)}

.terminal-component[data-type="preloader"]{width:100%;padding:20px;text-align:center;pointer-events:none}
.preloader-label{font-size:calc(var(--terminal-font-size)*.9);opacity:.7;margin-bottom:12px}
.preloader-track{width:60%;height:3px;background:rgba(255,255,255,.15);margin:0 auto;overflow:hidden;position:relative}
.preloader-fill{position:absolute;top:0;left:0;height:100%;background:#fff;width:0%;transition:width .4s ease}

.terminal-component[data-type="scroll-panel"]{overflow-y:auto;pointer-events:all;border:1px solid rgba(255,255,255,.1);padding:4px}
.terminal-component[data-type="scroll-panel"]::-webkit-scrollbar{width:4px}
.terminal-component[data-type="scroll-panel"]::-webkit-scrollbar-track{background:rgba(255,255,255,.05)}
.terminal-component[data-type="scroll-panel"]::-webkit-scrollbar-thumb{background:rgba(255,255,255,.2);border-radius:2px}

.terminal-component[data-type="memory-match"]{width:100%;padding:8px;pointer-events:all}
.mm-timer{text-align:center;font-size:calc(var(--terminal-font-size)*1.2);margin-bottom:8px;opacity:.8}
.mm-grid{display:grid;gap:6px;justify-content:center}
.mm-cell{width:60px;height:60px;border:1px solid rgba(255,255,255,.25);display:flex;align-items:center;justify-content:center;cursor:pointer;pointer-events:all;font-size:calc(var(--terminal-font-size)*.75);transition:all .2s ease;user-select:none;background:transparent;color:#fff;font-family:var(--terminal-font-family)}
.mm-cell.revealed{background:rgba(255,255,255,.15);border-color:rgba(255,255,255,.5)}
.mm-cell.matched{background:rgba(42,157,143,.3);border-color:#2a9d8f;opacity:.7;pointer-events:none}
.mm-cell.shake{animation:shake .3s cubic-bezier(.36,.07,.19,.97) both}

.terminal-component[data-type="command-console"]{width:100%;pointer-events:all;position:relative}
.cc-log{width:100%;max-height:200px;overflow-y:auto;padding:4px;font-size:calc(var(--terminal-font-size)*.8);line-height:1.3;font-family:'Courier New',monospace;background:rgba(255,255,255,.03);margin-bottom:4px}
.cc-log-line{white-space:pre-wrap;word-break:break-all;opacity:.85}
.cc-input-line{display:flex;align-items:center;gap:4px;padding:2px 4px}
.cc-prompt{opacity:.5;font-size:calc(var(--terminal-font-size)*.9)}
.cc-input{flex:1;background:transparent;border:none;color:#fff;font-family:var(--terminal-font-family);font-size:calc(var(--terminal-font-size)*.9);outline:none;caret-color:#fff}
.cc-input-line.err .cc-input{color:#ff4444}

.terminal-component[data-type="glitch-text"]{position:relative;display:inline}
@keyframes glitch-skew{0%{transform:skew(0deg)}20%{transform:skew(-2deg)}40%{transform:skew(1deg)}60%{transform:skew(-3deg)}80%{transform:skew(2deg)}100%{transform:skew(0deg)}}
@keyframes glitch-shift{0%{text-shadow:-2px 0 rgba(255,0,0,.5),2px 0 rgba(0,255,255,.5)}25%{text-shadow:2px 0 rgba(255,0,0,.5),-2px 0 rgba(0,255,255,.5)}50%{text-shadow:-1px 0 rgba(255,0,0,.3),1px 0 rgba(0,255,255,.3)}75%{text-shadow:1px 0 rgba(255,0,0,.3),-1px 0 rgba(0,255,255,.3)}100%{text-shadow:-2px 0 rgba(255,0,0,.5),2px 0 rgba(0,255,255,.5)}}
.glitch-active{animation:glitch-skew .3s ease infinite alternate,glitch-shift .2s ease infinite alternate}

.terminal-component[data-type="webgl-shader"]{pointer-events:none}
.shader-canvas{width:100%;height:100%;display:block}

.terminal-component[data-type="story-text"]{width:100%;pointer-events:all;position:relative}
.story-scroll{width:100%;max-height:300px;overflow-y:auto;padding:8px;-webkit-mask-image:linear-gradient(to bottom,transparent 0,#000 24px,#000 90%,transparent 100%);pointer-events:all}
.story-scroll::-webkit-scrollbar{width:4px}
.story-scroll::-webkit-scrollbar-track{background:rgba(255,255,255,.05)}
.story-scroll::-webkit-scrollbar-thumb{background:rgba(255,255,255,.2);border-radius:2px}
.story-line{margin-bottom:12px;opacity:0;animation:story-line-in .3s ease forwards;pointer-events:none}
.story-line .speaker{display:block;font-size:calc(var(--terminal-font-size)*.7);opacity:.5;letter-spacing:2px;margin-bottom:2px}
.story-line .text{font-size:calc(var(--terminal-font-size)*.9);line-height:1.5;opacity:.9;white-space:pre-wrap}
.story-line .text .char{opacity:0}
@keyframes story-line-in{0%{opacity:0;transform:translateY(8px)}100%{opacity:1;transform:translateY(0)}}
.story-continue{text-align:center;font-size:calc(var(--terminal-font-size)*.7);opacity:0;letter-spacing:3px;padding:8px;transition:opacity .4s ease;pointer-events:none}
.story-continue.show{opacity:.6}
"""


JS_TERMINAL = r"""
(function() {
'use strict';

class CARNIVALTerminal {
    constructor(config) {
        this.config = Object.assign({
            defaultPanel: 'panel-main',
            longPressDuration: 2000,
        }, config);
        this.activePanel = null;
        this.activePanelId = this.config.defaultPanel;
        this.cursor = null;
        this.grid = [];
        this.currentRowIndex = 0;
        this.currentColIndex = 0;
        this.longPressTimer = null;
        this.longPressStartTime = 0;
        this.isCharging = false;
        this.isEditingDigits = false;
        this.activeDigitComponent = null;
        this.activeDigitIndex = 0;
        this.isEditingSlider = false;
        this.activeSliderComponent = null;
        this.isEditingKeypad = false;
        this.activeKeypadComponent = null;
        this.activeKeypadRow = 0;
        this.activeKeypadCol = 0;
        this.isEditingChoices = false;
        this.activeChoiceComponent = null;
        this.activeChoiceIndex = 0;
        this.countdownInterval = null;
        this.typewriterInputBuffer = '';
        this.currentFontSize = 16;
        this.minFontSize = 12;
        this.maxFontSize = 24;
        this.callbackBase = this.config.apiBase || '/api';
        this.mouseCursor = null;
        this.snapDistance = 30;
        this.snappedComp = null;
        this.isMouseDown = false;
        this.mouseIdleTimer = null;
        this.mouseFadeTimer = null;
        this.isMouseIdle = false;
        this.mouseIdleDelay = 3000;
        this.fadeDuration = 400;

        this.init();
    }

    init() {
        this.mouseCursor = document.createElement('div');
        this.mouseCursor.id = 'terminal-cursor';
        document.body.appendChild(this.mouseCursor);

        document.querySelectorAll('.panel').forEach(panel => {
            if (panel.id === this.activePanelId) {
                panel.classList.add('active');
                this.activePanel = panel;
            }
        });
        if (!this.activePanel) {
            this.activePanel = document.querySelector('.panel.active') || document.querySelector('.panel');
            if (this.activePanel) {
                this.activePanel.classList.add('active');
                this.activePanelId = this.activePanel.id;
            }
        }
        this.initializeActivePanel();
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        document.addEventListener('keyup', this.handleKeyUp.bind(this));
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mousedown', this.handleMouseDown.bind(this));
        document.addEventListener('mouseup', this.handleMouseUp.bind(this));
        document.addEventListener('click', this.handleClick.bind(this));
    }

    initializeActivePanel() {
        this.stopDigitEdit();
        this.stopSliderEdit();
        this.stopKeypadEdit();
        if (this.cursor) { this.cursor.classList.remove('activated'); this.cursor.style.transition = 'none'; this.cursor.style.removeProperty('opacity'); }
        this.cursor = this.activePanel.querySelector('.cursor-highlight');
        if (!this.cursor) {
            this.cursor = document.createElement('div');
            this.cursor.className = 'cursor-highlight keyboard-cursor';
            this.activePanel.querySelector('.component-container')?.appendChild(this.cursor);
        } else {
            this.cursor.classList.add('keyboard-cursor');
        }
        this.cursor.style.transition = 'none';
        this.cursor.style.width = '0';
        this.cursor.style.height = '0';
        void this.cursor.offsetHeight;
        this.cursor.style.transition = '';
        this.applyCustomTextStyles();
        this.initializeSwitchComponents();
        this.initializeDropdownComponents();
        this.buildGrid();
        this.currentRowIndex = 0;
        this.currentColIndex = 0;
        if (this.grid.length > 0 && this.grid[0].length > 0) {
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    this.updateHighlight();
                });
            });
        }
        const behavior = this.activePanel.dataset.behavior;
        if (behavior === 'countdown') this.startCountdown();
        if (behavior === 'typewriter') this.resetTypewriter();
        this.activePanel.querySelectorAll('[data-type="log-gen"]').forEach(el => this.initLogGenerator(el));
        this.activePanel.querySelectorAll('[data-type="preloader"]').forEach(el => this.initPreloader(el));
        this.activePanel.querySelectorAll('[data-type="story-text"]').forEach(el => this.initStoryText(el));
        this.activePanel.querySelectorAll('[data-type="memory-match"]').forEach(el => this.initMemoryMatch(el));
        this.activePanel.querySelectorAll('[data-type="command-console"]').forEach(el => this.initCommandConsole(el));
        this.activePanel.querySelectorAll('[data-type="glitch-text"]').forEach(el => this.initGlitchText(el));
        this.activePanel.querySelectorAll('[data-type="webgl-shader"]').forEach(el => this.initWebGLShader(el));
    }

    buildGrid() {
        this.grid = [];
        const rows = this.activePanel.querySelectorAll('.component-row');
        rows.forEach(row => {
            const components = Array.from(row.querySelectorAll(
                'button.terminal-component, input.terminal-component, ' +
                '.digit-string-component, [data-type="switch"], [data-type="toggle"], ' +
                '[data-type="slider"], [data-type="checkbox"], [data-type="dropdown"], ' +
                '[data-type="keypad"], [data-type="long-press"], [data-type="digit-string"], ' +
                '[data-type="dragbar"], [data-type="choice-group"], [data-type="audio-toggle"], [data-type="story-text"]'
            ));
            if (components.length > 0) this.grid.push(components);
        });
    }

    applyCustomTextStyles() {
        this.activePanel.querySelectorAll('[data-type="text"]').forEach(el => {
            const sz = el.dataset.fontSize;
            const ff = el.dataset.fontFamily;
            if (sz) el.style.fontSize = sz;
            if (ff) el.style.fontFamily = ff;
        });
    }

    initializeSwitchComponents() {
        this.activePanel.querySelectorAll('[data-type="switch"]').forEach(sw => {
            const label = sw.dataset.label || '';
            const opts = (sw.dataset.options || '').split(',');
            let idx = parseInt(sw.dataset.currentIndex || '0', 10);
            if (isNaN(idx) || idx < 0 || idx >= opts.length) { idx = 0; sw.dataset.currentIndex = '0'; }
            sw.textContent = label + opts[idx];
        });
    }

    initializeDropdownComponents() {
        this.activePanel.querySelectorAll('[data-type="dropdown"]').forEach(dd => {
            const label = dd.dataset.label || '';
            const opts = (dd.dataset.options || '').split(',');
            let idx = parseInt(dd.dataset.currentIndex || '0', 10);
            if (isNaN(idx) || idx < 0 || idx >= opts.length) { idx = 0; dd.dataset.currentIndex = '0'; }
            dd.textContent = label + '[' + opts[idx] + ']';
        });
    }

    snapToComponent(comp) {
        if (!this.mouseCursor) return;
        this.snappedComp = comp;
        this.mouseCursor.classList.add('snapped');
        this.mouseCursor.classList.remove('fading');
        this.mouseCursor.style.removeProperty('opacity');
        if (this.cursor) { this.cursor.style.transition = 'none'; this.cursor.style.opacity = '0'; }
        const r = comp.getBoundingClientRect();
        this.mouseCursor.style.top = r.top + 'px';
        this.mouseCursor.style.left = r.left + 'px';
        this.mouseCursor.style.width = r.width + 'px';
        this.mouseCursor.style.height = r.height + 'px';
        this.mouseCursor.style.display = 'block';
        const container = this.activePanel?.querySelector('.component-container');
        if (container && this.cursor) {
            const cr = container.getBoundingClientRect();
            this.cursor.style.top = (r.top - cr.top) + 'px';
            this.cursor.style.left = (r.left - cr.left) + 'px';
            this.cursor.style.width = r.width + 'px';
            this.cursor.style.height = r.height + 'px';
        }
        this.grid.forEach(r => r.forEach(c => c.classList.remove('hover')));
        comp.classList.add('hover');
    }

    handleMouseMove(e) {
        if (this.isEditingDigits || this.isEditingSlider || this.isEditingKeypad) {
            this.mouseCursor.style.display = 'none';
            return;
        }
        if (this.mouseIdleTimer) { clearTimeout(this.mouseIdleTimer); this.mouseIdleTimer = null; }
        if (this.mouseFadeTimer) { clearTimeout(this.mouseFadeTimer); this.mouseFadeTimer = null; }
        if (this.isMouseIdle) {
            this.isMouseIdle = false;
            this.mouseCursor.classList.remove('fading');
            this.mouseCursor.style.removeProperty('opacity');
            this.mouseCursor.style.display = 'block';
            if (this.cursor) { this.cursor.style.transition = ''; this.cursor.style.opacity = '0'; }
        }
        const all = this.activePanel?.querySelectorAll(
            'button.terminal-component, input.terminal-component, ' +
            '.digit-string-component, [data-type="switch"], [data-type="toggle"], ' +
            '[data-type="slider"], [data-type="checkbox"], [data-type="dropdown"], ' +
            '[data-type="keypad"], [data-type="long-press"], [data-type="digit-string"], ' +
            '[data-type="dragbar"], [data-type="choice-group"], [data-type="audio-toggle"], [data-type="story-text"]'
        );
        if (!all || all.length === 0) {
            this.mouseCursor.style.display = 'none';
            return;
        }
        let nearest = null, minDist = this.snapDistance;
        all.forEach(el => {
            const r = el.getBoundingClientRect();
            const cx = r.left + r.width / 2, cy = r.top + r.height / 2;
            const dx = e.clientX - cx, dy = e.clientY - cy;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < minDist) { minDist = dist; nearest = el; }
        });
        if (nearest && nearest.offsetParent) {
            if (this.cursor) { this.cursor.style.opacity = '0'; this.cursor.style.transition = ''; }
            this.snapToComponent(nearest);
            this.grid.forEach(r => r.forEach(c => c.classList.remove('active')));
            nearest.classList.add('active');
        } else {
            this.snappedComp = null;
            this.mouseCursor.classList.remove('snapped');
            this.mouseCursor.style.display = 'block';
            this.mouseCursor.style.width = '20px';
            this.mouseCursor.style.height = '24px';
            this.mouseCursor.style.top = (e.clientY - 12) + 'px';
            this.mouseCursor.style.left = (e.clientX - 10) + 'px';
            if (this.cursor) { this.cursor.style.transition = ''; this.cursor.style.opacity = '0'; }
            this.grid.forEach(r => r.forEach(c => c.classList.remove('active', 'hover')));
        }
        this.mouseIdleTimer = setTimeout(() => {
            this.isMouseIdle = true;
            this.mouseCursor.style.removeProperty('opacity');
            this.mouseCursor.classList.add('fading');
            this.mouseFadeTimer = setTimeout(() => {
                this.mouseCursor.style.display = 'none';
                if (this.cursor) {
                    this.cursor.style.transition = 'opacity .4s ease, top .15s cubic-bezier(.4,0,.2,1), left .15s cubic-bezier(.4,0,.2,1), height .15s cubic-bezier(.4,0,.2,1), width .15s cubic-bezier(.4,0,.2,1)';
                    this.cursor.style.opacity = '0';
                    void this.cursor.offsetHeight;
                    this.updateHighlight();
                    this.cursor.style.opacity = '1';
                }
            }, this.fadeDuration);
        }, this.mouseIdleDelay);
    }

    handleMouseDown(e) {
        const comp = this.snappedComp;
        if (!comp) return;
        this.isMouseDown = true;
        this.mouseCursor.classList.add('clicked');
        if (this.cursor) { this.cursor.style.transition = ''; this.cursor.style.opacity = '0'; }
        for (let ri = 0; ri < this.grid.length; ri++) {
            for (let ci = 0; ci < this.grid[ri].length; ci++) {
                if (this.grid[ri][ci] === comp) {
                    this.currentRowIndex = ri;
                    this.currentColIndex = ci;
                    break;
                }
            }
        }
        this.updateHighlight();
        this.cursor?.classList.add('activated');
        const type = comp.dataset.type;
        if (type === 'digit-string') { this.startDigitEdit(comp); }
        else if (type === 'slider') { this.startSliderEdit(comp); }
        else if (type === 'keypad') { this.startKeypadEdit(comp); }
        else if (type === 'long-press') {
            this.activateComponent(comp);
            this.cancelLongPress();
        }
        else if (type === 'dragbar') { this.startDragbarEdit(e, comp); }
        else if (type === 'choice-group') { this.startChoiceEdit(comp); }
        else if (type === 'audio-toggle') { this.toggleAudio(comp); }
        else if (type === 'story-text') {
            const sc = comp.querySelector('.story-scroll');
            if (sc) sc.click();
        }
        else { this.activateComponent(comp); }
    }

    handleMouseUp(e) {
        this.isMouseDown = false;
        if (this.mouseCursor) this.mouseCursor.classList.remove('clicked');
        if (this.cursor) this.cursor.classList.remove('activated');
    }

    handleClick(e) {
        const key = e.target.closest('.keypad-key');
        if (key) { this.handleKeypadKey(key); return; }
        const choice = e.target.closest('.choice-btn');
        if (choice) {
            const group = choice.closest('[data-type="choice-group"]');
            if (group) {
                if (this.isEditingChoices) this.stopChoiceEdit();
                if (group.dataset.callbackId) {
                    const idx = choice.dataset.choiceIndex;
                    fetch(this.callbackBase + '/callback/' + group.dataset.callbackId, {
                        method: 'POST', headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({value: idx})
                    }).then(r => r.json()).then(result => {
                        if (result.action) this.handleCallbackResult(result);
                    }).catch(() => {});
                }
            }
            return;
        }
        const backdrop = e.target.closest('.dialog-backdrop, .modal-backdrop');
        if (backdrop) {
            const action = backdrop.dataset.action;
            const target = backdrop.dataset.target;
            if (action === 'dialog-close') this.closeDialog(target);
            else if (action === 'modal-close') this.closeModal(target);
            return;
        }
        const comp = e.target.closest('.dialog-confirm, .modal-confirm');
        if (comp) {
            const target = comp.dataset.target;
            const p = comp.closest('.dialog-overlay, .modal-overlay');
            if (p) p.dataset.visible = 'false';
            if (this.grid.length > 0) setTimeout(() => this.updateHighlight(), 50);
            return;
        }
    }

    switchPanel(panelId) {
        if (this.activePanel?.dataset?.behavior === 'countdown') this.stopCountdown();
        const newPanel = document.getElementById(panelId);
        if (!newPanel || newPanel === this.activePanel) return;
        if (this.activePanel) this.activePanel.classList.remove('active');
        newPanel.classList.add('active');
        this.activePanel = newPanel;
        this.activePanelId = panelId;
        this.initializeActivePanel();
        this.mouseCursor.style.display = 'none';
    }

    updateHighlight() {
        if (!this.grid[this.currentRowIndex] || !this.grid[this.currentRowIndex][this.currentColIndex]) return;
        const comp = this.grid[this.currentRowIndex][this.currentColIndex];
        if (!comp || !this.cursor) return;
        this.grid.forEach(r => r.forEach(c => c.classList.remove('active')));
        comp.classList.add('active');
        const pos = () => {
            if (!comp.offsetParent) { requestAnimationFrame(pos); return; }
            const container = this.activePanel?.querySelector('.component-container');
            if (container) {
                const cr = container.getBoundingClientRect();
                const r = comp.getBoundingClientRect();
                this.cursor.style.top = (r.top - cr.top) + 'px';
                this.cursor.style.left = (r.left - cr.left) + 'px';
            } else {
                this.cursor.style.top = comp.offsetTop + 'px';
                this.cursor.style.left = comp.offsetLeft + 'px';
            }
            this.cursor.style.width = comp.offsetWidth + 'px';
            this.cursor.style.height = comp.offsetHeight + 'px';
            const sp = comp.closest('[data-type="scroll-panel"]');
            if (sp) {
                const cr = comp.getBoundingClientRect();
                const sr = sp.getBoundingClientRect();
                if (cr.bottom > sr.bottom) sp.scrollTop += cr.bottom - sr.bottom + 4;
                else if (cr.top < sr.top) sp.scrollTop -= sr.top - cr.top + 4;
            }
            if (this.mouseCursor && this.mouseCursor.style.display !== 'none') {
                const r = comp.getBoundingClientRect();
                this.mouseCursor.style.top = r.top + 'px';
                this.mouseCursor.style.left = r.left + 'px';
                this.mouseCursor.style.width = r.width + 'px';
                this.mouseCursor.style.height = r.height + 'px';
            }
        };
        requestAnimationFrame(pos);
    }

    handleKeyDown(e) {
        if (this.activePanel?.dataset?.behavior === 'typewriter' && /^[a-zA-Z]$/.test(e.key) && !e.repeat) {
            e.preventDefault();
            this.handleTypewriterLetterDown(e.key);
            return;
        }
        if (this.isEditingDigits) { this.handleDigitEdit(e); return; }
        if (this.isEditingSlider) { this.handleSliderEdit(e); return; }
        if (this.isEditingKeypad) { this.handleKeypadEdit(e); return; }
        if (this.isEditingChoices) { this.handleChoiceEdit(e); return; }
        if (this.grid.length === 0) return;

        const activeEl = document.activeElement;
        if (activeEl?.tagName === 'INPUT' && !['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Enter','Escape'].includes(e.key)) return;
        if (activeEl?.tagName === 'INPUT' && ['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key)) activeEl.blur();

        let moved = false, newRow = this.currentRowIndex, newCol = this.currentColIndex;
        switch (e.key) {
            case 'ArrowUp':
                e.preventDefault();
                if (newRow > 0) { newRow--; newCol = Math.min(this.currentColIndex, this.grid[newRow].length - 1); moved = true; }
                break;
            case 'ArrowDown':
                e.preventDefault();
                if (newRow < this.grid.length - 1) { newRow++; newCol = Math.min(this.currentColIndex, this.grid[newRow].length - 1); moved = true; }
                break;
            case 'ArrowLeft':
                e.preventDefault();
                if (newCol > 0) { newCol--; moved = true; }
                break;
            case 'ArrowRight':
                e.preventDefault();
                if (newCol < this.grid[this.currentRowIndex].length - 1) { newCol++; moved = true; }
                break;
            case 'Enter':
                e.preventDefault();
                if (activeEl?.tagName === 'INPUT') {
                    const inputComp = this.grid[this.currentRowIndex]?.[this.currentColIndex];
                    if (inputComp && inputComp.dataset.callbackId) this.triggerCallback(inputComp);
                    activeEl.blur();
                    return;
                }
                this.activateCurrentComponent(e);
                return;
            case 'Escape':
                e.preventDefault();
                if (activeEl?.tagName === 'INPUT') { activeEl.blur(); return; }
                const visibleDialog = document.querySelector('.dialog-overlay[data-visible="true"]');
                if (visibleDialog) { visibleDialog.dataset.visible = 'false'; }
                const visibleModal = document.querySelector('.modal-overlay[data-visible="true"]');
                if (visibleModal) { visibleModal.dataset.visible = 'false'; }
                return;
        }
        if (moved) {
            this.cancelLongPress();
            this.currentRowIndex = newRow;
            this.currentColIndex = newCol;
            this.updateHighlight();
        }
    }

    handleKeyUp(e) {
        if (this.activePanel?.dataset?.behavior === 'typewriter' && /^[a-zA-Z]$/.test(e.key)) {
            e.preventDefault();
            this.handleTypewriterLetterUp();
            return;
        }
        if (e.key === 'Enter') {
            const cursor = this.cursor;
            if (cursor) { cursor.classList.remove('activated'); }
            this.cancelLongPress();
        }
    }

    activateCurrentComponent(e) {
        const comp = this.grid[this.currentRowIndex]?.[this.currentColIndex];
        if (!comp) return;
        this.cursor?.classList.add('activated');
        const type = comp.dataset.type;
        if (type === 'digit-string') { this.startDigitEdit(comp); return; }
        if (type === 'slider') { this.startSliderEdit(comp); return; }
        if (type === 'keypad') { this.startKeypadEdit(comp); return; }
        if (type === 'choice-group') { this.startChoiceEdit(comp); return; }
        if (type === 'long-press') { if (!e.repeat && !this.isCharging) this.startLongPress(comp); return; }
        if (type === 'dragbar') { this.startDragbarEdit(e, comp); return; }
        this.activateComponent(comp);
    }

    activateComponent(comp) {
        const tag = comp.tagName.toLowerCase();
        if (tag === 'input') { comp.focus(); return; }
        const type = comp.dataset.type;
        if (type === 'switch' || type === 'toggle') { this.toggleSwitch(comp); return; }
        if (type === 'checkbox') { this.toggleCheckbox(comp); return; }
        if (type === 'dropdown') { this.cycleDropdown(comp); return; }
        if (type === 'choice-group') { return; }
        if (type === 'audio-toggle') { this.toggleAudio(comp); return; }
        if (type === 'story-text') {
            const sc = comp.querySelector('.story-scroll');
            if (sc) {
                sc.dispatchEvent(new PointerEvent('pointerdown', {bubbles: true}));
                sc.dispatchEvent(new PointerEvent('pointerup', {bubbles: true}));
                sc.click();
            }
            return;
        }
        const action = comp.dataset.action;
        const target = comp.dataset.target;
        if (action === 'switch-panel' && target) { this.switchPanel(target); return; }
        if (action === 'callback') { this.triggerCallback(comp); return; }
        if (action === 'dialog-open') { this.openDialog(comp.dataset.target); return; }
        if (action === 'dialog-close') { this.closeDialog(comp.dataset.target); return; }
        if (action === 'modal-open') { this.openModal(comp.dataset.target); return; }
        if (action === 'modal-close') { this.closeModal(comp.dataset.target); return; }
        if (action === 'change-font-size') { this.changeFontSize(comp.dataset.value); return; }
    }

    toggleAudio(comp) {
        const muted = comp.dataset.muted === 'true';
        comp.dataset.muted = muted ? 'false' : 'true';
        comp.textContent = muted ? '[🔊]' : '[🔇]';
        if (comp.dataset.callbackId) this.triggerCallback(comp);
    }

    initLogGenerator(comp) {
        if (comp.dataset._logStarted) return;
        comp.dataset._logStarted = 'true';
        const lines = JSON.parse(comp.dataset.lines || '[]');
        const speed = parseInt(comp.dataset.speed) || 50;
        const maxLines = parseInt(comp.dataset.maxLines) || 50;
        let idx = 0;
        comp.innerHTML = '';
        const append = () => {
            if (idx >= lines.length) idx = 0;
            const line = document.createElement('div');
            line.className = 'log-gen-line';
            line.textContent = lines[idx];
            comp.appendChild(line);
            comp.scrollTop = comp.scrollHeight;
            while (comp.children.length > maxLines) comp.removeChild(comp.firstChild);
            idx++;
        };
        append();
        setInterval(append, speed);
    }

    initPreloader(comp) {
        if (comp.dataset._preloadStarted) return;
        comp.dataset._preloadStarted = 'true';
        if (comp.dataset.autoStart !== 'true') return;
        try {
            const stages = JSON.parse(comp.dataset.stages);
            const fill = comp.querySelector('.preloader-fill');
            const label = comp.querySelector('.preloader-label');
            let i = 0;
            const advance = () => {
                if (i >= stages.length) {
                    if (comp.dataset.callbackId) this.triggerCallback(comp);
                    return;
                }
                const s = stages[i];
                if (fill) fill.style.width = s.pct + '%';
                if (label) label.textContent = s.label;
                i++;
                if (s.pct < 100) setTimeout(advance, s.delay || 800);
                else {
                    if (comp.dataset.callbackId) setTimeout(() => this.triggerCallback(comp), 600);
                }
            };
            advance();
        } catch(e) {}
    }

    initStoryText(comp) {
        if (comp.dataset._storyStarted) return;
        comp.dataset._storyStarted = 'true';
        let lines;
        try { lines = JSON.parse(comp.dataset.lines); } catch(e) { return; }
        if (!lines || lines.length === 0) return;
        const scroll = comp.querySelector('.story-scroll');
        const container = comp.querySelector('.story-lines');
        const cont = comp.querySelector('.story-continue');
        if (!scroll || !container) return;
        let lineIdx = 0;
        let isTyping = false;
        let typeTimer = null;

        const showLine = (lineData) => {
            const div = document.createElement('div');
            div.className = 'story-line';
            if (lineData.speaker) {
                const s = document.createElement('span');
                s.className = 'speaker';
                s.textContent = lineData.speaker;
                div.appendChild(s);
            }
            const t = document.createElement('span');
            t.className = 'text';
            const text = lineData.text || '';
            for (let ch of text) {
                const c = document.createElement('span');
                c.className = 'char';
                c.textContent = ch;
                t.appendChild(c);
            }
            div.appendChild(t);
            container.appendChild(div);

            let charIdx = 0;
            const chars = t.querySelectorAll('.char');
            isTyping = true;
            cont.classList.remove('show');

            const typeNext = () => {
                if (charIdx < chars.length) {
                    chars[charIdx].style.animation = '';
                    chars[charIdx].style.opacity = '1';
                    charIdx++;
                    const delay = lineData.speaker ? 30 : 25;
                    const extra = [',','.','!','?','，','。','！','？','…'].includes(text[charIdx-1]) ? 60 : 0;
                    typeTimer = setTimeout(typeNext, delay + extra);
                } else {
                    isTyping = false;
                    scroll.scrollTop = scroll.scrollHeight;
                    cont.classList.add('show');
                }
            };
            typeNext();
        };

        const nextLine = () => {
            if (isTyping) return;
            if (lineIdx >= lines.length) {
                if (comp.dataset.callbackId) this.triggerCallback(comp);
                return;
            }
            showLine(lines[lineIdx]);
            lineIdx++;
        };

        scroll.addEventListener('click', () => {
            if (isTyping) {
                if (typeTimer) clearTimeout(typeTimer);
                const chars = container.querySelectorAll('.story-line:last-child .char');
                chars.forEach(c => { c.style.animation = ''; c.style.opacity = '1'; });
                isTyping = false;
                scroll.scrollTop = scroll.scrollHeight;
                cont.classList.add('show');
            } else {
                nextLine();
            }
        });

        nextLine();
    }

    initMemoryMatch(comp) {
        if (comp.dataset._mmStarted) return;
        comp.dataset._mmStarted = 'true';
        const rows = parseInt(comp.dataset.rows) || 4;
        const cols = parseInt(comp.dataset.cols) || 6;
        const total = rows * cols;
        let pairs;
        try { pairs = JSON.parse(comp.dataset.pairs); } catch(e) { return; }
        if (total % 2 !== 0 || pairs.length < total / 2) return;
        const grid = comp.querySelector('.mm-grid');
        const timerEl = comp.querySelector('.mm-timer-val');
        if (!grid) return;
        grid.style.gridTemplateColumns = 'repeat(' + cols + ', 60px)';
        let cards = [];
        for (let i = 0; i < total / 2; i++) {
            cards.push({ id: i, text: pairs[i], revealed: false, matched: false });
            cards.push({ id: i, text: pairs[i], revealed: false, matched: false });
        }
        for (let i = cards.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cards[i], cards[j]] = [cards[j], cards[i]];
        }
        cards.forEach((card, idx) => {
            const div = document.createElement('div');
            div.className = 'mm-cell';
            div.dataset.index = idx;
            div.dataset.id = card.id;
            div.textContent = '?';
            div.addEventListener('click', () => this.clickMemoryCell(comp, idx));
            grid.appendChild(div);
        });
        comp._mmCards = cards;
        comp._mmSelected = null;
        comp._mmLocked = false;
        comp._mmMatched = 0;
        const totalSec = parseInt(comp.dataset.timer) || 180;
        let sec = totalSec;
        const tick = () => {
            if (comp._mmMatched >= total / 2) return;
            const m = String(Math.floor(sec / 60)).padStart(2, '0');
            const s = String(sec % 60).padStart(2, '0');
            if (timerEl) timerEl.textContent = m + ':' + s;
            if (sec <= 0) {
                comp.querySelectorAll('.mm-cell').forEach(el => el.style.display = 'none');
                if (timerEl) timerEl.textContent = 'TIME';
                return;
            }
            sec--;
            setTimeout(tick, 1000);
        };
        tick();
    }

    clickMemoryCell(comp, idx) {
        if (comp._mmLocked) return;
        const cards = comp._mmCards;
        if (!cards || cards[idx].revealed || cards[idx].matched) return;
        const cells = comp.querySelectorAll('.mm-cell');
        cards[idx].revealed = true;
        cells[idx].textContent = cards[idx].text;
        cells[idx].classList.add('revealed');
        if (comp._mmSelected === null) {
            comp._mmSelected = idx;
            return;
        }
        const first = comp._mmSelected;
        if (first === idx) return;
        if (cards[first].id === cards[idx].id) {
            cards[first].matched = true;
            cards[idx].matched = true;
            cells[first].classList.add('matched');
            cells[idx].classList.add('matched');
            comp._mmSelected = null;
            comp._mmMatched++;
            if (comp._mmMatched >= cards.length / 2) {
                if (comp.dataset.callbackId) this.triggerCallback(comp);
            }
        } else {
            comp._mmLocked = true;
            cells[first].classList.add('shake');
            cells[idx].classList.add('shake');
            setTimeout(() => {
                cards[first].revealed = false;
                cards[idx].revealed = false;
                cells[first].textContent = '?';
                cells[idx].textContent = '?';
                cells[first].classList.remove('revealed', 'shake');
                cells[idx].classList.remove('revealed', 'shake');
                comp._mmSelected = null;
                comp._mmLocked = false;
            }, 750);
        }
    }

    initCommandConsole(comp) {
        if (comp.dataset._ccStarted) return;
        comp.dataset._ccStarted = 'true';
        const log = comp.querySelector('.cc-log');
        const input = comp.querySelector('.cc-input');
        const line = comp.querySelector('.cc-input-line');
        if (!log || !input) return;
        let prompts, parser;
        try { prompts = JSON.parse(comp.dataset.prompts); } catch(e) { prompts = {}; }
        try { parser = JSON.parse(comp.dataset.parser); } catch(e) { parser = {}; }
        let errCount = 0;
        const addLine = (text, cls) => {
            const d = document.createElement('div');
            d.className = 'cc-log-line' + (cls ? ' ' + cls : '');
            d.textContent = text;
            log.appendChild(d);
            log.scrollTop = log.scrollHeight;
        };
        if (prompts.boot) {
            prompts.boot.forEach(l => addLine(l));
        }
        input.addEventListener('keydown', (e) => {
            if (e.key !== 'Enter') return;
            const cmd = input.value.trim().toLowerCase();
            input.value = '';
            if (!cmd) return;
            addLine('> ' + cmd);
            line.classList.remove('err');
            const resp = parser[cmd];
            if (resp) {
                if (typeof resp === 'string') addLine(resp);
                else if (resp.lines) resp.lines.forEach(l => addLine(l));
                if (resp.success && comp.dataset.callbackId) {
                    setTimeout(() => this.triggerCallback(comp), 500);
                }
            } else if (cmd === 'help') {
                const keys = Object.keys(parser);
                addLine('Available commands: ' + (keys.length ? keys.join(', ') : '(none)'));
            } else {
                errCount++;
                line.classList.add('err');
                addLine('Unknown command. ("help" for available commands)');
                if (prompts.hints && errCount >= 3) {
                    addLine(prompts.hints);
                }
            }
        });
        setTimeout(() => input.focus(), 100);
    }

    initGlitchText(comp) {
        if (comp.dataset._glStarted) return;
        comp.dataset._glStarted = 'true';
        const intensity = parseInt(comp.dataset.intensity) || 3;
        const orig = comp.textContent;
        if (!orig) return;
        comp.classList.add('glitch-active');
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
        const glitch = () => {
            if (!comp.isConnected) return;
            const len = orig.length;
            if (Math.random() < 0.3) {
                const idx = Math.floor(Math.random() * len);
                const ch = chars[Math.floor(Math.random() * chars.length)];
                const arr = orig.split('');
                arr[idx] = ch;
                comp.textContent = arr.join('');
                setTimeout(() => { if (comp.isConnected) comp.textContent = orig; }, 100);
            }
            setTimeout(glitch, 200 + Math.random() * 800);
        };
        setTimeout(glitch, 500);
    }

    initWebGLShader(comp) {
        if (comp.dataset._glslStarted) return;
        comp.dataset._glslStarted = 'true';
        const canvas = comp.querySelector('canvas');
        if (!canvas) return;
        const gl = canvas.getContext('webgl');
        if (!gl) return;
        const vsh = `attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}`;
        const fsh = comp.dataset.fragment || 'void main(){gl_FragColor=vec4(0.,0.,0.,1.);}';
        let vs, fs;
        try {
            vs = gl.createShader(gl.VERTEX_SHADER); gl.shaderSource(vs, vsh); gl.compileShader(vs);
            fs = gl.createShader(gl.FRAGMENT_SHADER); gl.shaderSource(fs, fsh); gl.compileShader(fs);
        } catch(e) { return; }
        if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS) || !gl.getShaderParameter(fs, gl.COMPILE_STATUS)) return;
        const prog = gl.createProgram();
        gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
        if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
        gl.useProgram(prog);
        const buf = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buf);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,1,1]), gl.STATIC_DRAW);
        const aLoc = gl.getAttribLocation(prog, 'a');
        gl.enableVertexAttribArray(aLoc);
        gl.vertexAttribPointer(aLoc, 2, gl.FLOAT, false, 0, 0);
        const uTime = gl.getUniformLocation(prog, 'u_time');
        const uRes = gl.getUniformLocation(prog, 'u_resolution');
        const resize = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            gl.viewport(0, 0, canvas.width, canvas.height);
            if (uRes) gl.uniform2f(uRes, canvas.width, canvas.height);
        };
        resize();
        window.addEventListener('resize', resize);
        const render = (t) => {
            if (comp.dataset.visible !== 'true') { requestAnimationFrame(render); return; }
            if (uTime) gl.uniform1f(uTime, t / 1000);
            gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
            requestAnimationFrame(render);
        };
        requestAnimationFrame(render);
    }

    async triggerCallback(comp) {
        const cbId = comp.dataset.callbackId;
        if (!cbId) return;
        let data = {};
        const type = comp.dataset.type;
        if (type === 'digit-string') {
            const digits = Array.from(comp.querySelectorAll('.digit-char')).map(d => d.textContent);
            data.value = digits.join('');
        } else if (type === 'slider') {
            data.value = comp.dataset.value;
        } else if (type === 'dragbar') {
            data.value = comp.dataset.value;
        } else if (comp.tagName === 'INPUT') {
            data.value = comp.value;
        } else if (type === 'switch') {
            const opts = (comp.dataset.options || '').split(',');
            const idx = parseInt(comp.dataset.currentIndex || '0', 10);
            data.value = opts[idx] || String(idx);
        } else if (type === 'toggle') {
            data.value = comp.dataset.checked;
        } else if (type === 'checkbox') {
            data.value = comp.dataset.checked;
        } else if (type === 'dropdown') {
            const opts = (comp.dataset.options || '').split(',');
            const idx = parseInt(comp.dataset.currentIndex || '0', 10);
            data.value = opts[idx] || String(idx);
        }
        try {
            const res = await fetch(this.callbackBase + '/callback/' + cbId, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const result = await res.json();
            if (result.action) this.handleCallbackResult(result);
        } catch (err) {
            console.error('Callback error:', err);
        }
    }

    handleCallbackResult(result) {
        if (result.action === 'set-text') {
            const el = document.querySelector(result.selector || '#' + result.target);
            if (el) el.textContent = result.value;
        } else if (result.action === 'show-dialog') {
            this.openDialog(result.dialogId);
        } else if (result.action === 'hide-dialog') {
            this.closeDialog(result.dialogId);
        } else if (result.action === 'switch-panel') {
            this.switchPanel(result.target);
        } else if (result.action === 'set-progress') {
            const el = document.querySelector(result.selector || '#' + result.target);
            if (el) {
                const fill = el.querySelector('.progress-fill');
                const txt = el.querySelector('.progress-text');
                const pct = (result.value / result.max) * 100;
                el.dataset.value = result.value;
                if (fill) fill.style.width = pct + '%';
                if (txt) txt.textContent = Math.round(pct) + '%';
            }
        } else if (result.action === 'set-slider') {
            const el = document.querySelector(result.selector || '#' + result.target);
            if (el) this.updateSliderUI(el, parseInt(result.value));
        } else if (result.action === 'set-digit') {
            const el = document.querySelector(result.selector || '#' + result.target);
            if (el) {
                const chars = el.querySelectorAll('.digit-char');
                const val = String(result.value);
                chars.forEach((c, i) => { c.textContent = val[i] || '_'; });
            }
        } else if (result.action === 'set-dragbar') {
            const el = document.querySelector(result.selector || '#' + result.target);
            if (el) this.updateDragbarUI(el, parseInt(result.value));
        } else if (result.action === 'set-visible') {
            const el = document.querySelector(result.selector || '#' + result.target);
            if (el) el.dataset.visible = el.dataset.visible === 'true' ? 'false' : 'true';
        }
    }

    toggleSwitch(comp) {
        const type = comp.dataset.type;
        if (type === 'toggle') {
            const checked = comp.dataset.checked === 'true';
            comp.dataset.checked = checked ? 'false' : 'true';
            const label = comp.dataset.label || '';
            comp.textContent = label + (checked ? 'OFF' : 'ON');
            this.updateHighlight();
            if (comp.dataset.callbackId) this.triggerCallback(comp);
            return;
        }
        const label = comp.dataset.label || '';
        const opts = (comp.dataset.options || '').split(',');
        let idx = parseInt(comp.dataset.currentIndex || '0', 10);
        idx = (idx + 1) % opts.length;
        comp.dataset.currentIndex = String(idx);
        comp.textContent = label + opts[idx];
        const action = comp.dataset.action;
        if (action === 'change-font-family') {
            document.documentElement.style.setProperty('--terminal-font-family', '"' + opts[idx] + '", sans-serif');
        }
        this.updateHighlight();
        if (comp.dataset.callbackId) this.triggerCallback(comp);
    }

    toggleCheckbox(comp) {
        const checked = comp.dataset.checked === 'true';
        comp.dataset.checked = checked ? 'false' : 'true';
        const text = comp.textContent;
        const label = text.includes(']') ? text.substring(text.indexOf(']') + 1).trim() : text;
        comp.textContent = (checked ? '[ ] ' : '[x] ') + label;
        this.updateHighlight();
        if (comp.dataset.callbackId) this.triggerCallback(comp);
    }

    cycleDropdown(comp) {
        const label = comp.dataset.label || '';
        const opts = (comp.dataset.options || '').split(',');
        let idx = parseInt(comp.dataset.currentIndex || '0', 10);
        idx = (idx + 1) % opts.length;
        comp.dataset.currentIndex = String(idx);
        comp.textContent = label + '[' + opts[idx] + ']';
        this.updateHighlight();
        if (comp.dataset.callbackId) this.triggerCallback(comp);
    }

    changeFontSize(direction) {
        if (direction === 'increase' && this.currentFontSize < this.maxFontSize) {
            this.currentFontSize++;
        } else if (direction === 'decrease' && this.currentFontSize > this.minFontSize) {
            this.currentFontSize--;
        }
        document.documentElement.style.setProperty('--terminal-font-size', this.currentFontSize + 'px');
        this.updateHighlight();
    }

    startLongPress(comp) {
        this.isCharging = true;
        this.longPressStartTime = Date.now();
        const duration = parseInt(comp.dataset.duration) || this.config.longPressDuration;
        const bar = comp.querySelector('.charge-bar');
        if (this.longPressTimer) clearInterval(this.longPressTimer);
        this.longPressTimer = setInterval(() => {
            if (!this.isCharging) { clearInterval(this.longPressTimer); this.longPressTimer = null; return; }
            const elapsed = Date.now() - this.longPressStartTime;
            const progress = Math.min(elapsed / duration, 1);
            if (bar) {
                bar.style.height = (progress * 100) + '%';
                bar.style.opacity = String(progress * 0.8);
            }
            if (progress >= 1) {
                clearInterval(this.longPressTimer);
                this.longPressTimer = null;
                this.activateComponent(comp);
                this.cancelLongPress();
            }
        }, 30);
    }

    cancelLongPress() {
        if (this.isCharging) {
            this.isCharging = false;
            if (this.longPressTimer) { clearInterval(this.longPressTimer); this.longPressTimer = null; }
            this.activePanel?.querySelectorAll('[data-type="long-press"] .charge-bar').forEach(bar => {
                bar.style.height = '0%';
                bar.style.opacity = '0';
            });
        }
    }

    startSliderEdit(comp) {
        this.isEditingSlider = true;
        this.activeSliderComponent = comp;
        this.cursor?.classList.add('editing-special');
    }

    stopSliderEdit() {
        if (!this.isEditingSlider) return;
        this.isEditingSlider = false;
        const comp = this.activeSliderComponent;
        if (comp?.dataset?.callbackId) this.triggerCallback(comp);
        this.activeSliderComponent = null;
        this.cursor?.classList.remove('editing-special');
    }

    handleSliderEdit(e) {
        e.preventDefault();
        const comp = this.activeSliderComponent;
        if (!comp) return;
        const type = comp.dataset.type;
        let val = parseInt(comp.dataset.value, 10);
        const min = type === 'dragbar' ? 0 : parseInt(comp.dataset.min, 10);
        const max = type === 'dragbar' ? 100 : parseInt(comp.dataset.max, 10);
        const step = type === 'dragbar' ? 1 : (parseInt(comp.dataset.step, 10) || 1);
        switch (e.key) {
            case 'ArrowUp': case 'ArrowRight':
                val = Math.min(max, val + step);
                break;
            case 'ArrowDown': case 'ArrowLeft':
                val = Math.max(min, val - step);
                break;
            case 'Enter': case 'Escape':
                if (type === 'dragbar') this.stopDragbarEdit();
                else this.stopSliderEdit();
                return;
        }
        if (type === 'dragbar') this.updateDragbarUI(comp, val);
        else this.updateSliderUI(comp, val);
    }

    startDigitEdit(comp) {
        this.isEditingDigits = true;
        this.activeDigitComponent = comp;
        comp.classList.add('editing');
        this.cursor?.classList.add('editing-special');
        this.activeDigitIndex = 0;
        const digits = comp.querySelectorAll('.digit-char');
        if (digits[this.activeDigitIndex]?.textContent === '_') digits[this.activeDigitIndex].textContent = '0';
        this.updateDigitHighlight();
    }

    stopDigitEdit() {
        if (!this.isEditingDigits) return;
        this.isEditingDigits = false;
        if (this.activeDigitComponent) {
            this.activeDigitComponent.classList.remove('editing');
            this.activeDigitComponent.querySelectorAll('.digit-char').forEach(d => d.classList.remove('selected'));
        }
        this.cursor?.classList.remove('editing-special');
        this.activeDigitComponent = null;
        this.activeDigitIndex = 0;
    }

    handleDigitEdit(e) {
        e.preventDefault();
        const digits = this.activeDigitComponent.querySelectorAll('.digit-char');
        const maxIdx = digits.length - 1;
        let cur = parseInt(digits[this.activeDigitIndex].textContent, 10);
        if (/^[0-9]$/.test(e.key)) {
            digits[this.activeDigitIndex].textContent = e.key;
            if (this.activeDigitIndex < maxIdx) {
                this.activeDigitIndex++;
                if (digits[this.activeDigitIndex]?.textContent === '_') digits[this.activeDigitIndex].textContent = '0';
            }
            this.updateDigitHighlight();
            return;
        }
        switch (e.key) {
            case 'ArrowUp':
                cur = isNaN(cur) ? 0 : (cur + 1) % 10;
                digits[this.activeDigitIndex].textContent = String(cur);
                break;
            case 'ArrowDown':
                cur = isNaN(cur) ? 0 : (cur - 1 + 10) % 10;
                digits[this.activeDigitIndex].textContent = String(cur);
                break;
            case 'ArrowLeft':
                if (this.activeDigitIndex > 0) { this.activeDigitIndex--; }
                break;
            case 'ArrowRight':
                if (this.activeDigitIndex < maxIdx) {
                    this.activeDigitIndex++;
                    if (digits[this.activeDigitIndex]?.textContent === '_') digits[this.activeDigitIndex].textContent = '0';
                }
                break;
            case 'Enter': case 'Escape':
                if (e.key === 'Enter' && this.activeDigitComponent.dataset.callbackId) {
                    this.triggerCallback(this.activeDigitComponent);
                }
                this.stopDigitEdit();
                break;
        }
        this.updateDigitHighlight();
    }

    updateDigitHighlight() {
        if (!this.activeDigitComponent) return;
        this.activeDigitComponent.querySelectorAll('.digit-char').forEach((d, i) => d.classList.toggle('selected', i === this.activeDigitIndex));
        const display = this.activePanel.querySelector('[data-digit-display]');
        if (display) {
            const vals = Array.from(this.activeDigitComponent.querySelectorAll('.digit-char')).map(d => d.textContent);
            display.textContent = vals.every(v => v !== '_') ? vals.join('') : vals.join('').replace(/_/g, '-');
        }
    }

    showDigitError() {
        const comp = this.activeDigitComponent;
        if (comp) { comp.classList.add('error'); setTimeout(() => comp.classList.remove('error'), 500); }
    }

    adjustSlider(btn, dir) {
        const slider = btn.closest('[data-type="slider"]');
        if (!slider) return;
        let val = parseInt(slider.dataset.value, 10);
        const min = parseInt(slider.dataset.min, 10);
        const max = parseInt(slider.dataset.max, 10);
        const step = parseInt(slider.dataset.step, 10) || 1;
        val = Math.max(min, Math.min(max, val + dir * step));
        this.updateSliderUI(slider, val);
        if (slider.dataset.callbackId) this.triggerCallback(slider);
    }

    updateSliderUI(slider, val) {
        const min = parseInt(slider.dataset.min, 10);
        const max = parseInt(slider.dataset.max, 10);
        slider.dataset.value = String(val);
        const valueEl = slider.querySelector('.slider-value');
        const fillEl = slider.querySelector('.slider-fill');
        if (valueEl) valueEl.textContent = String(val);
        if (fillEl) {
            const pct = max > min ? ((val - min) / (max - min)) * 100 : 0;
            fillEl.style.width = pct + '%';
        }
    }

    startKeypadEdit(comp) {
        this.isEditingKeypad = true;
        this.activeKeypadComponent = comp;
        this.activeKeypadRow = 0;
        this.activeKeypadCol = 0;
        this.cursor?.classList.add('editing-special');
        this.highlightKeypadKey();
    }

    stopKeypadEdit() {
        if (!this.isEditingKeypad) return;
        this.isEditingKeypad = false;
        if (this.activeKeypadComponent) {
            this.activeKeypadComponent.querySelectorAll('.keypad-key').forEach(k => k.classList.remove('active-key'));
        }
        this.activeKeypadComponent = null;
        this.cursor?.classList.remove('editing-special');
    }

    highlightKeypadKey() {
        if (!this.activeKeypadComponent) return;
        this.activeKeypadComponent.querySelectorAll('.keypad-key').forEach(k => k.classList.remove('active-key'));
        const rows = this.activeKeypadComponent.querySelectorAll('.keypad-row');
        const keys = rows[this.activeKeypadRow]?.querySelectorAll('.keypad-key');
        if (keys?.[this.activeKeypadCol]) keys[this.activeKeypadCol].classList.add('active-key');
        const keyEl = keys?.[this.activeKeypadCol];
        if (keyEl && this.cursor) {
            setTimeout(() => {
                if (!keyEl.offsetParent) return;
                const container = this.activePanel?.querySelector('.component-container');
                if (container) {
                    const cr = container.getBoundingClientRect();
                    const kr = keyEl.getBoundingClientRect();
                    this.cursor.style.top = (kr.top - cr.top) + 'px';
                    this.cursor.style.left = (kr.left - cr.left) + 'px';
                } else {
                    this.cursor.style.top = keyEl.offsetTop + 'px';
                    this.cursor.style.left = keyEl.offsetLeft + 'px';
                }
                this.cursor.style.width = keyEl.offsetWidth + 'px';
                this.cursor.style.height = keyEl.offsetHeight + 'px';
            }, 20);
        }
    }

    handleKeypadEdit(e) {
        e.preventDefault();
        const comp = this.activeKeypadComponent;
        if (!comp) return;
        const rows = comp.querySelectorAll('.keypad-row');
        const currentRow = rows[this.activeKeypadRow];
        const keys = currentRow?.querySelectorAll('.keypad-key');
        if (!keys) return;
        const cols = keys.length;
        switch (e.key) {
            case 'ArrowUp':
                if (this.activeKeypadRow > 0) { this.activeKeypadRow--; this.activeKeypadCol = Math.min(this.activeKeypadCol, comp.querySelectorAll('.keypad-row')[this.activeKeypadRow].querySelectorAll('.keypad-key').length - 1); }
                break;
            case 'ArrowDown':
                if (this.activeKeypadRow < rows.length - 1) { this.activeKeypadRow++; this.activeKeypadCol = Math.min(this.activeKeypadCol, comp.querySelectorAll('.keypad-row')[this.activeKeypadRow].querySelectorAll('.keypad-key').length - 1); }
                break;
            case 'ArrowLeft':
                if (this.activeKeypadCol > 0) { this.activeKeypadCol--; }
                break;
            case 'ArrowRight':
                if (this.activeKeypadCol < cols - 1) { this.activeKeypadCol++; }
                break;
            case 'Enter':
                const target = rows[this.activeKeypadRow].querySelectorAll('.keypad-key')[this.activeKeypadCol];
                if (target) {
                    this.handleKeypadKey(target);
                    if (target.dataset.key === '✓') {
                        this.stopKeypadEdit();
                        this.updateHighlight();
                    }
                }
                return;
            case 'Escape':
                this.stopKeypadEdit();
                return;
        }
        this.highlightKeypadKey();
    }

    startChoiceEdit(comp) {
        this.isEditingChoices = true;
        this.activeChoiceComponent = comp;
        this.activeChoiceIndex = 0;
        this.cursor?.classList.add('editing-special');
        this.highlightChoiceButton();
    }

    stopChoiceEdit() {
        if (!this.isEditingChoices) return;
        this.isEditingChoices = false;
        if (this.activeChoiceComponent) {
            this.activeChoiceComponent.querySelectorAll('.choice-btn').forEach(b => b.classList.remove('active-choice'));
        }
        this.activeChoiceComponent = null;
        this.activeChoiceIndex = 0;
        this.cursor?.classList.remove('editing-special');
    }

    handleChoiceEdit(e) {
        e.preventDefault();
        const comp = this.activeChoiceComponent;
        if (!comp) return;
        const btns = comp.querySelectorAll('.choice-btn');
        if (!btns || btns.length === 0) { this.stopChoiceEdit(); return; }
        switch (e.key) {
            case 'ArrowUp':
                if (this.activeChoiceIndex > 0) this.activeChoiceIndex--;
                break;
            case 'ArrowDown':
                if (this.activeChoiceIndex < btns.length - 1) this.activeChoiceIndex++;
                break;
            case 'Enter':
                const data = {value: String(this.activeChoiceIndex)};
                if (comp.dataset.callbackId) {
                    fetch(this.callbackBase + '/callback/' + comp.dataset.callbackId, {
                        method: 'POST', headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(data)
                    }).then(r => r.json()).then(result => {
                        if (result.action) this.handleCallbackResult(result);
                    }).catch(() => {});
                }
                this.stopChoiceEdit();
                this.updateHighlight();
                return;
            case 'Escape':
                this.stopChoiceEdit();
                return;
        }
        this.highlightChoiceButton();
    }

    highlightChoiceButton() {
        if (!this.activeChoiceComponent) return;
        this.activeChoiceComponent.querySelectorAll('.choice-btn').forEach(b => b.classList.remove('active-choice'));
        const btns = this.activeChoiceComponent.querySelectorAll('.choice-btn');
        const btn = btns[this.activeChoiceIndex];
        if (!btn) return;
        btn.classList.add('active-choice');
        if (this.cursor) {
            setTimeout(() => {
                if (!btn.offsetParent) return;
                const container = this.activePanel?.querySelector('.component-container');
                if (container) {
                    const cr = container.getBoundingClientRect();
                    const br = btn.getBoundingClientRect();
                    this.cursor.style.top = (br.top - cr.top) + 'px';
                    this.cursor.style.left = (br.left - cr.left) + 'px';
                } else {
                    this.cursor.style.top = btn.offsetTop + 'px';
                    this.cursor.style.left = btn.offsetLeft + 'px';
                }
                this.cursor.style.width = btn.offsetWidth + 'px';
                this.cursor.style.height = btn.offsetHeight + 'px';
            }, 20);
        }
    }

    handleKeypadKey(comp) {
        const key = comp.dataset.key;
        if (key === '←') {
            const target = comp.closest('[data-type="keypad"]');
            if (target?.dataset.target) this.triggerBackspace(target.dataset.target);
            return;
        }
        if (key === '✓') {
            const target = comp.closest('[data-type="keypad"]');
            if (target?.dataset.target) this.triggerKeypadSubmit(target.dataset.target);
            return;
        }
        const target = comp.closest('[data-type="keypad"]');
        if (target?.dataset.target) this.triggerKeypadInput(target.dataset.target, key);
        this.highlightKeypadKey();
    }

    triggerKeypadInput(targetId, key) {
        const ds = document.querySelector('[data-digit-display], [data-callback-id="' + targetId + '"]');
        if (ds) {
            const digits = ds.closest('[data-type="digit-string"]') || ds.closest('.digit-string-component');
            if (digits) {
                const chars = digits.querySelectorAll('.digit-char');
                for (let i = 0; i < chars.length; i++) {
                    if (chars[i].textContent === '_') { chars[i].textContent = key; break; }
                }
            }
        }
    }

    triggerBackspace(targetId) {
        const ds = document.querySelector('[data-digit-display], [data-callback-id="' + targetId + '"]');
        const digits = ds?.closest('[data-type="digit-string"]');
        if (digits) {
            const chars = digits.querySelectorAll('.digit-char');
            for (let i = chars.length - 1; i >= 0; i--) {
                if (chars[i].textContent !== '_') { chars[i].textContent = '_'; break; }
            }
        }
    }

    triggerKeypadSubmit(targetId) {
        const ds = document.querySelector('[data-digit-display], [data-callback-id="' + targetId + '"]');
        const digits = ds?.closest('[data-type="digit-string"]');
        if (digits && digits.dataset.callbackId) this.triggerCallback(digits);
    }

    startDragbarEdit(e, comp) {
        this.isEditingSlider = true;
        this.activeSliderComponent = comp;
        this.cursor?.classList.add('editing-special');
    }

    stopDragbarEdit() {
        if (this.activeSliderComponent?.dataset?.callbackId) this.triggerCallback(this.activeSliderComponent);
        this.isEditingSlider = false;
        this.activeSliderComponent = null;
        this.cursor?.classList.remove('editing-special');
    }

    updateDragbarUI(comp, val) {
        comp.dataset.value = String(val);
        const fill = comp.querySelector('.dragbar-fill');
        const thumb = comp.querySelector('.dragbar-thumb');
        const valueEl = comp.querySelector('.dragbar-value');
        if (fill) fill.style.width = val + '%';
        if (thumb) thumb.style.left = val + '%';
        if (valueEl) valueEl.textContent = val + '%';
    }

    openModal(modalId) {
        const m = document.querySelector('[data-modal-id="' + modalId + '"]');
        if (m) m.dataset.visible = 'true';
    }

    closeModal(modalId) {
        const m = document.querySelector('[data-modal-id="' + modalId + '"]');
        if (m) m.dataset.visible = 'false';
    }

    startCountdown() {
        this.stopCountdown();
        const update = () => {
            const display = this.activePanel.querySelector('[data-countdown-display]');
            if (!display) return;
            const targetStr = this.activePanel.dataset.targetDate;
            if (!targetStr) return;
            const target = new Date(targetStr);
            const now = new Date();
            let diff = target - now;
            if (diff <= 0) { diff = 0; display.innerHTML = '&#8734;'; this.stopCountdown(); return; }
            const mode = this.activePanel.dataset.countdownMode || 'standard';
            if (mode === 'standard') {
                const d = Math.floor(diff / 86400000);
                const h = String(Math.floor((diff % 86400000) / 3600000)).padStart(2,'0');
                const m = String(Math.floor((diff % 3600000) / 60000)).padStart(2,'0');
                const s = String(Math.floor((diff % 60000) / 1000)).padStart(2,'0');
                const ms = String(Math.floor(diff % 1000)).padStart(3,'0');
                display.innerHTML = d + '<span>d </span>' + h + '<span>:</span>' + m + '<span>:</span>' + s + '<span>.</span>' + ms;
            } else {
                display.textContent = diff.toLocaleString('en-US') + ' ms';
            }
        };
        update();
        this.countdownInterval = setInterval(update, 43);
    }

    stopCountdown() {
        if (this.countdownInterval) { clearInterval(this.countdownInterval); this.countdownInterval = null; }
    }

    resetTypewriter() {
        this.typewriterInputBuffer = '';
        const msg = document.getElementById('typewriter-message-display');
        const big = document.getElementById('typewriter-large-char-display');
        if (msg) { msg.textContent = this.activePanel.dataset.typewriterPrompt || 'Press any letter key...'; msg.classList.remove('hidden'); }
        if (big) big.classList.remove('visible');
    }

    handleTypewriterLetterDown(key) {
        const msg = document.getElementById('typewriter-message-display');
        const big = document.getElementById('typewriter-large-char-display');
        if (msg) msg.classList.add('hidden');
        if (big) { big.textContent = key.toUpperCase(); big.classList.add('visible'); }
        this.typewriterInputBuffer += key.toLowerCase();
        this.checkTypewriterSecrets();
    }

    handleTypewriterLetterUp() {
        const big = document.getElementById('typewriter-large-char-display');
        if (big) big.classList.remove('visible');
    }

    checkTypewriterSecrets() {
        const secretStr = this.activePanel?.dataset?.secretWords;
        if (!secretStr) return;
        let secrets;
        try { secrets = JSON.parse(secretStr); } catch(e) { return; }
        const msg = document.getElementById('typewriter-message-display');
        for (const [word, response] of Object.entries(secrets)) {
            if (this.typewriterInputBuffer.endsWith(word)) {
                setTimeout(() => {
                    if (msg) { msg.textContent = response; msg.classList.remove('hidden'); }
                }, 200);
                this.typewriterInputBuffer = '';
                return;
            }
        }
    }

    openDialog(dialogId) {
        const dlg = document.querySelector('[data-dialog-id="' + dialogId + '"]');
        if (!dlg) return;
        dlg.dataset.visible = 'true';
        const btn = dlg.querySelector('.dialog-confirm, .modal-confirm');
        if (btn) setTimeout(() => btn.focus(), 50);
    }

    closeDialog(dialogId) {
        const dlg = document.querySelector('[data-dialog-id="' + dialogId + '"]');
        if (!dlg) return;
        dlg.dataset.visible = 'false';
        if (this.grid.length > 0) {
            setTimeout(() => this.updateHighlight(), 50);
        }
    }

    showError(msg) {
        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const err = document.createElement('div');
        err.className = 'terminal-component';
        err.style.cssText = 'color:#ff4444;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        err.textContent = msg;
        container.appendChild(err);
        setTimeout(() => err.remove(), 3000);
    }

    showSuccess(msg) {
        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const el = document.createElement('div');
        el.className = 'terminal-component';
        el.style.cssText = 'color:#2a9d8f;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        el.textContent = msg;
        container.appendChild(el);
        setTimeout(() => el.remove(), 3000);
    }
}

window.CARNIVALTerminal = CARNIVALTerminal;
})();
"""


def render_panels_html(panels, dialogs):
    parts = []
    overlays = []
    for panel in panels:
        p_id = panel.id
        p_attrs = f' id="{p_id}" class="panel"'
        behavior_parts = []
        if panel.typewriter_config:
            behavior_parts.append('data-behavior="typewriter"')
            behavior_parts.append(
                'data-typewriter-prompt="' + panel.typewriter_config.prompt.replace('"', '&quot;') + '"'
            )
            if panel.typewriter_config.secret_words:
                behavior_parts.append(
                    'data-secret-words=\'' + json.dumps(panel.typewriter_config.secret_words, ensure_ascii=False) + '\''
                )
        if panel.countdown_config:
            behavior_parts.append('data-behavior="countdown"')
            behavior_parts.append(
                'data-target-date="' + panel.countdown_config.target_date + '"'
            )
            behavior_parts.append('data-countdown-mode="standard"')
        if behavior_parts:
            p_attrs += " " + " ".join(behavior_parts)

        parts.append(f"<div{p_attrs}>")
        parts.append('<div class="component-container">')
        parts.append('<div class="cursor-highlight"></div>')
        for row in panel.rows:
            if not row:
                continue
            parts.append('<div class="component-row">')
            for comp in row:
                if hasattr(comp, 'type') and comp.type in ('dialog', 'modal'):
                    overlays.append(comp.render())
                else:
                    parts.append(comp.render())
            parts.append("</div>")
        parts.append("</div></div>")
    return "\n".join(parts), "\n".join(overlays)


def render_typewriter_elements():
    return (
        '<div id="typewriter-large-char-display"></div>\n'
        '<div id="typewriter-message-display" class="typewriter-message"></div>'
    )


def build_html(app):
    has_typewriter = any(p.typewriter_config for p in app.panels)
    has_countdown = any(p.countdown_config for p in app.panels)

    panels_html, overlays = render_panels_html(app.panels, app.dialogs)
    tw_elements = render_typewriter_elements() if has_typewriter else ""

    font_url = app.assets_url + "fonts/LanaPixel.ttf" if app.assets_url else "assets/fonts/LanaPixel.ttf"

    config_json = json.dumps({
        "defaultPanel": app.default_panel,
        "longPressDuration": app.long_press_duration,
        "apiBase": app.api_base,
    })

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{app.title}</title>
<style>
@font-face{{font-family:'LanaPixel';src:url('{font_url}') format('truetype')}}
{CSS}
</style>
</head>
<body>
<div id="terminal">
<div class="terminal-content">
{panels_html}
{tw_elements}
</div>
{overlays}
</div>
<script>
var TERMINAL_CONFIG = {config_json};
{JS_TERMINAL}
document.addEventListener('DOMContentLoaded', function() {{
    new CARNIVALTerminal(TERMINAL_CONFIG);
}});
</script>
</body>
</html>"""
