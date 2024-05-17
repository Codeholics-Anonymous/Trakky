from datetime import datetime, date

def calculate_days_difference(starting_date, ending_date):
    if isinstance(starting_date, str):
        starting_date = datetime.strptime(starting_date, "%Y-%m-%d").date()
    if isinstance(ending_date, str):
        ending_date = datetime.strptime(ending_date, "%Y-%m-%d").date()
    return (ending_date - starting_date).days + 1

def date_validation(starting_date, ending_date = date.today()):
    if (starting_date > ending_date):
        raise ValidationError("Incorrect date")

def age_validation(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.year, birth_date.day))
    if (age < 12):
        raise ValidationError("Birth date is incorrect.")