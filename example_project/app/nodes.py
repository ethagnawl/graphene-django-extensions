from taggit.models import TaggedItem
import graphene

from example_project.app.filtersets import (
    ExampleFilterSet,
    ForwardManyToManyFilterSet,
    ForwardManyToOneFilterSet,
    ForwardOneToOneFilterSet,
    ReverseManyToManyFilterSet,
    ReverseOneToManyFilterSet,
    ReverseOneToOneFilterSet,
)
from example_project.app.models import (
    Example,
    ForwardManyToMany,
    ForwardManyToOne,
    ForwardOneToOne,
    ReverseManyToMany,
    ReverseOneToMany,
    ReverseOneToOne,
)
from graphene_django_extensions import DjangoNode
from graphene_django_extensions.permissions import AllowAuthenticated


class ForwardOneToOneNode(DjangoNode):
    class Meta:
        model = ForwardOneToOne
        fields = [
            "pk",
            "name",
            "example_rel",
        ]
        permission_classes = [AllowAuthenticated]
        filterset_class = ForwardOneToOneFilterSet


class ForwardManyToOneNode(DjangoNode):
    class Meta:
        model = ForwardManyToOne
        fields = [
            "pk",
            "name",
            "example_rels",
        ]
        permission_classes = [AllowAuthenticated]
        filterset_class = ForwardManyToOneFilterSet


class ForwardManyToManyNode(DjangoNode):
    class Meta:
        model = ForwardManyToMany
        fields = [
            "pk",
            "name",
            "example_rels",
        ]
        permission_classes = [AllowAuthenticated]
        filterset_class = ForwardManyToManyFilterSet


class ReverseOneToOneNode(DjangoNode):
    class Meta:
        model = ReverseOneToOne
        fields = [
            "pk",
            "name",
            "example_field",
        ]
        permission_classes = [AllowAuthenticated]
        filterset_class = ReverseOneToOneFilterSet


class ReverseOneToManyNode(DjangoNode):
    class Meta:
        model = ReverseOneToMany
        fields = [
            "pk",
            "name",
            "example_field",
        ]
        permission_classes = [AllowAuthenticated]
        filterset_class = ReverseOneToManyFilterSet


class ReverseManyToManyNode(DjangoNode):
    class Meta:
        model = ReverseManyToMany
        fields = [
            "pk",
            "name",
            "example_fields",
        ]
        permission_classes = [AllowAny]
        filterset_class = ReverseManyToManyFilterSet


class TaggedItemNode(graphene.ObjectType):
    class Meta:
        model = TaggedItem
        fields = ["name"]

    name = graphene.String()


class ExampleNode(DjangoNode):
    forward_one_to_one_field = ForwardOneToOneNode.RelatedField()
    forward_many_to_one_field = ForwardManyToOneNode.RelatedField()
    forward_many_to_many_fields = ForwardManyToManyNode.ListField()
    reverse_one_to_one_rel = ReverseOneToOneNode.RelatedField()
    reverse_one_to_many_rels = ReverseOneToManyNode.ListField()
    reverse_many_to_many_rels = ReverseManyToManyNode.Connection()
    tagged_items = graphene.List(TaggedItemNode)

    def resolve_tagged_items(self, *args, **kwargs):
        return [TaggedItemNode(x) for x in self.tags.all()]

    class Meta:
        model = Example
        fields = [
            "duration",
            "email",
            "example_state",
            "forward_many_to_many_fields",
            "forward_many_to_one_field",
            "forward_one_to_one_field",
            "name",
            "number",
            "pk",
            "reverse_many_to_many_rels",
            "reverse_one_to_many_rels",
            "reverse_one_to_one_rel",
            "tagged_items",
        ]
        permission_classes = [AllowAuthenticated]
        restricted_fields = {
            "email": lambda user: user.is_superuser,
        }
        filterset_class = ExampleFilterSet
