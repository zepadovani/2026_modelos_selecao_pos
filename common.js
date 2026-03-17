
document.addEventListener('DOMContentLoaded', () => {
    // Inject the fixed author footer
    const footerHtml = `
    <div class="fixed-author" style="position: fixed; bottom: 10px; right: 10px; font-size: 0.75rem; color: #888; text-align: right; z-index: 9999; background: rgba(255,255,255,0.85); padding: 4px 8px; border-radius: 4px; pointer-events: auto;">
        Estudo realizado por José Henrique Padovani, 2026. Todos os direitos reservados.
        <a href="${window.BASE_PATH || ''}#sobre" style="color: #888; text-decoration: underline;">Veja metodologia do estudo</a> e
        <a href="javascript:void(0)" onclick="showCite()" style="color: #888; text-decoration: underline;">como citar</a>.
    </div>
    `;
    document.body.insertAdjacentHTML('beforeend', footerHtml);

    // Inject the citation modal if data is provided
    if (window.CITE_TXT && window.CITE_BIB) {
        const modalHtml = `
        <!-- Citation Modal -->
        <div id="citationModal" class="modal-overlay" onclick="if(event.target===this)closeCite()">
          <div class="modal-content">
            <button class="modal-close" onclick="closeCite()">&times;</button>
            <h3>Como citar</h3>

            <p style="margin-top:15px"><strong>Formato Texto (ABNT):</strong></p>
            <div class="citation-box" id="cite-txt">${window.CITE_TXT}</div>
            <button class="cite-btn" onclick="copyCite('cite-txt')">Copiar</button>

            <p style="margin-top:20px"><strong>BibTeX:</strong></p>
            <div class="citation-box" id="cite-bib">${window.CITE_BIB}</div>
            <button class="cite-btn" onclick="copyCite('cite-bib')">Copiar</button>
          </div>
        </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHtml);
    }
});

function showCite() {
    const modal = document.getElementById('citationModal');
    if (modal) modal.classList.add('active');
}

function closeCite() {
    const modal = document.getElementById('citationModal');
    if (modal) modal.classList.remove('active');
}

function copyCite(id) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(() => {
        alert('Citação copiada!');
    });
}
