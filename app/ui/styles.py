"""Theme and CSS for the AI Product Studio interface."""

import gradio as gr

CSS = """
:root {
    --studio-bg: #f5f7fb;
    --studio-surface: #ffffff;
    --studio-border: #e4e8f0;
    --studio-text: #182230;
    --studio-muted: #667085;
    --studio-accent: #3156d3;
    --studio-accent-dark: #2645ae;
}

.gradio-container {
    background: var(--studio-bg) !important;
    overflow-x: hidden;
}

.studio-shell {
    max-width: 1440px;
    margin: 0 auto;
    padding: 14px clamp(18px, 4vw, 56px) 28px;
    color: var(--studio-text);
}

.studio-header {
    background: var(--studio-surface);
    border: 1px solid #dfe5f0;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(24, 34, 48, 0.05);
    margin: 0 -12px 16px;
    padding: 18px 24px;
    text-align: center;
}

.studio-eyebrow {
    align-items: center;
    background: #eef2ff;
    border: 1px solid #dce4ff;
    border-radius: 999px;
    color: var(--studio-accent-dark);
    display: inline-flex;
    font-size: 0.68rem;
    font-weight: 700;
    gap: 6px;
    letter-spacing: 0.12em;
    padding: 4px 9px;
    text-transform: uppercase;
}

.studio-mark {
    align-items: center;
    background: var(--studio-accent);
    border-radius: 5px;
    color: #ffffff;
    display: inline-flex;
    font-size: 0.66rem;
    height: 16px;
    justify-content: center;
    letter-spacing: 0;
    width: 16px;
}

.studio-header h1 {
    color: var(--studio-text);
    font-size: clamp(1.8rem, 3vw, 2.45rem);
    letter-spacing: -0.04em;
    margin: 9px 0 5px;
}

.studio-header p {
    color: var(--studio-muted);
    font-size: 0.92rem;
    margin: 0;
}

.studio-grid {
    align-items: stretch;
    gap: 20px;
}

.studio-panel {
    background: var(--studio-surface);
    border: 1px solid var(--studio-border);
    border-radius: 16px;
    box-shadow:
        0 14px 32px rgba(24, 34, 48, 0.055),
        0 2px 6px rgba(24, 34, 48, 0.025);
    padding: clamp(18px, 2.4vw, 30px);
}

.studio-panel h2,
.studio-panel h3 {
    color: var(--studio-text);
    letter-spacing: -0.02em;
    margin: 0 0 4px;
}

.studio-panel h2 {
    font-size: 1.15rem;
}

.studio-panel h3 {
    font-size: 1.05rem;
}

.panel-intro {
    color: var(--studio-muted);
    font-size: 0.86rem;
    margin: 0 0 8px;
}

.panel-intro p,
.section-heading p {
    margin: 0 !important;
}

.section-heading {
    border: 0 !important;
    box-shadow: none !important;
    margin: 10px 0 8px;
    padding: 0 0 9px;
    position: relative;
}

.section-heading::after {
    background: var(--studio-border);
    bottom: 0;
    content: "";
    height: 1px;
    left: 0;
    position: absolute;
    right: 0;
}

.section-heading[data-testid="markdown"] {
    margin: 0;
    padding: 0;
}

.section-heading[data-testid="markdown"]::after {
    display: none;
}

.section-heading h4 {
    font-size: 0.82rem;
    letter-spacing: 0.08em;
    margin: 0 !important;
    text-transform: uppercase;
}

.section-heading p {
    color: var(--studio-muted);
    font-size: 0.78rem;
    margin-top: 2px !important;
}

.studio-panel .form-row {
    gap: 12px;
}

.studio-panel label span {
    color: var(--studio-text);
    font-size: 0.82rem;
    font-weight: 600;
}

.studio-panel input,
.studio-panel textarea,
.studio-panel [role="combobox"] {
    background: #fafbfe !important;
    border-color: #dfe5ef !important;
    border-radius: 10px !important;
    color: var(--studio-text) !important;
    transition: border-color 160ms ease, box-shadow 160ms ease, background-color 160ms ease;
}

.studio-panel input:focus,
.studio-panel textarea:focus,
.studio-panel [role="combobox"]:focus-within {
    background: #ffffff !important;
    border-color: var(--studio-accent) !important;
    box-shadow: 0 0 0 3px rgba(49, 86, 211, 0.12) !important;
}

.studio-panel .wrap {
    gap: 6px;
}

.studio-panel .gr-radio,
.centered-options {
    gap: 8px;
}

.studio-panel .gr-radio label,
.centered-options label {
    background: #fafbfe;
    border: 1px solid #dfe5ef;
    border-radius: 9px;
    padding: 9px 10px;
    transition: background-color 160ms ease, border-color 160ms ease, transform 160ms ease;
}

.studio-panel .gr-radio label:has(input:checked),
.centered-options label:has(input:checked) {
    background: #eef2ff;
    border-color: #9eaff0;
    color: var(--studio-accent-dark);
}

.centered-options .wrap,
.centered-options > div {
    justify-content: center !important;
}

.centered-options .wrap > label {
    flex: 1 1 0;
    justify-content: center;
    min-width: 0;
    text-align: center;
}

.studio-panel .gr-radio label:hover,
.centered-options label:hover {
    border-color: #b7c5ef;
    transform: translateY(-1px);
}

.generate-button {
    margin-top: 22px;
}

.generate-button button {
    border-radius: 9px !important;
    font-weight: 650;
    min-height: 46px;
    transition: background-color 160ms ease, transform 160ms ease;
}

.generate-button button:hover {
    background: var(--studio-accent-dark) !important;
    transform: translateY(-1px);
}

.generate-button button:focus-visible,
.regenerate-button button:focus-visible,
.download-output button:focus-visible,
.studio-panel input:focus-visible,
.studio-panel textarea:focus-visible {
    outline: 3px solid rgba(49, 86, 211, 0.22);
    outline-offset: 2px;
}

.result-panel {
    display: flex;
    flex-direction: column;
    min-height: 520px;
}

.result-panel .result-heading {
    align-items: center;
    display: flex;
    justify-content: space-between;
}

.result-panel .result-heading h3 {
    margin: 0;
}

.result-badge {
    background: #eef2ff;
    border-radius: 999px;
    color: var(--studio-accent-dark);
    font-size: 0.72rem;
    font-weight: 700;
    padding: 5px 9px;
}

.empty-state {
    align-items: center;
    background: #fbfcff;
    border: 1px dashed #c7d1e4;
    border-radius: 12px;
    display: flex;
    flex: 1;
    justify-content: center;
    margin: 8px 0 16px;
    min-height: 300px;
    text-align: center;
}

.empty-state-icon {
    align-items: center;
    background: #eef2ff;
    border-radius: 12px;
    color: var(--studio-accent);
    display: flex;
    font-size: 1.4rem;
    height: 46px;
    justify-content: center;
    margin: 0 auto 12px;
    width: 46px;
}

.empty-state h3 {
    font-size: 1rem;
    margin: 0 0 5px;
}

.empty-state p {
    color: var(--studio-muted);
    font-size: 0.83rem;
    margin: 0;
    max-width: 280px;
}

.result-image {
    margin: 8px 0 16px;
}

.result-image .image-container {
    background: #fbfcfe;
    border: 1px solid var(--studio-border);
    border-radius: 12px;
    min-height: 300px;
}

.result-image img {
    max-height: min(58vh, 620px);
    object-fit: contain;
}

.download-output {
    margin: 0 0 10px;
}

.download-output button {
    background: var(--studio-accent) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-weight: 650;
    min-height: 42px;
}

.download-output button:hover {
    background: var(--studio-accent-dark) !important;
}

.regenerate-button {
    margin-top: 0;
}

.regenerate-button button {
    border-color: #cbd5ea !important;
    border-radius: 8px !important;
    color: var(--studio-accent-dark) !important;
    font-weight: 600;
    min-height: 40px;
}

.status-output {
    background: #f7f9fd;
    border: 1px solid var(--studio-border);
    border-radius: 8px;
    font-size: 0.82rem;
    margin-top: 12px;
    padding: 10px 12px;
}

.status-output h3 {
    color: var(--studio-text);
    font-size: 0.9rem;
    margin: 0 0 4px;
}

.status-output p {
    color: var(--studio-muted);
    margin: 0;
}

@media (max-width: 900px) {
    .studio-shell {
        padding: 22px 18px 28px;
    }

    .studio-header {
        margin-left: -12px;
        margin-right: -12px;
    }

    .studio-grid {
        flex-direction: column;
    }

    .result-panel {
        min-height: 420px;
    }
}

@media (max-width: 520px) {
    .studio-shell {
        padding: 18px 12px 24px;
    }

    .studio-panel {
        border-radius: 12px;
        padding: 16px;
    }

    .studio-header {
        margin-bottom: 18px;
        margin-left: -12px;
        margin-right: -12px;
    }

    .studio-panel .form-row {
        flex-direction: column;
    }

    .studio-header h1 {
        font-size: 1.75rem;
    }

    .result-panel {
        min-height: 360px;
    }

    .result-panel .result-heading {
        gap: 10px;
    }

    .result-badge {
        font-size: 0.65rem;
    }
}

@media (prefers-reduced-motion: reduce) {
    .generate-button button,
    .studio-panel input,
    .studio-panel textarea,
    .studio-panel [role="combobox"],
    .studio-panel .gr-radio label,
    .centered-options label {
        transition: none;
    }
}
"""

THEME = gr.themes.Base(
    primary_hue="indigo",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("Inter"),
)

EMPTY_STATE = """
<div class="empty-state">
    <div>
        <div class="empty-state-icon">✦</div>
        <h3>Your creative will appear here</h3>
        <p>Configure your product and generate your first advertising visual.</p>
    </div>
</div>
"""
