from django.urls import path
from website.views.badge import issue_badge

urlpatterns = [
    path('repos/<str:repo_name>/issues/<int:issue_number>/badge/', issue_badge, name='issue_badge'),
]