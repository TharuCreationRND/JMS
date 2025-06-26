from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Finished', 'Finished'),
        ('Rejected', 'Rejected'),
        ('Purchase', 'Item in Purchase'),
    ]

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_jobs')  # who entered job

    job_date = models.DateField()  # Mandatory
    center = models.CharField(max_length=100)  # Mandatory
    area_manager = models.CharField(max_length=100)  # Mandatory
    area_manager_email = models.EmailField()  # Mandatory
    job_number = models.CharField(max_length=50, unique=True)  # Mandatory
    item_type = models.CharField(max_length=100)  # Mandatory
    request_by = models.CharField(max_length=100)  # Mandatory
    requester_designation = models.CharField(max_length=100)  # Mandatory
    job_assignee = models.CharField(max_length=100)  # Mandatory

    center_sent_date = models.DateField(null=True, blank=True)  # Optional
    head_office_receive_date = models.DateField(null=True, blank=True)  # Optional
    serial_number = models.CharField(max_length=100)  # Mandatory
    pronto_no_receive = models.CharField(max_length=100, null=True, blank=True)  # Optional
    pronto_no_sent = models.CharField(max_length=100, null=True, blank=True)  # Optional
    head_office_sent_date = models.DateField(null=True, blank=True)  # Optional
    center_receive_date = models.DateField(null=True, blank=True)  # Optional
    finish_date = models.DateField(null=True, blank=True)  # Optional

    status = models.CharField(max_length=20, choices=STATUS_CHOICES)  # Mandatory
    remark = models.TextField()  # Mandatory (removed blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_number} - {self.center}"


class Breakdown(models.Model):
    center = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=50)
    job_number = models.CharField(max_length=50)
    issue = models.TextField()
    job_assignee = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='breakdowns',
        null=True,    # allow null for now
        blank=True,
        editable=False
)


    def __str__(self):
        return f"{self.center} - {self.issue[:30]}"

class Borrow(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Returned', 'Item has returned'),
    ]
    date = models.DateField()
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    item_type = models.CharField(max_length=50)
    days = models.PositiveIntegerField()
    email = models.EmailField()
    hod_email = models.EmailField(blank=True, null=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    handover_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrows')
    reason = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.item_type} ({self.date})"


class BackupPlan(models.Model):
    PC_TYPE_CHOICES = [
    ('Desktop', 'Desktop'),
    ('Mini PC', 'Mini PC'),
    ('HP', 'HP'),
    ('Eswis', 'Eswis'),
    ]
    date = models.DateField()
    center_name = models.CharField(max_length=100)
    details_given_by = models.CharField(max_length=100)
    area_manager = models.CharField(max_length=100)

    testing_lane_1_pc = models.CharField(max_length=20, choices=PC_TYPE_CHOICES, null=True, blank=True)
    testing_lane_1_monitor = models.BooleanField(default=False)

    testing_lane_2_pc = models.CharField(max_length=20, choices=PC_TYPE_CHOICES, null=True, blank=True)
    testing_lane_2_monitor = models.BooleanField(default=False)

    testing_lane_3_pc = models.CharField(max_length=20, choices=PC_TYPE_CHOICES, null=True, blank=True)
    testing_lane_3_monitor = models.BooleanField(default=False)

    registration_lane_pc = models.CharField(max_length=20, choices=PC_TYPE_CHOICES, null=True, blank=True)
    registration_lane_monitor = models.BooleanField(default=False)

    certificate_lane_pc = models.CharField(max_length=20, choices=PC_TYPE_CHOICES, null=True, blank=True)
    certificate_lane_monitor = models.BooleanField(default=False)

    backup_pc = models.CharField(max_length=20, choices=PC_TYPE_CHOICES, null=True, blank=True)
    backup_monitor = models.BooleanField(default=False)

    fingerprint_machines = models.PositiveIntegerField(default=0)
    backup_fingerprint_machines = models.PositiveIntegerField(default=0)

    ups = models.PositiveIntegerField(default=0)
    backup_ups = models.PositiveIntegerField(default=0)

    wingles = models.PositiveIntegerField(default=0)
    backup_wingles = models.PositiveIntegerField(default=0)

    dongles = models.PositiveIntegerField(default=0)
    backup_dongles = models.PositiveIntegerField(default=0)

    octopuses = models.PositiveIntegerField(default=0)
    backup_octopuses = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def pc_count(self, pc_field_value):
        return 1 if pc_field_value and pc_field_value.strip() else 0


    # Property to get total PCs count
    @property
    def total_pc(self):
        return (
            self.pc_count(self.testing_lane_1_pc) +
            self.pc_count(self.testing_lane_2_pc) +
            self.pc_count(self.testing_lane_3_pc) +
            self.pc_count(self.registration_lane_pc) +
            self.pc_count(self.certificate_lane_pc) +
            self.pc_count(self.backup_pc)
        )

    # Property to get total monitors count
    @property
    def total_monitors(self):
        return sum([
            int(self.testing_lane_1_monitor),
            int(self.testing_lane_2_monitor),
            int(self.testing_lane_3_monitor),
            int(self.registration_lane_monitor),
            int(self.certificate_lane_monitor),
            int(self.backup_monitor),
        ])

