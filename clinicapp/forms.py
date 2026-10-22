from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import GalleryMedia, Feedback, Doctor
from django.core.validators import RegexValidator
from django.utils import timezone
from .models import Appointment, Contact, Doctor,Patient,FinanceIncome,FinanceExpense,StaffProfile,Department

phone_validator = RegexValidator(r"^[6-9]\d{9}$", "Enter a valid 10-digit Indian mobile number.")


class AppointmentForm(forms.ModelForm):
    phone = forms.CharField(max_length=10, validators=[phone_validator], widget=forms.TextInput(attrs={"inputmode": "numeric", "maxlength": "10", "placeholder": "10-digit mobile number"}))
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Appointment
        fields = ["name", "age", "gender", "place", "phone", "email", "service", "doctor", "appointment_date", "appointment_time", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "age": forms.NumberInput(attrs={"min": 1, "max": 120, "placeholder": "Age"}),
            "place": forms.TextInput(attrs={"placeholder": "Place"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email (optional)"}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Any additional information (optional)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = Doctor.objects.filter(active=True)
        self.fields["doctor"].required = False
        self.fields["doctor"].empty_label = "Any available doctor"
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"

    def clean_age(self):
        age = self.cleaned_data["age"]
        if not 1 <= age <= 120:
            raise forms.ValidationError("Age must be between 1 and 120.")
        return age

    def clean_appointment_date(self):
        date = self.cleaned_data["appointment_date"]
        if date < timezone.localdate():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return date


class ContactForm(forms.ModelForm):
    phone = forms.CharField(max_length=10, validators=[phone_validator], widget=forms.TextInput(attrs={"inputmode": "numeric", "maxlength": "10", "placeholder": "10-digit mobile number"}))

    class Meta:
        model = Contact
        fields = ["name", "age", "gender", "place", "phone", "email", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "age": forms.NumberInput(attrs={"min": 1, "max": 120, "placeholder": "Age (optional)"}),
            "place": forms.TextInput(attrs={"placeholder": "Place"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "How can we help you?"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"

    def clean_age(self):
        age = self.cleaned_data.get("age")
        if age is not None and not 1 <= age <= 120:
            raise forms.ValidationError("Age must be between 1 and 120.")
        return age

class PatientForm(forms.ModelForm):
    phone = forms.CharField(max_length=10,validators=[phone_validator],
                            widget=forms.TextInput(attrs={
                                                            "inputmode": "numeric",
                                                            "maxlength": "10",
                                                            "placeholder": "10-digit mobile number"
                                                        }
                                                    )
                            )

    class Meta:
        model = Patient
        fields = ["name", "age", "gender", "date", "place", "phone"]

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Full name"}
            ),
            "age": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 120,
                    "placeholder": "Age"
                }
            ),
            "date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
            "place": forms.TextInput(
                attrs={"placeholder": "Place"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = (
                "form-select"
                if isinstance(field.widget, forms.Select)
                else "form-control"
            )

    def clean_age(self):
        age = self.cleaned_data["age"]

        if not 1 <= age <= 120:
            raise forms.ValidationError("Age must be between 1 and 120.")

        return age

class FinanceIncomeForm(forms.ModelForm):

    class Meta:
        model = FinanceIncome

        fields = [
            "payment_date",
            "op_no",
            "patient_name",
            "age",
            "gender",
            "doctor_name",
            "phone",
            "procedure",
            "amount",
            "payment_method",
            "notes",
        ]

        widgets = {

            "payment_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "op_no": forms.TextInput(
                attrs={
                    "placeholder": "OP-0001"
                }
            ),

            "patient_name": forms.TextInput(
                attrs={
                    "placeholder": "Patient name"
                }
            ),

            "age": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 120,
                    "placeholder": "Age"
                }
            ),

            "doctor_name": forms.TextInput(
                attrs={
                    "placeholder": "Doctor name"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "maxlength": "10",
                    "placeholder": "10-digit mobile number"
                }
            ),

            "procedure": forms.TextInput(
                attrs={
                    "placeholder": "Procedure / Treatment"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Amount"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Additional notes (optional)"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            **kwargs
        )

        for field in self.fields.values():

            field.widget.attrs["class"] = (
                "form-select"
                if isinstance(
                    field.widget,
                    forms.Select
                )
                else "form-control"
            )
class FinanceExpenseForm(forms.ModelForm):

    class Meta:
        model = FinanceExpense

        fields = [
            "expense_date",
            "description",
            "amount",
            "notes",
        ]

        widgets = {
            "expense_date": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "description": forms.TextInput(
                attrs={
                    "placeholder": "Expense description"
                }
            ),

            "amount": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "Amount"
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Additional notes (optional)"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs["class"] = (
                "form-select"
                if isinstance(
                    field.widget,
                    forms.Select
                )
                else "form-control"
            )

class StaffAppointmentForm(AppointmentForm):
    """Appointment form for staff-entered walk-in patients."""
    class Meta(AppointmentForm.Meta):
        fields = ["name", "age", "gender", "place", "phone", "email", "service", "doctor", "appointment_date", "appointment_time", "message"]


class GalleryMediaForm(forms.ModelForm):
    class Meta:
        model = GalleryMedia
        fields = ["title", "description", "image", "video", "is_published"]
        widgets = {"description": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) or isinstance(field.widget, forms.CheckboxInput) else "form-control"

    def clean(self):
        cleaned = super().clean()
        image = cleaned.get("image") or getattr(self.instance, "image", None)
        video = cleaned.get("video") or getattr(self.instance, "video", None)
        if bool(image) == bool(video):
            raise forms.ValidationError("Choose exactly one file: either an image or a video.")
        upload = cleaned.get("video")
        if upload and upload.name:
            allowed = (".mp4", ".webm", ".ogg", ".mov", ".m4v")
            if not upload.name.lower().endswith(allowed):
                self.add_error("video", "Use an MP4, WebM, OGG, MOV or M4V video file.")
        return cleaned


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "rating", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "message": forms.Textarea(attrs={"rows": 3, "placeholder": "Share your experience (please do not include private medical details)"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"


class StaffCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_staff = True
        user.is_superuser = False
        if commit:
            user.save()
        return user


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ["name", "designation", "qualification", "bio", "photo", "image", "display_order", "active"]
        widgets = {"bio": forms.Textarea(attrs={"rows": 3}), "image": forms.TextInput(attrs={"placeholder": "Fallback image filename, e.g. doctor.png"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(field.widget, forms.Select) else "form-control"
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ["photo"]
        labels = {
            "photo": "Staff Photo",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs.update({
            "class": "form-control",
            "accept": "image/*",
        })


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department

        fields = [
            "name",
            "short_description",
            "description",
            "image",
            "is_active",
        ]

        labels = {
            "name": "Department Name",
            "short_description": "Short Description",
            "description": "Department Description",
            "image": "Choose Department Image",
            "is_active": "Show on Website",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. General Dentistry",
                }
            ),
            "short_description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter a short description",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Describe this department (optional)",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
