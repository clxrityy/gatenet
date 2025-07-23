// network-footer.js - Animated networking footer for Sphinx docs

document.addEventListener("DOMContentLoaded", function () {
  // Mark JS as enabled for fallback hiding
  document.body.classList.add("js-enabled");
  const footer = document.querySelector("footer, .footer");
  if (!footer) return;
  const container = document.createElement("div");
  container.id = "network-animation-footer";

  // SVG background: abstract purple wires
  const wires = document.createElement("div");
  wires.className = "network-wires-bg";
  wires.innerHTML = `
    <svg width="260" height="80" viewBox="0 0 260 80" fill="none" xmlns="http://www.w3.org/2000/svg">
      <g opacity="0.32">
        <path d="M10 60 Q 60 10, 130 40 T 250 60" stroke="#8000ff" stroke-width="2.5" fill="none" filter="url(#glow1)"/>
        <path d="M30 70 Q 80 30, 130 60 T 230 30" stroke="#a366ff" stroke-width="1.5" fill="none" filter="url(#glow2)"/>
        <path d="M20 40 Q 90 80, 200 20 T 240 70" stroke="#c299fc" stroke-width="1.2" fill="none" filter="url(#glow3)"/>
      </g>
      <defs>
        <filter id="glow1" x="-20" y="-20" width="300" height="120">
          <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <filter id="glow2" x="-20" y="-20" width="300" height="120">
          <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
        <filter id="glow3" x="-20" y="-20" width="300" height="120">
          <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>
    </svg>
  `;
  container.appendChild(wires);

  // Main animation
  container.innerHTML += `
      <div class="network-animation">
        <span class="node"></span>
        <span class="line"></span>
        <span class="node"></span>
        <span class="line"></span>
        <span class="node"></span>
        <span class="line"></span>
        <span class="node"></span>
      </div>
    `;
  footer.appendChild(container);

  // Animate the blue lines to fade in/out at the nodes (electricity effect)
  function animateLines() {
    const lines = container.querySelectorAll(".network-animation .line");
    const t = Date.now() / 1000;
    for (let i = 0; i < lines.length; ++i) {
      // Each line is active (bright) in a wave pattern
      let phase = t * 1.2 + i * 0.7;
      if (Math.sin(phase) > 0.5) {
        lines[i].classList.add("active");
      } else {
        lines[i].classList.remove("active");
      }
    }
    requestAnimationFrame(animateLines);
  }
  animateLines();
});
