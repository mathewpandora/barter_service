from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from .forms import AdForm
from .models import Ad, ExchangeProposal
from .forms import ExchangeProposalForm


@login_required
def create_ad(request):
    """
    Представление для создания нового объявления.
    При GET-запросе выводится пустая форма.
    При POST-запросе форма валидируется и, в случае успеха, создаётся объект Ad.
    Поле created_at устанавливается автоматически, а user привязывается к текущему пользователю.
    """
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            # Редирект на страницу деталей нового объявления (предполагается, что такой URL настроен)
            return redirect('http://127.0.0.1:8000/ads/list/')  # ← редирект на список
    else:
        form = AdForm()
    return render(request, 'ads/ad_form.html', {'form': form})


@login_required
def edit_ad(request, ad_id):
    """
    Представление для редактирования существующего объявления.
    Проверка: только автор объявления имеет право редактировать его.
    При GET-запросе выводится заполненная форма, при POST — обновляются данные.
    """
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        # Если текущий пользователь не является автором, возвращаем отказ в доступе.
        return HttpResponseForbidden("Вы не являетесь автором данного объявления.")

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            # Редирект на страницу деталей объявления после успешного редактирования.
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'ad': ad})


@login_required
def delete_ad(request, ad_id):
    """
    Представление для удаления объявления.
    Проверка: только автор объявления имеет право удалить его.
    При GET-запросе выводится страница подтверждения удаления.
    При POST-запросе объявление удаляется.
    """
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        return HttpResponseForbidden("Вы не являетесь автором данного объявления.")

    if request.method == 'POST':
        ad.delete()
        # Редирект на список объявлений после удаления
        return redirect('ad_list')

    # Вывод шаблона для подтверждения удаления
    return render(request, 'ads/ad_confirm_delete.html', {'ad': ad})


@login_required
def ad_list(request):
    """
    Представление для отображения списка объявлений с пагинацией.
    Объявления сортируются по дате создания (от новых к старым).
    Используется Paginator для ограничения числа объявлений на странице.
    """
    ad_queryset = Ad.objects.all().order_by('-created_at')
    paginator = Paginator(ad_queryset, 10)  # по 10 объявлений на страницу

    page_number = request.GET.get('page')
    ads = paginator.get_page(page_number)

    return render(request, 'ads/ad_list.html', {'ads': ads})


@login_required
def ad_detail(request, ad_id):
    """
    Представление для отображения деталей объявления.
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
    Представление для отображения всех объявлений текущего пользователя.
    """
    my_ads_queryset = Ad.objects.filter(user=request.user).order_by('-created_at')  # Получаем только объявления текущего пользователя
    return render(request, 'ads/my_ads.html', {'ads': my_ads_queryset})

@login_required
def my_barters(request):
    # Получаем все предложения обмена, отправленные или полученные пользователем
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
