/* jshint esversion: 8 */

/* PLASMA CONFIGURATION */
function config1() {
  const PLASMA_CONFIG = {
    ZOOM_FACTOR: 10, // Zoom level (1 = full view, higher = zoomed in)
    WAVE_AMPLITUDE: 32, // Intensity multiplier for wave values
    WAVE_OFFSET: 128, // Base value offset (center point)
    BASE_SPEED: 0.05, // Global animation speed multiplier

    PARAMS: {
      EVEN_LINE: {
        // SCALES[0]: Horizontal wave density: Smaller values, tighter ripples
        // SCALES[1]: Vertical wave density: Smaller values, tighter ripples
        // SCALES[2]: Diagonal wave density: Smaller values, finer diagonal patterns
        // SCALES[3]: Radial wave density
        SCALES: [20.6, 10.4, 20.8, 7.9],
        SPEEDS: [-0.72, -1.28, 1.5, 2], // Time multipliers for wave progression
        PHASE_OFFSET: Math.PI / 2.1, // Phase shift between lines
        COLOR_MODE: "hsv", // 'hsv' or 'grayscale'
        HSV: {
          SATURATION: 85, // 0-100% color intensity
          BRIGHTNESS: 65, // Base brightness (0-100)
          BRIGHTNESS_VAR: 15, // Brightness variation amplitude
          HUE_CYCLE_SPEED: 0.35, // Color cycling speed (0 = static)
        },
        GRAYSCALE: {
          RED_COEFF: 0.587, // Luminance coefficients (ITU-R BT.601)
          GREEN_COEFF: 0.587,
          BLUE_COEFF: 0.587,
          CONTRAST: 0.8, // Value scaling (0-1 = low-high contrast)
          BRIGHTNESS: 1.25, // Brightness multiplier
        },
      },
      ODD_LINE: {
        SCALES: [5.2, 10.0, 15.4, 9.0],
        SPEEDS: [1.37, 0.76, 0.56, 2.1],
        PHASE_OFFSET: Math.PI / 1.7,
        COLOR_MODE: "hsv",
        HSV: {
          SATURATION: 85,
          BRIGHTNESS: 65,
          BRIGHTNESS_VAR: 25,
          HUE_CYCLE_SPEED: 0.25,
        },
        GRAYSCALE: {
          RED_COEFF: 0.3,
          GREEN_COEFF: 0.3,
          BLUE_COEFF: 0.3,
          CONTRAST: 0.9,
          BRIGHTNESS: 1.2,
        },
      },
    },
  };
  return PLASMA_CONFIG;
}
