document.addEventListener('DOMContentLoaded', () => {
    // Read authentication status
    const authMeta = document.querySelector('meta[name="is-authenticated"]');
    window.IS_AUTHENTICATED = authMeta ? authMeta.content === 'true' : false;

    // Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const toolPanels = document.querySelectorAll('.tool-panel');
    const resultBox = document.getElementById('resultBox');
    const loader = document.getElementById('loader');

    function resetUI() {
        resultBox.style.display = 'none';
        loader.style.display = 'none';
        document.getElementById('resultContent').innerHTML = '';
    }

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all
            tabBtns.forEach(b => b.classList.remove('active'));
            toolPanels.forEach(p => p.classList.remove('active'));
            
            // Add active class to clicked
            btn.classList.add('active');
            const target = btn.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
            
            resetUI();
        });
    });

    // Image Upload Logic
    const dropZone = document.getElementById('drop-zone');
    const imageInput = document.getElementById('imageInput');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');
    const imagePreview = document.getElementById('imagePreview');
    const fileNameDisplay = document.getElementById('fileName');
    const analyzeImageBtn = document.getElementById('analyzeImageBtn');

    dropZone.addEventListener('click', () => imageInput.click());

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.background = '#e5e7eb';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.background = '#f9fafb';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.style.background = '#f9fafb';
        if (e.dataTransfer.files.length) {
            imageInput.files = e.dataTransfer.files;
            showImagePreview();
        }
    });

    imageInput.addEventListener('change', showImagePreview);

    function showImagePreview() {
        if (imageInput.files && imageInput.files[0]) {
            const file = imageInput.files[0];
            fileNameDisplay.textContent = file.name;
            
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                dropZone.style.display = 'none';
                imagePreviewContainer.style.display = 'block';
                analyzeImageBtn.style.display = 'block';
            };
            reader.readAsDataURL(file);
            resetUI();
        }
    }

    // Helper: Make API calls dynamically
    async function makeApiCall(endpoint, method, payload, isFormData = false) {
        if (!window.IS_AUTHENTICATED) {
            alert('Login is required to perform this action. Please login or register first.');
            return null;
        }

        loader.style.display = 'block';
        resultBox.style.display = 'none';
        
        try {
            const options = { method };
            if (isFormData) {
                options.body = payload;
                // Don't set content-type for formData, browser sets it with boundary
            } else {
                options.headers = { 'Content-Type': 'application/json' };
                options.body = JSON.stringify(payload);
            }

            const response = await fetch(endpoint, options);
            const data = await response.json();
            
            loader.style.display = 'none';
            resultBox.style.display = 'block';
            
            return data;
        } catch (error) {
            loader.style.display = 'none';
            resultBox.style.display = 'block';
            document.getElementById('resultContent').innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            return null;
        }
    }

    function renderConfidence(confidence) {
        if (confidence === undefined || confidence === null) return '';
        let colorClass = confidence > 80 ? 'confidence-high' : confidence > 50 ? 'confidence-med' : 'confidence-low';
        return `<div><span style="font-weight:bold;">Confidence Score:</span> <span class="${colorClass}">${confidence}%</span></div>`;
    }

    function renderOutput(htmlContent) {
        document.getElementById('resultContent').innerHTML = htmlContent;
    }

    // Event Listeners for API Calls
    analyzeImageBtn.addEventListener('click', async () => {
        if(!imageInput.files[0]) return;
        
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);
        
        const result = await makeApiCall('/image/detect', 'POST', formData, true);
        
        if (result && result.success) {
            let classColor = result.data.prediction === 'AI-Generated' ? 'color:#ef4444;' : 'color:#10b981;';
            let content = `
                <div class="result-item">
                    <strong>Prediction:</strong> <span style="${classColor} font-weight:bold;">${result.data.prediction}</span>
                </div>
                ${renderConfidence(result.data.confidence)}
            `;
            renderOutput(content);
        } else if (result) {
            renderOutput(`<p style="color:red;">Error: ${result.message}</p>`);
        }
    });

    document.getElementById('analyzeTextBtn').addEventListener('click', async () => {
        const text = document.getElementById('textDetectInput').value;
        const result = await makeApiCall('/text/detect', 'POST', { text });
        if (result && result.success) {
            let classColor = result.data.prediction === 'AI-Generated' ? 'color:#ef4444;' : 'color:#10b981;';
            renderOutput(`
                <div class="result-item"><strong>Prediction:</strong> <span style="${classColor} font-weight:bold;">${result.data.prediction}</span></div>
                ${renderConfidence(result.data.confidence)}
            `);
        }
    });

    document.getElementById('summarizeBtn').addEventListener('click', async () => {
        const text = document.getElementById('summarizeInput').value;
        const result = await makeApiCall('/summarize/', 'POST', { text });
        if (result && result.success) {
            renderOutput(`<div class="result-item"><strong>Summary:</strong><br>${result.data.summary}</div>`);
        }
    });

    document.getElementById('paraphraseBtn').addEventListener('click', async () => {
        const text = document.getElementById('paraphraseInput').value;
        const result = await makeApiCall('/paraphrase/', 'POST', { text });
        if (result && result.success) {
            renderOutput(`<div class="result-item"><strong>Paraphrased:</strong><br>${result.data.paraphrased}</div>`);
        }
    });

    document.getElementById('grammarBtn').addEventListener('click', async () => {
        const text = document.getElementById('grammarInput').value;
        const result = await makeApiCall('/grammar/', 'POST', { text });
        if (result && result.success) {
            let html = `<div class="result-item"><strong>Corrected Text:</strong><br>${result.data.corrected}</div>`;
            if (result.data.errors && result.data.errors.length > 0) {
                html += `<div style="margin-top:10px;"><strong>Errors Found:</strong><ul>`;
                result.data.errors.forEach(err => {
                    html += `<li><span style="color:red;">"${err.error}"</span> ➔ <span style="color:green;">"${err.suggestion}"</span> <em>(${err.message})</em></li>`;
                });
                html += `</ul></div>`;
            } else {
                html += `<div style="margin-top:10px; color:green;"><i class="fa-solid fa-check"></i> No grammatical errors found!</div>`;
            }
            renderOutput(html);
        }
    });
});
