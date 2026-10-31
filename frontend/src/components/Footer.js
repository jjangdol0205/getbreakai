export function renderFooter(state) {
  const t = state.t;

  return `
    <footer class="footer">
      <p><b>Regulatory & Compliance Disclaimer (Lemon Squeezy / Global MoR Standard):</b> ${t.disclaimer}</p>
      <p style="margin-top:8px;">${t.copyright}</p>
    </footer>
  `;
}
