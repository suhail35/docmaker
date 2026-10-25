const pd_consent_FIELDS = [
    { name: 'subject_full_name', label: 'ФИО субъекта', type: 'text', required: true },
    { name: 'subject_passport', label: 'Паспорт', type: 'text', required: true },
    { name: 'subject_inn', label: 'ИНН', type: 'text', pattern: '^\\d{10,12}$' },
    { name: 'subject_address', label: 'Адрес', type: 'text', required: true },
    { name: 'subject_phone', label: 'Телефон', type: 'tel', required: true },
    { name: 'subject_email', label: 'Email', type: 'email' },
    { name: 'operator_name', label: 'Наименование оператора', type: 'text', required: true },
    { name: 'operator_address', label: 'Адрес оператора', type: 'text', required: true },
    { name: 'purposes', label: 'Цели обработки', type: 'textarea', required: true },
    { name: 'data_types', label: 'Перечень персональных данных', type: 'textarea', required: true },
    { name: 'consent_period', label: 'Срок действия согласия', type: 'text', required: true, hint: 'например: 3 года' },
    { name: 'consent_date', label: 'Дата согласия', type: 'date', required: true },
];

if (typeof window !== 'undefined') {
    window.pd_consent_FIELDS = pd_consent_FIELDS;
    window.wizard_pd_consent = new DocumentWizard('pd_consent', { fields: pd_consent_FIELDS });
}
