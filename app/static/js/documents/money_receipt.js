const money_receipt_FIELDS = [
    { name: 'recipient_name', label: 'ФИО получателя денег', type: 'text', required: true },
    { name: 'recipient_passport', label: 'Паспорт получателя', type: 'text', required: true },
    { name: 'recipient_address', label: 'Адрес получателя', type: 'text', required: true },
    { name: 'payer_name', label: 'ФИО плательщика', type: 'text', required: true },
    { name: 'payer_passport', label: 'Паспорт плательщика', type: 'text' },
    { name: 'amount', label: 'Сумма (руб.)', type: 'number', required: true, step: '0.01' },
    { name: 'amount_in_words', label: 'Сумма прописью', type: 'text', required: true },
    { name: 'purpose', label: 'Основание получения', type: 'textarea', required: true },
    { name: 'receipt_date', label: 'Дата получения', type: 'date', required: true },
];

if (typeof window !== 'undefined') {
    window.money_receipt_FIELDS = money_receipt_FIELDS;
    window.wizard_money_receipt = new DocumentWizard('money_receipt', { fields: money_receipt_FIELDS });
}
