from django.contrib import admin

from .models import Teacher, Category, Course, Variant, VariantItem, Question_Answer, Question_Answer_Message, Cart, CartOrder, CartOrderItem, Certificate, CompletedLesson, EnrolledCourse, Note, Review, Notification, Coupon, Wishlist, Country
# Register your models here.

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'country']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'teacher', 'price', 'level', 'featured']

@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ['course', 'title', 'date']

@admin.register(VariantItem)
class VariantItemAdmin(admin.ModelAdmin):
    list_display = ['variant', 'title', 'duration', 'content_duration', 'preview']

@admin.register(Question_Answer)
class Question_AnswerAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'title', 'date']

@admin.register(Question_Answer_Message)
class Question_Answer_MessageAdmin(admin.ModelAdmin):
    list_display = ['course', 'question', 'user', 'message', 'date']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'price', 'tax_fee', 'total', 'country', 'date']

@admin.register(CartOrder)
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['student', 'total', 'payment_status', 'full_name', 'email', 'country', 'date']

@admin.register(CartOrderItem)
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'course', 'teacher', 'tax_fee', 'total', 'saved', 'date']

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'date']

@admin.register(CompletedLesson)
class CompletedLessonAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'variant_item', 'date']

@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'teacher', 'order_item', 'date']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'title', 'date']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'user', 'rating', 'review', 'active', 'date']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'teacher', 'order', 'order_item', 'review', 'notification_type', 'seen', 'date']

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'active', 'date']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax_rate', 'active']