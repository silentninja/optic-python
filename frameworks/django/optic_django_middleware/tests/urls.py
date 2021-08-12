# -*- coding: utf-8
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from test_app.views import form_view, json_view, view1, view2

urlpatterns = [
    url(r"^url-1$", view1, name="view-1"),
    url(r"^url-2$", view2, name="view-2"),
    url(r"^json-url-3$", json_view, name="view-3"),
    url(r"^form-url$", form_view, name="form-view"),
]
