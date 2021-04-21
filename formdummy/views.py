import json

from django.shortcuts import render
from django.views import View

# JSONschema validation
from django.http import JsonResponse
from jsonschema import validate
from jsonschema.exceptions import ValidationError

# MARSHMALLOW vaidation
from marshmallow import ValidationError as MarshValidationError

# pass csrf constraints
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# DJANGO forms validation + other
from .forms import DummyForm
from .json_shemas import REVIEW_SCHEMA
from .marsh_shemas import MarshReviewSchema

# LOGIN
from django.contrib.auth.mixins import LoginRequiredMixin


@method_decorator(csrf_exempt, name='dispatch')
class FormDummyView(LoginRequiredMixin, View):

    def get(self, request):
        form = DummyForm()
        return render(request, 'formdummy/form.html', {'form': form})

    def post(self, request):
        form = DummyForm(request.POST, request.FILES)
        if form.is_valid():
            context = form.cleaned_data
            print(context)
            return render(request, 'formdummy/form.html', context=context)
        else:
            return render(request, 'formdummy/error.html', context={'error': form.errors})


@method_decorator(csrf_exempt, name='dispatch')
class JsonSchemaView(View):

    def post(self, request):
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA)
            return JsonResponse(document, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MarshmallowView(View):

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = MarshReviewSchema()
            data = schema.load(document)

            return JsonResponse(data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except MarshValidationError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)











# class FormDummyView22(View):
#
#     # TODO: information content
#     def get22(self, request):
#         form = DummyForm()
#         # from pdb import set_trace
#         # set_trace()
#         return render(request, 'formdummy/form.html', {'form': form})
#
#     def post22(self, request):
#         text = request.POST.get('text')
#         grade = request.POST.get('grade')
#         image = request.FILES.get('image')
#         image_content = image.read()
#         context = {
#             'text': text,
#             'grade': grade,
#             'content': image_content
#         }
#         # from pdb import set_trace
#         # set_trace()
#
#         return render(request, 'formdummy/form.html', context=context)

