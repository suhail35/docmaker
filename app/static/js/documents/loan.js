const loan_FIELDS = [
    { name: 'lender_name', label: 'ФИО займодавца', type: 'text', required: true },
    { name: 'lender_passport', label: 'Паспорт займодавца', type: 'text', required: true },
    { name: 'lender_address', label: 'Адрес займодавца', type: 'text', required: true },
    { name: 'borrower_name', label: 'ФИО заёмщика', type: 'text', required: true },
    { name: 'borrower_passport', label: 'Паспорт заёмщика', type: 'text', required: true },
    { name: 'borrower_address', label: 'Адрес заёмщика', type: 'text', required: true },
    { name: 'loan_amount', label: 'Сумма займа (руб.)', type: 'number', required: true, step: '0.01' },
    { name: 'interest_rate', label: 'Проценты', type: 'text', required: true, hint: 'например: 10% годовых или без процентов' },
    { name: 'loan_date', label: 'Дата предоставления займа', type: 'date', required: true },
    { name: 'return_date', label: 'Срок возврата', type: 'date', required: true },
    { name: 'repayment_terms', label: 'Порядок возврата', type: 'textarea', required: true },
];

if (typeof window !== 'undefined') {
    window.loan_FIELDS = loan_FIELDS;
    window.wizard_loan = new DocumentWizard('loan', { fields: loan_FIELDS });
}
