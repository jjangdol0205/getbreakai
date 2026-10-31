export function renderCrossBanner(state) {
  const t = state.t;

  return `
    <section class="cross-banner">
      <div>
        <div style="font-size:0.78rem; font-weight:800; color:#93c5fd; text-transform:uppercase;">${t.crossTitle}</div>
        <h3 style="font-size:1.2rem; font-weight:900; margin:4px 0;">${t.crossHeading}</h3>
        <p style="font-size:0.88rem; color:var(--muted); max-width:820px;">
          ${t.crossDesc}
        </p>
      </div>
      <a class="btn btn-purple" href="https://truthofmarket.com" target="_blank" rel="noopener noreferrer">
        ${t.crossBtn}
      </a>
    </section>
  `;
}
