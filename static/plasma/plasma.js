/* jshint esversion: 8 */

// Inspired by Second Reality (Future Crew)
// https://github.com/mtuomi/SecondReality/blob/master/PLZPART/PLZ.C

function startPlasma(canvas, config) {
  // Let responsive CSS own the logical size; match the rendering buffer to it.
  const rect = canvas.getBoundingClientRect();

  // Set the actual size of the canvas (scaled for high DPI)
  const dpr = window.devicePixelRatio || 1;
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;

  // Transfer canvas control to worker
  const offscreen = canvas.transferControlToOffscreen();
  const worker = new Worker("plasma.worker.js");

  // Send initialization data
  worker.postMessage(
    {
      type: "init",
      canvas: offscreen,
      config: config(),
      dpr: window.devicePixelRatio || 1,
      width: canvas.width,
      height: canvas.height,
    },
    [offscreen],
  );

  // Animation driver
  worker.postMessage({ type: "start" });
}
