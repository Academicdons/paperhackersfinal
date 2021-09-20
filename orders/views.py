import string

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.forms import inlineformset_factory
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.db.models import Avg
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from .decorators import allowed_users
from django.db.models import Func
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from .forms import *
import uuid
from .utils import *
import random


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request , *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Client.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())

    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)

    posts = Post.published.all()[:2]
    reviews = Review.objects.all()[:4]

    def my_random_string(string_length=10):
        """Returns a random string of length string_length."""
        random = str(uuid.uuid4())  # Convert UUID format to a Python string.
        random = random.upper()  # Make all characters uppercase.
        random = random.replace("-", "")  # Remove the UUID '-'.
        return random[0:string_length]  # Return the random string.

    form = CreateUserForm()
    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        if form.is_valid():
            if profile_id is not None:
                recommended_by_profile = Client.objects.get(id = profile_id)

                createpassword = str(uuid.uuid4()).replace("-", "")[:12]
                createusername = str(random.randint(1000000, 9999999))

                password = createpassword
                print(password)
                print(createusername)
                user_new = form.save()
                user_new.is_admin = False
                user_new.set_password(password)
                user_new.save()
                Client.objects.create(user=user_new)
                registered_user = User.objects.get(id=user_new.id)
                registered_profile = Client.objects.get(user = registered_user)
                registered_profile.recommended_by = recommended_by_profile.user
                registered_profile.save()
                login(request, user_new)
                messages.success(request, 'Your account has been Created ' \
                                          'successfully')
            else:
                createpassword = str(uuid.uuid4()).replace("-", "")[:12]
                createusername = str(random.randint(1000000, 9999999))

                password = createpassword
                print(password)
                print(createusername)
                user_new = form.save()
                user_new.is_admin = False
                user_new.set_password(password)
                user_new.save()
                Client.objects.create(user=user_new)
                login(request, user_new)
                messages.success(request, 'Your account has been Created ' \
                                          'successfully')
            # client_email = user_new.email
            # subject_email = ['Welcome to Academic Dons']
            # subject = "Welcome To PaperHackers"
            # from_email = settings.EMAIL_HOST_USER
            # to_email = client_email
            # user = user_new.username
            #
            # context = {'password': password, 'user': user, 'client_email': client_email}
            # html_content = render_to_string('client_signup_email.html', context)  # render with dynamic value
            # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
                user_new = request.user
            user = user_new.id
            return redirect('order', pk=user)

    context = {'form': form, 'posts': posts, 'reviews': reviews}
    return render(request, 'index_new.html', context)


def about(request):
    return render(request, 'about.html')


def blogs(request):
    return render(request, 'blogs.html')


def createpass():
    createpassword = str(random.randint(1000000, 9999999))
    userpass = createpassword
    return (userpass)


#
# @login_required(login_url='writer_login')
# def createWriter(request, pk_dash):
#     writer = request.user.id
#     writer_profile = get_object_or_404(Writers, user__id=pk_dash)
#     writer_id = pk_dash
#     print(writer_id)
#     writer_pseudo = writer_profile.pseudonym
#     writer_idss = writer_id
#
#     form = CreateprofileForm(initial={'user': writer}, instance=writer_profile)
#     if request.method == 'POST':
#         form = CreateprofileForm(request.POST, instance=writer_profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created Successfully')
#
#             user_new = request.user
#             print(user_new.email)
#             # email_message = ['Thank you for signing up with us']
#             client_email = user_new.email
#             # subject_email = ['Welcome to Academic Dons']
#             subject = "Welcome To Academic-Dons"
#             from_email = settings.EMAIL_HOST_USER
#             to_email = client_email
#
#             # with open(settings.BASE_DIR + "/Order/templates/writer_update_profile.txt") as f:
#             #     signup_message = f.read()
#             # message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=[to_email])
#             # html_template = get_template('writer_update_profile.html').render()
#             #
#             # message.attach_alternative(html_template, 'text/html')
#             # message.send()
#             return redirect('writer_dashboard', pk_dash=writer_id)
#
#     context = {'form': form, 'writer_pseudo': writer_pseudo}
#     return render(request, 'client/update_profile.html', context)
#
#

def about(request):
    return render(request, 'about.html')


def botview(request, template_name="bot1.html"):
    context = {'title': 'Chatbot Version 2.0'}
    return render(request, template_name, context)


def error(request):
    return render(request, '404.html')


def superadmincreate(request):
    if request.user.is_authenticated:
        user_new = request.user
        return redirect('client_dashboard', pk_dash=user_new.id)

    else:
        form = CreateUserForm()
        if request.method == 'POST':

            form = CreateUserForm(request.POST)
            if form.is_valid():
                createpassword = str(random.randint(1000000, 9999999))
                password = createpassword
                print(password)
                user_new = form.save()
                user_new.is_admin = True
                user_new.set_password(password)
                user_new.save()
                login(request, user_new)
                messages.success(request, 'Your Account has been Created ' \
                                          'successfully')
                client_email = user_new.email
                # subject_email = ['Welcome to Academic Dons']
                subject = "Welcome To PaperHackers"
                from_email = settings.EMAIL_HOST_USER
                to_email = client_email
                user = user_new.id
                context = {'password': password, 'user': user, 'client_email': client_email}
                html_content = render_to_string('client_signup_email.html', context)  # render with dynamic value
                text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                user_new = request.user
            return redirect('admin')

    context = {'form': form}
    return render(request, 'reg.html', context)


def createpass():
    createpassword = str(random.randint(1000000, 9999999))
    userpass = createpassword
    return (userpass)


def client_registration(request):
    if request.user.is_authenticated:
        user_new = request.user
        return redirect('client_dashboard', pk_dash=user_new.id)

    else:
        form = CreateUserForm()
        if request.method == 'POST':

            form = CreateUserForm(request.POST)
            if form.is_valid():
                password = str(random.randint(1000000, 9999999))
                print('user password is ' + str(password))
                user_new = form.save()
                user_new.is_admin = False
                user_new.set_password(password)
                user_new.save()
                Client.objects.create(user=user_new)
                login(request, user_new)
                messages.success(request, 'Your account has been Created ' \
                                          'successfully')
                # client_email = user_new.email
                # # subject_email = ['Welcome to Academic Dons']
                # subject = "Welcome To PaperHackers"
                # from_email = settings.EMAIL_HOST_USER
                # to_email = client_email
                # user = user_new.id
                # context = {'password': password, 'user': user, 'client_email': client_email}
                # html_content = render_to_string('client_signup_email.html', context)  # render with dynamic value
                # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                user_new = request.user
            return redirect('order', pk=user_new.id)

    context = {'form': form}
    return render(request, 'client/signup.html', context)




def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, email=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('admin')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'signup.html', context)


def logoutUser(request):
    logout(request)
    return redirect('index')


def logoutwriter(request):
    logout(request)
    return redirect('writer_login')


def logoutadmin(request):
    logout(request)
    return redirect('admin_login')


# def Order_Details(request):
#     return render(request, 'index.html')
def post_list(request):
    posts = Post.published.all()
    object_list = Post.published.all()

    paginator = Paginator(object_list, 4)  # 5 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blogs.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    posts = Post.published.all().reverse()[:3]
    new_comment = None
    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request,
                  'blogDetails.html',
                  {'post': post,
                   'comments': comments, 'posts': posts,
                   'new_comment': new_comment,
                   'comment_form': comment_form})


def Writer_Dashboard(request):
    return render(request, 'writer_dashboard.html')


def rep_dashboard(request):
    return render(request, 'rep_dashboard.html')




def Support_profile(request, pk_support):
    client_profile = Support.objects.get(id=pk_support)
    orders = Order.objects.filter(support=client_profile).order_by('-id')
    Support_name = Support.objects.filter(name=client_profile).get()

    context = {'Support_names': Support_name, 'customer': client_profile, 'orders': orders}
    return render(request, 'support.html', context)










def new_writer_login(request):
    if request.user.is_authenticated:
        user = request.user
        return redirect('writer_dashboard', pk_dash=user.id)
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Your Profile has been Created ' \
                                          'successfully')
                return redirect('writer_update_profile', pk_dash=user.id)
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'writers/login.html', context)


def writer_login(request):
    if request.user.is_authenticated:
        user = request.user
        return redirect('writer_dashboard', pk_dash=user.id)
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged In ' \
                                          'successfully')
                return redirect('writer_dashboard', pk_dash=user.id)
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}

        return render(request, 'writers/login.html', context)


def writer_registration_view(request):
    if request.user.is_authenticated:
        user_new = request.user
        return redirect('writer_dashboard', pk_dash=user_new.id)

    else:
        form = CreateUserForm()
        if request.method == 'POST':

            form = CreateUserForm(request.POST)
            if form.is_valid():
                createpassword = str(random.randint(1000000, 9999999))
                password = createpassword
                userpass = "password"
                print(password)
                user_new = form.save()
                user_new.is_admin = False
                user_new.set_password(userpass)
                user_new.save()
                Writers.objects.create(user=user_new)
                login(request, user_new)
                print('Profile Created Successfully')
                messages.success(request, 'Your Account has been Created ' \
                                          'successfully')
                client_email = user_new.email
                # subject_email = ['Welcome to Academic Dons']
                # subject = "Welcome To PaperHackers"
                # from_email = settings.EMAIL_HOST_USER
                # to_email = client_email
                # user = user_new.id
                # context = {'userpass': userpass, 'user': user, 'client_email': client_email}
                # html_content = render_to_string('writer_signup_email.html', context)  # render with dynamic value
                # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
                # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                # msg.attach_alternative(html_content, "text/html")
                # msg.send()
                user_new = request.user
            return redirect('writer_update_profile', pk_dash=user_new.id)

    context = {'form': form}
    return render(request, 'writers/signup.html', context)

@login_required(login_url='writer_login')
def writer_profile(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_ordersss = Order.objects.filter(writer=writer_profile).order_by('-id')

    writer_orders_all = writer_ordersss.filter(order_status='Completed')
    writer_orders = writer_ordersss.filter(order_status='Completed')[:3]
    writer_orders_cancelled = writer_ordersss.filter(order_status='Cancelled')
    writer_orders_Inprogress = writer_ordersss.filter(order_status='Cancelled')

    Total_Orders_in_cancelled = writer_orders_cancelled.count()
    Total_Orders_in_progress = writer_orders_Inprogress.count()
    Total_Orders_in_completed = writer_orders_all.count()

    # writer_rating = Total_Orders_in_completed.annotate(avg_review=Round(Avg('writer_ratings__writerRating')))
    writer_name = writer_profile.pseudonym
    print('your psesudo is' ,writer_name)
    writer_dpic = writer_profile.image
    writer_level = writer_profile.writer_quality
    writer_decription = writer_profile.description

    context = {'writer_name': writer_name,
               # 'writer_rating': writer_rating,
               'writer': writer_profile, 'writer_id': writer_id, 'writer_dpic': writer_dpic,
               'Total_Orders_in_cancelled': Total_Orders_in_cancelled,
               'writer_orders_all': writer_orders_all,
               'Total_Orders_in_completed': Total_Orders_in_completed,
               'writer_level': writer_level, 'writer_decription': writer_decription,
               'Total_Orders_in_progress': Total_Orders_in_progress, 'writer_orders': writer_orders}
    return render(request, 'writers/profile.html', context)


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 0)'




# writers dashboard. Pardon the naming
@login_required(login_url='writer_login')
def Order_List(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_orders = Order.objects.filter(writer=writer_profile).order_by('-id')
    writer_names = writer_profile.pseudonym
    writer = pk_dash
    writer_id = writer

    print('you pseudo is', writer_names)

    # bids = Bids.writers.all()

    writer_name = writer_profile.pseudonym
    orders_in_progress = writer_orders.filter(order_status='Writer Assigned')
    orders_in_paid = Order.objects.filter(order_status='Paid')
    orders_in_Delivered = writer_orders.filter(order_status='Delivered')
    orders_in_Revision = writer_orders.filter(order_status='Revision')
    orders_in_Cancelled = writer_orders.filter(order_status='Cancelled')
    orders_in_Completed = writer_orders.filter(order_status='Completed')

    Total_Orders_paid = orders_in_paid.count()
    Total_Orders_in_progress = orders_in_progress.count()
    Total_Orders_in_Delivered = orders_in_Delivered.count()
    Total_Orders_in_revisions = orders_in_Revision.count()
    Total_Orders_in_canceled = orders_in_Cancelled.count()
    Total_Orders_in_completed = orders_in_Completed.count()

    context = {'writer_name': writer_name, 'writer_profile': writer_profile, 'writer_id': writer_id,
               'writer_orders': orders_in_progress,
               'writer': writer,
               'Delivered': orders_in_Delivered, 'revision': orders_in_Revision,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'Canceled': orders_in_Cancelled, 'completed': orders_in_Completed,

               'orders_in_paid': orders_in_paid,
               'Total_Orders_paid': Total_Orders_paid,
               'Total_Orders_in_Delivered': Total_Orders_in_Delivered,
               'Total_Orders_in_revisions': Total_Orders_in_revisions,
               'Total_Orders_in_canceled': Total_Orders_in_canceled,
               'Total_Orders_in_completed': Total_Orders_in_completed,
               }
    return render(request, 'writers/index.html', context)


# def client_dashboard(request, pk_dash):
# client_profile = get_object_or_404(Client, user__id=pk_dash)


@login_required(login_url='writer_login')
def Writer_Orders_Delivered(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_orders = Order.objects.filter(writer=writer_profile).order_by('-id')
    writer_name = writer_profile.pseudonym
    orders_in_Delivered = writer_orders.filter(order_status='Delivered')

    context = {'writer_name': writer_name, 'writer': writer_profile, 'writers_id': writer_idss, 'writer_id': writer_id,
               'orders_in_Delivered': orders_in_Delivered, 'writer_profile': writer_profile}
    return render(request, 'writers/delivered_orders.html', context)


@login_required(login_url='writer_login')
def AvailableOrders(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_orders = Order.objects.order_by('-id')
    writer_name = writer_profile.pseudonym
    orders_in_Delivered = writer_orders.filter(order_status='Paid')

    context = {'writer_name': writer_name, 'writer': writer_profile, 'writers_id': writer_idss, 'writer_id': writer_id,
               'available_orders': orders_in_Delivered, 'writer_profile': writer_profile}
    return render(request, 'writers/available.html', context)


@login_required(login_url='writer_login')
def Writer_Orders_Revision(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_orders = Order.objects.filter(writer=writer_profile).order_by('-id')
    writer_name = writer_profile.pseudonym
    orders_in_Delivered = writer_orders.filter(order_status='Revision')

    context = {'writer_name': writer_name, 'writer': writer_profile, 'writers_id': writer_idss, 'writer_id': writer_id,
               'Delivered': orders_in_Delivered, 'writer_profile': writer_profile}
    return render(request, 'writers/revisions.html', context)


@login_required(login_url='writer_login')
def Writer_Orders_Cancelled(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_orders = Order.objects.filter(writer=writer_profile).order_by('-id')
    writer_name = writer_profile.pseudonym
    orders_in_Delivered = writer_orders.filter(order_status='Cancelled')

    context = {'writer_name': writer_name, 'writer': writer_profile, 'writers_id': writer_idss, 'writer_id': writer_id,
               'Delivered': orders_in_Delivered, 'writer_profile': writer_profile}
    return render(request, 'writers/cancelled.html', context)


@login_required(login_url='writer_login')
def Writer_completed_orders(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_orders = Order.objects.filter(writer=writer_profile).order_by('-id')
    writer_name = writer_profile.pseudonym
    orders_in_Delivered = writer_orders.filter(order_status='Completed')

    context = {'writer_name': writer_name, 'writer': writer_profile, 'writers_id': writer_idss, 'writer_id': writer_id,
               'Delivered': orders_in_Delivered, 'writer_profile': writer_profile}
    return render(request, 'writers/completed.html', context)


@login_required(login_url='writer_login')
def Writer_Orders_in_progress(request, pk_dash):
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_idss = writer_id

    writer_orders = Order.objects.filter(writer=writer_profile).order_by('-id')
    writer_name = writer_profile.pseudonym
    orders_in_Delivered = writer_orders.filter(order_status='Writer Assigned')

    context = {'writer_name': writer_name, 'writer': writer_profile, 'writers_id': writer_idss, 'writer_id': writer_id,
               'orders_in_Delivered': orders_in_Delivered, 'writer_profile': writer_profile}
    return render(request, 'writers/progress.html', context)


@login_required(login_url='writer_login')
def Writer_assigned_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    writer_id = request.user.id
    user = writer_profile
    print('writer id is', writer_id)

    return render(request, 'writers/progres_view.html',
                  {'order': Orders, 'writer_id': writer_id,},
                  )


@login_required(login_url='writer_login')
def Writer_delivered_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    writer_id = request.user.id

    return render(request, 'writers/delivered_details.html',
                  {'order': Orders, 'writer_id': writer_id,},
                  )


@login_required(login_url='writer_login')
def Writer_revision_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    writer_id = request.user.id

    return render(request, 'writers/revision_details.html',
                  {'order': Orders, 'writer_id': writer_id,},
                  )


@login_required(login_url='writer_login')
def Writer_canceled_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    writer_id = request.user.id


    return render(request, 'writers/cancelled_details.html',
                  {'order': Orders, 'writer_id': writer_id,},
                  )


@login_required(login_url='writer_login')
def Writer_completed_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    writer_id = request.user.id


    return render(request, 'writers/completed_details.html',
                  {'order': Orders, 'writer_id': writer_id,},
                  )

@login_required(login_url='writer_login')
def Writer_available_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    writer_id = request.user.id
    writer = get_object_or_404(Writers, user__id=writer_id)
    print('writer id is', writer)
    form = TakeOrder(initial={'writer': writer}, instance=writer)
    if request.method == 'POST':
        form = TakeOrder(request.POST, initial={'writer': writer}, instance=writer)
        if form.is_valid():
            writer_new = form.save(commit=False)
            writer_new = form.cleaned_data.get('writer')

            writer_new.save()
            print('saving order')

        else:
            return redirect('404')
            print('did not save order')
            messages.error(request, 'Error taking the Order')

        return redirect('take', order_id=pk_writerdetails)



    return render(request, 'writers/available_details.html',
                  {'order': Orders, 'writer_id': writer_id,'form':form},
                  )


@login_required(login_url='writer_login')
def writer_complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    order.order_status = 'Delivered'
    order.save()
    writer_id = user.id
    messages.success(request, 'Order Completed  ' \
                              'successfully')
    return redirect('writer_delivered_orders', pk_dash=user.id)



@login_required(login_url='writer_login')
def take_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    writer = Writers.objects.get(user=user)
    order.order_status = 'Writer Assigned'
    order.set_writer = user
    order.save()

    messages.success(request, 'Order taken ' \
                                      'successfully')
    return redirect('Writer_assigned_order_details', pk_writerdetails=order)
























def client_login(request):
    if request.user.is_authenticated:
        user = request.user
        return redirect('client_dashboard', pk_dash=user.id)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, email=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Welcome' \
                                          'Back')
                try:
                    user = request.user
                    client = Client.objects.filter(user=user)
                    pending_orders = Order.objects.get(customer=client).filter(order_status='Pending Payment').count()
                    if pending_orders >=1:
                        return redirect('clientPending', pk_dash=user.id)
                    else:
                        return redirect('client_paid', pk_dash=user.id)
                except:
                    print('mi sijui niko wapi')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'client/login.html', context)


def client_dashboard(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)
    client_refferal = client_profile.recommended_by
    client_refferal_name = client_refferal
    print(client_refferal_name)

    # client_orders = Order.objects.filter(customer=writer_profile).order_by('-id')
    client_name = client_profile.name
    #  orders_in_progress = client_orders.filter(order_status='Writer Assigned')
    #   orders_in_Delivered = client_orders.filter(order_status='Delivered')
    #   orders_in_Revision = client_orders.filter(order_status='Revision')
    #  orders_in_Cancelled = client_orders.filter(order_status='Cancelled')
    #  orders_in_Completed = client_orders.filter(order_status='Completed')

    client_orders = Order.objects.filter(customer=client_profile).order_by('-id')
    client = pk_dash
    client_id = client

    client_name = client_profile.name
    client_id_get = client_profile.id

    orders_in_unpaid = client_orders.filter(order_status='Pending Payment')
    orders_in_paid = client_orders.filter(order_status='Paid')
    orders_in_progress = client_orders.filter(order_status='Writer Assigned')
    orders_in_Delivered = client_orders.filter(order_status='Delivered')
    orders_in_Revision = client_orders.filter(order_status='Revision')
    orders_in_Cancelled = client_orders.filter(order_status='Cancelled')
    orders_in_Completed = client_orders.filter(order_status='Completed')

    Total_Orders_in_unpaid = orders_in_unpaid.count()
    Total_Orders_in_paid = orders_in_paid.count()
    Total_Orders_in_progress = orders_in_progress.count()
    Total_Orders_in_Delivered = orders_in_Delivered.count()
    Total_Orders_in_revisions = orders_in_Revision.count()
    Total_Orders_in_canceled = orders_in_Cancelled.count()
    Total_Orders_in_completed = orders_in_Completed.count()
    print(Total_Orders_in_unpaid)
    print(Total_Orders_in_paid)

    context = {'writer_name': client_name, 'writer': writer_profile, 'Total_Orders_in_unpaid': Total_Orders_in_unpaid,
               'Total_Orders_in_paid': Total_Orders_in_paid, 'client_id_get': client_id_get, 'client_id': client_id,
               'writer_orders': orders_in_progress,
               'Delivered': orders_in_Delivered, 'revision': orders_in_Revision,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'Canceled': orders_in_Cancelled, 'completed': orders_in_Completed, 'client_profile': client_profile,
               'Total_Orders_in_Delivered': Total_Orders_in_Delivered,
               'Total_Orders_in_revisions': Total_Orders_in_revisions,'client_refferal_name': client_refferal_name,
               'Total_Orders_in_canceled': Total_Orders_in_canceled,
               'Total_Orders_in_completed': Total_Orders_in_completed,
               }
    return render(request, 'client_dashboard.html', context)

@login_required(login_url='client_login')
def client_profile(request, pk_profile):
    client_profile = Client.objects.get(id=pk_profile)
    orders = Order.objects.filter(customer=client_profile).order_by('-id')
    order_count = orders.count()

    client_name = client_profile.name

    context = {'client_name': client_name, 'customer': client_profile, 'orders_count': order_count, 'orders': orders}
    return render(request, 'client.html', context)


def client_pending_order_details(request, pk_writerdetails):
    client_id = request.user.id
    Orders = Order.objects.get(id=pk_writerdetails)


    return render(request, 'client/unpaid.html',
                  {'order': Orders, 'client_id': client_id, },
                  )


def client_delivered_order_details(request, pk_writerdetails):
    client_id = request.user.id
    Orders = Order.objects.get(id=pk_writerdetails)

    return render(request, 'client/delivered.html',
                  {'order': Orders, 'client_id': client_id, },
                  )


def client_revision_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    client_id = request.user.id

    return render(request, 'client/revision.html',
                  {'order': Orders, 'client_id': client_id, },
                  )
def client_paid_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    client_id = request.user.id

    return render(request, 'client/revision.html',
                  {'order': Orders, 'client_id': client_id, },
                  )
def client_assigned_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    client_id = request.user.id

    return render(request, 'client/assigned.html',
                  {'order': Orders, 'client_id': client_id, },
                  )


def client_cancelled_order_details(request, pk_writerdetails):
    client_id = request.user.id

    Orders = Order.objects.get(id=pk_writerdetails)

    return render(request, 'client/cancelled.html',
                  {'order': Orders, 'client_id': client_id, },
                  )


def client_completed_order_details(request, pk_writerdetails):
    client_id = request.user.id

    Orders = Order.objects.get(id=pk_writerdetails)

    return render(request, 'client/complete.html',
                  {'order': Orders, 'client_id': client_id, },
                  )


@login_required(login_url='client_login')
def clientPending(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    # client_orders = Order.objects.filter(customer=writer_profile).order_by('-id')
    client_name = client_profile.name
    #  orders_in_progress = client_orders.filter(order_status='Writer Assigned')
    #   orders_in_Delivered = client_orders.filter(order_status='Delivered')
    #   orders_in_Revision = client_orders.filter(order_status='Revision')
    #  orders_in_Cancelled = client_orders.filter(order_status='Cancelled')
    #  orders_in_Completed = client_orders.filter(order_status='Completed')

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    client_code = client_profile.code
    orders_in_progress = client_orders.filter(order_status='Pending Payment')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'writer_orders': orders_in_progress,
               'client_code': client_code,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/orders_assigned_list.html', context)



@login_required(login_url='client_login')
def clientavailable(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    client_name = client_profile.name

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    client_code = client_profile.code

    orders_in_progress = client_orders.filter(order_status='Paid')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'writer_orders': orders_in_progress,
               'client_code': client_code,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/paid_list.html', context)


@login_required(login_url='writer_login')
def client_revise_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    id = order_id
    order.order_status = 'Revision'
    order.save()
    return redirect('client_revision_order_details', pk_writerdetails=id)


@login_required(login_url='writer_login')
def client_complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    id = order_id
    order.order_status = 'Completed'
    order.save()
    return redirect('client_completed_order_details', pk_writerdetails=id)


@login_required(login_url='writer_login')
def client_cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    id = order_id
    order.order_status = 'Cancelled'
    order.save()
    return redirect('client_cancelled_order_details', pk_writerdetails=id)


@login_required(login_url='client_login')
def clientRevisions(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    # client_orders = Order.objects.filter(customer=writer_profile).order_by('-id')
    client_name = client_profile.name
    client_code = client_profile.code
    #  orders_in_progress = client_orders.filter(order_status='Writer Assigned')
    #   orders_in_Delivered = client_orders.filter(order_status='Delivered')
    #   orders_in_Revision = client_orders.filter(order_status='Revision')
    #  orders_in_Cancelled = client_orders.filter(order_status='Cancelled')
    #  orders_in_Completed = client_orders.filter(order_status='Completed')

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    orders_in_progress = client_orders.filter(order_status='Revision')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'writer_orders': orders_in_progress,
               'client_code': client_code,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/revision_list.html', context)


@login_required(login_url='client_login')
def clientCompleted(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    # client_orders = Order.objects.filter(customer=writer_profile).order_by('-id')
    client_name = client_profile.name
    client_code = client_profile.code
    #  orders_in_progress = client_orders.filter(order_status='Writer Assigned')
    #   orders_in_Delivered = client_orders.filter(order_status='Delivered')
    #   orders_in_Revision = client_orders.filter(order_status='Revision')
    #  orders_in_Cancelled = client_orders.filter(order_status='Cancelled')
    #  orders_in_Completed = client_orders.filter(order_status='Completed')

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    orders_in_progress = client_orders.filter(order_status='Completed')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'client_code': client_code,
               'writer_orders': orders_in_progress,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/completed_list.html', context)


@login_required(login_url='client_login')
def clientCancelled(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    client_code = client_profile.code
    orders_in_progress = client_orders.filter(order_status='Cancelled')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'client_code': client_code,
               'writer_orders': orders_in_progress,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/canceled_list.html', context)


@login_required(login_url='client_login')
def clientDelivered(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    client_code = client_profile.code
    orders_in_progress = client_orders.filter(order_status='Delivered')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'writer_orders': orders_in_progress,
               'client_code': client_code,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/delivered_list.html', context)


@login_required(login_url='client_login')
def clientAssigned(request, pk_dash):
    client_profile = get_object_or_404(Client, user__id=pk_dash)

    client_orders = Order.objects.filter(customer=client_profile).order_by('-pub_date')
    client = pk_dash
    print(client)
    client_id = client
    print(client_id)

    client_name = client_profile.name
    client_code = client_profile.code
    orders_in_progress = client_orders.filter(order_status='Writer Assigned')

    Total_Orders_in_progress = orders_in_progress.count()

    context = {'writer_name': client_name, 'writer': writer_profile, 'client_id': client_id,
               'writer_orders': orders_in_progress,
               'client_code': client_code,
               'Total_Orders_in_progress': Total_Orders_in_progress,
               'client_profile': client_profile
               }
    return render(request, 'client/assigned_list.html', context)


def createOrder(request, pk):
    # client_profile = get_object_or_404(Client, user__id=pk)

    # client_orders = Order.objects.filter(customer=writer_profile).order_by('-id')
    #  orders_in_progress = client_orders.filter(order_status='Writer Assigned')
    #   orders_in_Delivered = client_orders.filter(order_status='Delivered')
    #   orders_in_Revision = client_orders.filter(order_status='Revision')
    #  orders_in_Cancelled = client_orders.filter(order_status='Cancelled')
    #  orders_in_Completed = client_orders.filter(order_status='Completed')
    client_profile = get_object_or_404(Client, user__id=pk)
    transaction_id = datetime.now().timestamp()

    client = pk
    client_id = client
    client_name = client_profile.name

    form = ClientorderForm(initial={'customer': client_profile})
    Order.customorderID = transaction_id
    if request.method == 'POST':
        # print('Printing POST', request.POST)
        form = ClientorderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Created ' \
                                      'successfully')
            # user_new = request.user
            # client_email = client_profile.email
            # subject_email = ['Welcome to Academic Dons']
            # subject = "Order Created Successfully"
            # from_email = settings.EMAIL_HOST_USER
            # to_email = client_email
            # user = user_new.id
            # context = {'user': user, 'client_email': client_email}
            # html_content = render_to_string('client_place_order_email.html', context)  # render with dynamic value
            # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            user = pk
            print(user)
            orderid1 = Order.objects.filter(customer=user).first()
            orderid = orderid1
            print(orderid)
            print('message sent')
            return redirect('client_checkout_redirect')

        else:
            user = pk
            messages.error(request, 'Error creating your Order')
            return redirect('order', pk=user)


    context = {'form': form, 'client_name': client_name}
    return render(request, 'client_order_form_new.html', context)


def checkout_redirect(request):
    user = request.user
    client = Client.objects.get(user=user)
    order = Order.objects.filter(customer= client).latest('id')
    order_id = order

    return redirect('client_checkout', order_id=order_id)

def client_checkout(request, order_id):
    clientid = request.user
    client_id = clientid.id
    order = get_object_or_404(Order, id=order_id)
    print(order)

    return render(request, 'client/checkout.html',
                  {'order': order, 'client_id':client_id,},
                  )


def processOrder(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    user = request.user
    total = order.calculate_total_price
    if total == order.calculate_total_price:
        order.order_status = 'Paid'
        order.save()
        messages.success(request, 'Order Created ' \
                                  'successfully')
    else:
        messages.error(request, 'Error creating your Order')
    return redirect('client_paid', pk_dash=user.id)


























@login_required(login_url='writer_login')
def Order_admin(request):
    admin_orders = Order.objects.all().order_by('pub_date').reverse()[:5]

    admin_clients = Client.objects.all().order_by('id').reverse()[:3]
    admin_writer = Writers.objects.all().order_by('id').reverse()[:3]
    admin_Support = Support.objects.all().order_by('id').reverse()[:3]

    Order_count = Order.objects.count()
    Clients_count = Client.objects.count()
    Writers_count = Writers.objects.count()

    context = {'Writers_counts': Writers_count, 'admin_Supports': admin_Support,
               'Clients_counts': Clients_count, 'Order_counts': Order_count, 'admin_order': admin_orders,
               'admin_client': admin_clients, 'admin_writers': admin_writer}
    return render(request, 'admin_dash.html', context)


@login_required(login_url='writer_login')
def adminunpaid(request):
    orders = Order.objects.all().order_by('pub_date').reverse()
    orders_in_bided = orders.filter(order_status='Pending Payment')
    admin_orders = orders_in_bided

    return render(request, 'adminunpaid.html', {'orders_in_bided': orders_in_bided, 'admin_orders': admin_orders})


@login_required(login_url='writer_login')
def adminbidded(request):
    orders = Order.objects.all().order_by('-pub_date')
    orders_in_bided = orders.filter(order_status='Paid')
    admin_orders = orders_in_bided

    return render(request, 'admin_bidded.html', {'orders_in_bided': orders_in_bided, 'admin_orders': admin_orders})


@login_required(login_url='writer_login')
def admin_progress(request):
    orders = Order.objects.all().order_by('-pub_date')
    orders_in_bided = orders.filter(order_status='Writer Assigned')

    return render(request, 'admin_proress.html', {'orders_in_bided': orders_in_bided})


@login_required(login_url='writer_login')
def admindelivered(request):
    orders = Order.objects.all().order_by('-pub_date')
    orders_in_bided = orders.filter(order_status='Delivered')

    return render(request, 'admin_delivered.html', {'orders_in_bided': orders_in_bided})


@login_required(login_url='writer_login')
def adminrevision(request):
    orders = Order.objects.all().order_by('-pub_date')
    orders_in_bided = orders.filter(order_status='Revision')

    return render(request, 'admin_revision.html', {'orders_in_bided': orders_in_bided})


@login_required(login_url='writer_login')
def admincancelled(request):
    orders = Order.objects.all().order_by('-pub_date')
    orders_in_bided = orders.filter(order_status='Cancelled')

    return render(request, 'admin_cancelled.html', {'orders_in_bided': orders_in_bided})


@login_required(login_url='writer_login')
def admincompleted(request):
    orders = Order.objects.all().order_by('-pub_date')
    orders_in_bided = orders.filter(order_status='Completed')

    return render(request, 'admin_completed.html', {'orders_in_bided': orders_in_bided})


@login_required(login_url='writer_login')
def Writer_List(request):
    admin_writer = Writers.objects.all().order_by('pub_date').reverse()

    return render(request, 'writer_list.html', {'admin_writers': admin_writer})


@login_required(login_url='writer_login')
def admin_assign_Order(request, pk):
    order = Order.objects.get(id=pk)
    form = adminUpdateorderForm(instance=order, initial={'order_status': 'Writer Assigned'})
    if request.method == 'POST':
        form = adminUpdateorderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin')

    context = {'form': form}
    return render(request, 'assignwriter.html', context)


@login_required(login_url='writer_login')
def writer_revise_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.order_status = 'Revision'
    order.save()
    messages.success(request, 'Order updated ' \
                              'successfully')

    return redirect('adminrevision')


@login_required(login_url='writer_login')
def admin_complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.order_status = 'Completed'
    order.save()
    messages.success(request, 'Order updated ' \
                              'successfully')
    return redirect('admincompleted')


def Writer_order_details(request, pk_writerdetails):
    Orders = Order.objects.get(id=pk_writerdetails)
    print(Orders.id)

    return render(request, 'writer_Order_Details.html', {'order': Orders})


def Support_List(request):
    admin_Support = Support.objects.all().order_by('id').reverse()[:3]
    return render(request, 'support_list.html', {'admin_Supports': admin_Support})


@login_required(login_url='client_login')
def Client_List(request):
    admin_clients = Client.objects.all().order_by('id').reverse()

    return render(request, 'client_list.html', {'admin_client': admin_clients})


def Writer_List(request):
    admin_writer = Writers.objects.all().order_by('id').reverse()

    return render(request, 'writer_list.html', {'admin_writers': admin_writer})


@login_required(login_url='writer_login')
def admincreateOrder(request):
    form = ClientorderForm()
    if request.method == 'POST':
        # print('Printing POST', request.POST)
        form = ClientorderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order Created ' \
                                      'successfully')
        else:
            messages.error(request, 'Error creating your Order')
            user_new = request.user
            client_email = user_new.email
            # subject_email = ['Welcome to Academic Dons']
            # subject = "Welcome To PaperHackers"
            # from_email = settings.EMAIL_HOST_USER
            # to_email = client_email
            # user = user_new.id
            # context = {'user': user, 'client_email': client_email}
            # html_content = render_to_string('admin_place_order_email.html', context)  # render with dynamic value
            # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
            print('message sent')

        return redirect('admin')

    context = {'form': form}
    return render(request, 'client_order_form_new.html', context)


def createclient(request):
    form = ClientForm()

    if request.method == 'POST':
        # print('Printing POST', request.POST)
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Client Created ' \
                                      'successfully')
        else:
            messages.error(request, 'Error creating Client')
            user_new = request.user
            client_email = user_new.email
            # subject_email = ['Welcome to Academic Dons']
            # subject = "Welcome To PaperHackers"
            # from_email = settings.EMAIL_HOST_USER
            # to_email = client_email
            # user = user_new.id
            # context = {'user': user, 'client_email': client_email}
            # html_content = render_to_string('admin_place_order_email.html', context)  # render with dynamic value
            # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()
        return redirect('admin')

    context = {'form': form}
    return render(request, 'clientForm_form.html', context)


@login_required(login_url='writer_login')
def createWriter(request, pk_dash):
    writer = request.user.id
    writer_profile = get_object_or_404(Writers, user__id=pk_dash)
    writer_id = pk_dash
    print(writer_id)
    writer_pseudo = writer_profile.pseudonym
    writer_idss = writer_id

    form = CreateprofileForm(initial={'user': writer}, instance=writer_profile)
    if request.method == 'POST':
        form = CreateprofileForm(request.POST, request.FILES, instance=writer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created Successfully')

            user_new = request.user
            print(user_new.email)
            # # email_message = ['Thank you for signing up with us']
            # client_email = user_new.email
            # # subject_email = ['Welcome to Academic Dons']
            # subject = "Welcome To Academic-Dons"
            # from_email = settings.EMAIL_HOST_USER
            # to_email = client_email
            # user = user_new.id
            # context = {'user': user, 'client_email': client_email}
            # html_content = render_to_string('writer_update_profile.html', context)  # render with dynamic value
            # text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.
            # msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            #
            #
            # msg.attach_alternative(html_content, 'text/html')
            # msg.send()
            writer=request.user
            writer_id=writer.id
        writer_id=writer_id
        return redirect('writer_dashboard', pk_dash=writer_id)

    context = {'form': form, 'writer_pseudo': writer_pseudo, 'writer_id':writer_id}
    return render(request, 'writers/update_profile.html', context)


def createTodo(request):
    form = todo()
    if request.method == 'POST':
        # print('Printing POST', request.POST)
        form = todo(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin')

    context = {'form': form}
    return render(request, 'todoform.html', context)


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = AdminOrderForm(instance=order)
    if request.method == 'POST':
        form = AdminOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin')

    context = {'form': form}
    return render(request, 'Order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('admin')
    context = {'item': order}
    return render(request, 'delete.html', context)


def services(request):
    return HttpResponse('services')
