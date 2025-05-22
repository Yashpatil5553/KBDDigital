from django.shortcuts import render, redirect
from .models import User, GLS_Data, UserData
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import models
from django.db.models import Q
import pandas as pd
from django.http import HttpResponse
from io import BytesIO
from django.contrib import messages
from django.utils.dateparse import parse_datetime
from django.core.files.storage import FileSystemStorage
import pandas as pd
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserData, GLS_Data


def folio_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'folio' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

def logout_view(request):
    request.session.flush()
    return redirect('login')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass")
        user = User.objects.filter(Folio_Number=username, Password=password).first()
        if user:
            request.session['folio'] = user.Folio_Number
            return redirect('home')
        else:
            return render(request, "homeapp/index.html", {"error": "Invalid credentials"})
    return render(request, "homeapp/index.html")

@folio_login_required
def home(request):
    folio = request.session.get('folio')
    user = User.objects.filter(Folio_Number=folio).first()
    return render(request, "homeapp/home.html", {"user": user})


def gls_checkin(request):
    # STEP 1: Login with Folio Number + Password
    if request.method == 'POST' and 'folio_number' in request.POST and 'password' in request.POST:
        folio_number = request.POST.get('folio_number').strip()
        password = request.POST.get('password').strip()

        try:
            user = User.objects.get(Folio_Number=folio_number)

            if password == user.Password:
                request.session['folio_number'] = folio_number
                return redirect('gls_checkin_form')
            else:
                return render(request, 'homeapp/gls_checkin_login.html', {'error': "Incorrect password."})
        except User.DoesNotExist:
            return render(request, 'homeapp/gls_checkin_login.html', {'error': "Folio number not found."})

    return render(request, 'homeapp/gls_checkin_login.html')




def gls_checkin_form(request):
    folio_number = request.session.get('folio_number')

    if not folio_number:
        return redirect('gls_checkin')  # fallback

    try:
        user = User.objects.get(Folio_Number=folio_number)
        gls_data = GLS_Data.objects.get(user=user)

        if gls_data.Checked_In:
            return render(request, 'homeapp/gls_checkin_success.html', { 
                'user': user,
                'gls': gls_data
            })

        if request.method == 'POST':
            arrival = request.POST.get('arrival', '').strip()
            parsed_arrival = parse_datetime(arrival)

            terms_agree = request.POST.get('terms_agree')
            first_time = request.POST.get('first_time')
            emergency_contact = request.POST.get('emergency_contact', '').strip()
            transport = request.POST.getlist('transport')

            # ✅ Backend validations
            if terms_agree != 'yes':
                messages.error(request, "You must agree to the Terms & Conditions to check in.")
            elif not parsed_arrival:
                messages.error(request, "Please provide a valid expected arrival time.")
            elif not first_time:
                messages.error(request, "Please indicate whether this is your first GLS event.")
            elif not emergency_contact or not emergency_contact.isdigit() or len(emergency_contact) != 10:
                messages.error(request, "Please provide a valid 10-digit emergency contact number.")
            elif not transport:
                messages.error(request, "Please select at least one mode of transport.")
            else:
                # Save valid data
                gls_data.Checked_In = True
                gls_data.Checkin_Time = timezone.now()
                gls_data.Expected_Arrival = parsed_arrival
                gls_data.First_Time_Attendee = (first_time == 'yes')
                gls_data.Emergency_Contact = emergency_contact
                gls_data.Mode_of_Transport = ', '.join(transport)
                gls_data.save()

                return render(request, 'homeapp/gls_checkin_success.html', {
                    'user': user,
                    'gls': gls_data
                })

        return render(request, 'homeapp/gls_checkin_form.html', {
            'user': user
        })

    except (User.DoesNotExist, GLS_Data.DoesNotExist):
        return redirect('gls_checkin')

    
def gls_checked_list(request):
    query = request.GET.get('q', '').strip()
    batch_filter = request.GET.get('batch', 'ALL')
    checked_users = GLS_Data.objects.filter(Checked_In=True).select_related('user')

    if query:
        checked_users = checked_users.filter(
            Q(user__Name__icontains=query) |
            Q(user__Folio_Number__icontains=query) |
            Q(Batch__icontains=query)
        )

    if batch_filter != "ALL":
        checked_users = checked_users.filter(Batch=batch_filter)

    if 'download' in request.GET:
        data = [{
            'Name': d.user.Name,
            'Folio Number': d.user.Folio_Number,
            'Code': d.user.Code,
            'Batch': d.Batch,
            'Seat Number': d.Seat_Number,
            'Expected_Arrival Time': d.Expected_Arrival.strftime('%d-%m-%Y %I:%M %p') if d.Expected_Arrival else '',
            'Admit': 'Yes' if getattr(d, 'Admit', False) else 'No'
        } for d in checked_users]

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='CheckedIn')
        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=checked_in_participants.xlsx'
        return response

    return render(request, 'homeapp/gls_checked_list.html', {
        'checked_users': checked_users,
        'query': query,
        'batch_filter': batch_filter,
    })


def gls_qr_scan(request):
    message = None
    user_data = None
    message_class = ""
    show_admit_button = False

    if request.method == 'POST':
        folio = request.POST.get('folio_number', '').strip()
        action = request.POST.get('action')

        try:
            user = User.objects.get(Folio_Number=folio)
            try:
                gls = GLS_Data.objects.get(user=user)
            except GLS_Data.DoesNotExist:
                message = f"⚠️ No check-in record found for {user.Name}. Please contact admin."
                return render(request, 'homeapp/gls_qr_scan.html', {
                    'message': message,
                    'message_class': "error",
    })


            if action == 'admit':
                if not gls.Admit:
                    gls.Admit = True
                    gls.save()
                    message = f"✅ {user.Name} successfully admitted!"
                    message_class = "success"
                else:
                    message = "⚠️ Already admitted!"
                    message_class = "warning"
            else:
                user_data = user
                show_admit_button = not gls.Admit
                message = f"🔍 Scanned: {user.Name}" if not gls.Admit else "⚠️ Already admitted!"
                message_class = "warning" if gls.Admit else "success"

        except User.DoesNotExist:
            message = "❌ Invalid QR Code."
            message_class = "error"

    return render(request, 'homeapp/gls_qr_scan.html', {
        'message': message,
        'user_data': user_data,
        'show_admit_button': show_admit_button,
        'message_class': message_class
    })



def gls_admitted_list(request):
    query = request.GET.get('q', '').strip()
    batch_filter = request.GET.get('batch', 'ALL')

    admitted_users = GLS_Data.objects.filter(Admit=True).select_related('user')

    if query:
        admitted_users = admitted_users.filter(
            Q(user__Name__icontains=query) |
            Q(user__Folio_Number__icontains=query) |
            Q(Batch__icontains=query)
        )

    if batch_filter != "ALL":
        admitted_users = admitted_users.filter(Batch=batch_filter)

    if 'download' in request.GET:
        data = [{
            'Name': d.user.Name,
            'Folio Number': d.user.Folio_Number,
            'Code': d.user.Code,
            'Batch': d.Batch,
            'Seat Number': d.Seat_Number,
            'Check-in Time': d.Checkin_Time.strftime('%d-%m-%Y %I:%M %p') if d.Checkin_Time else '',
            'Admitted': 'Yes'
        } for d in admitted_users]

        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Admitted')
        output.seek(0)

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=admitted_participants.xlsx'
        return response

    return render(request, 'homeapp/gls_admitted_report.html', {
        'admitted_users': admitted_users,
        'query': query,
        'batch_filter': batch_filter,
    })






def parse_datetime_safe(value):
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None  # fallback for float, NaN, None


def bulk_upload_view(request):
    if request.method == 'POST':
        # PREVIEW MODE
        if 'preview' in request.POST:
            file = request.FILES.get('excel_file')
            if not file:
                messages.error(request, "No file uploaded.")
                return redirect('bulkupload')

            try:
                df = pd.read_excel(file)
                preview_records = df.to_dict(orient='records')
                request.session['preview_data'] = preview_records
                return render(request, 'homeapp/bulk_upload.html', {
                    'preview_data': preview_records
                })
            except Exception as e:
                messages.error(request, f"Failed to read Excel file: {e}")
                return redirect('bulkupload')

        # CONFIRM UPLOAD
        elif 'confirm_upload' in request.POST:
            preview_data = request.session.get('preview_data', [])
            success_count = 0
            for row in preview_data:
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
                    messages.error(request, f"Error uploading folio {row.get('Folio_Number', '')}: {e}")

            messages.success(request, f"{success_count} row(s) uploaded successfully.")
            return redirect('bulkupload')

    return render(request, 'homeapp/bulk_upload.html')

def bulk(request):
    if request.method == 'POST':
        # PREVIEW MODE
        if 'preview' in request.POST:
            file = request.FILES.get('excel_file')
            if not file:
                messages.error(request, "No file uploaded.")
                return redirect('bulk')

            try:
                df = pd.read_excel(file)
                preview_records = df.to_dict(orient='records')
                request.session['preview_data'] = preview_records
                return render(request, 'homeapp/bulk_upload.html', {
                    'preview_data': preview_records
                })
            except Exception as e:
                messages.error(request, f"Failed to read Excel file: {e}")
                return redirect('bulk')

        # CONFIRM UPLOAD
        elif 'confirm_upload' in request.POST:
            preview_data = request.session.get('preview_data', [])
            success_count = 0
            for row in preview_data:
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
                    messages.error(request, f"Error uploading folio {row.get('Folio_Number', '')}: {e}")

            messages.success(request, f"{success_count} row(s) uploaded successfully.")
            return redirect('bulk')

    return render(request, 'homeapp/bulk_upload.html')