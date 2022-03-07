from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings
from django.utils.safestring import mark_safe

# Create your models here.


class UserManager(BaseUserManager):
    """ custom manager is use to tell django to use email instead of username"""

    def create_user(self, first_name, last_name, email, password=None):
        """ create a user """
        if not email:
            raise ValueError("Email is required. *****")

        email_lower = email
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email_lower.lower()),
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, first_name, last_name, email, password=None):
        """ define how a superuser is created """
        email_lowercase = email
        user = self.create_user(first_name, last_name, email_lowercase.lower(), password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Create custom user model/ table details for login """

    email = models.EmailField(verbose_name = 'email address', max_length = 255, unique = True)
    first_name = models.CharField(verbose_name = 'first name', max_length = 255)
    last_name = models.CharField(verbose_name = 'last name', max_length = 255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, blank=True)


    middle_name = models.CharField(max_length = 255, default="")
    SELECT_PAR = 'Parish'

    PARISH = [
        (SELECT_PAR ,'***select***'),
        ('Kingston','Kingston'),
        ('St. Andrew','St. Andrew'),
        ('Portland','Portland'),
        ('St. Thomas','St. Thomas'),
        ('St. Catherine','St. Catherine'),
        ('St. Mary','St. Mary'),
        ('St. Ann','St. Ann'),
        ('Manchester','Manchester'),
        ('Clarendon','Clarendon'),
        ('Hanover','Hanover'),
        ('Westmoreland','Westmoreland'),
        ('St. James','St. James'),
        ('Trelawny','Trelawny'),
        ('St. Elizabeth','St. Elizabeth'),
    ]


# gender
    SELECT = '***'
    MALE = 'M'
    FEMALE = 'F'

    GENDER = [
        (SELECT, 'M/F'),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    
    dob = models.DateField(verbose_name = 'dob', default="2000-01-01")
    gender = models.CharField(max_length = 10, choices=GENDER, default="")
    phone_no = models.CharField(max_length = 13, default=0)
    home_address = models.CharField(max_length = 255, default="")
    location = models.CharField(max_length = 50, choices=PARISH, default="")
    employee_number = models.IntegerField(default=0)
    regulation_number = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    trn = models.CharField(max_length=11, default=0)
    employer = models.CharField(max_length=100, default="")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]


    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name():
        return self.first_name
        
        

class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='upload', blank=True) # new changes 14/02/202
    slug = models.SlugField(unique=True, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reversed('prod_cat', kwargs={'slug': self.slug})
    
    # new changes 14/02/202
    def image_tag(self):
        if self.icon:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.icon.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    

class ProductSubCategory(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True)
    is_interested = models.BooleanField(default=False)
    prod_id = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, related_name='prod')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title


class ConfirmEmailNew(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user = models.EmailField(verbose_name = 'email address', max_length = 255)
    code = models.CharField(max_length=6, null=False, blank=False)

    def __str__(self):
        return 'Code' + ' ({})'.format(self.user)
