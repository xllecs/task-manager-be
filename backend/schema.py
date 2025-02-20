import graphene
from graphene_django import DjangoObjectType
from backend_app.models import Task

class TaskType(DjangoObjectType):
  class Meta:
    model = Task
    fields = '__all__'

class Query(graphene.ObjectType):
  tasks = graphene.List(TaskType, status=graphene.String(required=True))

  def resolve_tasks(self, root, status):
    return Task.objects.filter(status=status)

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

class Mutation(graphene.ObjectType):
  update_status = UpdateStatus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
