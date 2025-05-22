import os
import django
import pandas as pd
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KBDDigitalPRO.settings')
django.setup()

from homeapp.models import User, UserData, GLS_Data

def parse_datetime_safe(value):
    try:
        dt = pd.to_datetime(value)
        if pd.isna(dt) or str(dt) == 'NaT':
            return None
        return dt.to_pydatetime()
    except:
        return None

def upload_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        records = df.to_dict(orient='records')
    except Exception as e:
        print(f"❌ Failed to read Excel file: {e}")
        return

    success_count = 0
    for row in records:
        try:
            user, created = User.objects.update_or_create(
                Folio_Number=row['Folio_Number'],
                defaults={
                    'Name': row['Name'],
                    'Code': row['Code'],
                    'Rank': row['Rank'],
                    'Password': row['Password'],
                    'Phone_Number': str(row['Phone_Number']),
                    'GLS_4_Participation': bool(row.get('GLS_4_Participation', False)),
                    'TC_Filled': bool(row.get('TC_Filled', False)),
                }
            )

            UserData.objects.update_or_create(
                user=user,
                defaults={k: float(row.get(k, 0)) for k in [
                    'Income_24_25', 'Sales_24_25', 'Team_24_25', 'Team_23_24',
                    'RPM_24_25', 'TEL_T_24_25', 'UP_T_24_25', 'RJ_T_24_25',
                    'PB_T_24_25', 'HR_T_24_25', 'HP_T_24_25'
                ]}
            )

            GLS_Data.objects.update_or_create(
                user=user,
                defaults={
                    'Batch': row.get('Batch', ''),
                    'Seat_Number': str(row.get('Seat_Number', '')),
                    'Checked_In': bool(row.get('Checked_In', False)),
                    'Checkin_Time': parse_datetime_safe(row.get('Checkin_Time')),
                    'Logged_In': bool(row.get('Logged_In', False)),
                    'Feedback_Form_Filled': bool(row.get('Feedback_Form_Filled', False)),
                    'Expected_Arrival': parse_datetime_safe(row.get('Expected_Arrival')),
                    'First_Time_Attendee': bool(row.get('First_Time_Attendee', False)),
                    'Mode_of_Transport': str(row.get('Mode_of_Transport', '')),
                    'Emergency_Contact': str(row.get('Emergency_Contact', '')),
                    'Admit': bool(row.get('Admit', False)),
                }
            )

            success_count += 1
        except Exception as e:
            print(f"❌ Error uploading folio {row.get('Folio_Number', '')}: {e}")

    print(f"\n✅ Upload completed. {success_count} row(s) uploaded successfully.\n")


if __name__ == '__main__':
    excel_path = 'bulk_upload.xlsx'
    upload_from_excel(excel_path)
