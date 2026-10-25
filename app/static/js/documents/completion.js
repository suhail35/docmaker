const completion_FIELDS = [
    { name: 'performer_name', label: 'Наименование исполнителя', type: 'text', required: true },
    { name: 'performer_inn', label: 'ИНН исполнителя', type: 'text', required: true, pattern: '^\\d{10,12}$' },
    { name: 'performer_address', label: 'Адрес исполнителя', type: 'text', required: true },
    { name: 'customer_name', label: 'Наименование заказчика', type: 'text', required: true },
    { name: 'customer_inn', label: 'ИНН заказчика', type: 'text', pattern: '^\\d{10,12}$' },
    { name: 'customer_address', label: 'Адрес заказчика', type: 'text', required: true },
    { name: 'contract_number', label: 'Номер договора', type: 'text', required: true },
    { name: 'contract_date', label: 'Дата договора', type: 'date', required: true },
    { name: 'work_description', label: 'Описание выполненных работ', type: 'textarea', required: true },
    { name: 'work_amount', label: 'Стоимость (руб.)', type: 'number', required: true, step: '0.01' },
    { name: 'work_date', label: 'Дата акта', type: 'date', required: true },
];

if (typeof window !== 'undefined') {
    window.completion_FIELDS = completion_FIELDS;
    window.wizard_completion = new DocumentWizard('completion', { fields: completion_FIELDS });
}
