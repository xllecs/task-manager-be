from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
  TASK_STATUS = [
    ('TO_DO', 'To Do'),
    ('IN_PROGRESS', 'In Progress'),
    ('DONE', 'Done'),
  ]

  TASK_PRIORITY = [
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High'),
  ]

  @staticmethod
  def get_default_user():
    return User.objects.get(id=3).id

  title = models.CharField(max_length=200)
  description = models.TextField()
  status = models.CharField(max_length=20, choices=TASK_STATUS, default='TO_DO', blank=False)
  reporter = models.ForeignKey(User, on_delete=models.CASCADE, null=False, default=get_default_user(), related_name='reporter_tasks')
  assignee = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='assignee_tasks')
  priority = models.CharField(max_length=20, choices=TASK_PRIORITY, default='LOW', blank=False)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  def __str__(self):
    return self.title

  class Meta:
    db_table = 'tm_task'

class Label(models.Model):
  tag = models.CharField(max_length=20)
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='labels')

  def __str__(self):
    return self.tag
  class Meta:
    db_table = 'tm_label'
