from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .forms import AdForm
from .models import Ad, ExchangeProposal
from .forms import ExchangeProposalForm


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)  # Добавлен request.FILES
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('http://127.0.0.1:8000/ads/list/')
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором данного объявления.")

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)  # Добавлен request.FILES
        if form.is_valid():
            form.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'ad': ad})

@login_required
def delete_ad(request, ad_id):
    """

    """
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором данного объявления.")

    if request.method == 'POST':
        ad.delete()
        # Редирект на список объявлений после удаления
        return redirect('ad_list')

    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required
def ad_list(request):
    """

    """
    ad_queryset = Ad.objects.all().order_by('-created_at').filter(is_archived=False)
    paginator = Paginator(ad_queryset, 10)

    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {'ads': ads})


@login_required
def ad_detail(request, ad_id):
    """

    """
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/ad_detail.html', {'ad': ad})


@login_required
def propose_exchange(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)

    if ad.user == request.user:
        return redirect('ad_list')

    my_ads = Ad.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ExchangeProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_sender = form.cleaned_data['ad_sender']
            proposal.ad_receiver = ad
            proposal.status = ExchangeProposal.STATUS_PENDING  # Статус по умолчанию
            proposal.save()
            return redirect('ad_list')  # Перенаправляем на страницу списка объявлений
    else:
        form = ExchangeProposalForm(user=request.user)

    return render(request, 'ads/exchange_form.html', {'form': form, 'my_ads': my_ads, 'ad': ad})


@login_required
def my_ads(request):
    """
    """
    my_ads_queryset = Ad.objects.filter(user=request.user).order_by('-created_at')  # Получаем только объявления текущего пользователя
    return render(request, 'ads/my_ads.html', {'ads': my_ads_queryset})


@login_required
def my_barters(request):
    pending_proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user, status=ExchangeProposal.STATUS_PENDING
    ) | ExchangeProposal.objects.filter(
        ad_receiver__user=request.user, status=ExchangeProposal.STATUS_PENDING
    )

    accepted_proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user, status=ExchangeProposal.STATUS_ACCEPTED
    ) | ExchangeProposal.objects.filter(
        ad_receiver__user=request.user, status=ExchangeProposal.STATUS_ACCEPTED
    )

    declined_proposals = ExchangeProposal.objects.filter(
        ad_sender__user=request.user, status=ExchangeProposal.STATUS_DECLINED
    ) | ExchangeProposal.objects.filter(
        ad_receiver__user=request.user, status=ExchangeProposal.STATUS_DECLINED
    )

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
    return redirect('my_barters')


@login_required
def decline_exchange(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user == request.user:
        proposal.status = ExchangeProposal.STATUS_DECLINED
        proposal.save()
    return redirect('my_barters')


def redirect_view(request):
    return redirect('/ads/list')  # Редирект на нужный URL


