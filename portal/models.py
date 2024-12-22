from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from chatbot.models import Bot

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and extra fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()
    username = None
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    

    def __str__(self):
        return self.email

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class KnowledgeBase(models.Model):
    KNOWLEDGE_BASE_TYPE = (
        (1, "Document"),
        (2, "URL"),
    )
    bot = models.OneToOneField(Bot, on_delete=models.CASCADE)
    collection_name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    knowledge_base_type = models.IntegerField(choices=KNOWLEDGE_BASE_TYPE)
    url = models.URLField(null=True, blank=True)
    company = models.ForeignKey("Company", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = (
            "collection_name",
            "company",
        )  # Ensures unique titles within each company

    def __str__(self):
        return self.title

    def clean(self):
        """Ensure that only one of 'document' or 'url' is filled."""
        if self.knowledge_base_type == 1 and not self.documents.exists():
            raise ValidationError(
                "At least one document must be provided if the knowledge base type is Document."
            )
        if self.knowledge_base_type == 2 and not self.url:
            raise ValidationError(
                "URL must be provided if the knowledge base type is URL."
            )

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
        return f"Document for {self.knowledge_base.collection_name} - {self.document.name}"
