/**
 * Document wizard: form → preview → PDF download.
 */
class DocumentWizard {
    constructor(docType, config) {
        this.docType = docType;
        this.config = config;
        this.formData = {};
        this.init();
    }

    init() {
        this.renderFields();
        this.loadDraft();
        this.bindEvents();
        this.bindAutoFill();
    }

    renderFields() {
        const fields = this.config.fields || [];
        const container = document.getElementById('form-fields');
        if (!container || fields.length === 0) return;

        let html = '';
        fields.forEach(field => {
            html += `<div class="mb-3">`;
            html += `<label for="field-${field.name}" class="form-label">${field.label}</label>`;

            if (field.type === 'textarea') {
                html += `<textarea class="form-control" id="field-${field.name}" name="${field.name}" rows="3" ${field.required ? 'required' : ''}></textarea>`;
            } else if (field.type === 'select') {
                html += `<select class="form-select" id="field-${field.name}" name="${field.name}" ${field.required ? 'required' : ''}>`;
                if (field.options) {
                    field.options.forEach(opt => {
                        const val = typeof opt === 'object' ? opt.value : opt;
                        const label = typeof opt === 'object' ? opt.label : opt;
                        html += `<option value="${val}">${label}</option>`;
                    });
                }
                html += `</select>`;
            } else {
                html += `<input type="${field.type}" class="form-control" id="field-${field.name}" name="${field.name}" `;
                if (field.pattern) html += `pattern="${field.pattern}" `;
                if (field.step) html += `step="${field.step}" `;
                if (field.min) html += `min="${field.min}" `;
                if (field.max) html += `max="${field.max}" `;
                html += `${field.required ? 'required' : ''}>`;
            }

            if (field.hint) {
                html += `<div class="form-text">${field.hint}</div>`;
            }

            html += `<div class="form-source manual" id="source-${field.name}">введено вручную</div>`;
            html += `</div>`;
        });

        container.innerHTML = html;
    }

    loadDraft() {
        const draft = localStorage.getItem(`docmaker_draft_${this.docType}`);
        if (draft) {
            try {
                this.formData = JSON.parse(draft);
                Object.keys(this.formData).forEach(key => {
                    const input = document.querySelector(`[name="${key}"]`);
                    if (input) {
                        input.value = this.formData[key];
                        if (this.formData[key] && this.formData[key + '_source'] === 'auto') {
                            const sourceEl = document.getElementById(`source-${key}`);
                            if (sourceEl) {
                                sourceEl.textContent = 'заполнено из ЕГРЮЛ';
                                sourceEl.classList.remove('manual');
                            }
                        }
                    }
                });
            } catch (e) {
                this.formData = {};
            }
        }
    }

    saveDraft() {
        localStorage.setItem(
            `docmaker_draft_${this.docType}`,
            JSON.stringify(this.formData)
        );
    }

    bindEvents() {
        const form = document.getElementById(`form-${this.docType}`);
        if (!form) return;

        form.addEventListener('input', (e) => {
            const input = e.target;
            if (input.name) {
                this.formData[input.name] = input.value;
                // Reset source indicator on manual edit
                const sourceEl = document.getElementById(`source-${input.name}`);
                if (sourceEl) {
                    sourceEl.textContent = 'введено вручную';
                    sourceEl.classList.add('manual');
                }
                this.saveDraft();
            }
        });

        // Auto-fill INN on blur
        const innInputs = form.querySelectorAll('[name$="_inn"]');
        innInputs.forEach(innInput => {
            innInput.addEventListener('blur', () => {
                const inn = innInput.value.replace(/\s/g, '');
                if (inn.length >= 10 && inn.length <= 12 && /^\d+$/.test(inn)) {
                    this.autoFillByInn(inn, innInput);
                }
            });
        });
    }

    bindAutoFill() {
        // Auto-fill by INN if present (from draft)
        const innInput = document.querySelector('[name$="_inn"]');
        if (innInput && innInput.value && innInput.value.length >= 10) {
            this.autoFillByInn(innInput.value, innInput);
        }
    }

    async autoFillByInn(inn, innInput) {
        // Show loading indicator
        const sourceEl = document.getElementById(`source-${innInput.name}`);
        if (sourceEl) {
            sourceEl.textContent = 'загрузка...';
            sourceEl.classList.remove('manual');
            sourceEl.style.color = '#0d6efd';
        }

        try {
            const resp = await fetch(`/api/auto-fill/inn/${inn}`);
            if (resp.ok) {
                const data = await resp.json();
                if (data.name) {
                    // Find the name input field
                    const nameInput = document.querySelector('[name$="_name"]');
                    if (nameInput) {
                        nameInput.value = data.name;
                        this.formData[nameInput.name] = data.name;
                        const nameSourceEl = document.getElementById(`source-${nameInput.name}`);
                        if (nameSourceEl) {
                            nameSourceEl.textContent = 'заполнено из ЕГРЮЛ';
                            nameSourceEl.classList.remove('manual');
                            nameSourceEl.style.color = '#198754';
                        }
                        this.saveDraft();
                    }
                    if (data.address) {
                        const addressInput = document.querySelector('[name$="_address"]');
                        if (addressInput) {
                            addressInput.value = data.address;
                            this.formData[addressInput.name] = data.address;
                            const addrSourceEl = document.getElementById(`source-${addressInput.name}`);
                            if (addrSourceEl) {
                                addrSourceEl.textContent = 'заполнено из ЕГРЮЛ';
                                addrSourceEl.classList.remove('manual');
                                addrSourceEl.style.color = '#198754';
                            }
                        }
                    }
                    if (sourceEl) {
                        sourceEl.textContent = 'данные подтянуты';
                        sourceEl.style.color = '#198754';
                    }
                } else {
                    if (sourceEl) {
                        sourceEl.textContent = 'данные не найдены';
                        sourceEl.classList.add('manual');
                        sourceEl.style.color = '#6c757d';
                    }
                }
            } else {
                if (sourceEl) {
                    sourceEl.textContent = 'ошибка запроса';
                    sourceEl.classList.add('manual');
                    sourceEl.style.color = '#dc3545';
                }
            }
        } catch (e) {
            if (sourceEl) {
                sourceEl.textContent = 'ошибка сети';
                sourceEl.classList.add('manual');
                sourceEl.style.color = '#dc3545';
            }
        }
    }

    collectFormData() {
        const form = document.getElementById(`form-${this.docType}`);
        if (!form) return {};
        const formData = {};
        form.querySelectorAll('[name]').forEach(input => {
            formData[input.name] = input.value;
        });
        return formData;
    }

    async generatePdf() {
        const formData = this.collectFormData();
        const response = await fetch(`/api/generate-pdf/${this.docType}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(formData),
        });
        const result = await response.json();
        if (result.pdf) {
            return result;
        }
        return null;
    }

    async downloadPdf(pdfHex, filename) {
        const bytes = new Uint8Array(
            pdfHex.match(/.{2}/g).map(b => parseInt(b, 16))
        );
        const blob = new Blob([bytes], { type: 'application/pdf' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

function showStep(stepId) {
    document.querySelectorAll('.wizard-step').forEach(s => s.style.display = 'none');
    document.getElementById(stepId).style.display = 'block';
}

function previewDocument(docType) {
    const wizard = window[`wizard_${docType}`];
    if (!wizard) return;

    wizard.generatePdf().then(result => {
        if (result && result.pdf) {
            const bytes = new Uint8Array(
                result.pdf.match(/.{2}/g).map(b => parseInt(b, 16))
            );
            const blob = new Blob([bytes], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            document.getElementById('pdf-preview').src = url;
            showStep('step-preview');
        }
    });
}

function downloadPdf(docType) {
    const wizard = window[`wizard_${docType}`];
    if (!wizard) return;

    wizard.generatePdf().then(result => {
        if (result && result.pdf) {
            wizard.downloadPdf(result.pdf, result.filename);
        }
    });
}

function clearForm(docType) {
    if (confirm('Очистить все поля формы?')) {
        const form = document.getElementById(`form-${docType}`);
        if (form) form.reset();
        localStorage.removeItem(`docmaker_draft_${docType}`);
        window[`wizard_${docType}`] = new DocumentWizard(docType, {
            fields: window[`${docType}_FIELDS`] || []
        });
    }
}

function clearAllDrafts() {
    if (confirm('Очистить все черновики? Это действие нельзя отменить.')) {
        Object.keys(localStorage).forEach(key => {
            if (key.startsWith('docmaker_draft_')) {
                localStorage.removeItem(key);
            }
        });
        alert('Все черновики удалены.');
    }
}
