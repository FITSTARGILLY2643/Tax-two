from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch  import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, default="avatar.svg")
    bio = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        db_table = 'profile'

    @receiver(post_save, sender=User)
    def update_create_profile(sender,instance,created, **kwargs):
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)

    def save_profile(self):
        self.save()

class TaxApplication(models.Model):
    client= models.OneToOneField(User, on_delete=models.CASCADE)
    TYPE = (('Renewal','Renewal',),('Appeal','Appeal'),('First Application','First Application'))
    application_type = models.CharField(max_length=50, choices=TYPE, null=True, blank=True)
    id_card = models.FileField(upload_to='doc/',null=True, blank=True)
    date_applied = models.DateTimeField(default=timezone.now())
    


