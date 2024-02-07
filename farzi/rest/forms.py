from accounts import forms
from django import forms
from .models import Appointment
from accounts.models import CustomUser
from datetime import date, timedelta

class BootstrapTextInput(forms.TextInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().init(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for select fields
class BootstrapSelect(forms.Select):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().init(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg datepicker"
        super().init(*args, **kwargs)
from django import forms
from datetime import date, timedelta  # Import the date module from datetime
tomorrow = date.today() + timedelta(days=1)
class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',
                'id': 'date',
                'name': 'date',
                'class': 'form-control form-control-lg date-picker',
                'type': 'date', 'min': tomorrow.strftime('%Y-%m-%d')
                # 'min': date.today().strftime('%Y-%m-%d')  # Set the minimum date to today
            }
        )
    )
    def init(self, *args, **kwargs):
        therapist_leave_dates = kwargs.pop('therapist_leave_dates', [])
        super().init(*args, **kwargs)
        self.fields['date'].widget.attrs['data-therapist-leave-dates'] = ','.join(therapist_leave_dates)

    # def init(self, *args, **kwargs):
    #     super().init(*args, **kwargs)


        

    class Meta:
        model = Appointment
        fields = ['date','time_slot','mobile','location','order_id','desc']
        widgets = {
            'time_slot': BootstrapSelect(attrs={'placeholder': 'Select State', 'id': 'time_slot'}),
            'date': forms.TextInput(attrs={'class': 'custom-input'}),
            'mobile': forms.TextInput(attrs={'class': 'custom-input'}),
            'location': forms.TextInput(attrs={'class': 'custom-input'}),
            'order_id': forms.TextInput(attrs={'class': 'custom-input'}),
            'desc': forms.Textarea(attrs={'class': 'custom-textarea'}),
        }
        labels = {
        'date': 'Date Label',
        'time_slot': 'Time Slot Label',
        'mobile': 'Mobile Label',
        'location': 'Location Label',
        'order_id': ' ID Label',
        'desc': 'Description Label',
        }