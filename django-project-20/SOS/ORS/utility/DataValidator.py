from datetime import datetime, date
import re

class DataValidator:

    @classmethod
    def isNotNull(cls, val):
        return val is not None and str(val).strip() != ""

    @classmethod
    def isNull(cls, val):
        return val is None or str(val).strip() == ""

    @classmethod
    def isDate(cls, val):
        try:
            input_date = datetime.strptime(val, "%Y-%m-%d")
            return input_date > datetime.today()
        except:
            return False

    @classmethod
    def isCheck(cls, val):
        try:
            num = int(val)
            return 0 <= num <= 100
        except:
            return False

    @classmethod
    def isCheckRoll(cls, val):
        return bool(re.match(r"^(?=.*[A-Z])(?=.*\d).+$", val))

    @classmethod
    def isAlphaCheck(cls, val):
        return bool(re.match(r"^[a-zA-Z\s]+$", val))

    @classmethod
    def isMobileCheck(cls, val):
        return bool(re.match(r"^[6-9]\d{9}$", val))

    @classmethod
    def isEmail(cls, val):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", val))

    @classmethod
    def isPhoneCheck(cls, val):
        return bool(re.match(r"^(?:(?:\+|0{0,2})91[\s-]?)?[6-9]\d{9}$", val))
