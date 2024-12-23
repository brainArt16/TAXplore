from django.db import models
from django.core.exceptions import ValidationError
from portal.models import Company, User


class Tag(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Bot(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="bots", null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="bots")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BotTemplate(models.Model):
    bot = models.OneToOneField(Bot, on_delete=models.CASCADE)
    template = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bot.name


class KnowledgeBase(models.Model):
    KNOWLEDGE_BASE_TYPE = (
        (1, "Document"),
        (2, "URL"),
    )
    bot = models.OneToOneField(Bot, on_delete=models.CASCADE, related_name="knowledge_base")
    collection_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    knowledge_base_type = models.IntegerField(choices=KNOWLEDGE_BASE_TYPE)
    url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "collection_name",
            "bot",
        )  # Ensures unique titles per bot

    def __str__(self):
        return self.collection_name

    def get_documents(self):
        """Returns all linked documents."""
        return self.knowledgebasedocument_set.all()


class KnowledgeBaseDocument(models.Model):
    knowledge_base = models.ForeignKey(
        KnowledgeBase, related_name="documents", on_delete=models.CASCADE
    )
    document = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"Document for {self.knowledge_base.collection_name} - {self.document.name}"
        )
