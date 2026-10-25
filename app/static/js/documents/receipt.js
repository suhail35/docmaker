const receipt_FIELDS = [
    { name: 'issuer_name', label: 'Наименование исполнителя', type: 'text', required: true },
    { name: 'issuer_inn', label: 'ИНН исполнителя', type: 'text', pattern: '^\\d{10,12}$' },
    { name: 'issuer_address', label: 'Адрес исполнителя', type: 'text', required: true },
    { name: 'payment_date', label: 'Дата оплаты', type: 'date', required: true },
    { name: 'amount', label: 'Сумма (руб.)', type: 'number', required: true, step: '0.01' },
    { name: 'service_description', label: 'Описание услуги', type: 'textarea', required: true },
    { name: 'payment_method', label: 'Способ оплаты', type: 'select', options: ['bank_transfer', 'cash'], required: true },
];

if (typeof window !== 'undefined') {
    window.receipt_FIELDS = receipt_FIELDS;
    window.wizard_receipt = new DocumentWizard('receipt', { fields: receipt_FIELDS });
}
