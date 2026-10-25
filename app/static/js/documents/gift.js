const gift_FIELDS = [
    { name: 'donor_name', label: 'ФИО дарителя', type: 'text', required: true },
    { name: 'donor_passport', label: 'Паспорт дарителя', type: 'text', required: true },
    { name: 'donor_address', label: 'Адрес дарителя', type: 'text', required: true },
    { name: 'donee_name', label: 'ФИО одаряемого', type: 'text', required: true },
    { name: 'donee_passport', label: 'Паспорт одаряемого', type: 'text', required: true },
    { name: 'donee_address', label: 'Адрес одаряемого', type: 'text', required: true },
    { name: 'donee_relationship', label: 'Степень родства', type: 'text', required: true, hint: 'например: брат, сын, супруг' },
    { name: 'property_description', label: 'Описание имущества', type: 'textarea', required: true },
    { name: 'property_value', label: 'Оценочная стоимость (руб.)', type: 'number', required: true, step: '0.01' },
    { name: 'gift_date', label: 'Дата дарения', type: 'date', required: true },
];

if (typeof window !== 'undefined') {
    window.gift_FIELDS = gift_FIELDS;
    window.wizard_gift = new DocumentWizard('gift', { fields: gift_FIELDS });
}
