import os
import django
from django.core.cache import cache
import hashlib


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'exchange_platform.settings')

django.setup()

from rest_framework.authentication import TokenAuthentication
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, AdSerializer
from django.contrib.auth.decorators import login_required
from rest_framework import status, permissions
from rest_framework.response import Response
from django.http import HttpResponseForbidden,Http404
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import AdForm, ExchangeProposalForm
from .models import Ad, ExchangeProposal


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_list')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором данного объявления.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором данного объявления.")

    if request.method == 'POST':
        ad.delete()
        return redirect('ad_list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required
def ad_list(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')
    page_number = request.GET.get('page', '1')


    cache_key = f"ad_list:{hashlib.md5(f'{query}:{selected_category}:{page_number}'.encode()).hexdigest()}"
    cached_response = cache.get(cache_key)

    if cached_response:
        #":1:ad_list:837ec5754f503cfaaee0929fd48974e7" - так хранится в редис кешичекккк
        return cached_response

    ads_list = Ad.objects.filter(is_archived=False).order_by('-created_at')
    if query:
        ads_list = ads_list.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if selected_category:
        ads_list = ads_list.filter(category=selected_category)

    paginator = Paginator(ads_list, 10)
    ads = paginator.get_page(page_number)

    response = render(request, 'ads/ad_list.html', {
        'ads': ads,
        'search_query': query,
        'selected_category': selected_category,
        'category_choices': Ad.CATEGORY_CHOICES,
    })

    cache.set(cache_key, response, 60 * 5)  # 5 минут
    return response


@login_required
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    is_owner = ad.user == request.user

    exchange_proposals = ExchangeProposal.objects.filter(ad_receiver=ad)

    return render(request, 'ads/ad_detail.html', {
        'ad': ad,
        'is_owner': is_owner,
        'exchange_proposals': exchange_proposals
    })


@login_required
def propose_exchange(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user == request.user:
        return redirect('ad_detail', ad_id=ad.id)

    my_ads = Ad.objects.filter(user=request.user, is_archived=False)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = form.cleaned_data['ad_sender']
            proposal.ad_receiver = ad
            proposal.status = ExchangeProposal.STATUS_PENDING
            proposal.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'ads/exchange_form.html', {
        'form': form,
        'ad': ad,
        'my_ads': my_ads
    })


@login_required
def my_ads(request):
    ads = Ad.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'ads/my_ads.html', {'ads': ads})


@login_required
def my_barters(request):
    pending_proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user),
        status=ExchangeProposal.STATUS_PENDING
    ).select_related('ad_sender', 'ad_receiver')

    accepted_proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user),
        status=ExchangeProposal.STATUS_ACCEPTED
    ).select_related('ad_sender', 'ad_receiver')

    declined_proposals = ExchangeProposal.objects.filter(
        Q(ad_sender__user=request.user) | Q(ad_receiver__user=request.user),
        status=ExchangeProposal.STATUS_DECLINED
    ).select_related('ad_sender', 'ad_receiver')

    return render(request, 'ads/my_barters.html', {
        'pending_proposals': pending_proposals,
        'accepted_proposals': accepted_proposals,
        'declined_proposals': declined_proposals,
    })


@login_required
def accept_exchange(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user == request.user:
        proposal.status = ExchangeProposal.STATUS_ACCEPTED
        proposal.save()

        proposal.ad_sender.is_archived = True
        proposal.ad_receiver.is_archived = True
        proposal.ad_sender.save()
        proposal.ad_receiver.save()

    return redirect('my_barters')


@login_required
def decline_exchange(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user == request.user:
        proposal.status = ExchangeProposal.STATUS_DECLINED
        proposal.save()
    return redirect('my_barters')


def redirect_view(request):
    return redirect('ad_list')

"""
API-ручки 

GET /api/v1/ads/ — возвращает все объявления текущего пользователя.
POST /api/v1/ads/ — создаёт новое объявление для текущего пользователя.
GET /api/v1/ads/<ad_id>/ — возвращает детали конкретного объявления.
PUT /api/v1/ads/<ad_id>/ — обновляет объявление.
DELETE /api/v1/ads/<ad_id>/ — удаляет объявление.

"""

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ads = Ad.objects.filter(user=request.user, is_archived=False)
        serializer = AdSerializer(ads, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, ad_id, user):
        try:
            return Ad.objects.get(id=ad_id, user=user)
        except Ad.DoesNotExist:
            raise Http404

    def get(self, request, ad_id):
        ad = self.get_object(ad_id, request.user)
        serializer = AdSerializer(ad)
        return Response(serializer.data)

    def put(self, request, ad_id):
        ad = self.get_object(ad_id, request.user)
        serializer = AdSerializer(ad, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ad_id):
        ad = self.get_object(ad_id, request.user)
        ad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


