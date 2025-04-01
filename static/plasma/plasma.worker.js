/* jshint esversion: 8 */

let ctx, WIDTH, HEIGHT, PLASMA_CONFIG;
let time = 0;
let imgData, rawImgData; // Declare these globally for reuse

let startTime = performance.now();
let frameCount = 0;


function HSVtoRGB(h, s, v) 
{
    h /= 60; // Sector 0-5
    s /= 100;
    v /= 100;
    const i = Math.floor(h);
    const f = h - i;
    const p = v * (1 - s);
    const q = v * (1 - s * f);
    const t = v * (1 - s * (1 - f));
    const [r, g, b] = i === 0 ? [v, t, p]
                    : i === 1 ? [q, v, p]
                    : i === 2 ? [p, v, t]
                    : i === 3 ? [p, q, v]
                    : i === 4 ? [t, p, v]
                              : [v, p, q];

    return [
        Math.round(r * 255),
        Math.round(g * 255),
        Math.round(b * 255),
        255
    ];
}


function render() 
{
    for (let y = 0; y < HEIGHT; y++) {
        const isEven = y % 2 === 0;
        const params = isEven ? PLASMA_CONFIG.PARAMS.EVEN_LINE
            : PLASMA_CONFIG.PARAMS.ODD_LINE;
        
        const zy = zyi[y] + params.PHASE_OFFSET;
        for (let x = 0; x < WIDTH; x++) {
            // Apply zoom and phase offset
            const zx = zxi[x] + params.PHASE_OFFSET;
            // Wave equation components
            const value = PLASMA_CONFIG.WAVE_OFFSET + PLASMA_CONFIG.WAVE_AMPLITUDE * (
                Math.sin(zx                 / params.SCALES[0] + time * params.SPEEDS[0]) +
                Math.sin(zy                 / params.SCALES[1] + time * params.SPEEDS[1]) +
                Math.sin((zx + zy)          / params.SCALES[2] + time * params.SPEEDS[2]) +
                Math.sin(Math.hypot(zx, zy) / params.SCALES[3] - time * params.SPEEDS[3]));

            const idx = (y * WIDTH + x) * 4;

            if (params.COLOR_MODE === "grayscale") {
                // Grayscale conversion
                const gray = Math.min(255, Math.max(0,
                        value *
                            params.GRAYSCALE.CONTRAST *
                            params.GRAYSCALE.BRIGHTNESS ));
                rawImgData[idx]   = gray * params.GRAYSCALE.RED_COEFF;
                rawImgData[idx+1] = gray * params.GRAYSCALE.GREEN_COEFF;
                rawImgData[idx+2] = gray * params.GRAYSCALE.BLUE_COEFF;
                rawImgData[idx+3] = 255;
            } 
            else if (params.COLOR_MODE === "hsv") {
                // HSV color conversion
                const hue = (value + time * params.HSV.HUE_CYCLE_SPEED * 100) % 360;
                const brightness =
                    params.HSV.BRIGHTNESS +
                    Math.sin(time) * params.HSV.BRIGHTNESS_VAR;
                const rgb = HSVtoRGB(
                    hue,
                    params.HSV.SATURATION,
                    brightness,
                );
                rawImgData[idx]   = rgb[0];
                rawImgData[idx+1] = rgb[1];
                rawImgData[idx+2] = rgb[2];
                rawImgData[idx+3] = rgb[3];
            } 
            else {
                rawImgData[idx]   = 0;
                rawImgData[idx+1] = 0;
                rawImgData[idx+2] = 0;
                rawImgData[idx+3] = 255;
            }
        }
    }

    ctx.putImageData(imgData, 0, 0);
    time += PLASMA_CONFIG.BASE_SPEED;

    frameCount++;
    if (frameCount%50==0) {
        newTime = performance.now();
        console.log( "FPS: " + 1000*frameCount / (newTime - startTime ));
        frameCount = 0;
        startTime = newTime;
    }
    requestAnimationFrame(render);
}


onmessage = function (e) {
    switch (e.data.type) {
        case 'init':
            const { canvas, config, dpr, width, height } = e.data;
            ctx = canvas.getContext('2d', { desynchronized: true });
            PLASMA_CONFIG = config;
            WIDTH = width;
            HEIGHT = height;

            // Scale the drawing context to match the device pixel ratio
            ctx.scale(dpr, dpr);
            imgData = ctx.createImageData(canvas.width, canvas.height);
            rawImgData = imgData.data;

            zxi = new Float32Array(WIDTH);
            zyi = new Float32Array(HEIGHT);            
            for (let x = 0; x < WIDTH; x++) {
                zxi[x] = x / PLASMA_CONFIG.ZOOM_FACTOR;
            }
            
            for (let y = 0; y < HEIGHT; y++) {
                zyi[y] = y / PLASMA_CONFIG.ZOOM_FACTOR;
            }

            break;

        case 'start':
            requestAnimationFrame(render);
            break;
    }
};
