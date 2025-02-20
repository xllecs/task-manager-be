from django.db import models

# Create your models here.
class Task(models.Model):
  TASK_STATUS = [
    ('to-do', 'To Do'),
    ('in-progress', 'In Progress'),
    ('done', 'Done'),
  ]

  title = models.CharField(max_length=200)
  description = models.TextField()
  status = models.CharField(max_length=20, choices=TASK_STATUS, default='To Do')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now=True)

  class Meta:
    db_table = 'tm_task'
