
document.addEventListener('DOMContentLoaded', function() {
    // Farbkreis zeichnen
    drawColorWheel();

    // Event-Listener für Klicks auf den Farbkreis
    const canvas = document.getElementById('colorWheel');
    if (canvas) {
        canvas.addEventListener('click', function(event) {
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;

            // Farbwerte aus dem Klickpunkt berechnen
            const color = getColorFromWheel(x, y);
            if (color) {
                updateAllColorValues(color.r, color.g, color.b);
                updateColorPoint(x, y);
            }
        });
    }
});

// Zeichnet den Farbkreis
function drawColorWheel() {
    const canvas = document.getElementById('colorWheel');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 5;

    // Koordinaten für spätere Klickberechnungen
    canvas.centerX = centerX;
    canvas.centerY = centerY;
    canvas.radius = radius;

    for (let angle = 0; angle < 360; angle += 1) {
        const startAngle = (angle - 2) * Math.PI / 180;
        const endAngle = (angle + 2) * Math.PI / 180;

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, startAngle, endAngle);
        ctx.closePath();

        // HSV zu RGB: Volles S und V, nur H ändert sich mit dem Winkel
        const h = angle / 360;
        const s = 1.0;
        const v = 1.0;
        const rgb = HSVtoRGB(h, s, v);

        ctx.fillStyle = `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`;
        ctx.fill();
    }

    // Weißer Kreis in der Mitte für Helligkeit/Sättigung
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius / 3, 0, Math.PI * 2);
    ctx.fillStyle = 'white';
    ctx.fill();
}

// Berechnet die Farbe aus der Position im Farbkreis
function getColorFromWheel(x, y) {
    const canvas = document.getElementById('colorWheel');
    if (!canvas) return null;

    const centerX = canvas.centerX;
    const centerY = canvas.centerY;
    const radius = canvas.radius;

    // Abstand vom Zentrum
    const dx = x - centerX;
    const dy = y - centerY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    // Wenn außerhalb des Kreises, keine Farbe zurückgeben
    if (distance > radius) return null;

    // Winkel berechnen (0-360 Grad)
    let angle = Math.atan2(dy, dx) * 180 / Math.PI;
    if (angle < 0) angle += 360;

    // Sättigung basierend auf Abstand vom Zentrum
    const saturation = Math.min(distance / radius, 1);

    // HSV zu RGB konvertieren
    const h = angle / 360;
    const s = saturation;
    const v = 1.0;

    return HSVtoRGB(h, s, v);
}

// Aktualisiert den Farbpunkt auf dem Farbkreis
function updateColorPoint(x, y) {
    const point = document.getElementById('selected-color-point');
    if (!point) return;

    point.style.display = 'block';
    point.style.left = `${x}px`;
    point.style.top = `${y}px`;
}

// Aktualisiert alle Farbwerte basierend auf den RGB-Werten
function updateAllColorValues(r, g, b) {
    // RGB-Werte aktualisieren
    document.getElementById('r-slider').value = r;
    document.getElementById('g-slider').value = g;
    document.getElementById('b-slider').value = b;
    document.getElementById('r-value').textContent = r;
    document.getElementById('g-value').textContent = g;
    document.getElementById('b-value').textContent = b;

    // HEX-Wert berechnen und aktualisieren
    const hex = RGBtoHEX(r, g, b);
    document.getElementById('hex-value').value = hex;

    // HSL-Wert berechnen und aktualisieren
    const hsl = RGBtoHSL(r, g, b);
    document.getElementById('hsl-value').value = `${hsl.h}, ${hsl.s}%, ${hsl.l}%`;

    // HSV-Wert berechnen und aktualisieren
    const hsv = RGBtoHSV(r, g, b);
    document.getElementById('hsv-value').value = `${hsv.h}, ${hsv.s}%, ${hsv.v}%`;

    // Farbvorschau aktualisieren
    updateColorPreview(hex);
}

// Aktualisiert die Farbvorschau
function updateColorPreview(hexColor) {
    const preview = document.querySelector('.color-converter-result .row:first-child .col-md-6 > div:first-child');
    if (preview) {
        preview.style.backgroundColor = hexColor;
    }
}

// Aktualisiert Farbe basierend auf Slidern
function updateFromSliders() {
    const r = parseInt(document.getElementById('r-slider').value);
    const g = parseInt(document.getElementById('g-slider').value);
    const b = parseInt(document.getElementById('b-slider').value);

    document.getElementById('r-value').textContent = r;
    document.getElementById('g-value').textContent = g;
    document.getElementById('b-value').textContent = b;

    updateAllColorValues(r, g, b);
}

// Aktualisiert Farbe basierend auf Texteingabe
function updateColorFromInput(input) {
    const format = input.dataset.format;
    const value = input.value.trim();

    try {
        let r, g, b;

        if (format === 'HEX') {
            const hex = value.replace('#', '');
            r = parseInt(hex.substr(0, 2), 16);
            g = parseInt(hex.substr(2, 2), 16);
            b = parseInt(hex.substr(4, 2), 16);
        } else if (format === 'RGB') {
            const rgbValues = value.split(',').map(v => parseInt(v.trim()));
            r = rgbValues[0];
            g = rgbValues[1];
            b = rgbValues[2];
        } else if (format === 'HSL') {
            const hslValues = value.split(',').map(v => parseFloat(v.trim().replace('%', '')));
            const h = hslValues[0] / 360;
            const s = hslValues[1] / 100;
            const l = hslValues[2] / 100;
            const rgb = HSLtoRGB(h, s, l);
            r = rgb.r;
            g = rgb.g;
            b = rgb.b;
        } else if (format === 'HSV') {
            const hsvValues = value.split(',').map(v => parseFloat(v.trim().replace('%', '')));
            const h = hsvValues[0] / 360;
            const s = hsvValues[1] / 100;
            const v = hsvValues[2] / 100;
            const rgb = HSVtoRGB(h, s, v);
            r = rgb.r;
            g = rgb.g;
            b = rgb.b;
        }

        // Wenn gültige RGB-Werte, aktualisiere alles
        if (!isNaN(r) && !isNaN(g) && !isNaN(b)) {
            updateAllColorValues(r, g, b);
        }
    } catch (e) {
        console.error("Fehler beim Parsen der Farbe:", e);
    }
}

// Setzt eine bestimmte Farbe (für Standard-Farbpalette)
function setColor(hexColor) {
    document.getElementById('hex-value').value = hexColor;
    updateColorFromInput(document.getElementById('hex-value'));
}

// Hilfs-Konvertierungsfunktionen
function RGBtoHEX(r, g, b) {
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
}

function RGBtoHSL(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, l = (max + min) / 2;

    if (max === min) {
        h = s = 0; // achromatic
    } else {
        const d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }

        h /= 6;
    }

    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        l: Math.round(l * 100)
    };
}

function RGBtoHSV(r, g, b) {
    r /= 255;
    g /= 255;
    b /= 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    let h, s, v = max;

    const d = max - min;
    s = max === 0 ? 0 : d / max;

    if (max === min) {
        h = 0; // achromatic
    } else {
        switch (max) {
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }

        h /= 6;
    }

    return {
        h: Math.round(h * 360),
        s: Math.round(s * 100),
        v: Math.round(v * 100)
    };
}

function HSLtoRGB(h, s, l) {
    let r, g, b;

    if (s === 0) {
        r = g = b = l; // achromatic
    } else {
        const hue2rgb = (p, q, t) => {
            if (t < 0) t += 1;
            if (t > 1) t -= 1;
            if (t < 1/6) return p + (q - p) * 6 * t;
            if (t < 1/2) return q;
            if (t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        };

        const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        const p = 2 * l - q;

        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}

function HSVtoRGB(h, s, v) {
    let r, g, b;

    const i = Math.floor(h * 6);
    const f = h * 6 - i;
    const p = v * (1 - s);
    const q = v * (1 - f * s);
    const t = v * (1 - (1 - f) * s);

    switch (i % 6) {
        case 0: r = v; g = t; b = p; break;
        case 1: r = q; g = v; b = p; break;
        case 2: r = p; g = v; b = t; break;
        case 3: r = p; g = q; b = v; break;
        case 4: r = t; g = p; b = v; break;
        case 5: r = v; g = p; b = q; break;
    }

    return {
        r: Math.round(r * 255),
        g: Math.round(g * 255),
        b: Math.round(b * 255)
    };
}