from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=32, blank=True)

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SiteSetting(TimeStampedModel):
    key = models.CharField(max_length=64, unique=True)
    value = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.key

class Banner(TimeStampedModel):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to='banners/', blank=True, null=True)
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.title

class MenuItem(TimeStampedModel):
    label = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.label

class StaffProfile(TimeStampedModel):
    ROLE_CHOICES = [
        ('manager','Manager'),
        ('support','Support'),
        ('fulfillment','Fulfillment'),
        ('marketing','Marketing'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=32, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=32, blank=True)
    def __str__(self):
        return f'{self.user.username} ({self.role})'

class Notification(TimeStampedModel):
    LEVELS = [('info','Info'), ('warn','Warn'), ('error','Error')]
    level = models.CharField(max_length=8, choices=LEVELS, default='info')
    message = models.CharField(max_length=240)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return f'[{self.level}] {self.message[:30]}'

class AuditLog(TimeStampedModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=64)
    model = models.CharField(max_length=64)
    object_id = models.CharField(max_length=64)
    meta = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return f'{self.action} {self.model}:{self.object_id}'

class Announcement(TimeStampedModel):
    title = models.CharField(max_length=160)
    body = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title

class AdminTask(TimeStampedModel):
    STATUS = [('todo','To Do'), ('doing','Doing'), ('done','Done')]
    title = models.CharField(max_length=160)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='admin_tasks')
    status = models.CharField(max_length=16, choices=STATUS, default='todo')
    due_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    def __str__(self):
        return self.title

class QuickLink(TimeStampedModel):
    label = models.CharField(max_length=64)
    url = models.CharField(max_length=256)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['order']
    def __str__(self):
        return self.label

class SavedReport(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    params = models.JSONField(default=dict, blank=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.name

class ScheduledExport(TimeStampedModel):
    FORMAT = [('csv','CSV'), ('xlsx','XLSX'), ('json','JSON')]
    name = models.CharField(max_length=120, unique=True)
    format = models.CharField(max_length=8, choices=FORMAT, default='csv')
    params = models.JSONField(default=dict, blank=True)
    cron = models.CharField(max_length=64, help_text='* * * * *')
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class AdminNote(TimeStampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=160)
    body = models.TextField()
    pinned = models.BooleanField(default=False)
    def __str__(self):
        return self.title