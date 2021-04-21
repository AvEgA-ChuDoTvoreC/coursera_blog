import json

from django import forms
from django.http import HttpResponse, JsonResponse
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django.forms.models import model_to_dict

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .models import Item, Review
from .forms import GOODS_ADD_SCHEMA, GOODS_REVIEW_SCHEMA


# FIXME: There is some kinda problem which don't wanna read json response while using Django forms; BUT jsonschema - OK
#  CHECK this way:
#  1)
#  curl -v -H "Content-Type: application/json" -X POST -d
#  '{"title": "Сыр \"Российский\"", "description": "Очень вкусный сыр, да еще и российский.", "price": 100}'
#  http://127.0.0.1:8000/api/v1/goods/
#  2)
#  curl -v -H "Content-Type: application/json" -X POST -d
#  '{"text": "Best. Cheese. Ever.", "grade": 9}'
#  http://127.0.0.1:8000/api/v1/goods/1/reviews/
#  3)
#  curl -v -H "Content-Type: application/json" -X GET
#  http://127.0.0.1:8000/api/v1/goods/1/


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            validate(data, GOODS_ADD_SCHEMA)
            item = Item(title=data['title'],
                        description=data['description'],
                        price=data['price'])
            item.save()

            return JsonResponse({"id": item.id}, status=201)
        except ValueError:
            return JsonResponse({}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            item = Item.objects.get(id=item_id)
            data = json.loads(request.body)
            validate(data, GOODS_REVIEW_SCHEMA)
            review = Review(grade=data['grade'],
                            text=data['text'],
                            item=item)
            review.save()

            return JsonResponse({"id": review.id}, status=201)
        except ValueError:
            return JsonResponse({}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)
        except Item.DoesNotExist:
            return JsonResponse({}, status=404)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            print("info: ", item_id)
            item = Item.objects.prefetch_related('review_set').get(id=item_id)
            print("item_info: ", item)
        except Item.DoesNotExist:
            return JsonResponse(status=404, data={})
        data = model_to_dict(item)
        item_views = [model_to_dict(x) for x in item.review_set.all()]
        item_views = sorted(item_views, key=lambda review: review['id'], reverse=True)[:5]
        print("item_info: ", data, item_views)
        for review in item_views:
            review.pop('item', None)
        data['reviews'] = item_views
        return JsonResponse(data, status=200)


