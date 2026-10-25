const invoice_FIELDS = [
    { name: 'issuer_name', label: 'ФИО исполнителя (самозанятый)', type: 'text', required: true },
    { name: 'issuer_inn', label: 'ИНН исполнителя', type: 'text', required: true, pattern: '^\\d{12}$', hint: '12 цифр' },
    { name: 'issuer_phone', label: 'Телефон', type: 'tel', required: true, hint: '+7XXXXXXXXXX' },
    { name: 'issuer_address', label: 'Адрес исполнителя', type: 'text', required: true },
    { name: 'recipient_name', label: 'Наименование заказчика', type: 'text', required: true },
    { name: 'recipient_inn', label: 'ИНН заказчика', type: 'text', pattern: '^\\d{10,12}$', hint: '10 или 12 цифр' },
    { name: 'recipient_address', label: 'Адрес заказчика', type: 'text', required: true },
    { name: 'invoice_number', label: 'Номер счёта', type: 'text', required: true },
    { name: 'invoice_date', label: 'Дата счёта', type: 'date', required: true },
    { name: 'service_description', label: 'Описание услуги', type: 'textarea', required: true },
    { name: 'service_amount', label: 'Сумма (руб.)', type: 'number', required: true, step: '0.01', min: '0.01' },
    { name: 'payment_method', label: 'Способ оплаты', type: 'select', options: ['bank_transfer', 'cash'], required: true },
];

if (typeof window !== 'undefined') {
    window.invoice_FIELDS = invoice_FIELDS;
    window.wizard_invoice = new DocumentWizard('invoice', { fields: invoice_FIELDS });
}
