from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_user_reviews
from django.contrib.auth import login, logout, authenticate, get_user
import logging
import uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {'navbar': 'about'}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {'navbar': 'contact'}
    if request.method == "GET":
        return render(request, 'djangoapp/contact_us.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def get_dealerships(request):
    '''
    GET all dealerships with cloud function
    '''
    context = {'navbar': 'home'}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/77ec479f-bcfa-4ab2-8b39-03ba98a9125c/default/getAllDealerships"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        # dealer_names = ','.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        context['dealers'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealer_details(request, dealer_id):
    '''
    render the reviews of a dealer using a cloud functions
    '''
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/77ec479f-bcfa-4ab2-8b39-03ba98a9125c/default/getReviewsByDealerId"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['dealer_reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)


def add_review(request, dealer_id):
    '''submit a review
    '''
    context = {}
    user = request.user

    if user.is_authenticated:
        review = {}

        id = str(uuid.uuid4())
        review["doc_id"] = id
        review["name"] = get_user(request).username
        review["dealership"] = dealer_id
        review["review"] = request.POST['review']
        review["purchase"] = request.POST['purchase']
        review["purchase_date"] = request.POST['purchase_date']
        review["car_make"] = request.POST['car_make']
        review["car_model"] = request.POST['car_model']
        review["car_year"] = request.POST['car_year']

        post_review_result = post_user_reviews(review)
        if post_review_result:
            return redirect('djangoapp:dealer_details', dealer_id)
