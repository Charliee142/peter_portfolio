/* ================================================================
   Hero 3D Scene (home page only) — Three.js r128
   Low-poly, optimised, ~30fps throttled
   ================================================================ */
'use strict';
(function () {
  if (typeof THREE === 'undefined') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const container = document.getElementById('threejs-hero');
  if (!container) return;

  const scene    = new THREE.Scene();
  const camera   = new THREE.PerspectiveCamera(55, window.innerWidth / window.innerHeight, 1, 1800);
  camera.position.set(0, 90, 320);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: false, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1.2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  container.appendChild(renderer.domElement);

  // Cyber grid plane
  const grid = new THREE.GridHelper(1100, 36, 0x00D9FF, 0x002838);
  grid.position.y = -55;
  scene.add(grid);

  // Floating low-poly orbs (16 sides = icosahedron detail 1)
  const orbGeo = new THREE.IcosahedronGeometry(4, 1);   // low-poly
  const orbMat = new THREE.MeshBasicMaterial({ color: 0x00D9FF, wireframe: true, transparent: true, opacity: 0.35 });
  const orbs   = [];
  for (let i = 0; i < 14; i++) {
    const o = new THREE.Mesh(orbGeo, orbMat);
    o.position.set(
      (Math.random()-0.5)*600, Math.random()*180-30,
      (Math.random()-0.5)*280-60
    );
    o.userData = { vx: (Math.random()-0.5)*0.22, vy: (Math.random()-0.5)*0.14 };
    scene.add(o); orbs.push(o);
  }

  let mouseX = 0, mouseY = 0;
  document.addEventListener('mousemove', e => {
    mouseX = (e.clientX / window.innerWidth  - 0.5) * 44;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 28;
  }, { passive: true });

  let t = 0; let frame = 0;
  function animate() {
    requestAnimationFrame(animate);
    frame++;
    if (frame % 2 !== 0) return;   // ~30fps
    t += 0.012;
    grid.position.z = (t * 7) % 30;
    orbs.forEach((o, i) => {
      o.position.x += o.userData.vx;
      o.position.y += Math.sin(t + i * 0.6) * 0.22;
      o.rotation.y += 0.012;
      if (Math.abs(o.position.x) > 320) o.userData.vx *= -1;
    });
    camera.position.x += (mouseX - camera.position.x) * 0.025;
    camera.position.y += (-mouseY + 90 - camera.position.y) * 0.025;
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  }, { passive: true });
})();
