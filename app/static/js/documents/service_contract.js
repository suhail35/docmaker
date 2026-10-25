const service_contract_FIELDS = [
    { name: 'provider_name', label: 'Наименование исполнителя', type: 'text', required: true },
    { name: 'provider_inn', label: 'ИНН исполнителя', type: 'text', pattern: '^\\d{10,12}$' },
    { name: 'provider_address', label: 'Адрес исполнителя', type: 'text', required: true },
    { name: 'client_name', label: 'Наименование заказчика', type: 'text', required: true },
    { name: 'client_inn', label: 'ИНН заказчика', type: 'text', pattern: '^\\d{10,12}$' },
    { name: 'client_address', label: 'Адрес заказчика', type: 'text', required: true },
    { name: 'contract_number', label: 'Номер договора', type: 'text', required: true },
    { name: 'contract_date', label: 'Дата договора', type: 'date', required: true },
    { name: 'subject', label: 'Предмет договора (описание услуг)', type: 'textarea', required: true },
    { name: 'price', label: 'Стоимость (руб.)', type: 'number', required: true, step: '0.01' },
    { name: 'term_start', label: 'Начало срока оказания услуг', type: 'date', required: true },
    { name: 'term_end', label: 'Окончание срока', type: 'date', required: true },
    { name: 'payment_terms', label: 'Порядок оплаты', type: 'textarea', required: true },
];

if (typeof window !== 'undefined') {
    window.service_contract_FIELDS = service_contract_FIELDS;
    window.wizard_service_contract = new DocumentWizard('service_contract', { fields: service_contract_FIELDS });
}
