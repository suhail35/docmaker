const acceptance_FIELDS = [
    { name: 'transferor_name', label: 'Наименование передающей стороны', type: 'text', required: true },
    { name: 'transferor_address', label: 'Адрес передающей стороны', type: 'text', required: true },
    { name: 'transferee_name', label: 'Наименование принимающей стороны', type: 'text', required: true },
    { name: 'transferee_address', label: 'Адрес принимающей стороны', type: 'text', required: true },
    { name: 'transfer_date', label: 'Дата передачи', type: 'date', required: true },
    { name: 'item_description', label: 'Описание передаваемого имущества/работ', type: 'textarea', required: true },
    { name: 'item_condition', label: 'Состояние имущества', type: 'text', required: true },
    { name: 'defects', label: 'Выявленные дефекты (если есть)', type: 'textarea' },
    { name: 'reference_contract', label: 'Ссылка на договор', type: 'text' },
];

if (typeof window !== 'undefined') {
    window.acceptance_FIELDS = acceptance_FIELDS;
    window.wizard_acceptance = new DocumentWizard('acceptance', { fields: acceptance_FIELDS });
}
