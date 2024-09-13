from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from api import serializers as api_serializers
from userauths.models import User, Profile
from api import models as api_models

import stripe

import random
from decimal import Decimal


# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializers.RegisterSerializer


def generate_random_otp(length=7):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.UserSerializer

    def get_object(self):
        email = self.kwargs['email']

        user = User.objects.filter(email=email).first()

        if user:

            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()

            link = f'http://localhost:5173/create-new-password/?otp={
                user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}'

            context = {
                "link": link,
                "username": user.username,
            }

            subject = "Password Reset Email"
            text_body = render_to_string('email/password_reset.txt', context)
            html_body = render_to_string('email/password_reset.html', context)

            message = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email],
                body=text_body,
            )

            message.attach_alternative(html_body, "text/html")
            message.send()

            print("Link ===========", link)

        return user


class PasswordChangeAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_serializers.UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uuidb64 = payload['uuidb64']
        password = payload['password']

        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            # user.otp = ""
            user.save()

            return Response({"message": "Password changed successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)


class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active=True)
    serializer_class = api_serializers.CategorySerializer
    permission_classes = [AllowAny]


class CourseListAPIView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(
        platform_status="Published", teacher_course_status="Approved")
    serializer_class = api_serializers.CourseSerializer
    permission_classes = [AllowAny]


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = api_models.Course.objects.filter(
        platform_status="Published", teacher_course_status="Published")
    serializer_class = api_serializers.CourseSerializer
    permission_classes = [AllowAny]
    # lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(
            slug=slug, platform_status="Published", teacher_course_status="Published")
        return course


class CartAPIView(generics.CreateAPIView):
    queryset = api_models.Cart.objects.all()
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        payload = request.data

        # course_id = payload.get('course_id')
        # user_id = payload.get('user_id')
        # price = payload.get('price')
        # country_name = payload.get('country_name')
        # cart_id = payload.get('cart_id')

        course_id = payload['course_id']
        user_id = payload['user_id']
        price = payload['price']
        country_name = payload['country_name']
        cart_id = payload['cart_id']

        course = api_models.Course.objects.filter(id=course_id).first()

        user = User.objects.filter(id=user_id).first()

        country_object = api_models.Country.objects.filter(
            name=country_name).first()
        country = country_object.name if country_object else "Unknown Country"

        if country_object:
            tax_rate = country_object.tax_rate / 100
        else:
            tax_rate = 0

        cart = api_models.Cart.objects.filter(
            cart_id=cart_id, course=course).first()

        if cart:
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()
            return Response({"message": "Cart updated Successfully"}, status=status.HTTP_200_OK)

        else:
            cart = api_models.Cart()
            cart.course = course
            cart.user = user
            cart.price = price
            cart.tax_fee = Decimal(price) * Decimal(tax_rate)
            cart.country = country
            cart.cart_id = cart_id
            cart.total = Decimal(cart.price) + Decimal(cart.tax_fee)
            cart.save()

            return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)

    # cart, created = api_models.Cart.objects.update_or_create(
    #     cart_id=cart_id,
    #     defaults={
    #         'course': course,
    #         'user': user,
    #         'price': price,
    #         'tax_fee': Decimal(price) * Decimal(tax_rate),
    #         'country': country,
    #         'total': Decimal(price) + (Decimal(price) * Decimal(tax_rate))
    #     }
    # )

    # if created:
    #     return Response({"message": "Cart Created Successfully"}, status=status.HTTP_201_CREATED)
    # if cart:
    #     return Response({"message": "Cart Updated Successfully"}, status=status.HTTP_200_OK)


class CartlistAPIView(generics.ListAPIView):
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset

class CartItemDeleteAPIView(generics.DestroyAPIView):
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']
        
        return api_models.Cart.objects.filter(id=item_id, cart_id=cart_id).first()
    
class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        total_price = 0.00
        total_tax = 0.00
        total_total = 0.00

        for cart_item in queryset:
            total_price += float(self.calculate_price(cart_item))
            total_tax += float(self.calculate_tax(cart_item))
            total_total += round(float(self.calculate_total(cart_item)), 2)

        data = {
            "price": total_price,
            "tax": total_tax,
            "total": total_total,
        }

        return Response(data, status=status.HTTP_200_OK)

    def calculate_price(self, cart_item):
        return cart_item.price

    def calculate_tax(self, cart_item):
        return cart_item.tax_fee

    def calculate_total(self, cart_item):
        return cart_item.total
    

class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()

    def create(self, request, *args, **kwargs):
        payload = request.data

        full_name = payload['full_name']
        email = payload['email']
        country = payload['country']
        cart_id = payload['cart_id']
        user_id = payload['user_id']
        
        if user_id != 0:
            user = User.objects.get(id=user_id)
        else:
            user = None 

        
        cart_items = api_models.Cart.objects.filter(cart_id=cart_id)

        total_price = Decimal('0.00')
        total_tax = Decimal('0.00')
        total_initial_total = Decimal('0.00')
        total_total = Decimal('0.00')

        order = api_models.CartOrder.objects.create(
            full_name=full_name,
            email=email,
            country=country,
            student=user
        )

        for cart_item in cart_items:
            api_models.CartOrderItem.objects.create(
                order=order,
                course=cart_item.course,
                price=cart_item.price,
                tax_fee=cart_item.tax_fee,
                total=cart_item.total,
                initial_total=cart_item.price,
                teacher=cart_item.course.teacher,
            )

            total_price += Decimal(cart_item.price)
            total_tax += Decimal(cart_item.tax_fee)
            total_initial_total += Decimal(cart_item.price)
            total_total += Decimal(cart_item.total)

            order.teachers.add(cart_item.course.teacher)

        order.subtotal = total_price
        order.tax = total_tax
        order.initial_total = total_initial_total
        order.total = total_total
        order.save()
        
        return Response({"message": "Order Created Successfully"}, status=status.HTTP_201_CREATED)
    

class CheckoutAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()
    lookup_field = 'oid'


class CouponApplyAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CouponSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        
        order_oid = request.data['order_oid']
        coupon_code = request.data['coupon_code']
        
        order = api_models.CartOrder.objects.get(oid=order_oid)
        coupon = api_models.Coupon.objects.get(code=coupon_code)

        if coupon:
            order_items = api_models.CartOrderItem.objects.filter(order=order, teacher=coupon.teacher)
            for order_item in order_items:
                if not coupon in order_item.coupons.all():
                    discount = order_item.total * coupon.discount / 100

                    order_item.total -= discount
                    order_item.price -= discount
                    order_item.saved += discount
                    order_item.applied_coupon = True
                    order_item.coupons.add(coupon)

                    order.coupons.add(coupon)
                    order.total -= discount
                    order.subtotal -= discount
                    order.saved += discount
                    

                    order_item.save()
                    order.save()
                    coupon.used_by.add(order.student)

                    return Response({"message": "Coupon Applied Successfully", "icon": "success"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Coupon Already Applied", "icon": "warning"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "Coupon Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)


class StripeCheckoutAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        
        order_oid = self.kwargs['order_oid']
        order = api_models.CartOrder.objects.get(oid=order_oid)
        
        if not order:
            return Response({"message": "Order Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=order.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': order.full_name,
                            },
                            'unit_amount': int(order.total * 100),
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=settings.FRONTEND_SITE_URL + '/payment-success/' + order.oid + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.FRONTEND_SITE_URL + '/payment-failed/'
            )
            # print("Checkout Session =================", checkout_session)
            order.stripe_session_id = checkout_session.id

            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return Response({"message": f"Something went wrong. Error: {str(e)}", "icon": "error"}, status=status.HTTP_400_BAD_REQUEST)
