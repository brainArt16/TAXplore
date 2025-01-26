from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, AnalysisView, ChatView, DeploymentView, KnowledgeView

app_name = "portal"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("analysis/<int:pk>/", AnalysisView.as_view(), name="analysis"),
    path("chat/<int:pk>/", ChatView.as_view(), name="chat"),
    path("deployment/<int:pk>/", DeploymentView.as_view(), name="deployment"),
    path("knowledge/<int:pk>/", KnowledgeView.as_view(), name="knowledge"),
    
  
]