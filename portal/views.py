from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    login_url = "/login/"
    
    
class AnalysisView(LoginRequiredMixin, TemplateView):
    template_name = "analysis.html"
    login_url = "/login/"
    
class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat.html"
    login_url = "/login/"
    
class DeploymentView(LoginRequiredMixin, TemplateView):
    template_name = "deployment.html"
    login_url = "/login/"
    
class KnowledgeView(LoginRequiredMixin, TemplateView):
    template_name = "knowledge.html"
    login_url = "/login/"