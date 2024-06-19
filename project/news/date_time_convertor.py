from datetime import datetime, timedelta

# UTC to Nepal Standard Time (NPT) offset
NPT_OFFSET = timedelta(hours=5, minutes=45)

# Function to convert UTC datetime to Nepali datetime
def utc_to_nepali(utc_datetime_str):
    try:
        utc_datetime = datetime.fromisoformat(
            utc_datetime_str.replace('Z', '+00:00'))
    except ValueError:
        raise ValueError(
            "Invalid datetime format. Use ISO format (YYYY-MM-DDTHH:MM:SSZ).")

    nepali_datetime = utc_datetime + NPT_OFFSET
    return nepali_datetime.strftime("%Y-%m-%d %H:%M:%S"), nepali_datetime.date()

def date_time_object():
    utc_datetime_str =  datetime.now().isoformat()+'Z'
    try: 
        nepali_datetime_str, nepali_date = utc_to_nepali(utc_datetime_str)
        nepali_year, nepali_month, nepali_day = nepali_date.year, nepali_date.month, nepali_date.day
        nepali_date = {nepali_year}-{nepali_month}-{nepali_day}
        return nepali_date 

    except ValueError as e:
        return e