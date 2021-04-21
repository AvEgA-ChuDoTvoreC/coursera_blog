import json

from django.http import HttpResponse, JsonResponse
from django.views import View

from marshmallow import Schema, ValidationError, fields, post_load
from marshmallow.validate import Length, Range

from .models import Item, Review


class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=Length(1, 64))
    description = fields.Str(required=True, validate=Length(1, 1024))
    price = fields.Int(required=True, validate=Range(1, 1000000), strict=True)

    @post_load
    def make(self, data):
        return Item(**data)


class ReviewSchema(Schema):
    id = fields.Int(dump_only=True)
    grade = fields.Int(required=True, validate=Range(1, 10), strict=True)
    text = fields.Str(required=True, validate=Length(1, 1024))

    @post_load
    def make(self, data):
        return Review(**data)


class AddItemView(View):
    """View РґР»СЏ СЃРѕР·РґР°РЅРёСЏ С‚РѕРІР°СЂР°."""

    def post(self, request):

        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
            item = schema.load(document).data
            item.save()
        except (json.JSONDecodeError, ValidationError):
            return HttpResponse(status=400)

        return JsonResponse({'id': item.pk}, status=201)


class PostReviewView(View):
    """View РґР»СЏ СЃРѕР·РґР°РЅРёСЏ РѕС‚Р·С‹РІР° Рѕ С‚РѕРІР°СЂРµ."""

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

        return JsonResponse({'id': review.pk}, status=201)


class GetItemView(View):
    """View РґР»СЏ РїРѕР»СѓС‡РµРЅРёСЏ РёРЅС„РѕСЂРјР°С†РёРё Рѕ С‚РѕРІР°СЂРµ.

    РџРѕРјРёРјРѕ РѕСЃРЅРѕРІРЅРѕР№ РёРЅС„РѕСЂРјР°С†РёРё РІС‹РґР°РµС‚ РїРѕСЃР»РµРґРЅРёРµ РѕС‚Р·С‹РІС‹ Рѕ С‚РѕРІР°СЂРµ, РЅРµ Р±РѕР»РµРµ 5
    С€С‚СѓРє.
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