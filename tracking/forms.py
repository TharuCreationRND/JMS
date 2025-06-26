from django import forms
from .models import Job
from .models import Breakdown
from django.core.exceptions import ValidationError
from .models import Borrow
from .models import BackupPlan

INPUT_CLASSES = "w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400 focus:border-transparent"

INPUT_STYLE = "w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-green-500 focus:outline-none"

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['created_by']
        widgets = {
            'job_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'center': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'area_manager': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'area_manager_email': forms.EmailInput(attrs={'class': INPUT_STYLE}),
            'job_number': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'item_type': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'request_by': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'requester_designation': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'job_assignee': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'center_sent_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'head_office_receive_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'serial_number': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'pronto_no_receive': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'pronto_no_sent': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'head_office_sent_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'center_receive_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'finish_date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'status': forms.Select(attrs={'class': INPUT_STYLE}),
            'remark': forms.Textarea(attrs={'class': INPUT_STYLE, 'rows': 3}),
        }

def __init__(self, *args, **kwargs):
        super(JobForm, self).__init__(*args, **kwargs)

        # Optional fields
        optional_fields = [
            'center_sent_date',
            'head_office_receive_date',
            'pronto_no_receive',
            'pronto_no_sent',
            'head_office_sent_date',
            'center_receive_date',
            'finish_date',
        ]

        for field in optional_fields:
            self.fields[field].required = False

        # Make sure "remark" is mandatory
        self.fields['remark'].required = True
        

class BreakdownForm(forms.ModelForm):
    class Meta:
        model = Breakdown
        fields = ['center', 'date', 'time', 'duration', 'job_number', 'issue', 'job_assignee', 'comment']
        widgets = {
            'center': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': INPUT_STYLE}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': INPUT_STYLE}),
            'duration': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'job_number': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'issue': forms.Textarea(attrs={'class': INPUT_STYLE, 'rows': 3}),
            'job_assignee': forms.TextInput(attrs={'class': INPUT_STYLE}),
            'comment': forms.Textarea(attrs={'class': INPUT_STYLE, 'rows': 3}),
        }


ITEM_TYPE_CHOICES = [
    ('Mobile', 'Mobile'),
    ('Projector', 'Projector'),

]

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Returned', 'Item has returned'),
]

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        exclude = ['created_by']
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-3 py-2 w-full'}),
            'name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'designation': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'department': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'item_type': forms.Select(choices=ITEM_TYPE_CHOICES, attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'days': forms.NumberInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'hod_email': forms.EmailInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),  # Add this!
            'status': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'handover_date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-3 py-2 w-full'}),
            'reason': forms.Textarea(attrs={'class': 'border rounded px-3 py-2 w-full', 'rows': 3}),
        }


from django import forms
from .models import BackupPlan

class BackupPlanForm(forms.ModelForm):
    class Meta:
        model = BackupPlan
        exclude = ['created_by'] 
        fields = '__all__'  # or list the specific fields you want in the form
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-3 py-2 w-full'}),
        }
