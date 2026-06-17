/* ================================================================
   Optimised Particle Network — Three.js r128
   Max 150 particles, low-poly, requestAnimationFrame throttled
   ================================================================ */
'use strict';
(function () {
  if (typeof THREE === 'undefined') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const canvas = document.getElementById('particle-canvas');
  if (!canvas) return;

  const scene    = new THREE.Scene();
  const camera   = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 1, 2000);
  camera.position.z = 420;

  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.2));
  renderer.setSize(window.innerWidth, window.innerHeight);

  // ── Particles ────────────────────────────────────────────
  const COUNT = 130;
  const pos   = new Float32Array(COUNT * 3);
  const vel   = [];

  for (let i = 0; i < COUNT; i++) {
    pos[i*3]   = (Math.random() - 0.5) * 900;
    pos[i*3+1] = (Math.random() - 0.5) * 700;
    pos[i*3+2] = (Math.random() - 0.5) * 400;
    vel.push({
      x: (Math.random() - 0.5) * 0.18,
      y: (Math.random() - 0.5) * 0.18,
    });
  }

  const geom = new THREE.BufferGeometry();
  geom.setAttribute('position', new THREE.BufferAttribute(pos, 3));

  const mat = new THREE.PointsMaterial({
    color: 0x00D9FF, size: 2.2, transparent: true,
    opacity: 0.50, sizeAttenuation: true,
  });

  scene.add(new THREE.Points(geom, mat));

  // ── Connection lines ─────────────────────────────────────
  const lineMat   = new THREE.LineBasicMaterial({ color: 0x00D9FF, transparent: true, opacity: 0.07 });
  const lineGroup = new THREE.Group();
  scene.add(lineGroup);

  let frameCount = 0;

  function updateLines() {
    while (lineGroup.children.length) {
      const c = lineGroup.children[0];
      c.geometry.dispose();
      lineGroup.remove(c);
    }
    const MAX_DIST = 140;
    for (let i = 0; i < COUNT; i++) {
      for (let j = i + 1; j < COUNT; j++) {
        const dx = pos[i*3] - pos[j*3];
        const dy = pos[i*3+1] - pos[j*3+1];
        if (Math.abs(dx) > MAX_DIST || Math.abs(dy) > MAX_DIST) continue;
        const dist = Math.sqrt(dx*dx + dy*dy + (pos[i*3+2]-pos[j*3+2])**2);
        if (dist < MAX_DIST) {
          const lg = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(pos[i*3], pos[i*3+1], pos[i*3+2]),
            new THREE.Vector3(pos[j*3], pos[j*3+1], pos[j*3+2]),
          ]);
          lineGroup.add(new THREE.Line(lg, lineMat));
        }
      }
    }
  }

  // ── Animate ──────────────────────────────────────────────
  function animate() {
    requestAnimationFrame(animate);
    frameCount++;
    if (frameCount % 2 !== 0) return;  // throttle to ~30fps

    for (let i = 0; i < COUNT; i++) {
      pos[i*3]   += vel[i].x;
      pos[i*3+1] += vel[i].y;
      if (Math.abs(pos[i*3])   > 450) vel[i].x *= -1;
      if (Math.abs(pos[i*3+1]) > 350) vel[i].y *= -1;
    }
    geom.attributes.position.needsUpdate = true;
    if (frameCount % 4 === 0) updateLines();
    renderer.render(scene, camera);
  }
  animate();

  // Resize
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }, { passive: true });
})();
