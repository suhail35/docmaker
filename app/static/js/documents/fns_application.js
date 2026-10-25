const fns_application_FIELDS = [
    { name: 'applicant_name', label: 'ФИО заявителя', type: 'text', required: true },
    { name: 'applicant_inn', label: 'ИНН', type: 'text', required: true, pattern: '^\\d{10,12}$' },
    { name: 'applicant_address', label: 'Адрес', type: 'text', required: true },
    { name: 'applicant_phone', label: 'Телефон', type: 'tel', required: true },
    { name: 'fns_office', label: 'Наименование инспекции ФНС', type: 'text', required: true },
    { name: 'application_type', label: 'Тип заявления', type: 'select', options: ['пояснение', 'заявление', 'заявка'], required: true },
    { name: 'subject', label: 'Тема', type: 'text', required: true },
    { name: 'details', label: 'Подробности/пояснение', type: 'textarea', required: true },
    { name: 'application_date', label: 'Дата заявления', type: 'date', required: true },
];

if (typeof window !== 'undefined') {
    window.fns_application_FIELDS = fns_application_FIELDS;
    window.wizard_fns_application = new DocumentWizard('fns_application', { fields: fns_application_FIELDS });
}
