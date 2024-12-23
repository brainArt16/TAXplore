from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from chatbot.models import Bot, Tag
from portal.models import Company


class HomeView(LoginRequiredMixin, ListView):
    model = Bot
    template_name = "index.html"
    login_url = "/login/"
    extra_context = {
        "tags": Tag.objects.all().values("name", "id")
    }

    def post(self, request, *args, **kwargs):
        bot_name = request.POST.get("bot_name")
        bot_description = request.POST.get("bot_description")
        bot_tag = request.POST.get("bot-tag")
        user = request.user

        user_company = Company.objects.get(user=user)

        bot = Bot.objects.create(
            name=bot_name,
            description=bot_description,
            tag=bot_tag,
            company=user_company
        )

        messages.success(request, f"{bot.name} Bot created successfully.")
        return redirect("portal:knowledge", pk=bot.id)


class KnowledgeView(LoginRequiredMixin, DetailView):
    template_name = "knowledge.html"
    login_url = "/login/"
    model = Bot
    context_object_name = "bot"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        knowledge = (
            self.object.knowledge_base
            if hasattr(self.object, "knowledge_base")
            else None
        )

        print(knowledge)

        if knowledge:
            documents = (
                knowledge.documents.all()
                if knowledge.knowledge_base_type == 1
                else None
            )
            context["documents"] = documents

        print(context)
        return context
    
    def post(self, request, *args, **kwargs):
        bot = self.get_object()
        
        # New Knowledge Base
        if "knowledge_base" in request.POST:
            collection_name = bot.name
            description = request.POST.get("description")
            knowledge_base_type = request.POST.get("knowledge_base_type")
        
            bot.knowledge_base.create(
                collection_name=collection_name,
                description=description,
                knowledge_base_type=knowledge_base_type
            )
        
        else:
            url = request.POST.get("url") if request.POST.get("url") else None
            documents = request.FILES.getlist("documents") if request.FILES.getlist("documents") else None
            
            if not url and not documents:
                messages.error(request, "Please provide a URL or upload documents.")
                return redirect("portal:knowledge", pk=bot.id)
            
            knowledge_base = bot.knowledge_base
            knowledge_base.url = url
            knowledge_base.save()
            
            for document in documents:
                knowledge_base.documents.create(document=document)
                
                
        messages.success(request, f"{collection_name} Knowledge Base created successfully.")
        return redirect("portal:knowledge", pk=bot.id)


class AnalysisView(LoginRequiredMixin, TemplateView):
    template_name = "analysis.html"
    login_url = "/login/"

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = "chat.html"
    login_url = "/login/"

class DeploymentView(LoginRequiredMixin, TemplateView):
    template_name = "deployment.html"
    login_url = "/login/"
