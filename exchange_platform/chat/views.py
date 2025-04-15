from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Chat
from .forms import MessageForm
from ads.models import ExchangeProposal

@login_required
def chat_view(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    chat, created = Chat.objects.get_or_create(proposal=proposal)


    chat.participants.add(
        request.user,
        proposal.ad_sender.user,
        proposal.ad_receiver.user
    )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.chat = chat
            message.sender = request.user
            message.save()
            # Перенаправляем обратно на тот же чат, чтобы обновить страницу
            return redirect('chat_view', proposal_id=proposal.id)
    else:
        form = MessageForm()

    messages = chat.messages.select_related('sender').order_by('created_at')

    return render(request, 'chat/chat_view.html', {
        'chat': chat,
        'messages': messages,
        'form': form
    })


@login_required
def chat_list_view(request):
    user = request.user
    chats = Chat.objects.filter(participants=user).prefetch_related('participants', 'messages', 'proposal')

    chat_data = []
    for chat in chats:
        last_message = chat.messages.order_by('-created_at').first()
        chat_data.append({
            'chat': chat,
            'last_message': last_message,
        })

    chat_data.sort(
        key=lambda c: c['last_message'].created_at if c['last_message'] else c['chat'].created_at,
        reverse=True
    )

    return render(request, 'chat/chat_list.html', {'chat_data': chat_data})