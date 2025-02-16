from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from chatbot.models import Bot, Tag, AIModel, BotSetting
from portal.models import Company
from django.shortcuts import get_object_or_404

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

        if knowledge:
            documents = (
                knowledge.documents.all()
                if knowledge.knowledge_base_type == 1
                else None
            )
            context["documents"] = documents

        bot_settings = BotSetting.objects.filter(bot=self.object)
        context["bot_settings"] = bot_settings[0] if bot_settings else None
        
        print(bot_settings[0].template)
        
        models = AIModel.objects.all().values("name", "id", "max_tokens", "context_window", "license_type")
        
        context["models"] = models

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


class BotSettingsView(LoginRequiredMixin, FormView):
    template_name = "models/bot_configuration.html"
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        bot_id = request.POST.get("bot_id")
        model_id = request.POST.get("selected_model")
        template = request.POST.get("custom_prompts")
        token_limit = request.POST.get("max_tokens")
        temperature = request.POST.get("temperature")

        bot = get_object_or_404(Bot, id=bot_id)
        ai_model = get_object_or_404(AIModel, id=model_id)

        bot_setting, created = BotSetting.objects.update_or_create(
            bot=bot,
            defaults={
            "ai_model": ai_model,
            "template": template,
            "token_limit": token_limit,
            "temperature": temperature,
            },
        )

        if created:
            messages.success(request, f"{bot.name} Bot settings created successfully.")
        else:
            messages.success(
                request, f"{bot.name} Bot settings updated successfully."
            )

        # return the page which set the request
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


class AnalysisView(LoginRequiredMixin, DetailView):
    template_name = "analysis.html"
    login_url = "/login/"
    model = Bot
    context_object_name = "bot"


class ChatView(LoginRequiredMixin, DetailView):
    template_name = "chat.html"
    login_url = "/login/"
    model = Bot
    context_object_name = "bot"


class DeploymentView(LoginRequiredMixin, DetailView):
    template_name = "deployment.html"
    login_url = "/login/"
    model = Bot
    context_object_name = "bot"
    
    def telegram_deployment(self):
        pass
    
    def whatsapp_deployment(self):
        pass # TODO: Implement this method
    
    def facebook_deployment(self):
        pass # TODO: Implement this method
    
    def get_context_data(self, **kwargs):
        context=   super().get_context_data(**kwargs)
        
        # Check if the bot has settings
        bot_settings = BotSetting.objects.filter(bot=self.object)
        context["bot_settings"] = bot_settings[0] if bot_settings else None
        
        # Get AI Models
        models = AIModel.objects.all().values("name", "id", "max_tokens", "context_window", "license_type")
        context["models"] = models
        
        
        
        
        
        return context
