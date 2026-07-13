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
        this.mouseIdleDelay = 5000;
        this.fadeDuration = 3000;

        this.init();
    }
    init() {
        this.mouseCursor = document.createElement('div');
        this.mouseCursor.id = 'terminal-cursor';
        document.body.appendChild(this.mouseCursor);
        document.addEventListener('mousemove', this.handleMouseMove.bind(this));
        document.addEventListener('mousedown', this.handleMouseDown.bind(this));
        document.addEventListener('mouseup', this.handleMouseUp.bind(this));

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
        document.addEventListener('click', this.handleClick.bind(this));
    }

    initializeActivePanel() {

        this.stopDigitEdit();
        this.stopSliderEdit();
        this.stopKeypadEdit();
        if (this.cursor) this.cursor.classList.remove('activated');
        this.cursor = this.activePanel.querySelector('.cursor-highlight');
        if (!this.cursor) {
            this.cursor = document.createElement('div');
            this.cursor.className = 'cursor-highlight keyboard-cursor';
            this.activePanel.querySelector('.component-container')?.appendChild(this.cursor);
        } else {
            this.cursor.classList.add('keyboard-cursor');
        }
        this.cursor.style.width = '0';
        this.cursor.style.height = '0';
        this.applyCustomTextStyles();
        this.initializeSwitchComponents();
        this.initializeDropdownComponents();
        this.buildGrid();
        this.currentRowIndex = 0;
        this.currentColIndex = 0;
        if (this.grid.length > 0 && this.grid[0].length > 0) {
        
};

CARNIVALTerminal.prototype.buildGrid = function() {
        this.grid = [];
        const rows = this.activePanel.querySelectorAll('.component-row');
        rows.forEach(row => {
            const components = Array.from(row.querySelectorAll(
                'button.terminal-component, input.terminal-component, ' +
                '.digit-string-component, [data-type="switch"], [data-type="toggle"], ' +
                '[data-type="slider"], [data-type="checkbox"], [data-type="dropdown"], ' +
                '[data-type="keypad"], [data-type="long-press"], [data-type="digit-string"], ' +
                '[data-type="dragbar"]'
            ));
            if (components.length > 0) this.grid.push(components);
        });
    }
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
                '[data-type="dragbar"]'
            ));
            if (components.length > 0) this.grid.push(components);
        })
    }

    applyCustomTextStyles() {

        this.activePanel.querySelectorAll('[data-type="text"]').forEach(el => {
            const sz = el.dataset.fontSize;
            const ff = el.dataset.fontFamily;
            if (sz) el.style.fontSize = sz;
            if (ff) el.style.fontFamily = ff;
        })
    }

    initializeSwitchComponents() {

        this.activePanel.querySelectorAll('[data-type="switch"]').forEach(sw => {
            const label = sw.dataset.label || '';
            const opts = (sw.dataset.options || '').split(',');
            let idx = parseInt(sw.dataset.currentIndex || '0', 10);
            if (isNaN(idx) || idx < 0 || idx >= opts.length) { idx = 0; sw.dataset.currentIndex = '0'; }
            sw.textContent = label + opts[idx];
        })
    }

    initializeDropdownComponents() {

        this.activePanel.querySelectorAll('[data-type="dropdown"]').forEach(dd => {
            const label = dd.dataset.label || '';
            const opts = (dd.dataset.options || '').split(',');
            let idx = parseInt(dd.dataset.currentIndex || '0', 10);
            if (isNaN(idx) || idx < 0 || idx >= opts.length) { idx = 0; dd.dataset.currentIndex = '0'; }
            dd.textContent = label + '[' + opts[idx] + ']';
        })
    }

    switchPanel(panelId) {

        if (this.activePanel?.dataset?.behavior === 'countdown') this.stopCountdown();
        const newPanel = document.getElementById(panelId);
        if (!newPanel || newPanel === this.activePanel) return;
        if (this.activePanel) this.activePanel.classList.remove('active');
        newPanel.classList.add('active');
        this.activePanel = newPanel;
        this.activePanelId = panelId;
        this.initializeActivePanel()
    }

    updateHighlight() {

        if (!this.grid[this.currentRowIndex] || !this.grid[this.currentRowIndex][this.currentColIndex]) return;
        const comp = this.grid[this.currentRowIndex][this.currentColIndex];
        if (!comp || !this.cursor) return;
        this.grid.forEach(r => r.forEach(c => c.classList.remove('active')));
        comp.classList.add('active');
        const pos = () => {
            if (!comp.offsetParent) {
            
};

CARNIVALTerminal.prototype.handleKeyDown = function(e) {
        if (this.activePanel?.dataset?.behavior === 'typewriter' && /^[a-zA-Z]$/.test(e.key) && !e.repeat) {
            e.preventDefault();
            this.handleTypewriterLetterDown(e.key);
            return;
        }
        if (this.isEditingDigits) { this.handleDigitEdit(e); return; }
        if (this.isEditingSlider) { this.handleSliderEdit(e); return; }
        if (this.isEditingKeypad) { this.handleKeypadEdit(e); return; }
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
};

CARNIVALTerminal.prototype.handleKeyUp = function(e) {
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

    handleClick(e) {

        const key = e.target.closest('.keypad-key');
        if (key) { this.handleKeypadKey(key); return; }
        const comp = e.target.closest('.terminal-component');
        if (!comp) return;
        if (!this.snappedComp || this.snappedComp !== comp) {
            const tag = comp.tagName.toLowerCase();
            if (tag === 'button' || tag === 'input') {
                this.activateComponent(comp);
            }
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
        if (type === 'long-press') { if (!e.repeat && !this.isCharging) this.startLongPress(comp); return; }
        if (type === 'dragbar') { this.startDragbarEdit(e, comp); return; }
        this.activateComponent(comp)
    }

    activateComponent(comp) {

        const tag = comp.tagName.toLowerCase();
        if (tag === 'input') { comp.focus(); return; }
        const type = comp.dataset.type;
        if (type === 'switch' || type === 'toggle') { this.toggleSwitch(comp); return; }
        if (type === 'checkbox') { this.toggleCheckbox(comp); return; }
        if (type === 'dropdown') { this.cycleDropdown(comp); return; }
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
        if (comp.dataset.callbackId) this.triggerCallback(comp)
    }

    changeFontSize(direction) {

        if (direction === 'increase' && this.currentFontSize < this.maxFontSize) {
            this.currentFontSize++;
        } else if (direction === 'decrease' && this.currentFontSize > this.minFontSize) {
            this.currentFontSize--;
        }
        document.documentElement.style.setProperty('--terminal-font-size', this.currentFontSize + 'px');
        this.updateHighlight()
    }

    toggleCheckbox(comp) {

        const checked = comp.dataset.checked === 'true';
        comp.dataset.checked = checked ? 'false' : 'true';
        const text = comp.textContent;
        const label = text.includes(']') ? text.substring(text.indexOf(']') + 1).trim() : text;
        comp.textContent = (checked ? '[ ] ' : '[x] ') + label;
        this.updateHighlight();
        if (comp.dataset.callbackId) this.triggerCallback(comp)
    }

    cycleDropdown(comp) {

        const label = comp.dataset.label || '';
        const opts = (comp.dataset.options || '').split(',');
        let idx = parseInt(comp.dataset.currentIndex || '0', 10);
        idx = (idx + 1) % opts.length;
        comp.dataset.currentIndex = String(idx);
        comp.textContent = label + '[' + opts[idx] + ']';
        this.updateHighlight();
        if (comp.dataset.callbackId) this.triggerCallback(comp)
    }

    startLongPress(comp) {

        this.isCharging = true;
        this.longPressStartTime = Date.now();
        const duration = parseInt(comp.dataset.duration) || this.config.longPressDuration;
        if (this.longPressTimer) clearInterval(this.longPressTimer);
        this.longPressTimer = setInterval(() => {
            if (!this.isCharging) { clearInterval(this.longPressTimer); this.longPressTimer = null; return; }
            const elapsed = Date.now() - this.longPressStartTime;
            const progress = Math.min(elapsed / duration, 1);
            comp.style.setProperty('--charge-progress', (progress * 100) + '%');
            comp.style.setProperty('--charge-opacity', String(progress * 0.8));
            if (progress >= 1) {
            
};

CARNIVALTerminal.prototype.cancelLongPress = function() {
        if (this.isCharging) {
            this.isCharging = false;
            if (this.longPressTimer) { clearInterval(this.longPressTimer); this.longPressTimer = null; }
            const comp = this.activePanel?.querySelector('[data-type="long-press"]');
            if (comp) {
                comp.style.setProperty('--charge-progress', '0%');
                comp.style.setProperty('--charge-opacity', '0');
            }
        }
    }
};


CARNIVALTerminal.prototype.tapLongPress = function(comp) {
        this.isCharging = true;
        comp.style.setProperty('--charge-progress', '100%');
        comp.style.setProperty('--charge-opacity', '0.8');
        setTimeout(() => {
            this.activateComponent(comp);
            this.cancelLongPress();
        }, 150);
    };

CARNIVALTerminal.prototype.startSliderEdit = function(comp) {
        this.isEditingSlider = true;
        this.activeSliderComponent = comp;
        this.cursor?.classList.add('editing-special');
    }
    }

    cancelLongPress() {

        if (this.isCharging) {
            this.isCharging = false;
            if (this.longPressTimer) { clearInterval(this.longPressTimer); this.longPressTimer = null; }
            const comp = this.activePanel?.querySelector('[data-type="long-press"]');
            if (comp) {
                comp.style.setProperty('--charge-progress', '0%');
                comp.style.setProperty('--charge-opacity', '0');
            }
        }
    }

    tapLongPress(comp) {

        this.isCharging = true;
        comp.style.setProperty('--charge-progress', '100%');
        comp.style.setProperty('--charge-opacity', '0.8');
        setTimeout(() => {
            this.activateComponent(comp);
            this.cancelLongPress();
        }, 150)
    }

    startSliderEdit(comp) {

        this.isEditingSlider = true;
        this.activeSliderComponent = comp;
        this.cursor?.classList.add('editing-special')
    }

    stopSliderEdit() {

        if (!this.isEditingSlider) return;
        this.isEditingSlider = false;
        const comp = this.activeSliderComponent;
        if (comp?.dataset?.callbackId) this.triggerCallback(comp);
        this.activeSliderComponent = null;
        this.cursor?.classList.remove('editing-special')
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
        else this.updateSliderUI(comp, val)
    }

    startDigitEdit(comp) {

        this.isEditingDigits = true;
        this.activeDigitComponent = comp;
        comp.classList.add('editing');
        this.cursor?.classList.add('editing-special');
        this.activeDigitIndex = 0;
        const digits = comp.querySelectorAll('.digit-char');
        if (digits[this.activeDigitIndex]?.textContent === '_') digits[this.activeDigitIndex].textContent = '0';
        this.updateDigitHighlight()
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
        this.activeDigitIndex = 0
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
        this.updateDigitHighlight()
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
        if (slider.dataset.callbackId) this.triggerCallback(slider)
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
        this.highlightKeypadKey()
    }

    stopKeypadEdit() {

        if (!this.isEditingKeypad) return;
        this.isEditingKeypad = false;
        if (this.activeKeypadComponent) {
            this.activeKeypadComponent.querySelectorAll('.keypad-key').forEach(k => k.classList.remove('active-key'));
        }
        this.activeKeypadComponent = null;
        this.cursor?.classList.remove('editing-special')
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
        this.highlightKeypadKey()
    }

    highlightKeypadKey() {

        if (!this.activeKeypadComponent) return;
        this.activeKeypadComponent.querySelectorAll('.keypad-key').forEach(k => k.classList.remove('active-key'));
        const rows = this.activeKeypadComponent.querySelectorAll('.keypad-row');
        const keys = rows[this.activeKeypadRow]?.querySelectorAll('.keypad-key');
        if (keys?.[this.activeKeypadCol]) keys[this.activeKeypadCol].classList.add('active-key');
        const keyEl = keys?.[this.activeKeypadCol];
        if (keyEl && this.cursor) {
            const kp = this.activeKeypadComponent;
            const relTop = keyEl.offsetTop;
            const relLeft = keyEl.offsetLeft;
        
};

CARNIVALTerminal.prototype.handleKeypadKey = function(comp) {
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
        this.highlightKeypadKey()
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
        if (digits && digits.dataset.callbackId) this.triggerCallback(digits)
    }

    startDragbarEdit(e, comp) {

        this.isEditingSlider = true;
        this.activeSliderComponent = comp;
        this.cursor?.classList.add('editing-special')
    }

    stopDragbarEdit() {

        if (this.activeSliderComponent?.dataset?.callbackId) this.triggerCallback(this.activeSliderComponent);
        this.isEditingSlider = false;
        this.activeSliderComponent = null;
        this.cursor?.classList.remove('editing-special')
    }

    updateDragbarUI(comp, val) {

        comp.dataset.value = String(val);
        const fill = comp.querySelector('.dragbar-fill');
        const thumb = comp.querySelector('.dragbar-thumb');
        const valueEl = comp.querySelector('.dragbar-value');
        if (fill) fill.style.width = val + '%';
        if (thumb) thumb.style.left = val + '%';
        if (valueEl) valueEl.textContent = val + '%'
    }

    triggerCallback(comp) {

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
        }
    }

    snapToComponent(comp) {

        if (!this.mouseCursor) return;
        this.snappedComp = comp;
        this.mouseCursor.classList.add('snapped');
        this.mouseCursor.classList.remove('fading');
        this.mouseCursor.style.opacity = '1';
        if (this.cursor) { this.cursor.classList.remove('fade-in'); this.cursor.classList.add('mouse-active'); }
        const r = comp.getBoundingClientRect();
        this.mouseCursor.style.top = r.top + 'px';
        this.mouseCursor.style.left = r.left + 'px';
        this.mouseCursor.style.width = r.width + 'px';
        this.mouseCursor.style.height = r.height + 'px';
        this.mouseCursor.style.display = 'block';
        this.grid.forEach(r => r.forEach(c => c.classList.remove('hover')));
        comp.classList.add('hover')
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
            this.mouseCursor.style.opacity = '1';
            this.mouseCursor.style.display = 'block';
            if (this.cursor) this.cursor.classList.remove('fade-in');
        }

        const all = this.activePanel?.querySelectorAll(
            'button.terminal-component, input.terminal-component, ' +
            '.digit-string-component, [data-type="switch"], [data-type="toggle"], ' +
            '[data-type="slider"], [data-type="checkbox"], [data-type="dropdown"], ' +
            '[data-type="keypad"], [data-type="long-press"], [data-type="digit-string"], ' +
            '[data-type="dragbar"]'
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
            if (this.cursor) { this.cursor.classList.remove('fade-in'); this.cursor.classList.add('mouse-active'); }
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
            if (this.cursor) { this.cursor.classList.remove('fade-in'); this.cursor.classList.add('mouse-active'); }
            this.grid.forEach(r => r.forEach(c => c.classList.remove('active', 'hover')));
        }
        this.mouseIdleTimer = setTimeout(() => {
            this.isMouseIdle = true;
            this.mouseCursor.classList.add('fading');
            this.mouseFadeTimer = setTimeout(() => {
                this.mouseCursor.style.display = 'none';
                if (this.cursor) { this.cursor.classList.remove('mouse-active'); this.cursor.classList.add('fade-in'); }
                this.updateHighlight();
            }, this.fadeDuration);
        }, this.mouseIdleDelay)
    }

    handleMouseDown(e) {

        const comp = this.snappedComp;
        if (!comp) return;
        this.isMouseDown = true;
        this.mouseCursor.classList.add('clicked');
        if (this.cursor) { this.cursor.classList.remove('fade-in'); this.cursor.classList.add('mouse-active'); }
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
        else { this.activateComponent(comp); }
    }

    handleMouseUp(e) {

        this.isMouseDown = false;
        if (this.mouseCursor) this.mouseCursor.classList.remove('clicked');
        if (this.cursor) this.cursor.classList.remove('activated')
    }

    openModal(modalId) {

        const m = document.querySelector('[data-modal-id="' + modalId + '"]');
        if (m) m.dataset.visible = 'true'
    }

    closeModal(modalId) {

        const m = document.querySelector('[data-modal-id="' + modalId + '"]');
        if (m) m.dataset.visible = 'false'
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
        }
    }

    stopCountdown() {

        if (this.countdownInterval) { clearInterval(this.countdownInterval); this.countdownInterval = null; }
    }

    resetTypewriter() {

        this.typewriterInputBuffer = '';
        const msg = document.getElementById('typewriter-message-display');
        const big = document.getElementById('typewriter-large-char-display');
        if (msg) { msg.textContent = this.activePanel.dataset.typewriterPrompt || 'Press any letter key...'; msg.classList.remove('hidden'); }
        if (big) big.classList.remove('visible')
    }

    handleTypewriterLetterDown(key) {

        const msg = document.getElementById('typewriter-message-display');
        const big = document.getElementById('typewriter-large-char-display');
        if (msg) msg.classList.add('hidden');
        if (big) { big.textContent = key.toUpperCase(); big.classList.add('visible'); }
        this.typewriterInputBuffer += key.toLowerCase();
        this.checkTypewriterSecrets()
    }

    handleTypewriterLetterUp() {

        const big = document.getElementById('typewriter-large-char-display');
        if (big) big.classList.remove('visible')
    }

    checkTypewriterSecrets() {

        const secretStr = this.activePanel?.dataset?.secretWords;
        if (!secretStr) return;
        let secrets;
        try { secrets = JSON.parse(secretStr); } catch(e) { return; }
        const msg = document.getElementById('typewriter-message-display');
        for (const [word, response] of Object.entries(secrets)) {
            if (this.typewriterInputBuffer.endsWith(word)) {
            
};

CARNIVALTerminal.prototype.openDialog = function(dialogId) {
        const dlg = document.querySelector('[data-dialog-id="' + dialogId + '"]');
        if (!dlg) return;
        dlg.dataset.visible = 'true';
        const btn = dlg.querySelector('.dialog-confirm, .modal-confirm');
        if (btn) setTimeout(() => btn.focus(), 50);
    }
};

CARNIVALTerminal.prototype.closeDialog = function(dialogId) {
        const dlg = document.querySelector('[data-dialog-id="' + dialogId + '"]');
        if (!dlg) return;
        dlg.dataset.visible = 'false';
        if (this.grid.length > 0) {
        
};

CARNIVALTerminal.prototype.showError = function(msg) {
        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const err = document.createElement('div');
        err.className = 'terminal-component';
        err.style.cssText = 'color:#ff4444;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        err.textContent = msg;
        container.appendChild(err);
    
};

CARNIVALTerminal.prototype.showSuccess = function(msg) {
        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const el = document.createElement('div');
        el.className = 'terminal-component';
        el.style.cssText = 'color:#2a9d8f;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        el.textContent = msg;
        container.appendChild(el);
    
};




window.CARNIVALTerminal = CARNIVALTerminal;
})()
    }

    openDialog(dialogId) {

        const dlg = document.querySelector('[data-dialog-id="' + dialogId + '"]');
        if (!dlg) return;
        dlg.dataset.visible = 'true';
        const btn = dlg.querySelector('.dialog-confirm, .modal-confirm');
        if (btn) setTimeout(() => btn.focus(), 50)
    }

    closeDialog(dialogId) {

        const dlg = document.querySelector('[data-dialog-id="' + dialogId + '"]');
        if (!dlg) return;
        dlg.dataset.visible = 'false';
        if (this.grid.length > 0) {
        
};

CARNIVALTerminal.prototype.showError = function(msg) {
        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const err = document.createElement('div');
        err.className = 'terminal-component';
        err.style.cssText = 'color:#ff4444;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        err.textContent = msg;
        container.appendChild(err);
    
};

CARNIVALTerminal.prototype.showSuccess = function(msg) {
        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const el = document.createElement('div');
        el.className = 'terminal-component';
        el.style.cssText = 'color:#2a9d8f;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        el.textContent = msg;
        container.appendChild(el);
    
};




window.CARNIVALTerminal = CARNIVALTerminal
    }

    showError(msg) {

        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const err = document.createElement('div');
        err.className = 'terminal-component';
        err.style.cssText = 'color:#ff4444;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        err.textContent = msg;
        container.appendChild(err)
    }

    showSuccess(msg) {

        const container = this.activePanel?.querySelector('.component-container');
        if (!container) return;
        const el = document.createElement('div');
        el.className = 'terminal-component';
        el.style.cssText = 'color:#2a9d8f;padding:2px 4px;font-size:calc(var(--terminal-font-size)*0.85)';
        el.textContent = msg;
        container.appendChild(el)
    }
}

window.CARNIVALTerminal = CARNIVALTerminal;
})();