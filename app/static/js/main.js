document.addEventListener('DOMContentLoaded', function() {
    const app = document.getElementById('app');
    if (!app) return;

    const documents = [
        { id: 'invoice', name: 'Счёт (НПД)', category: 'self-employed' },
        { id: 'completion', name: 'Акт выполненных работ', category: 'self-employed' },
        { id: 'service_contract', name: 'Договор возмездного оказания услуг', category: 'self-employed' },
        { id: 'receipt', name: 'Чек-подтверждение', category: 'self-employed' },
        { id: 'gift', name: 'Договор дарения движимого имущества', category: 'individual' },
        { id: 'money_receipt', name: 'Расписка в получении денег', category: 'individual' },
        { id: 'loan', name: 'Договор займа между физлицами', category: 'individual' },
        { id: 'acceptance', name: 'Акт приёма-передачи', category: 'individual' },
        { id: 'pd_consent', name: 'Согласие на обработку ПДн', category: 'individual' },
        { id: 'fns_application', name: 'Заявление-пояснение в ФНС', category: 'individual' },
    ];

    let html = '<h2 class="mb-4">Выберите документ</h2>';

    // Self-employed
    html += '<h4 class="mb-3">Для самозанятых (НПД)</h4>';
    html += '<div class="row mb-4">';
    documents.filter(d => d.category === 'self-employed').forEach(doc => {
        html += `<div class="col-md-4 mb-3">
            <div class="card document-card" onclick="openDocument('${doc.id}')">
                <div class="card-body">
                    <h5 class="card-title">${doc.name}</h5>
                </div>
            </div>
        </div>`;
    });
    html += '</div>';

    // Individuals
    html += '<h4 class="mb-3">Для физических лиц</h4>';
    html += '<div class="row mb-4">';
    documents.filter(d => d.category === 'individual').forEach(doc => {
        html += `<div class="col-md-4 mb-3">
            <div class="card document-card" onclick="openDocument('${doc.id}')">
                <div class="card-body">
                    <h5 class="card-title">${doc.name}</h5>
                </div>
            </div>
        </div>`;
    });
    html += '</div>';

    // Clear drafts button
    html += '<div class="text-center mt-4">';
    html += '<button class="btn btn-outline-danger" onclick="clearAllDrafts()">Очистить все черновики</button>';
    html += '</div>';

    app.innerHTML = html;
});

function openDocument(docId) {
    window.location.href = `/document/${docId}`;
}
