import re
import os
from io import StringIO
from html.parser import HTMLParser
import html
import nepali_datetime
from datetime import datetime
from datetime import timedelta

# Donot change unless and until stated
nepali_month_mapping = {
    "वैशाख": 1,
    "बैशा ख": 1,
    "बैशाख": 1,
    "जेठ": 2,
    "जेष्ठ": 2,
    "असार": 3,
    "आषाढ": 3,
    "साउन": 4,
    "श्रावण": 4,
    "भदौ": 5,
    "भाद्र": 5,
    "असोज": 6,
    "आश्विन": 6,
    "कात्तिक": 7,
    'कार्तिक': 7,
    "मंसिर": 8,
    "मङ्सिर": 8,
    "पुस": 9,
    "पुष": 9,
    "पौष": 9,
    "माघ": 10,
    "फागुन": 11,
    "फाल्गुन": 11,
    "चैत": 12,
    "चैत्र": 12
}


def escape(s, quote=True):
    """
    Replace special characters "&", "<" and ">" to HTML-safe sequences.
    If the optional flag quote is true (the default), the quotation mark
    characters, both double quote (") and single quote (') characters are also
    translated.
    """
    s = s.replace("&", "&amp;")  # Must be done first!
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    if quote:
        s = s.replace('"', "&quot;")
        s = s.replace('\'', "&#x27;")
    return s


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def word_60(data: str = None):
    s = MLStripper()
    s.feed(data)
    text = s.get_data()
    text = data.split(" ")
    if len(text) < 60:
        return
    text = text[:60]
    text = ' '.join(text)
    text = re.sub('<.*?>', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('&zwj;', '', text)
    text = re.sub(r'\[&#\d+;\]', '', text)
    text = html.unescape(text)
    return text


def validate_date(date):
    try:
        if not date:
            return False
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def annapurnapost_datetime(ndate):
    date_string = ndate
    date_parts = date_string.split(" ")
    nepali_day = int(date_parts[1].strip(','))
    nepali_month = nepali_month_mapping[date_parts[0]]
    nepali_year = int(date_parts[2])

    formatted_date = f"{nepali_month:02d} {nepali_day:02d} {nepali_year}"
    dateobject = nepali_datetime.datetime.strptime(formatted_date, "%m %d %Y")
    english_date = dateobject.to_datetime_date()
    formatted_date = english_date.strftime("%Y-%m-%d")
    return str(formatted_date)


def kathmandupost_conversion(date):
    published_date_str = date.split(':', 1)[-1].strip()
    date_object = datetime.strptime(published_date_str, '%B %d, %Y')
    formatted_date = date_object.strftime('%Y-%m-%d')
    return formatted_date


def bbcnepali_date_conversion(cleaned_time):
    date_object = datetime.strptime(cleaned_time, "%m/%d/%Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    return str(formatted_date)


def ekantipur_conversion(time):
    date_string = time
    date_parts = date_string.split(" ")
    nepali_day = int(date_parts[1].strip(','))
    nepali_month = nepali_month_mapping[date_parts[0]]
    nepali_year = int(date_parts[2])

    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    dateobject = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = dateobject.to_datetime_date()
    formatted_date = english_date.strftime('%Y-%m-%d')
    return str(formatted_date)


def gorkhapatraonline_datetime_parser(nepali_date):

    date_parts = nepali_date.split()
    nepali_day = int(date_parts[0])
    nepali_month = nepali_month_mapping[date_parts[1]]
    nepali_year = int(date_parts[2].strip(','))
    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    date_object = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = date_object.to_datetime_date()
    formatted_date = english_date.strftime("%Y-%m-%d")
    return formatted_date


def tht_timeconversion(date):
    print(f'------inside utils-----{date}')
    date_time = datetime.strptime(date, "Published: %I:%M %p %b %d, %Y")
    formatted_date = date_time.strftime("%Y-%m-%d")
    print(f'-----inside utils------{formatted_date}')
    return formatted_date


def nagariknews__dateconverter(date_string):
    date_parts = date_string.split()
    nepali_day = int(date_parts[0])
    nepali_month = nepali_month_mapping[date_parts[1]]
    nepali_year = int(date_parts[2])
    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    date_object = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = date_object.to_datetime_date()
    formatted_datetime = english_date.strftime("%Y-%m-%d")
    return formatted_datetime


def online_khabar_conversion(time):
    # test_date = '२०८० असार १० गते ११:२४'
    # nepali_month_mapping = {
    #         "बैशाख": '०१',
    #         "जेष्ठ": '०२',
    #         "असार": '०३',
    #         "श्रावण": '०४',
    #         "भाद्र": '०५',
    #         "आश्वीन": '०६',
    #         "कात्तिक": '०७',
    #         "मंसिर": '०८',
    #         "पौष": '०९',
    #         "माघ": '१०',
    #         "फागुन": '११',
    #         "चैत्र": '१२'
    #     }
    if time:
        date = time.split()
        nepali_year = date[0]
        nepali_month = nepali_month_mapping[date[1]]
        nepali_day = date[2]
        # Format the Nepali date as yyyy-mm-dd
        formatted_date = f"{nepali_year}-{nepali_month}-{nepali_day}"
        # Convert the Nepali date to English date
        english_date = nepali_datetime.date(
            int(nepali_year), int(nepali_month), int(nepali_day))
        english_date = english_date.to_datetime_date()
        # Format the English date as mm/dd/yyyy
        formatted_date = english_date.strftime("%Y-%m-%d")
        return formatted_date
    else:
        return None


def ratopati_date_conversion(dt):
    date = dt.split(',')
    new_date = date[1]
    date = new_date[1:]

    date = date.split()
    nepali_month = nepali_month_mapping[date[1]]
    nepali_day = date[0]
    nepali_year = date[2]

    # Convert the Nepali date to an English date
    english_date = nepali_datetime.date(
        int(nepali_year), int(nepali_month), int(nepali_day))
    english_date = english_date.to_datetime_date()
    # Format the English date as mm/dd/yyyy
    formatted_date = english_date.strftime("%Y-%m-%d")
    return formatted_date


def republica_conversion(cleaned_time):
    publishdate = (cleaned_time.strip()).replace(' By:', '')
    fromattedate = " ".join(publishdate.split(' ')[:3])
    input_date = datetime.strptime(fromattedate, "%B %d, %Y")
    output_date_str = input_date.strftime("%Y-%m-%d")
    return output_date_str


def everestHeadlines_conversion(date):
    try:
        date = date.strip()
        date = date.replace(",", " ")
        date_parts = date.split()

        if len(date_parts) != 4:
            raise ValueError("Invalid Nepali date format")

        year = int(date_parts[3])
        day = int(date_parts[2])
        month_str = date_parts[1]

        if month_str not in nepali_month_mapping:
            raise ValueError(f"Invalid Nepali month name: {month_str}")

        month = nepali_month_mapping[month_str]

        formattedDate = f"{year:04d}-{month:02d}-{day:02d}"
        return formattedDate

    except (ValueError, IndexError) as e:
        raise ValueError(f"Error converting Nepali date '{date}': {e}")


def RatopatiEnglish_conversion(date):
    formatted_date = date.replace('\n', '')
    input_date = datetime.strptime(formatted_date, "%B %d, %Y")
    output_date_string = input_date.strftime("%Y-%m-%d")
    return output_date_string


def eAdarsha_conversion(date):
    try:
        date = date.strip()
        date = date.replace(",", " ")
        date_parts = date.split()

        if len(date_parts) != 3:
            raise ValueError("Invalid Nepali date format")

        year = int(date_parts[2])
        day = int(date_parts[1])
        month_str = date_parts[0]

        if month_str not in nepali_month_mapping:
            raise ValueError(f"Invalid Nepali month name: {month_str}")

        month = nepali_month_mapping[month_str]

        formattedDate = f"{year:04d}-{month:02d}-{day:02d}"
        return formattedDate

    except (ValueError, IndexError) as e:
        raise ValueError(f"Error converting Nepali date '{date}': {e}")


def techlekh_dateconverter(date_string):
    date_string = date_string.split()
    date_month = date_string[-3]
    date_day = date_string[-2].replace(",", "")
    date_year = date_string[-1]
    date = datetime.strptime(
        f"{date_month} {date_day}, {date_year}", "%B %d, %Y")
    formatted_date = date.strftime("%Y-%m-%d")
    return formatted_date


def himalkhabar_conversion(date):
    formatted_date = None  # Initialize with a default value
    if 'मिनेट' in date or 'घण्टा' in date or 'दिन' in date:
        if 'मिनेट' in date or 'घण्टा' in date:
            current_date = datetime.now()
            formatted_date = current_date.strftime("%Y-%m-%d")

        if 'दिन' in date:
            date_parts = date.split()
            passed_date = int(date_parts[0])
            published_date = datetime.today() - timedelta(days=passed_date)
            formatted_date = published_date.strftime("%Y-%m-%d")

        if 'महिना' in date:
            return None
        return formatted_date
    else:
        pass

    date_parts = date.split()
    nepali_day = int(date_parts[-2].strip(","))
    nepali_month = nepali_month_mapping[date_parts[-3].strip(",")]
    nepali_year = int(date_parts[-1])
    formatted_date = f"{nepali_month}/{nepali_day}/{nepali_year}"
    date_object = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = date_object.to_datetime_date()
    formatted_date = english_date.strftime("%Y-%m-%d")
    return formatted_date


def bizmandu_datetime(ndate):
    date_string = ndate
    date_parts = date_string.split(" ")
    nepali_day = int(date_parts[2].strip(','))
    nepali_month = nepali_month_mapping[date_parts[1]]
    nepali_year = int(date_parts[0].strip(','))

    formatted_date = f"{nepali_month:02d} {nepali_day:02d} {nepali_year}"
    dateobject = datetime.strptime(formatted_date, "%m %d %Y")
    formatted_date = dateobject.strftime('%Y-%m-%d')

    return str(formatted_date)


def lokaantar_conversion(date):
    date_string = date
    date_parts = date_string.split(" ")
    nepali_day = int(date_parts[1].strip(','))
    nepali_month = nepali_month_mapping[date_parts[0]]
    nepali_year = int(date_parts[2])

    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    dateobject = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = dateobject.to_datetime_date()
    formatted_date = english_date.strftime('%Y-%m-%d')
    return str(formatted_date)


def setopati_datetime_parser(nepali_date):
    date_parts = nepali_date.split()
    nepali_year = int(date_parts[5].replace(',', ''))
    nepali_day = ''.join(filter(str.isdigit, date_parts[4]))
    nepali_day = int(nepali_day)
    nepali_month = nepali_month_mapping[date_parts[3]]
    formatted_date = f"{nepali_month:02d}/{nepali_day:02d}/{nepali_year}"
    date_object = nepali_datetime.datetime.strptime(formatted_date, "%m/%d/%Y")
    english_date = date_object.to_datetime_date()
    formatted_datetime = english_date.strftime("%Y-%m-%d")
    return formatted_datetime


def get_report_file_path():
    return os.path.join(os.getcwd(), 'output', f'Status-Report-{datetime.today().now().date()}.csv')


def delete_report_file():
    os.remove(os.path.join(os.getcwd(), 'output',
              f'Status-Report-{datetime.today().now().date()}.csv'))
