from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value
from itertools import chain

from authentication.models import User
from website.models import Review, UserFollows, Ticket
from website import forms


@login_required
def flux(request):
    """
    Manage the feed, to show their own and subscribers' tickets and reviews
    """

    # Get the IDs of users followed by the logged-in user
    users_followed_ids = UserFollows.objects.filter(user=request.user).values_list('followed_user', flat=True)

    # Get reviews of users followed by the logged-in user
    reviews_followed = Review.objects.filter(user__in=users_followed_ids)

    # Get tickets of the logged-in user and users followed
    tickets_user_and_followed = Ticket.objects.filter(user__in=[request.user] + list(users_followed_ids))

    # Get reviews from tickets of the logged-in user
    reviews_from_tickets = Review.objects.filter(ticket__in=tickets_user_and_followed)

    # Get reviews of the logged-in user (excluding reviews from tickets not followed)
    reviews_user = Review.objects.filter(user=request.user).exclude(pk__in=reviews_from_tickets)

    # Annotate the type of content for each type of object
    reviews_user = reviews_user.annotate(content_type=Value('REVIEW', CharField()))
    reviews_followed = reviews_followed.annotate(content_type=Value('REVIEW', CharField()))
    reviews_from_tickets = reviews_from_tickets.annotate(content_type=Value('REVIEW', CharField()))

    # Get tickets already answered by reviews
    tickets_already_answer = Ticket.objects.filter(review__in=reviews_followed)

    # Combine all objects (reviews and tickets) and sort by date of creation
    posts = sorted(chain(reviews_user, reviews_followed, reviews_from_tickets, tickets_user_and_followed),
                   key=lambda post: post.time_created, reverse=True)

    return render(request, 'website/flux.html', context={'posts': posts, 'tickets_already_answer': tickets_already_answer})


@login_required
def create_ticket(request):
    """
    Permit to create a new ticket
    """
    ticket_form = forms.TicketForm()
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    context = {"ticket_form": ticket_form}
    return render(request, 'website/create_ticket.html', context=context)


@login_required
def create_review(request):
    """
    Permet de créer une nouvelle review avec un ticket associé
    """
    if request.method == "POST":
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        review_form = forms.ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect('flux')
    else:
        ticket_form = forms.TicketForm()
        review_form = forms.ReviewForm()

    context = {"review_form": review_form, "ticket_form": ticket_form}
    return render(request, 'website/create_review.html', context=context)



@login_required
def create_review_from_ticket(request, ticket_id):
    """
    Permet de créer une review en réponse à un ticket
    """
    ticket = None
    review_form = forms.ReviewForm()

    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        if request.method == "POST":
            review_form = forms.ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.ticket = ticket
                review.save()
                return redirect('flux')
    except UnboundLocalError:
        return redirect('flux')
    except Ticket.DoesNotExist:
        return redirect('flux')

    return render(request, 'website/create_review_from_ticket.html', context={"ticket": ticket, "review_form": review_form})



@login_required
def display_posts(request):
    """
    Display all ticket et review from user connected
    """
    tickets = Ticket.objects.filter(user=request.user)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    reviews = Review.objects.filter(user=request.user)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    posts = sorted(chain(reviews, tickets),
                   key=lambda post: post.time_created, reverse=True)
    return render(request, 'website/posts.html', context={"posts": posts})


@login_required
def follow_users(request):
    """
    Manage the subscription system
    """
    users_follow_you = [user_follow.user.username for user_follow in
                        UserFollows.objects.filter(followed_user=request.user.id)]

    users_followed = UserFollows.objects.filter(user_id=request.user)
    users_to_exclude = [user_followed.followed_user.username for user_followed in users_followed]
    users_to_exclude.append(request.user.username)
    users_to_follow = User.objects.exclude(username__in=users_to_exclude)
    if request.method == "POST":
        to_follow = User.objects.get(pk=request.POST["to_follow"])
        if to_follow in users_to_follow:
            UserFollows(user=request.user, followed_user=to_follow).save()
    users_followed = UserFollows.objects.filter(user_id=request.user)
    return render(request, 'website/follow_users.html', context={"users_followed": users_followed,
                                                                 "users_to_follow": users_to_follow,
                                                                 "users_follow_you": users_follow_you})


@login_required
def delete_follow_user(request, user_id):
    """
        Delete a follow user
    """
    try:
        user_follow = UserFollows.objects.get(user=request.user, followed_user=user_id)
    except UserFollows.DoesNotExist:
        return redirect('follow_users')
    if request.method == "POST":
        user_follow.delete()
        return redirect('follow_users')


@login_required
def delete_review(request, review_id):
    """
        Delete a review
    """
    try:
        review = Review.objects.get(pk=review_id)
        if review.user != request.user:
            return redirect('posts')
    except UserFollows.DoesNotExist:
        return redirect('posts')
    if request.method == "POST":
        review.delete()
        return redirect('posts')


@login_required
def update_review(request, review_id):
    """
        Modifie a review
    """
    try:
        review = Review.objects.get(pk=review_id)
        if review.user != request.user:
            return redirect('posts')
    except Review.DoesNotExist:
        return redirect('posts')

    review_form = forms.ReviewForm(instance=review)
    if request.method == "POST":
        update_form = forms.ReviewForm(request.POST)
        if update_form.is_valid():
            review_updated = update_form.save()
            return redirect('posts')
    context = {"review_form": review_form}
    return render(request, 'website/update_review.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    """
        Delete a review
    """
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        if ticket.user != request.user:
            return redirect('posts')
    except UserFollows.DoesNotExist:
        pass
    if request.method == "POST":
        ticket.delete()
        return redirect('posts')


@login_required
def update_ticket(request, ticket_id):
    """
        Modifie a ticket
    """
    try:
        ticket = Ticket.objects.get(pk=ticket_id)
        if ticket.user != request.user:
            return redirect('posts')
    except Ticket.DoesNotExist:
        return redirect('posts')
    ticket_form = forms.TicketForm(instance=ticket)
    if request.method == "POST":
        update_form = forms.TicketForm(request.POST, request.FILES)
        if update_form.is_valid():
            ticket_updated = update_form.save()
            return redirect('posts')
    context = {"ticket_form": ticket_form}
    return render(request, 'website/update_ticket.html', context=context)
