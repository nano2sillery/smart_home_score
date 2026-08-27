/**
 * Smart Home Score Lovelace Card (v0.7.0-beta.2)
 * Author: Cyrille LEFRANC
 * 100% Local Lovelace UI Card for Home Assistant.
 * Zero-YAML card picker integration, resilient setConfig, dynamic audit rendering.
 */

class SmartHomeScoreCard extends HTMLElement {
  constructor() {
    super();
    this._config = {};
    this._hass = null;
    this._activeTab = 'overview';
    this.attachShadow({ mode: 'open' });
  }

  static getStubConfig() {
    return {};
  }

  setConfig(config) {
    this._config = config || {};
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    this._render();
  }

  getCardSize() {
    return 6;
  }

  _render() {
    if (!this.shadowRoot) return;

    const globalScoreSensor = this._hass?.states?.['sensor.smart_home_score_global_score'];
    const completenessSensor = this._hass?.states?.['sensor.smart_home_score_completeness'];
    const maturitySensor = this._hass?.states?.['sensor.smart_home_score_maturity_level'];
    const criticalSensor = this._hass?.states?.['sensor.smart_home_score_critical_risks'];
    const potentialGainSensor = this._hass?.states?.['sensor.smart_home_score_potential_gain'];

    const hasData = globalScoreSensor && globalScoreSensor.state !== 'unknown' && globalScoreSensor.state !== 'unavailable';
    const scoreVal = hasData ? parseFloat(globalScoreSensor.state) : 0.0;
    const completenessVal = completenessSensor && completenessSensor.state !== 'unknown' ? parseFloat(completenessSensor.state) : 0.0;
    const maturityText = maturitySensor?.state && maturitySensor.state !== 'unknown' ? maturitySensor.state : 'Non évalué';
    const criticalCount = criticalSensor?.state && criticalSensor.state !== 'unknown' ? parseInt(criticalSensor.state, 10) : 0;
    const potentialGain = potentialGainSensor?.state && potentialGainSensor.state !== 'unknown' ? parseFloat(potentialGainSensor.state) : 0.0;

    const isProvisional = globalScoreSensor?.attributes?.is_provisional ?? (completenessVal < 100);

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --shs-primary: #3b82f6;
          --shs-success: #10b981;
          --shs-warning: #f59e0b;
          --shs-danger: #ef4444;
          --shs-bg: var(--ha-card-background, var(--card-background-color, #1e293b));
          --shs-text: var(--primary-text-color, #f8fafc);
          --shs-muted: var(--secondary-text-color, #94a3b8);
          font-family: var(--paper-font-body1_-_font-family, system-ui, -apple-system, sans-serif);
          display: block;
        }
        .shs-container {
          background: var(--shs-bg);
          color: var(--shs-text);
          border-radius: 16px;
          padding: 20px;
          box-shadow: var(--ha-card-box-shadow, 0 4px 20px rgba(0,0,0,0.25));
          border: 1px solid rgba(255, 255, 255, 0.08);
          box-sizing: border-box;
        }
        .shs-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 16px;
        }
        .shs-branding {
          display: flex;
          align-items: center;
          gap: 10px;
          font-size: 1.15rem;
          font-weight: 700;
          color: #60a5fa;
        }
        .shs-badge-beta {
          background: rgba(59, 130, 246, 0.18);
          color: #93c5fd;
          padding: 3px 8px;
          border-radius: 9999px;
          font-size: 0.75rem;
          font-weight: 600;
        }
        .shs-welcome-box {
          background: rgba(0, 0, 0, 0.2);
          border: 1px dashed rgba(255, 255, 255, 0.15);
          border-radius: 12px;
          padding: 24px;
          text-align: center;
          margin: 12px 0;
        }
        .shs-welcome-title {
          font-size: 1.2rem;
          font-weight: 700;
          margin-bottom: 8px;
          color: #f8fafc;
        }
        .shs-welcome-desc {
          color: var(--shs-muted);
          font-size: 0.9rem;
          margin-bottom: 16px;
          line-height: 1.4;
        }
        .shs-score-hero {
          background: rgba(0, 0, 0, 0.25);
          border-radius: 12px;
          padding: 16px;
          margin-bottom: 16px;
        }
        .shs-score-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .shs-score-val {
          font-size: 1.8rem;
          font-weight: 800;
          color: #60a5fa;
        }
        .shs-provisional-tag {
          font-size: 0.75rem;
          background: rgba(245, 158, 11, 0.2);
          color: #fde68a;
          padding: 2px 6px;
          border-radius: 4px;
          margin-left: 6px;
          vertical-align: middle;
        }
        .shs-progress-bar {
          background: rgba(255, 255, 255, 0.1);
          height: 6px;
          border-radius: 9999px;
          margin: 10px 0 6px 0;
          overflow: hidden;
        }
        .shs-progress-fill {
          background: #3b82f6;
          height: 100%;
          border-radius: 9999px;
          transition: width 0.3s ease;
        }
        .shs-nav-tabs {
          display: flex;
          gap: 6px;
          margin-bottom: 14px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
          padding-bottom: 8px;
          overflow-x: auto;
        }
        .shs-tab-btn {
          background: transparent;
          color: var(--shs-muted);
          border: none;
          padding: 6px 12px;
          border-radius: 8px;
          font-weight: 600;
          font-size: 0.82rem;
          cursor: pointer;
          transition: all 0.2s;
          white-space: nowrap;
        }
        .shs-tab-btn.active {
          background: rgba(59, 130, 246, 0.2);
          color: #60a5fa;
        }
        .shs-btn {
          background: #2563eb;
          color: white;
          border: none;
          padding: 10px 16px;
          border-radius: 8px;
          font-size: 0.9rem;
          font-weight: 600;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
          width: 100%;
          transition: background 0.2s;
          box-sizing: border-box;
        }
        .shs-btn:hover {
          background: #1d4ed8;
        }
        .shs-btn-sec {
          background: rgba(255, 255, 255, 0.08);
          color: var(--shs-text);
        }
        .shs-btn-sec:hover {
          background: rgba(255, 255, 255, 0.15);
        }
        .shs-domain-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 8px;
          margin-top: 12px;
        }
        .shs-domain-card {
          background: rgba(0, 0, 0, 0.2);
          border-radius: 8px;
          padding: 10px;
          font-size: 0.8rem;
        }
        .shs-domain-title {
          font-weight: 600;
          color: var(--shs-muted);
          margin-bottom: 4px;
        }
        .shs-domain-score {
          font-size: 1rem;
          font-weight: 700;
          color: #93c5fd;
        }
      </style>

      <div class="shs-container">
        <div class="shs-header">
          <div class="shs-branding">
            <span>🏠 Smart Home Score</span>
          </div>
          <span class="shs-badge-beta">Bêta v0.7.0-beta.2</span>
        </div>

        ${!hasData ? `
          <div class="shs-welcome-box">
            <div class="shs-welcome-title">Bienvenue dans Smart Home Score</div>
            <div class="shs-welcome-desc">
              Évaluez l'autonomie, la sécurité et la résilience de votre installation Home Assistant en quelques minutes (100 % local).
            </div>
            <button class="shs-btn" id="btn-start-first-audit">
              🚀 Lancer mon premier audit
            </button>
          </div>
        ` : `
          <div class="shs-score-hero">
            <div class="shs-score-row">
              <div>
                <span style="font-weight:700; font-size:1rem;">Indice de maturité :</span>
                ${isProvisional ? '<span class="shs-provisional-tag">Provisoire</span>' : ''}
                <div style="color:var(--shs-muted); font-size:0.85rem; margin-top:2px;">
                  Niveau : <strong>${maturityText}</strong> • ${criticalCount > 0 ? `<span style="color:#f87171; font-weight:700;">⚠️ ${criticalCount} risque(s) critique(s)</span>` : '✅ 0 risque critique'}
                </div>
              </div>
              <div class="shs-score-val">${scoreVal.toFixed(1)} <span style="font-size:1rem; font-weight:600; color:var(--shs-muted);">/ 100</span></div>
            </div>

            <div class="shs-progress-bar">
              <div class="shs-progress-fill" style="width: ${Math.min(100, Math.max(0, completenessVal))}%;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--shs-muted);">
              <span>Éléments traités : ${completenessVal.toFixed(0)} %</span>
              <span>Potentiel : +${potentialGain.toFixed(1)} pts</span>
            </div>
          </div>

          <div class="shs-nav-tabs">
            <button class="shs-tab-btn ${this._activeTab === 'overview' ? 'active' : ''}" id="tab-overview">📊 Synthèse</button>
            <button class="shs-tab-btn ${this._activeTab === 'domains' ? 'active' : ''}" id="tab-domains">🏛️ Domaines</button>
            <button class="shs-tab-btn ${this._activeTab === 'actions' ? 'active' : ''}" id="tab-actions">⚡ Actions</button>
          </div>

          <div id="shs-tab-body">
            ${this._renderTabBody(isProvisional)}
          </div>

          <button class="shs-btn shs-btn-sec" id="btn-scan" style="margin-top: 14px;">
            🔄 Relancer l'analyse automatique
          </button>
        `}
      </div>
    `;

    this._bindEvents();
  }

  _renderTabBody(isProvisional) {
    if (this._activeTab === 'domains') {
      const getDom = (key) => this._hass?.states?.[`sensor.smart_home_score_${key}`]?.state ?? '—';
      return `
        <div class="shs-domain-grid">
          <div class="shs-domain-card"><div class="shs-domain-title">⚡ Électricité</div><div class="shs-domain-score">${getDom('elec_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🔒 Cybersécurité</div><div class="shs-domain-score">${getDom('cyber_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🛡️ Résilience</div><div class="shs-domain-score">${getDom('res_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">⚙️ Automatisations</div><div class="shs-domain-score">${getDom('auto_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">☀️ Énergie</div><div class="shs-domain-score">${getDom('ener_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🔌 Protocoles Locaux</div><div class="shs-domain-score">${getDom('inter_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">📱 Expérience / UX</div><div class="shs-domain-score">${getDom('ux_score')} / 100</div></div>
          <div class="shs-domain-card"><div class="shs-domain-title">🛠️ Maintenance</div><div class="shs-domain-score">${getDom('maint_score')} / 100</div></div>
        </div>
      `;
    }

    if (this._activeTab === 'actions') {
      return `
        <div style="font-size:0.85rem; color:var(--shs-muted); line-height:1.4;">
          <div style="background:rgba(0,0,0,0.2); border-radius:8px; padding:12px; margin-bottom:8px;">
            <strong style="color:#93c5fd;">🎯 Recommandations ciblées</strong>
            <p style="margin:4px 0 0 0;">Consultez les suggestions hiérarchisées pour augmenter la fiabilité et l'autonomie de votre logement.</p>
          </div>
        </div>
      `;
    }

    // Overview default
    return `
      <div style="font-size:0.85rem; color:var(--shs-muted); line-height:1.5;">
        ${isProvisional ? `
          <div style="background:rgba(245,158,11,0.1); border-left:3px solid #f59e0b; padding:8px 12px; border-radius:4px; margin-bottom:8px;">
            Score provisoire : répondez aux questions restantes pour finaliser votre bilan complet.
          </div>
        ` : `
          <div style="background:rgba(16,185,129,0.1); border-left:3px solid #10b981; padding:8px 12px; border-radius:4px; margin-bottom:8px; color:#a7f3d0;">
            Audit complet validé. Consultez les recommandations pour progresser vers le niveau supérieur.
          </div>
        `}
      </div>
    `;
  }

  _bindEvents() {
    this.shadowRoot.getElementById('btn-start-first-audit')?.addEventListener('click', () => {
      this._hass?.callService('smart_home_score', 'run_analysis', {});
    });

    this.shadowRoot.getElementById('btn-scan')?.addEventListener('click', () => {
      this._hass?.callService('smart_home_score', 'run_analysis', {});
    });

    this.shadowRoot.getElementById('tab-overview')?.addEventListener('click', () => {
      this._activeTab = 'overview';
      this._render();
    });

    this.shadowRoot.getElementById('tab-domains')?.addEventListener('click', () => {
      this._activeTab = 'domains';
      this._render();
    });

    this.shadowRoot.getElementById('tab-actions')?.addEventListener('click', () => {
      this._activeTab = 'actions';
      this._render();
    });
  }
}

customElements.define('smart-home-score-card', SmartHomeScoreCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'smart-home-score-card',
  name: 'Smart Home Score',
  preview: true,
  description: "Indice de maturité et plan d'amélioration de votre maison connectée",
});
