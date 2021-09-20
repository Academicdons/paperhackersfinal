from django.db import models
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, User
)
from django_countries.fields import CountryField

from .utils import *
from datetime import datetime, date

# Create your models here.

# class MyUserManager(BaseUserManager):
#     def create_user(self, email):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')
#
#         createusername = str(random.randint(1000000, 9999999))
#         createpassword = str(random.randint(1000000, 9999999))
#         print(createusername)
#         print(createpassword)
#
#         user = self.model(
#             email=self.normalize_email(email),
#             username=createusername,
#         )
#
#         user.set_password(createpassword)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         createusername = str(random.randint(1000000, 9999999))
#         createpassword = str(random.randint(1000000, 9999999))
#         print(createusername)
#         print(createpassword)
#         user = self.create_user(
#             email,
#             username=createusername,
#         )
#         user.set_password(createpassword)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

#
# class User(AbstractBaseUser):
#     def random_string():
#         return str(random.randint(1000000, 9999999))
#
#     id = models.CharField(primary_key=True, default=random_string, editable=False, max_length=100000000000)
#     email = models.EmailField(
#         verbose_name='email address',
#         max_length=255,
#         unique=True,
#     )
#     username = models.CharField(unique=True, null=True, max_length=50)
#     password = models.CharField(max_length=200, null=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     objects = MyUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['']
#
#     def __str__(self):
#         return self.id
#
#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         return True
#
#     @property
#     def is_staff(self):
#         "Is the user a member of staff?"
#         # Simplest possible answer: All admins are staff
#         return self.is_admin


class Client(models.Model):
    def random_string():
        return str(random.randint(1000000, 9999999))

    id = models.CharField(primary_key=True, default=random_string, editable=False, max_length=100000000000)
    user = models.ForeignKey(User, blank=True, related_name='Client', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, null=True, default='')
    country = CountryField(multiple=True)
    phone = models.CharField(max_length=15, null=True, default='')
    code = models.CharField(max_length=12, blank=True)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True,null=True,related_name='ref_by')
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.code}"

    def get_reccomended_profile(self):
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            name = self.user.username
            self.code = code
            self.name = name
        super().save(*args, **kwargs)

class Writers(models.Model):
    Writer_Quality = (
        ('Beginner Writer', 'Beginner Writer'),
        ('Advanced Writer', 'Advanced Writer'),
        ('Expert Writer', 'Expert Writer'),
    )
    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    Degree = (
        ('Bachelors', 'Bachelors'),
        ('Masters', 'Masters'),
        ('Ph.D', 'Ph.D'),
    )

    def random_string():
        return str(random.randint(1000000, 9999999))

    id = models.CharField(primary_key=True, default=random_string, editable=False, max_length=100000000000)

    user = models.OneToOneField(User, blank=True, related_name='writerprof', null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=10, null=False, default='')
    second_name = models.CharField(max_length=10, null=False, default='')
    pseudonym = models.CharField(max_length=30, null=False, default='')
    city = models.CharField(max_length=10, null=False, default='')
    phone = models.CharField(max_length=15, null=False, default='')
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)
    description = models.TextField(default='', null=True)

    gender = models.CharField(choices=Gender, max_length=300, default='')
    country = CountryField()
    governid = models.FileField(null=True, blank=True)

    university = models.CharField(max_length=10, null=True, default='')
    unidept = models.CharField(max_length=10, null=True, default='')
    diploma = models.FileField(null=True, blank=True)

    statement = models.TextField(default='', null=True)
    writer_quality = models.CharField(choices=Writer_Quality, max_length=300, default=('Beginner Writer'))
    image = models.ImageField(null=True, blank=True, upload_to='images/',
                              default='images/NoImageAvailable.png')

    def save(self, *args, **kwargs):
        if self.pseudonym == "":
            pseudonym = self.user.username
            first_name = self.user.username
            self.pseudonym = pseudonym
            self.first_name = first_name
        super().save(*args, **kwargs)


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_writer_rating(self):
        completed_orders = self.orders.filter(order_status='Completed')
        count = 0
        rating_sum = 0
        for order in completed_orders:
            if order.rating != '0':
                rating_sum += int(order.rating)
                count += 1
        if count:
            return rating_sum / count
        else:
            return 'No rating available'

    def __str__(self):
        return self.first_name

class Support(models.Model):
    Gender = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    user = models.ForeignKey(User, related_name='Support', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=75, null=False, default='')
    country = CountryField()
    gender = models.CharField(choices=Gender, max_length=300, default='')
    phone = models.CharField(max_length=15, null=False, default='+447584221456')
    statement = models.TextField(default='')
    date_joined = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name



class AbstractDateModel(models.Model):
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class Order(AbstractDateModel):
    WRITING_FROM_SCRATCH_CPP = "6.00"
    EDITING_AND_REVISION_CPP = "0.50"
    Type_of_service = (
        (WRITING_FROM_SCRATCH_CPP, 'Writing From Scratch'),
        (EDITING_AND_REVISION_CPP, 'Editing And Revision'),

    )
    HIGH_SCHOOL_CPP = "1.00"
    COLLEGE_1_CPP = "2.00"
    COLLEGE_2_CPP = "2.50"
    MASTERS_CPP = "3.50"
    PHD_CPP = "4.5"
    Academic_level = (
        (HIGH_SCHOOL_CPP, 'High school'),
        (COLLEGE_1_CPP, 'College 1'),
        (COLLEGE_2_CPP, 'college 2'),
        (MASTERS_CPP, 'Masters'),
        (PHD_CPP, 'Phd'),

    )
    ESSAY_ANY_TYPE = "0.0"
    ADMISSION_ESSAY = "0.25"
    ANNOINTED_BIBLIOGRAPHY = "0.25"
    ARTICLE_REVIEW = "0.25"
    BOOK_REVIEW = "0.25"
    BUSINESS_PLAN = "0.25"
    CASE_STUDY = "0.25"
    COURSE_WORK = "0.25"
    CREATIVE_WRITING = "0.50"
    CRITICAL_WRITING = "1.25"
    PRESENTATION = "0.0"
    SPEECH = "1.0"
    RESEARCH_PROPOSAL = "2.5"
    RESEARCH_PAPER = "1.5"
    TERM_PAPER = "0.75"
    THESIS = "3.0"
    DISSERTATION = "4.0"
    Essay_type = [
        (ESSAY_ANY_TYPE, 'Essay any type'),
        (ADMISSION_ESSAY, 'Admission essay'),
        (ANNOINTED_BIBLIOGRAPHY, 'Annointed bibliography'),
        (ARTICLE_REVIEW, 'Article review'),
        (BOOK_REVIEW, 'Book review'),
        (BUSINESS_PLAN, 'Business plan'),
        (CASE_STUDY, 'Case study'),
        (COURSE_WORK, 'Course work'),
        (CREATIVE_WRITING, 'Creative writing'),
        (CRITICAL_WRITING, 'Critical writing'),
        (PRESENTATION, 'Presentation'),
        (SPEECH, 'Speech'),
        (RESEARCH_PROPOSAL, 'Research proposal'),
        (RESEARCH_PAPER, 'Research paper'),
        (TERM_PAPER, 'Term paper'),
        (THESIS, 'Thesis'),
        (DISSERTATION, 'Dissertation'),
    ]
    ACCOUNTING = "4.00"
    African_American_study = "1.25"
    Architecture = "4.00"
    Anthropology = "1.25"
    Business = "1.25"
    Art = "1.25"
    Chemistry = "4.00"
    Computer = "4.00"
    Engineering = "4.00"
    Mathematics = "4.00"
    Economics = "4.00"
    Finance = "4.00"
    Physics = "4.00"
    Music = "2.00"
    Law = "5.00"
    Communication = "1.25"
    Education = "1.25"
    Ethics = "1.25"
    Environmental = "1.25"
    Geography = "3.25"
    Health = "1.25"
    History = "1.25"
    International = "1.25"
    Linguistics = "1.25"
    Management = "1.25"
    Marketing = "1.25"
    Psychology = "1.25"
    Nursing = "1.25"
    Nutrition = "1.25"
    Philosophy = "1.25"
    Political = "1.25"
    Sports = "1.25"
    Sociology = "1.25"
    Religion = "1.25"
    Technology = "4.25"
    Tourism = "1.25"
    Subject = (
        (ACCOUNTING, 'Accounting'),
        (African_American_study, 'African American study'),
        (Architecture, 'Architecture'),
        (Anthropology, 'Anthropology'),
        (Business, 'Business and entrepreneur'),
        (Art, 'Art theater films'),
        (Chemistry, 'Chemistry'),
        (Communication, 'Communication strategies'),
        (Computer, 'Computer science'),
        (Economics, 'Economics'),
        (Education, 'Education'),
        (Engineering, 'Engineering'),
        (Ethics, 'Ethics'),
        (Environmental, 'Environmental issues'),
        (Finance, 'Finance'),
        (Geography, 'Geography'),
        (Health, 'Health care'),
        (History, 'History'),
        (International, 'International public relationship'),
        (Law, 'Law'),
        (Linguistics, 'Linguistics'),
        (Management, 'Management'),
        (Marketing, 'Marketing'),
        (Mathematics, 'Mathematics'),
        (Music, 'Music'),
        (Nursing, 'Nursing'),
        (Nutrition, 'Nutrition'),
        (Philosophy, 'Philosophy'),
        (Physics, 'Physics'),
        (Political, 'Political Science'),
        (Psychology, 'Psychology'),
        (Religion, 'Religion And Theology'),
        (Sports, 'Sports'),
        (Sociology, 'Sociology'),
        (Technology, 'Technology'),
        (Tourism, 'Tourism'),
    )
    References = (
        ('Mla', 'Mla'),
        ('Apa', 'Apa'),
        ('Harvard', 'Harvard'),
        ('Chicago', 'Chicago'),
        ('Other', 'Other'),
    )
    spacing = (
        ('Single', 'Single'),
        ('Double', 'Double'),

    )
    order_status_options = (
        ('Pending Payment', 'Pending Payment'),
        ('Paid', 'Paid'),
        ('Writer Assigned', 'Writer Assigned'),
        ('Delivered', 'Delivered'),
        ('Revision', 'Revision'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    )
    FOUR_HOURS = "6.0"
    SIX_HOURS = "5.50"
    EIGHT_HOURS = "5.25"
    TWELVE_HOURS = "5.0"
    TWENTY_FOUR_HOURS = "4.75"
    TWO_DAYS = "4.50"
    THREE_DAYS = "4.25"
    FOUR_DAYS = "4.00"
    FIVE_DAYS = "3.75"
    SIX_DAYS = "3.50"
    ONE_WEEK = "3.25"
    order_deadline_options = (
        (FOUR_HOURS, '4'),
        (SIX_HOURS, '6'),
        (EIGHT_HOURS, '8'),
        (TWELVE_HOURS, '12'),
        (TWENTY_FOUR_HOURS, '24'),
        (TWO_DAYS, '48'),
        (THREE_DAYS, '72'),
        (FOUR_DAYS, '96'),
        (FIVE_DAYS, '120'),
        (SIX_DAYS, '144'),
        (ONE_WEEK, '168'),
    )
    RATINGS = (
        ('0', 'Not Rated'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    def random_string():
        return str(random.randint(1000000, 9999999))

    id = models.CharField(primary_key=True, default=random_string, editable=False, max_length=100000000000)

    topic = models.CharField(max_length=60, null=False, default='Writers Choice')
    service_type = models.CharField(max_length=300, null=False, choices=Type_of_service,
                                    default=WRITING_FROM_SCRATCH_CPP)
    academic_level = models.CharField(choices=Academic_level, default=COLLEGE_1_CPP, max_length=300)
    essay_type = models.CharField(choices=Essay_type, max_length=300, default=(CASE_STUDY))
    subject = models.CharField(choices=Subject, max_length=300, default=(ACCOUNTING))
    bid_statement = models.TextField(default='', null=True)
    number_of_pages = models.IntegerField(default='2')
    deadline = models.CharField(choices=order_deadline_options, max_length=300, null=True, default=("2.00"))
    Paper_Instruction = models.TextField(default='', null=True)
    references = models.CharField(choices=References, max_length=300, default=('SOME STRING'))
    spacing = models.CharField(choices=spacing, max_length=300, default=('SOME STRING'))
    Paper_heading = models.CharField(max_length=60, null=True, default='This is the Paper on:')
    Paperdetails = models.TextField(default='', null=True)
    revision_comment = models.TextField(default='', null=True)

    file_upload = models.FileField(null=True, blank=True)
    number_of_references = models.IntegerField(default='')
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    order_status = models.CharField(choices=order_status_options, default='Pending Payment', max_length=300)
    customer = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    writer = models.ForeignKey(Writers, null=True, related_name='orders', on_delete=models.SET_NULL)
    support = models.ForeignKey(Support, null=True, on_delete=models.SET_NULL)
    rating = models.CharField(choices=RATINGS, default='0', max_length=1)

    def save(self, *args, **kwargs):
        if self.writer == "":
            writer = self.user.username
            self.writer = writer
        super().save(*args, **kwargs)

    @property
    def calculate_total_price(self):
        order_price = round(
            (float(self.service_type) + float(self.essay_type) + float(self.academic_level) + float(self.subject) + float(self.deadline)) * int(
                self.number_of_pages), 2)

        return order_price

    @property
    def writer_cpp(self):

        writercpp = round(int(self.writer_pay) / int(self.number_of_pages), 2)

        return writercpp

    @property
    def writer_pay(self):

        writerpay = round(int(self.calculate_total_price) / 4, 2)

        return writerpay

    @property
    def get_writer_rating(self):
        if self.rating != '0':
            return self.rating
        else:
            return 'Not yet rated'

    @property
    def show_page_numbers(self):
        return self.number_of_pages

    @property
    def show_no_of_words(self):
        number = round(int(self.number_of_pages)*275, 1)
        return number

    @property
    def show_essay_type(self):
        return self.get_essay_type_display()

    @property
    def show_essay_subject(self):
        return self.get_subject_display()

    @property
    def show_writer_level(self):
        return self.get_academic_level_display()

    @property
    def show_service_type(self):
        return self.get_service_type_display()

    @property
    def show_academic_level(self):
        return self.get_academic_level_display()

    @property
    def show_deadline(self):
        deadline = self.date_added + timedelta(hours=int(self.get_deadline_display()))
        if deadline - timezone.now() > timedelta(days=1):
            remaining_time = str(deadline - timezone.now()).split(", ")
            return remaining_time[0] + " " + remaining_time[1].split(":")[0] + 'hrs ' + remaining_time[1].split(":")[
                1] + 'mins '
        elif deadline - timezone.now() < timedelta(days=1):
            return str(deadline - timezone.now()).split(":")[0] + 'hrs ' + str(deadline - timezone.now()).split(":")[
                1] + 'mins '
        else:
            return str(deadline - timezone.now()).split(":")[0] + 'mins '

    def __str__(self):
        return str(self.id)



class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                     self).get_queryset() \
            .filter(status='published')


class Review(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_posts')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='review_order')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return str(self.author)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    image = models.ImageField(null=True, blank=True, upload_to='images/', height_field="image_height",
                              width_field="image_width", editable=True,
                              default='images/NoImageAvailable.png')
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="100")

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
