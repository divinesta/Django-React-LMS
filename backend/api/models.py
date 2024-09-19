from django.db import models
from django.utils.text import slugify
from django.utils import timezone

from userauths.models import User, Profile
from shortuuid.django_fields import ShortUUIDField
from moviepy.editor import VideoFileClip
import math
# Create your models here.


LANGUAGE = (
    ("English", "English"),
    ("French", "French"),
    ("Spanish", "Spanish"),
)

LEVEL = (
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advanced", "Advanced"),
)

TEACHER_STATUS = (
    ("Draft", "Draft"),
    ("Disabled", "Disabled"),
    ("Published", "Published"),
)

PAYMENT_STATUS = (
    ("Paid", "Paid"),
    ("Processing", "Processing"),
    ("Failed", "Failed"),
)

PLATFORM_STATUS = (
    ("Review", "Review"),
    ("Disabled", "Disabled"),
    ("Rejected", "Rejected"),
    ("Draft", "Draft"),
    ("Published", "Published"),
)

RATING = (
    ("1 Star", "1 Star"),
    ("2 Star", "2 Star"),
    ("3 Star", "3 Star"),
    ("4 Star", "4 Star"),
    ("5 Star", "5 Star"),
)

NOTIFICATION_TYPE = (
    ("New Order", "New Order"),
    ("New Review", "New Review"),
    ("New Course Question", "New Course Question"),
    ("Course Published", "Course Published"),
    ("Course Enrollment Completed", "Course Enrollment Completed"),
)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="course-file", null=True, blank=True, default="default.jpg")
    full_name = models.CharField(max_length=100)
    bio = models.TextField(max_length=100, null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.full_name

    def students(self):
        return CartOrderItem.objects.filter(teacher=self)
    
    def courses(self):
        return Course.objects.filter(teacher=self)
    
    def review(self):
        return Course.objects.filter(teacher=self).count()


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to="course-file", null=True, blank=True, default="category.jpg")
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Category"
        ordering = ["title"]
    
    def __str__(self):
        return self.title
    
    def course_count(self):
        return Course.objects.filter(category=self).count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Course(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    image = models.FileField(upload_to="course-file", null=True, blank=True, default="course.jpg")
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    language = models.CharField(max_length=100, choices=LANGUAGE, default="English")
    level = models.CharField(max_length=100, choices=LEVEL, default="Beginner")
    platform_status = models.CharField(max_length=100, choices=PLATFORM_STATUS, default="Published")
    teacher_course_status = models.CharField(max_length=100, choices=TEACHER_STATUS, default="Published")
    featured = models.BooleanField(default=False)
    course_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    slug = models.SlugField(unique=True, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def students(self):
        return EnrolledCourse.objects.filter(course=self)
    
    def curriculum(self):
        return Variant.objects.filter(course=self)
    
    def lectures(self):
        return VariantItem.objects.filter(variant__course=self)
    
    def average_rating(self):
        average_rating = Review.objects.filter(course=self).aggregate(avg_rating=models.Avg("rating"))
        return average_rating["avg_rating"]
    
    def rating_count(self):
        return Review.objects.filter(course=self, active=True).count()

    def reviews(self):
        return Review.objects.filter(course=self, active=True)


class Variant(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    variant_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    
    def variant_items(self):
        return VariantItem.objects.filter(variant=self)

    def items(self):
        return VariantItem.objects.filter(variant=self)


class VariantItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name="variant_items")
    title = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="course-file", null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    content_duration = models.CharField(max_length=1000, null=True, blank=True)
    preview = models.BooleanField(default=False)
    variant_item_id = ShortUUIDField(
        unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.variant.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.file:
            clip = VideoFileClip(self.file.path)
            duration_seconds = clip.duration
            minutes, seconds = divmod(duration_seconds, 60)
            minutes = math.floor(minutes)
            seconds = math.floor(seconds)
            self.content_duration = f"{minutes}m {seconds}s"
            super().save(update_fields=["content_duration"])


class Question_Answer(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    qa_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    class Meta:
        ordering = ["-date"]

    def messages(self):
        return Question_Answer_Message.objects.filter(question=self)

    def profile(self):
        return Profile.objects.get(user=self.user)


class Question_Answer_Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.ForeignKey(Question_Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    qam_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
    class Meta:
        ordering = ["date"]

    def profile(self):
        return Profile.objects.get(user=self.user)


class Cart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    country = models.CharField(max_length=100, null=True, blank=True)
    cart_id = ShortUUIDField(length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title


class CartOrder(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teachers = models.ManyToManyField(Teacher, blank=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS, default="Processing")
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    coupons = models.ManyToManyField("api.Coupon", blank=True)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    stripe_session_id = models.CharField(max_length=1000, null=True, blank=True)
    oid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.oid
    
    class Meta:
        ordering = ["-date"]

    def order_items(self):
        return CartOrderItem.objects.filter(order=self)


class CartOrderItem(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, related_name="orderitem")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="order_item")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    tax_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    initial_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    saved = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    coupons = models.ManyToManyField("api.Coupon", blank=True)
    applied_coupon = models.BooleanField(default=False)
    oid = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def order_id(self):
        return f"Order ID #{self.order.oid}"
    
    def payment_status(self):
        return f"{self.order.payment_status}"
    
    def __str__(self):
        return self.oid


class Certificate(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    certificate_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title


class CompletedLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    variant_item = models.ForeignKey(VariantItem, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title


class EnrolledCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.CASCADE)
    enrollment_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title

    def lectures(self):
        return VariantItem.objects.filter(variant__course=self.course)

    def completed_lesson(self):
        return CompletedLesson.objects.filter(course=self.course, user=self.user)
    
    def curriculum(self):
        return Variant.objects.filter(course=self.course)
    
    def note(self):
        return Note.objects.filter(course=self.course, user=self.user)
    
    def question_answer(self):
        return Question_Answer.objects.filter(course=self.course)
    
    def review(self):
        return Review.objects.filter(course=self.course, user=self.user).first()


class Note(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=1000, null=True, blank=True)
    note = models.TextField()
    note_id = ShortUUIDField(unique=True, length=6, max_length=20, alphabet="abcdefghijklmn0123456789")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.CharField(max_length=100, choices=RATING, default="None")
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.course.title
    
    def profile(self):
        return Profile.objects.get(user=self.user)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True, blank=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, null=True, blank=True)
    review = models.ForeignKey(Review, on_delete=models.SET_NULL, null=True, blank=True)
    notification_type = models.CharField(max_length=100, choices=NOTIFICATION_TYPE, default="None")
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.notification_type
    
class Coupon(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    used_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=100, unique=True)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.course.title)
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    tax_rate = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name





