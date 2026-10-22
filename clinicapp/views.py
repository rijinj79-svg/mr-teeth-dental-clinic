from django.contrib.auth import authenticate, login, logout
from django.contrib import auth, messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AppointmentForm,
    ContactForm,
    PatientForm,
    FinanceIncomeForm,
    FinanceExpenseForm,
    StaffAppointmentForm,
    GalleryMediaForm,
    FeedbackForm,
    StaffCreationForm,
    DoctorForm,
    StaffProfileForm,
    DepartmentForm,
)
from .models import (
    Appointment,
    Contact,
    Doctor,
    StaffProfile,
    Patient,
    FinanceIncome,
    FinanceExpense,
    GalleryMedia,
    Feedback,
    Department,
)


# =========================================================
# PUBLIC PAGES
# =========================================================

def home(request):
    feedback_form = FeedbackForm()
    return render(
        request,
        "home.html",
        {
            "doctors": Doctor.objects.filter(active=True),
            "feedback_form": feedback_form,
            "approved_feedback": Feedback.objects.filter(
                is_approved=True
            )[:6],
        },
    )


def about(request):
    return render(request, "about.html")


def depart(request):
    doctors = Doctor.objects.filter(
        active=True
    ).order_by("display_order", "name")

    return render(
        request,
        "depart.html",
        {
            "doctors": doctors,
        },
    )

def gallery(request):
    legacy_images = [
        "interior1.jpg",
        "interior2.jpg",
        "interior3.jpg",
        "dental1.jpg",
        "dental2.jpg",
        "dental3.png",
        "client1.jpg",
        "client2.jpg",
        "client3.jpg",
        "client4.jpg",
        "client5.jpg",
        "client6.jpg",
    ]

    uploaded_media = GalleryMedia.objects.filter(is_published=True)

    return render(
        request,
        "gallery.html",
        {
            "gallery_images": legacy_images,
            "uploaded_images": uploaded_media.filter(
                image__isnull=False
            ),
            "uploaded_videos": uploaded_media.filter(
                video__isnull=False
            ),
        },
    )


def submit_feedback(request):
    if request.method != "POST":
        return redirect("home")

    form = FeedbackForm(request.POST)

    if form.is_valid():
        form.save()
        messages.success(
            request,
            "Thank you for your feedback! It will appear after clinic approval.",
        )
    else:
        messages.error(
            request,
            "Please check the feedback form and try again.",
        )

    return redirect("/#feedback")


def admin_register(request):
    messages.info(
        request,
        "Administrator accounts cannot be registered publicly. "
        "Please contact the existing website administrator.",
    )
    return redirect("admin_login")


# =========================================================
# ADMIN LOGIN AND DASHBOARD
# =========================================================

def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("admin_dashboard")

        messages.error(
            request,
            "You do not have administrator access.",
        )
        return redirect("home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")

        messages.error(
            request,
            "Invalid credentials or administrator access is not permitted.",
        )

    return render(request, "admin_login.html")


@require_POST
def admin_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("admin_login")


def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not request.user.is_superuser:
        messages.error(
            request,
            "You do not have administrator access.",
        )
        return redirect("home")

    return render(request, "admin_dashboard.html")


# =========================================================
# ACCESS CONTROL
# =========================================================

def admin_required(user):
    return user.is_authenticated and user.is_superuser


def staff_required(user):
    return user.is_authenticated and user.is_staff


def admin_or_staff_required(user):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser
    )


# =========================================================
# ADMIN DOCTOR MANAGEMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_doctors(request):
    if request.method == "POST":
        action = request.POST.get("action")
        doctor_id = request.POST.get("doctor_id")

        if action in {"toggle", "delete"} and doctor_id:
            doctor = get_object_or_404(Doctor, pk=doctor_id)

            if action == "toggle":
                doctor.active = not doctor.active
                doctor.save(update_fields=["active"])
                messages.success(
                    request,
                    "Doctor visibility updated.",
                )
            else:
                doctor.delete()
                messages.success(
                    request,
                    "Doctor profile deleted.",
                )

            return redirect("admin_doctors")

        instance = (
            get_object_or_404(Doctor, pk=doctor_id)
            if doctor_id
            else None
        )

        form = DoctorForm(
            request.POST,
            request.FILES,
            instance=instance,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Doctor profile saved successfully.",
            )
            return redirect("admin_doctors")

    else:
        doctor_id = request.GET.get("edit")
        instance = (
            get_object_or_404(Doctor, pk=doctor_id)
            if doctor_id
            else None
        )
        form = DoctorForm(instance=instance)

    return render(
        request,
        "admin_doctors.html",
        {
            "form": form,
            "doctors": Doctor.objects.all(),
            "editing": bool(request.GET.get("edit")),
        },
    )


# =========================================================
# ADMIN STAFF MANAGEMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_staff(request):
    if request.method == "POST":
        action = request.POST.get("action")
        staff_id = request.POST.get("staff_id")

        if action == "toggle" and staff_id:
            staff_user = get_object_or_404(
                User,
                pk=staff_id,
                is_staff=True,
                is_superuser=False,
            )

            staff_user.is_active = not staff_user.is_active
            staff_user.save(update_fields=["is_active"])

            messages.success(
                request,
                "Staff account status updated.",
            )
            return redirect("admin_staff")

        form = StaffCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Staff account created successfully.",
            )
            return redirect("admin_staff")

    else:
        form = StaffCreationForm()

    staff_users = User.objects.filter(
        is_staff=True,
        is_superuser=False,
    ).order_by("username")

    return render(
        request,
        "admin_staff.html",
        {
            "form": form,
            "staff_users": staff_users,
        },
    )


# =========================================================
# ADMIN GALLERY MANAGEMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_gallery_media(request):
    if (
        request.method == "POST"
        and request.POST.get("action") in {"toggle", "delete"}
    ):
        item = get_object_or_404(
            GalleryMedia,
            pk=request.POST.get("media_id"),
        )

        if request.POST["action"] == "toggle":
            item.is_published = not item.is_published
            item.save(update_fields=["is_published"])
            messages.success(
                request,
                "Gallery item publication status updated.",
            )
        else:
            item.delete()
            messages.success(
                request,
                "Gallery item deleted.",
            )

        return redirect("admin_gallery_media")

    form = GalleryMediaForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and not request.POST.get("action"):
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Gallery media uploaded successfully.",
            )
            return redirect("admin_gallery_media")

    return render(
        request,
        "admin_gallery_media.html",
        {
            "form": form,
            "media_items": GalleryMedia.objects.all(),
        },
    )


# =========================================================
# ADMIN FEEDBACK MANAGEMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_feedback(request):
    if request.method == "POST":
        feedback_id = request.POST.get("feedback_id")
        action = request.POST.get("action")

        feedback = get_object_or_404(
            Feedback,
            pk=feedback_id,
        )

        if action == "toggle":
            feedback.is_approved = not feedback.is_approved
            feedback.save(update_fields=["is_approved"])
            messages.success(
                request,
                "Feedback moderation status updated.",
            )

        elif action == "delete":
            feedback.delete()
            messages.success(request, "Feedback deleted.")

        return redirect("admin_feedback")

    return render(
        request,
        "admin_feedback.html",
        {
            "feedback_items": Feedback.objects.all(),
        },
    )


# =========================================================
# ADMIN EDIT APPOINTMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_edit_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if request.method == "POST":
        doctor_id = request.POST.get("doctor")
        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")

        if (
            not doctor_id
            or not appointment_date
            or not appointment_time
        ):
            messages.error(
                request,
                "Please fill in all required fields.",
            )
            return redirect(
                "admin_edit_appointment",
                appointment_id=appointment.id,
            )

        conflict = Appointment.objects.filter(
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=["Pending", "Confirmed"],
        ).exclude(pk=appointment.id)

        if conflict.exists():
            messages.error(
                request,
                "This doctor already has an appointment "
                "at the selected date and time.",
            )
            return redirect(
                "admin_edit_appointment",
                appointment_id=appointment.id,
            )

        appointment.doctor_id = doctor_id
        appointment.appointment_date = appointment_date
        appointment.appointment_time = appointment_time
        appointment.save()

        messages.success(
            request,
            "Appointment updated successfully.",
        )
        return redirect("staff_appointments")

    return render(
        request,
        "admin_edit_appointment.html",
        {
            "appointment": appointment,
            "doctors": Doctor.objects.filter(active=True),
        },
    )


# =========================================================
# ADMIN DELETE APPOINTMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_delete_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if request.method == "POST":
        appointment.delete()
        messages.success(
            request,
            "Appointment deleted successfully.",
        )
        return redirect("staff_appointments")

    return render(
        request,
        "admin_delete_appointment.html",
        {
            "appointment": appointment,
        },
    )


# =========================================================
# PATIENT APPOINTMENT BOOKING
# =========================================================

@login_required
def appoint(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            date = form.cleaned_data["appointment_date"]
            time = form.cleaned_data["appointment_time"]
            doctor = form.cleaned_data.get("doctor")

            conflicts = Appointment.objects.filter(
                appointment_date=date,
                appointment_time=time,
                status__in=["Pending", "Confirmed"],
            )

            if doctor:
                conflicts = conflicts.filter(doctor=doctor)

            if conflicts.exists():
                form.add_error(
                    "appointment_time",
                    "That slot is already requested. "
                    "Please choose another time.",
                )
            else:
                appointment = form.save(commit=False)
                appointment.patient = request.user

                if not appointment.email:
                    appointment.email = request.user.email

                patient_record = Patient.objects.filter(
                    phone=appointment.phone
                ).first()

                if patient_record:
                    appointment.patient_record = patient_record

                appointment.save()

                # Send notifications without preventing the booking
                # from being saved if email configuration is unavailable.
                recipient = getattr(
                    settings,
                    "ADMIN_EMAIL",
                    None,
                )

                if recipient:
                    try:
                        send_mail(
                            "New dental appointment request",
                            (
                                f"Patient: {appointment.name}\n"
                                f"Phone: {appointment.phone}\n"
                                f"Service: {appointment.service}\n"
                                f"Date: {appointment.appointment_date}\n"
                                f"Time: {appointment.appointment_time}\n"
                            ),
                            settings.DEFAULT_FROM_EMAIL,
                            [recipient],
                            fail_silently=True,
                        )
                    except Exception:
                        pass

                messages.success(
                    request,
                    "Appointment request submitted. "
                    "The clinic will confirm your slot.",
                )
                return redirect("my_appointments")

    else:
        form = AppointmentForm(
            initial={
                "appointment_date": timezone.localdate(),
            }
        )

    return render(
        request,
        "appointment.html",
        {
            "form": form,
        },
    )
# =========================================================
# PATIENT APPOINTMENTS
# =========================================================

@login_required
def my_appointments(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("doctor").order_by(
        "-appointment_date",
        "-appointment_time",
    )

    return render(
        request,
        "my_appointments.html",
        {
            "appointments": appointments,
        },
    )


@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
        patient=request.user,
    )

    if appointment.status in ["Pending", "Confirmed"]:
        appointment.status = "Cancelled"
        appointment.save(update_fields=["status"])
        messages.success(
            request,
            "Your appointment has been cancelled.",
        )
    else:
        messages.error(
            request,
            "This appointment cannot be cancelled.",
        )

    return redirect("my_appointments")


# =========================================================
# PATIENT REGISTRATION AND LOGIN
# =========================================================

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = auth.forms.UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                "Your account has been created successfully.",
            )
            return redirect("dashboard")
    else:
        form = auth.forms.UserCreationForm()

    return render(
        request,
        "registration.html",
        {
            "form": form,
        },
    )


def user_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("staff_dashboard")
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and not user.is_staff:
            login(request, user)
            messages.success(
                request,
                "You have logged in successfully.",
            )
            return redirect("dashboard")

        messages.error(
            request,
            "Invalid username or password.",
        )

    return render(request, "login.html")


@login_required
@require_POST
def user_logout(request):
    if request.user.is_staff:
        messages.error(
            request,
            "Please use the staff logout option.",
        )
        return redirect("staff_dashboard")

    logout(request)
    messages.success(
        request,
        "You have logged out successfully.",
    )
    return redirect("home")


@login_required
def dashboard(request):
    appointments = Appointment.objects.filter(
        patient=request.user
    ).select_related("doctor").order_by(
        "-appointment_date",
        "-appointment_time",
    )

    return render(
        request,
        "dashboard.html",
        {
            "appointments": appointments,
        },
    )


# =========================================================
# CONTACT FORM
# =========================================================

def call(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your message has been submitted successfully.",
            )
            return redirect("call")

        messages.error(
            request,
            "Please correct the errors in the contact form.",
        )
    else:
        form = ContactForm()

    return render(
        request,
        "contact.html",
        {
            "form": form,
        },
    )


# =========================================================
# STAFF LOGIN AND LOGOUT
# =========================================================

def staff_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("staff_dashboard")

        messages.error(
            request,
            "Please use the patient login page.",
        )
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(
                request,
                "Staff login successful.",
            )
            return redirect("staff_dashboard")

        messages.error(
            request,
            "Invalid credentials or staff access is not permitted.",
        )

    return render(request, "staff_login.html")


@login_required
@require_POST
def staff_logout(request):
    if not request.user.is_staff:
        messages.error(
            request,
            "You do not have staff access.",
        )
        return redirect("home")

    logout(request)
    messages.success(
        request,
        "Staff logout successful.",
    )
    return redirect("staff_login")


# =========================================================
# STAFF DASHBOARD
# =========================================================


@user_passes_test(staff_required, login_url="staff_login")
def staff_dashboard(request):
    today = timezone.localdate()

    # Get today's appointment records for the table
    today_appointments = Appointment.objects.filter(
        appointment_date=today,
    ).select_related("doctor").order_by("appointment_time")

    # Dashboard statistics
    pending_count = Appointment.objects.filter(
        status="Pending",
    ).count()

    confirmed_count = Appointment.objects.filter(
        status="Confirmed",
    ).count()

    message_count = Contact.objects.filter(
        status="New",
    ).count()

    context = {
        "today": today,
        "today_appointments": today_appointments,
        "pending_count": pending_count,
        "confirmed_count": confirmed_count,
        "message_count": message_count,
    }

    return render(
        request,
        "staff_dashboard.html",
        context,
    )


# =========================================================
# STAFF APPOINTMENT MANAGEMENT
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
def staff_appointments(request):
    appointments = Appointment.objects.select_related(
        "doctor",
        "patient",
        "patient_record",
    ).order_by(
        "-appointment_date",
        "-appointment_time",
    )

    return render(
        request,
        "staff_appointments.html",
        {
            "appointments": appointments,
        },
    )


@user_passes_test(staff_required, login_url="staff_login")
def staff_add_appointment(request):
    if request.method == "POST":
        form = StaffAppointmentForm(request.POST)

        if form.is_valid():
            appointment_date = form.cleaned_data[
                "appointment_date"
            ]
            appointment_time = form.cleaned_data[
                "appointment_time"
            ]
            doctor = form.cleaned_data.get("doctor")

            conflicts = Appointment.objects.filter(
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                status__in=["Pending", "Confirmed"],
            )

            if doctor:
                conflicts = conflicts.filter(doctor=doctor)

            if conflicts.exists():
                form.add_error(
                    "appointment_time",
                    "This appointment slot is already occupied.",
                )
            else:
                appointment = form.save(commit=False)

                patient_record = Patient.objects.filter(
                    phone=appointment.phone
                ).first()

                if patient_record:
                    appointment.patient_record = patient_record

                appointment.save()

                messages.success(
                    request,
                    "Appointment added successfully.",
                )
                return redirect("staff_appointments")
    else:
        form = StaffAppointmentForm(
            initial={
                "appointment_date": timezone.localdate(),
            }
        )

    return render(
        request,
        "staff_add_appointment.html",
        {
            "form": form,
        },
    )


@user_passes_test(staff_required, login_url="staff_login")
@require_POST
def confirm_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if appointment.status == "Pending":
        appointment.status = "Confirmed"
        appointment.save(update_fields=["status"])
        messages.success(
            request,
            "Appointment confirmed successfully.",
        )
    else:
        messages.error(
            request,
            "Only pending appointments can be confirmed.",
        )

    return redirect("staff_appointments")


@user_passes_test(staff_required, login_url="staff_login")
@require_POST
def complete_appointment(request, appointment_id):
    appointment = get_object_or_404(
        Appointment,
        pk=appointment_id,
    )

    if appointment.status == "Confirmed":
        appointment.status = "Completed"
        appointment.save(update_fields=["status"])
        messages.success(
            request,
            "Appointment marked as completed.",
        )
    else:
        messages.error(
            request,
            "Only confirmed appointments can be completed.",
        )

    return redirect("staff_appointments")


# =========================================================
# STAFF PATIENT RECORDS
# =========================================================

def generate_op_number():
    existing_numbers = Patient.objects.values_list(
        "op_no",
        flat=True,
    )

    highest_number = 0

    for op_no in existing_numbers:
        if op_no and op_no.startswith("OP-"):
            try:
                number = int(op_no.split("-", 1)[1])
                highest_number = max(highest_number, number)
            except (ValueError, IndexError):
                continue

    return f"OP-{highest_number + 1:04d}"


@user_passes_test(staff_required, login_url="staff_login")
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)

        if form.is_valid():
            patient = form.save(commit=False)
            patient.op_no = generate_op_number()
            patient.save()

            messages.success(
                request,
                f"Patient added successfully. OP Number: {patient.op_no}",
            )
            return redirect("patient_records")
    else:
        form = PatientForm(
            initial={
                "date": timezone.localdate(),
            }
        )

    return render(
        request,
        "add_patient.html",
        {
            "form": form,
        },
    )


@user_passes_test(staff_required, login_url="staff_login")
def patient_records(request):
    query = request.GET.get("q", "").strip()

    patients = Patient.objects.all()

    if query:
        patients = patients.filter(
            Q(op_no__icontains=query)
            | Q(name__icontains=query)
            | Q(phone__icontains=query)
        )

    return render(
        request,
        "patient_records.html",
        {
            "patients": patients,
            "query": query,
        },
    )


@user_passes_test(staff_required, login_url="staff_login")
def patient_detail(request, pk):
    patient = get_object_or_404(
        Patient,
        pk=pk,
    )

    appointments = Appointment.objects.filter(
        patient_record=patient,
    ).select_related("doctor").order_by(
        "-appointment_date",
        "-appointment_time",
    )

    return render(
        request,
        "patient_detail.html",
        {
            "patient": patient,
            "appointments": appointments,
        },
    )


@user_passes_test(staff_required, login_url="staff_login")
def edit_patient(request, pk):
    patient = get_object_or_404(
        Patient,
        pk=pk,
    )

    if request.method == "POST":
        form = PatientForm(
            request.POST,
            instance=patient,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Patient record updated successfully.",
            )
            return redirect(
                "patient_detail",
                pk=patient.pk,
            )
    else:
        form = PatientForm(instance=patient)

    return render(
        request,
        "edit_patient.html",
        {
            "form": form,
            "patient": patient,
        },
    )


@user_passes_test(staff_required, login_url="staff_login")
def delete_patient(request, pk):
    patient = get_object_or_404(
        Patient,
        pk=pk,
    )

    if request.method == "POST":
        patient.delete()
        messages.success(
            request,
            "Patient record deleted successfully.",
        )
        return redirect("patient_records")

    return render(
        request,
        "delete_patient.html",
        {
            "patient": patient,
        },
    )
# =========================================================
# STAFF CONTACT MESSAGES
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
def staff_messages(request):
    if request.method == "POST":
        contact_id = request.POST.get("contact_id")
        action = request.POST.get("action")

        contact = get_object_or_404(
            Contact,
            pk=contact_id,
        )

        if action == "read":
            contact.status = "Read"
            contact.save(update_fields=["status"])
            messages.success(request, "Message marked as read.")

        elif action == "replied":
            contact.status = "Replied"
            contact.save(update_fields=["status"])
            messages.success(request, "Message marked as replied.")

        elif action == "delete":
            contact.delete()
            messages.success(request, "Message deleted.")

        return redirect("staff_messages")

    contacts = Contact.objects.all().order_by("-created_at")

    return render(
        request,
        "staff_messages.html",
        {
            "contacts": contacts,
            "messages_list": contacts,
        },
    )


# =========================================================
# FINANCE DASHBOARD
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
def finance_dashboard(request):
    today = timezone.localdate()

    today_income = FinanceIncome.objects.filter(
        payment_date=today,
    )

    today_expenses = FinanceExpense.objects.filter(
        expense_date=today,
    )

    income_total = today_income.aggregate(
        total=Sum("amount")
    )["total"] or 0

    expense_total = today_expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "finance_dashboard.html",
        {
            "today_income": today_income,
            "today_expenses": today_expenses,
            "income_total": income_total,
            "expense_total": expense_total,
            "cash_in_hand": income_total - expense_total,
            "today_income_total": income_total,
            "today_expense_total": expense_total,
        },
    )


# =========================================================
# ADD FINANCE INCOME
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
def add_finance_income(request):
    if request.method == "POST":
        form = FinanceIncomeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Income record added successfully.",
            )
            return redirect("finance_dashboard")
    else:
        form = FinanceIncomeForm(
            initial={
                "payment_date": timezone.localdate(),
            }
        )

    return render(
        request,
        "add_finance_income.html",
        {
            "form": form,
        },
    )


# =========================================================
# EDIT FINANCE INCOME
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
def edit_finance_income(request, pk):
    income = get_object_or_404(
        FinanceIncome,
        pk=pk,
    )

    if request.method == "POST":
        form = FinanceIncomeForm(
            request.POST,
            instance=income,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Income record updated successfully.",
            )
            return redirect("finance_dashboard")
    else:
        form = FinanceIncomeForm(instance=income)

    return render(
        request,
        "edit_finance_income.html",
        {
            "form": form,
            "income": income,
        },
    )


# =========================================================
# DELETE FINANCE INCOME
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
@require_POST
def delete_finance_income(request, pk):
    income = get_object_or_404(
        FinanceIncome,
        pk=pk,
    )

    income.delete()

    messages.success(
        request,
        "Income record deleted successfully.",
    )

    return redirect("finance_records")


# =========================================================
# ADD FINANCE EXPENSE
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
def add_finance_expense(request):
    if request.method == "POST":
        form = FinanceExpenseForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Expense record added successfully.",
            )
            return redirect("finance_dashboard")
    else:
        form = FinanceExpenseForm(
            initial={
                "expense_date": timezone.localdate(),
            }
        )

    return render(
        request,
        "add_finance_expense.html",
        {
            "form": form,
        },
    )


# =========================================================
# DELETE FINANCE EXPENSE
# =========================================================

@user_passes_test(staff_required, login_url="staff_login")
@require_POST
def delete_finance_expense(request, pk):
    expense = get_object_or_404(
        FinanceExpense,
        pk=pk,
    )

    expense.delete()

    messages.success(
        request,
        "Expense record deleted successfully.",
    )

    return redirect("finance_records")


# =========================================================
# FINANCE RECORDS
# =========================================================

@user_passes_test(admin_or_staff_required, login_url="staff_login")
def finance_records(request):
    incomes = FinanceIncome.objects.all().order_by(
        "-payment_date",
        "-id",
    )

    expenses = FinanceExpense.objects.all().order_by(
        "-expense_date",
        "-id",
    )

    total_income = incomes.aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expenses = expenses.aggregate(
        total=Sum("amount")
    )["total"] or 0

    return render(
        request,
        "finance_records.html",
        {
            "incomes": incomes,
            "expenses": expenses,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "balance": total_income - total_expenses,
        },
    )
# =========================================================
# PUBLIC DEPARTMENTS PAGE
# =========================================================

def departments(request):
    department_list = Department.objects.filter(
        is_active=True
    ).order_by(
        "display_order",
        "name",
    )

    return render(
        request,
        "departments.html",
        {
            "departments": department_list,
        },
    )


# =========================================================
# ADMIN DEPARTMENT MANAGEMENT
# =========================================================

@user_passes_test(admin_required, login_url="admin_login")
def admin_departments(request):
    if request.method == "POST":
        action = request.POST.get("action")
        department_id = request.POST.get("department_id")

        # Toggle department visibility.
        if action == "toggle" and department_id:
            department = get_object_or_404(
                Department,
                pk=department_id,
            )

            department.is_active = not department.is_active
            department.save(update_fields=["is_active"])

            messages.success(
                request,
                "Department visibility updated successfully.",
            )

            return redirect("admin_departments")

        # Delete a department.
        if action == "delete" and department_id:
            department = get_object_or_404(
                Department,
                pk=department_id,
            )

            department.delete()

            messages.success(
                request,
                "Department deleted successfully.",
            )

            return redirect("admin_departments")

        # Create or update a department.
        edit_id = request.POST.get("edit_id")
        instance = (
            get_object_or_404(Department, pk=edit_id)
            if edit_id
            else None
        )

        form = DepartmentForm(
            request.POST,
            request.FILES,
            instance=instance,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Department saved successfully.",
            )

            return redirect("admin_departments")

    else:
        edit_id = request.GET.get("edit")
        instance = (
            get_object_or_404(Department, pk=edit_id)
            if edit_id
            else None
        )

        form = DepartmentForm(instance=instance)

    department_list = Department.objects.all().order_by(
        "display_order",
        "name",
    )

    return render(
        request,
        "admin_departments.html",
        {
            "form": form,
            "departments": department_list,
            "editing": instance is not None,
            "editing_department": instance,
        },
    )