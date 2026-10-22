from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.user_login, name="user_login"),
    path("home/", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin-manage/staff/", views.admin_staff, name="admin_staff"),
    path("admin-manage/doctors/", views.admin_doctors, name="admin_doctors"),
    path("admin-manage/gallery/", views.admin_gallery_media, name="admin_gallery_media"),
    path("admin-manage/feedback/", views.admin_feedback, name="admin_feedback"),
    path("admin-register/",views.admin_register,name="admin_register"),
    path("admin-login/",views.admin_login,name="admin_login"),
    path("admin-logout/",views.admin_logout,name="admin_logout"),
    path("admin-manage/appointments/<int:appointment_id>/edit/",views.admin_edit_appointment,name="admin_edit_appointment"),
    path("admin-manage/appointments/<int:appointment_id>/delete/",views.admin_delete_appointment,name="admin_delete_appointment"),
    path("appointments/", views.my_appointments, name="my_appointments"),
    path("appointment/", views.appoint, name="appoint"),
    path("logout/", views.user_logout, name="user_logout"),
    path("register/", views.register, name="register"),
    path("contact/", views.call, name="call"),
    path("about/", views.about, name="about"),
    path("services/", views.depart, name="depart"),
    path("gallery/", views.gallery, name="gallery"),
    path("feedback/submit/", views.submit_feedback, name="submit_feedback"),
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/patients/add/",views.add_patient,name="add_patient"),
    path("staff/appointments/", views.staff_appointments, name="staff_appointments"),
    path("staff/appointments/add/", views.staff_add_appointment, name="staff_add_appointment"),
    path("staff/messages/", views.staff_messages, name="staff_messages"),
    path("staff-login/", views.staff_login, name="staff_login"),
    path("staff/logout/",views.staff_logout,name="staff_logout"),
    path("appointment/<int:appointment_id>/confirm/",views.confirm_appointment,name="confirm_appointment"),
    path("appointment/<int:appointment_id>/cancel/",views.cancel_appointment,name="cancel_appointment"),
    path("appointment/<int:appointment_id>/complete/",views.complete_appointment,name="complete_appointment"),
    path("staff/patients/", views.patient_records, name="patient_records"),
    path("staff/patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("staff/patients/<int:pk>/edit/", views.edit_patient, name="edit_patient"),
    path("staff/patients/<int:pk>/delete/",views.delete_patient,name="delete_patient"),
    path("staff/finance/",views.finance_dashboard,name="finance_dashboard"),
    path("staff/finance/income/add/",views.add_finance_income,name="add_finance_income"),
    path("staff/finance/expense/add/",views.add_finance_expense,name="add_finance_expense"),
    path("staff/finance/income/<int:pk>/edit/",views.edit_finance_income,name="edit_finance_income"),
    path("staff/finance/income/<int:pk>/delete/",views.delete_finance_income,name="delete_finance_income"),
    path("staff/finance/expense/<int:pk>/delete/",views.delete_finance_expense,name="delete_finance_expense"),
    path("staff/finance/records/",views.finance_records,name="finance_records",),
    path("departments/",views.departments,name="departments"),
    path("admin-dashboard/departments/",views.admin_departments,name="admin_departments"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
