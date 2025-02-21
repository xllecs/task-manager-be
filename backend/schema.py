import graphene
from graphene_django import DjangoObjectType
from backend_app.models import Task, Label
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
  class Meta:
    model = User
    fields = '__all__'

class TaskType(DjangoObjectType):
  class Meta:
    model = Task
    fields = '__all__'

  assignee = graphene.Field(UserType)
  reporter = graphene.Field(UserType)

class LabelType(DjangoObjectType):
  class Meta:
    model = Label
    fields = '__all__'

class Query(graphene.ObjectType):
  tasks = graphene.List(TaskType, status=graphene.String(required=True))
  labels = graphene.List(LabelType)

  def resolve_tasks(self, root, status):
    return Task.objects.filter(status=status)
  
  def resolve_labels(self, root):
    return Label.objects.all()

class UpdateStatus(graphene.Mutation):
  class Arguments:
    task_id = graphene.ID(required=True)
    new_status = graphene.String(required=True)

  task = graphene.Field(lambda: TaskType)

  def mutate(root, info, task_id, new_status):
    task = Task.objects.get(id=task_id)
    task.status = new_status
    task.save()

    return UpdateStatus(task=task)

class UpdatePriority(graphene.Mutation):
  class Arguments:
    task_id = graphene.ID(required=True)
    new_priority = graphene.String(required=True)

  task = graphene.Field(lambda: TaskType)

  def mutate(root, info, task_id, new_priority):
    task = Task.objects.get(id=task_id)
    task.priority = new_priority
    task.save()

    return UpdatePriority(task=task)

class Mutation(graphene.ObjectType):
  update_status = UpdateStatus.Field()
  update_priority = UpdatePriority.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
