"""Tests for validation functions."""

from app.documents.validation import validate_inn, validate_bik, validate_date, validate_phone, validate_amount


class TestValidateINN:
    def test_valid_10_digit_inn(self):
        # Пример валидного ИНН (10 цифр)
        assert validate_inn("7707083893") is True  # Лысенко

    def test_valid_12_digit_inn(self):
        # Пример валидного ИНН (12 цифр)
        assert validate_inn("77070838931" + "0") is False  # Проверим
        # Простой тест: 12 цифр
        assert validate_inn("770708389310") is True

    def test_invalid_inn_short(self):
        assert validate_inn("12345") is False

    def test_invalid_inn_letters(self):
        assert validate_inn("ABCDEF") is False

    def test_invalid_inn_wrong_length(self):
        assert validate_inn("123456789") is False
        assert validate_inn("12345678901") is False

    def test_empty_inn(self):
        assert validate_inn("") is False


class TestValidateBIK:
    def test_valid_bik(self):
        assert validate_bik("044525225") is True

    def test_invalid_bik_short(self):
        assert validate_bik("12345678") is False

    def test_invalid_bik_long(self):
        assert validate_bik("1234567890") is False

    def test_invalid_bik_letters(self):
        assert validate_bik("ABCDEFGHI") is False


class TestValidateDate:
    def test_valid_date(self):
        assert validate_date("2024-01-15") is True

    def test_invalid_date(self):
        assert validate_date("2024-13-01") is False
        assert validate_date("not-a-date") is False
        assert validate_date("") is False


class TestValidatePhone:
    def test_valid_phone_international(self):
        assert validate_phone("+79161234567") is True

    def test_valid_phone_no_plus(self):
        assert validate_phone("79161234567") is True

    def test_valid_phone_with_eight(self):
        assert validate_phone("89161234567") is True

    def test_invalid_phone_short(self):
        assert validate_phone("123") is False


class TestValidateAmount:
    def test_valid_amount(self):
        assert validate_amount("1000.00") is True
        assert validate_amount("1000") is True

    def test_invalid_amount_zero(self):
        assert validate_amount("0") is False

    def test_invalid_amount_negative(self):
        assert validate_amount("-100") is False

    def test_invalid_amount_letters(self):
        assert validate_amount("abc") is False
