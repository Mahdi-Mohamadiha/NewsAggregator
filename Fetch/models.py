from django.db.models import *
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

# Create your models here.


class Archive(Model):
    title = CharField("Title", max_length=255)
    is_trend = BooleanField("Is Trend", default=False)
    description = TextField("Description", null=True)
    publish_date = DateField("Publish date", null=True, blank=True)

    def __str__(self):
        return self.title


class UserManager(BaseUserManager):
    def create_user(self, username, password, fname, lname=None, email=None):
        if not username:
            raise ValueError("The username field must be set")
        if not password:
            raise ValueError("The password field must be set")
        if not fname:
            raise ValueError("The first name field must be set")

        user = self.model(
            username=username,
            fname=fname,
            lname=lname,
            email=self.normalize_email(email) if email else None,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, fname, lname=None, email=None):
        user = self.create_user(username, password, fname, lname, email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    fname = CharField("First Name", max_length=255)
    lname = CharField("Last Name", max_length=255, null=True)
    username = CharField("Username", max_length=255, unique=True)
    password = CharField("Password", max_length=255)
    email = EmailField("Email Address", unique=True, null=True)
    last_login = DateTimeField("Last Login", auto_now=True)

    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "fname"]

    def __str__(self):
        return self.username


class Author(Model):
    name = CharField("Name", max_length=255)
    is_valid = BooleanField("Is Valid", default=False)
    user = ManyToManyField(User, through="MapAuthorToUser")

    def __str__(self):
        return self.name


class Category(Model):
    title = CharField("Title", max_length=255)
    description = TextField("Description", null=True, blank=True)
    user = ManyToManyField(User, through="MapCategoryToUser")

    def __str__(self):
        return self.title


class MapAuthorToUser(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    author = ForeignKey(Author, on_delete=CASCADE)
    join_date = DateTimeField("Join Date", auto_now_add=True)


class MapCategoryToUser(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    category = ForeignKey(Category, on_delete=CASCADE)
    join_date = DateTimeField("Join Date", auto_now_add=True)
