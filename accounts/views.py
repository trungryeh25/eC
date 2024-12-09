# accounts/views.py

from re import split
from carts.models import Cart, CartItem
from django.shortcuts import redirect, render
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

from .forms import RegistrationForm
from accounts.models import Account
from carts.views import _cart_id

import requests # type: ignore


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Lấy dữ liệu từ form và tạo tài khoản
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0] # Sử dụng phần trước dấu @ làm tên người dùng

            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # gửi email xác thực
            current_site = get_current_site(request=request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('accounts/active_email.html', {
                'user': user, # Là đối tượng người dùng  (từ model Account). Tham số này được truyền vào template để có thể sử dụng thông tin như tên người dùng, email, v.v
                'domain': current_site.domain, # đây là tên miền của trang web hiện tại (lấy từ current.site.domain). Tham số này sẽ được sử dụng để tạo một liên kết đầy đủ mà người dùng có thể click vào để kích hoạt tài khoản.
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # Đây là ID của người dùng đã được mã hóa dưới dạng base64. `urlsafe_base64_code` chuyển đổi ID người dùng thành một chuỗi an toàn cho URL. force_bytes(user.pk) chuyển dổi ID của người dùng thành kiểu byte trước khi mã hóa.
                'token': default_token_generator.make_token(user) # token: Đây là một mã xác thực được tạo ra thông qua `default_token_generator.make_token(user)`. Token này là duy nhất cho mỗi người dùng và sẽ được sử dụng để xác thực liên kết kích hoạt tài khoản.
            })

            # Thông báo thành công và chuyển hướng đến trang đăng nhập
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()
            messages.success(
                request=request,
                message="Please confirm your email address to complete the registration"
            )
            return redirect('login')
        else:
            messages.error(request=request, message="Register failed!")
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == "POST":
        # Xác thực thông tin đăng nhập
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password) # Kết quả trả về là `user` hoặc `None`.

        # Liên kết giỏ hàng khi đăng nhập thành công (Trường hợp hoạt động thêm, xóa sản phẩm ở giỏ hàng ở người dùng chưa thực hiện xác thực tài khoản và id giỏ hàng chỉ lưu ở session store của máy local trước đó. Và giờ họ tiến hàng đăng nhập).
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart) # Truy vấn tất cả các mục item trong giỏ hàng chưa liên kết với người dùng

                # Xử lý sản phẩm trong giỏ hàng
                if cart_items.exists():
                    product_variation = []
                    for cart_item in cart_items:
                        variations = cart_item.variations.all() # Lấy danh sách các thuộc tính (biến thể) của từng sản phẩm trong giỏ hàng.
                        product_variation.append(list(variations))
                        # cart_item.user = user
                        # cart_item.save()
                    cart_items = CartItem.objects.filter(user=user) # Lấy danh sách các sản phẩm trong giỏ hàng đã liên kết với tài khoản người dùng.
                    existing_variation_list = [list(item.variations.all()) for item in cart_items] # Danh sách các biến thể của những sản phẩm đã liên kết
                    id = [item.id for item in cart_items] # Danh sách ID của các sản phẩm

                    for product in product_variation:
                        if product in existing_variation_list:
                            index = existing_variation_list.index(product)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()
            except Exception:
                pass
            auth.login(request=request, user=user)
            messages.success(request=request, message="Login successful!")

            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    next_page = params["next"]
                    return redirect(next_page)
            except Exception:
                return redirect('home')
        else:
            messages.error(request=request, message="Login failed!")
    context = {
        'email': email if 'email' in locals() else '',
        'password': password if 'password' in locals() else '',
    }
    return render(request, 'accounts/login.html', context=context)


@login_required(login_url="login") # The django function that ensures a user must be logged in before they can log out is @login_required
def logout(request):
    auth.logout(request)
    messages.success(request=request, message="You are logged out!")
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request=request, message="Your account is activated, please login!")
        return render(request, 'accounts/login.html')
    else:
        messages.error(request=request, message="Activation link is invalid!")
        return redirect('home')


@login_required(login_url="login")
def dashboard(request):
    return render(request, "accounts/dashboard.html")


def forgotPassword(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request=request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            send_email = EmailMessage(mail_subject, message, to=[email])
            send_email.send()

            messages.success(
                request=request, message="Password reset email has been sent to your email address")
    except Exception:
        messages.error(request=request, message="Account does not exist!")
    finally:
        context = {
            'email': email if 'email' in locals() else '',
        }
        return render(request, "accounts/forgotPassword.html", context=context)


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request=request, message='Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request=request, message="This link has been expired!")
        return redirect('home')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, message="Password reset successful!")
            return redirect('login')
        else:
            messages.error(request, message="Password do not match!")
    return render(request, 'accounts/reset_password.html')
