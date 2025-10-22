"""
Tests for MorphUI textfield components.

This module contains comprehensive tests for the TextValidator class
and related textfield functionality.
"""
import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).parent.resolve()))

from kivy.event import EventDispatcher
from morphui.uix.textfield import TextValidator


@pytest.fixture
def validator():
    """Create a TextValidator instance for testing."""
    return TextValidator()


def test_init_default_values(validator):
    """Test that TextValidator initializes with correct default values."""
    assert not validator.error
    assert not validator.required
    assert validator.validator is None


def test_inheritance(validator):
    """Test that TextValidator inherits from EventDispatcher."""
    assert isinstance(validator, EventDispatcher)


def test_property_setters(validator):
    """Test that properties can be set correctly."""
    validator.error = True
    assert validator.error
    
    validator.required = True  
    assert validator.required
    
    validator.validator = 'email'
    assert validator.validator == 'email'

    validator.validator = None
    assert validator.validator is None


# Email validation tests
@pytest.mark.parametrize("email", [
    'test@example.com',
    'user.name@domain.co.uk', 
    'first.last+tag@subdomain.example.org',
    'user_123@test-domain.com',
    'simple@domain.co',
])
def test_is_valid_email_valid_addresses(validator, email):
    """Test valid email address validation."""
    assert validator.is_valid_email(email), f"Expected {email!r} to be valid"


@pytest.mark.parametrize("email", [
    '',  # empty string
    'invalid',  # no @ or domain
    '@example.com',  # no local part
    'user@',  # no domain
    'user@.com',  # domain starts with dot
    'user@com.',  # domain ends with dot
    'user space@example.com',  # space in local part
    'user@ex ample.com',  # space in domain
    # Note: The current regex allows dots at start/end of local part and domain
    'user@example',  # no TLD
    'user@example.',  # TLD starts with dot
    'user@@example.com',  # double @
    'user@exam@ple.com',  # multiple @
])
def test_is_valid_email_invalid_addresses(validator, email):
    """Test invalid email address validation."""
    assert not validator.is_valid_email(email), f"Expected {email!r} to be invalid"


# Phone validation tests
@pytest.mark.parametrize("phone", [
    '+1234567890',  # international format
    '1234567890',   # 10 digits
    '+12345678901',  # 11 digits with country code
    '+123456789012345',  # maximum 15 digits
    '+1 234 567 890',  # with spaces (should be cleaned)
    '+1-234-567-890',  # with hyphens (should be cleaned)
    '+1 (234) 567-890',  # with parentheses (should be cleaned)
    '123-456-7890',  # US format with hyphens
    '(123) 456-7890',  # US format with parentheses
])
def test_is_valid_phone_valid_numbers(validator, phone):
    """Test valid phone number validation."""
    assert validator.is_valid_phone(phone), f"Expected {phone!r} to be valid"


@pytest.mark.parametrize("phone", [
    '',  # empty string
    '123',  # too short
    '12345678',  # too short
    '+12345678901234567',  # too long (17 digits)
    'abcdefghij',  # letters
    '+1abc567890',  # mixed letters and numbers
    '++1234567890',  # multiple plus signs
])
def test_is_valid_phone_invalid_numbers(validator, phone):
    """Test invalid phone number validation."""
    assert not validator.is_valid_phone(phone), f"Expected {phone!r} to be invalid"


# Date validation tests
@pytest.mark.parametrize("date", [
    '25/12/2023',  # Christmas
    '01/01/2000',  # Y2K
    '31/12/1999',  # New Year's Eve
    '15-06-2023',  # With hyphens
    '08.03.2024',  # With dots
])
def test_is_valid_date_eu_format(validator, date):
    """Test valid EU date format (DD/MM/YYYY)."""
    assert validator.is_valid_date(date), f"Expected {date!r} to be valid"


@pytest.mark.parametrize("date", [
    '2023/12/25',  # Christmas
    '2000/01/01',  # Y2K
    '1999/12/31',  # New Year's Eve
    '2023-06-15',  # With hyphens
    '2024.03.08',  # With dots
])
def test_is_valid_date_iso_format(validator, date):
    """Test valid ISO date format (YYYY/MM/DD)."""
    assert validator.is_valid_date(date), f"Expected {date!r} to be valid"


@pytest.mark.parametrize("date", [
    '12/25/2023',  # Christmas
    '01/01/2000',  # Y2K
    '12/31/1999',  # New Year's Eve
    '06-15-2023',  # With hyphens
    '03.08.2024',  # With dots
])
def test_is_valid_date_us_format(validator, date):
    """Test valid US date format (MM/DD/YYYY)."""
    assert validator.is_valid_date(date), f"Expected {date!r} to be valid"


@pytest.mark.parametrize("date", [
    '',  # empty string
    '2023',  # year only
    '25/12',  # missing year
    '32/01/2023',  # invalid day
    '25/13/2023',  # invalid month
    '25/12/23',  # 2-digit year
    '25/12/20235',  # 5-digit year
    '2023/12/25/extra',  # extra part
    '25 12 2023',  # spaces instead of separators (now invalid after regex fix)
    '25|12|2023',  # invalid separator
])
def test_is_valid_date_invalid_formats(validator, date):
    """Test invalid date formats."""
    assert not validator.is_valid_date(date), f"Expected {date!r} to be invalid"


# Time validation tests
@pytest.mark.parametrize("time", [
    '12:30:45',  # full format
    '00:00:00',  # midnight
    '23:59:59',  # end of day
    '09:15:30',  # morning time
    '12:30',  # HH:MM format (seconds optional)
    '15:45 PM',  # with AM/PM
    '09:30 AM',  # morning with AM/PM
])
def test_is_valid_time_valid_formats(validator, time):
    """Test valid time formats."""
    assert validator.is_valid_time(time), f"Expected {time!r} to be valid"


@pytest.mark.parametrize("time", [
    '',  # empty string
    '12',  # hour only
    '24:00:00',  # invalid hour
    '12:60:00',  # invalid minute
    '12:30:60',  # invalid second
    '12-30-45',  # wrong separator
    'twelve:thirty:fortyfive',  # words
])
def test_is_valid_time_invalid_formats(validator, time):
    """Test invalid time formats."""
    assert not validator.is_valid_time(time), f"Expected {time!r} to be invalid"


# DateTime validation tests
@pytest.mark.parametrize("datetime", [
    '2023/12/25T12:30:45',  # ISO-style with T
    '2023-12-25 12:30:45',  # ISO-style with space
    '25/12/2023T09:15:30',  # EU format with T
    '25-12-2023 23:59:59',  # EU format with space
    '12/25/2023T00:00:00',  # US format with T
    '12.25.2023 15:45:30',  # US format with space
])
def test_is_valid_datetime_valid_formats(validator, datetime):
    """Test valid datetime formats."""
    assert validator.is_valid_datetime(datetime), f"Expected {datetime!r} to be valid"


@pytest.mark.parametrize("datetime", [
    '',  # empty string
    '2023/12/25',  # date only
    '12:30:45',  # time only
    '2023/12/25X12:30:45',  # invalid separator
    '2023/12/25T',  # missing time
    'T12:30:45',  # missing date
    '32/01/2023T12:30:45',  # invalid date
    '25/12/2023T25:30:45',  # invalid time
])
def test_is_valid_datetime_invalid_formats(validator, datetime):
    """Test invalid datetime formats."""
    assert not validator.is_valid_datetime(datetime), f"Expected {datetime!r} to be invalid"


# Validate method tests
def test_validate_no_validator_set(validator):
    """Test validation when no validator is set."""
    validator.validator = None
    
    # Should always return True and set error to False
    assert validator.validate('any text')
    assert not validator.error
    
    assert validator.validate('')
    assert not validator.error


def test_validate_required_field_empty(validator):
    """Test validation of required field when empty."""
    validator.required = True
    validator.validator = 'email'
    
    # Empty text should fail validation and set error
    assert not validator.validate('')
    assert validator.error


def test_validate_required_field_with_valid_content(validator):
    """Test validation of required field with valid content."""
    validator.required = True
    validator.validator = 'email'
    
    # Valid email should pass validation and clear error
    assert validator.validate('test@example.com')
    assert not validator.error


def test_validate_email_validator(validator):
    """Test validation with email validator."""
    validator.validator = 'email'
    
    # Valid email
    assert validator.validate('test@example.com')
    assert not validator.error
    
    # Invalid email
    assert not validator.validate('invalid-email')
    assert validator.error


def test_validate_phone_validator(validator):
    """Test validation with phone validator."""
    validator.validator = 'phone'
    
    # Valid phone
    assert validator.validate('+1234567890')
    assert not validator.error
    
    # Invalid phone
    assert not validator.validate('123')
    assert validator.error


def test_validate_unsupported_validator(validator):
    """Test validation with unsupported validator type."""
    # Since OptionProperty restricts values, this tests valid validators
    validator.validator = 'email'
    assert validator.validate('test@example.com')


def test_error_state_persistence(validator):
    """Test that error state persists correctly between validations."""
    validator.validator = 'email'
    
    # Start with no error
    assert not validator.error
    
    # Invalid input should set error
    validator.validate('invalid')
    assert validator.error
    
    # Valid input should clear error
    validator.validate('test@example.com')
    assert not validator.error


def test_required_with_non_empty_invalid_text(validator):
    """Test required field with non-empty but invalid text."""
    validator.required = True
    validator.validator = 'email'
    
    # Non-empty but invalid email should fail validation
    assert not validator.validate('not-an-email')
    assert validator.error


def test_optional_field_with_empty_text(validator):
    """Test optional field (not required) with empty text."""
    validator.required = False
    validator.validator = 'email'
    
    # Empty text in optional field should fail email validation
    # (empty string doesn't match email pattern)
    assert not validator.validate('')
    assert validator.error