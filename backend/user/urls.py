from django.urls import path
from user.views import (api_update_userprofile_view, api_detail_userprofile_view, api_delete_userprofile_view)

app_name = 'user'

urlpatterns = [
    path('userprofile/<int:userprofile_id>/', api_detail_userprofile_view, name='userprofile_detail'),
    path('userprofile/update/<int:userprofile_id>/', api_update_userprofile_view, name='userprofile_update'),
    path('userprofile/delete/<int:userprofile_id>/', api_delete_userprofile_view, name='userprofile_delete')
]