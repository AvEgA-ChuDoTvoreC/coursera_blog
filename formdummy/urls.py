from django.conf.urls import url

from .views import FormDummyView, JsonSchemaView, MarshmallowView
# from template.views import echo, filters, extend


# .as_view() because FormDummyView is a class
urlpatterns = [
    url(r'^form/$', FormDummyView.as_view()),
    url(r'^json/$', JsonSchemaView.as_view()),
    url(r'^marsh/$', MarshmallowView.as_view()),
]
