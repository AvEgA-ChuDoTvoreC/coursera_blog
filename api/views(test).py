import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from marshmallow import Schema, ValidationError, fields, post_load
from marshmallow.validate import Length, Range

from .models import Item, Review


class ItemSchema(Schema):
    """Django схема валидации товара"""

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(1, 64))
    description = fields.Str(required=True, validate=Length(1, 1024))
    price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)

    @post_load
    def make(self, data):
        return Item(**data)


class ReviewSchema(Schema):
    """Django схема валидации отзыва"""

    id = fields.Int(dump_only=True)
    grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
    text = fields.Str(required=True, validate=Length(1, 1024))

    @post_load
    def make(self, data):
        return Review(**data)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
            item = schema.load(document).data
            item.save()
        except (json.JSONDecodeError, ValidationError, AssertionError):
            return HttpResponse(status=400)
        data = {'id': item.pk}
        return JsonResponse(data, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            review = schema.load(document).data
            review.item = item
            review.save()
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        except (json.JSONDecodeError, ValidationError):
            return HttpResponse(status=400)
        data = {'id': review.pk}
        return JsonResponse(data, status=201)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5 штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
        schema = ItemSchema()
        data = schema.dump(item).data
        query = Review.objects.filter(item=item).order_by('-id')
        reviews = query[:5]
        schema = ReviewSchema(many=True)
        data['reviews'] = schema.dump(reviews).data
        return JsonResponse(data, status=200)

