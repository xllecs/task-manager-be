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
  users = graphene.List(UserType)

  def resolve_tasks(self, root, status):
    return Task.objects.filter(status=status)
  
  def resolve_labels(self, root):
    return Label.objects.all()
  
  def resolve_users(self, root):
    return User.objects.all()
  
class CreateTask(graphene.Mutation):
  class Arguments:
    title = graphene.String(required=True)
    description = graphene.String()
    status = graphene.String(required=True)
    priority = graphene.String(required=True)

  task = graphene.Field(lambda: TaskType)

  def mutate(root, info, title, description, status, priority):
    task = Task(title=title, description=description, status=status, priority=priority)
    task.save()

    return CreateTask(task=task)
  
class UpdateTask(graphene.Mutation):
  class Arguments:
    task_id = graphene.ID()
    title = graphene.String()
    description = graphene.String()

  task = graphene.Field(lambda: TaskType)

  def mutate(root, info, task_id, title=None, description=None):
    task = Task.objects.get(id=task_id)

    if title:
      task.title = title

    if description:
      task.description = description

    task.save()

    return UpdateTask(task=task)

class SelectAssignee(graphene.Mutation):
  class Arguments:
    task_id = graphene.ID(required=True)
    user_id = graphene.ID(required=True)
    
  task = graphene.Field(lambda: TaskType)

  def mutate(root, info, task_id, user_id):
    task = Task.objects.get(id=task_id)
    user = User.objects.get(id=user_id)

    task.assignee = user
    task.save()

    return SelectAssignee(task=task)

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
  create_task = CreateTask.Field()
  update_task = UpdateTask.Field()
  select_assignee = SelectAssignee.Field()
  update_status = UpdateStatus.Field()
  update_priority = UpdatePriority.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
