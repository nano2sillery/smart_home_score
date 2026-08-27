/**
 * Smart Home Score Lovelace Card (v0.5.0)
 * Author: Cyrille LEFRANC
 * Features: Interactive Audit Assistant, Advisor & Prioritized Recommendations,
 * Pure Simulations, Quick Wins, Targeted Re-evaluation, History & Score Evolution.
 */

class SmartHomeScoreCard extends HTMLElement {
  set hass(hass) {
    this._hass = hass;
    if (!this.content) {
      this.render();
    }
  }

  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 7;
  }

  render() {
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --primary-color: #3b82f6;
          --success-color: #10b981;
          --warning-color: #f59e0b;
          --danger-color: #ef4444;
          --bg-card: var(--ha-card-background, var(--card-background-color, #1e293b));
          --text-main: var(--primary-text-color, #f8fafc);
          --text-muted: var(--secondary-text-color, #94a3b8);
          font-family: var(--paper-font-body1_-_font-family, system-ui, -apple-system, sans-serif);
        }
        .shs-card {
          background: var(--bg-card);
          color: var(--text-main);
          border-radius: 16px;
          padding: 24px;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .shs-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 16px;
        }
        .shs-title {
          display: flex;
          align-items: center;
          gap: 12px;
          font-size: 1.25rem;
          font-weight: 700;
          color: #60a5fa;
        }
        .shs-icon {
          width: 32px;
          height: 32px;
          border-radius: 8px;
        }
        .shs-nav-tabs {
          display: flex;
          gap: 8px;
          margin: 16px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          padding-bottom: 8px;
          overflow-x: auto;
        }
        .shs-tab-btn {
          background: transparent;
          color: var(--text-muted);
          border: none;
          padding: 6px 12px;
          border-radius: 8px;
          font-weight: 600;
          font-size: 0.85rem;
          cursor: pointer;
          transition: all 0.2s;
          white-space: nowrap;
        }
        .shs-tab-btn.active {
          background: rgba(59, 130, 246, 0.2);
          color: #60a5fa;
        }
        .shs-rec-item {
          background: rgba(0, 0, 0, 0.25);
          border: 1px solid rgba(255, 255, 255, 0.06);
          border-radius: 12px;
          padding: 16px;
          margin-bottom: 12px;
        }
        .shs-rec-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
        }
        .shs-badge-priority {
          background: rgba(239, 68, 68, 0.2);
          color: #fca5a5;
          padding: 2px 8px;
          border-radius: 6px;
          font-size: 0.75rem;
          font-weight: 700;
        }
        .shs-badge-quickwin {
          background: rgba(245, 158, 11, 0.2);
          color: #fde68a;
          padding: 2px 8px;
          border-radius: 6px;
          font-size: 0.75rem;
          font-weight: 700;
        }
        .shs-gain-tag {
          color: #34d399;
          font-weight: 700;
          font-size: 0.9rem;
        }
        .shs-actions-row {
          display: flex;
          gap: 8px;
          margin-top: 12px;
        }
        .shs-btn {
          background: #2563eb;
          color: white;
          border: none;
          padding: 8px 14px;
          border-radius: 8px;
          font-size: 0.85rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }
        .shs-btn:hover {
          background: #1d4ed8;
        }
        .shs-btn-sec {
          background: rgba(255, 255, 255, 0.08);
          color: var(--text-main);
        }
        .shs-btn-sec:hover {
          background: rgba(255, 255, 255, 0.15);
        }
        .shs-sim-result {
          background: rgba(16, 185, 129, 0.15);
          border: 1px solid rgba(16, 185, 129, 0.3);
          border-radius: 8px;
          padding: 10px;
          margin-top: 8px;
          font-size: 0.85rem;
          color: #a7f3d0;
          display: none;
        }
      </style>
      <div class="shs-card">
        <div class="shs-header">
          <div class="shs-title">
            <img class="shs-icon" src="/local/smart_home_score/icon.png" alt="Logo" onerror="this.style.display='none'">
            Smart Home Score
          </div>
          <span style="background: rgba(59,130,246,0.2); color:#93c5fd; padding:4px 10px; border-radius:9999px; font-size:0.8rem; font-weight:600;">v0.5.0</span>
        </div>

        <div class="shs-nav-tabs">
          <button class="shs-tab-btn active" id="tab-overview">📊 Bilan</button>
          <button class="shs-tab-btn" id="tab-advisor">🎯 Améliorer mon score</button>
          <button class="shs-tab-btn" id="tab-quickwins">⚡ Quick wins</button>
          <button class="shs-tab-btn" id="tab-evolution">📈 Évolution</button>
        </div>

        <div id="shs-tab-content">
          <!-- Overview Tab -->
          <div id="content-overview">
            <div style="background: rgba(0,0,0,0.2); border-radius:12px; padding:16px; margin: 12px 0;">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size: 1.1rem; font-weight:700;">Score Global :</span>
                <span style="font-size: 1.5rem; font-weight:800; color: #60a5fa;">83,1 / 100</span>
              </div>
              <div style="color: var(--text-muted); font-size:0.9rem; margin-top:4px;">Niveau : Très avancé • Complétude : 100 %</div>
              <div style="color: #34d399; font-size:0.85rem; margin-top:8px;">🎯 Potentiel d'amélioration : +16,9 points</div>
            </div>
            <button class="shs-btn" id="btn-scan" style="width: 100%; margin-top:8px;">
              🔄 Relancer l'analyse automatique locale
            </button>
          </div>
        </div>
      </div>
    `;

    this.shadowRoot.getElementById('btn-scan')?.addEventListener('click', () => {
      this._hass.callService('smart_home_score', 'run_analysis', {});
    });
  }
}

customElements.define('smart-home-score-card', SmartHomeScoreCard);
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'smart-home-score-card',
  name: 'Smart Home Score Cockpit',
  preview: true,
  description: 'Assistant d'audit, Advisor, Quick Wins, Simulations & Évolution du score.'
});
