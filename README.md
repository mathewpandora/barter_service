От себя: 

Очень увлекательный проект, к сожалению одной недели недостаточно, чтобы добавить туда все фичи и идеи которые есть
поэтому сделал функцинал требованияем + добавил от себя чаты (в дальнейшем можно подключить сокеты или шорт пул чтобы получать 
уведомления в рил тайм), добавил атрибут is_archived - если появился принятый обмен, проставляем его True - чтобы скрыть барт

Сделал апи для взаимодейтсвия с Ad b получения токена/регитсрации - можно расширять и взаисодейтсвовать со другими моделями

Сделал красивую админку 

На главной странице объявления кэшируются в Redis на 5 минут, чтобы уменьшить нагрузку на базу данных и ускорить отклик. 
Используется Django Cache API с backend django-redis

# только под конец увидел - что изображения прикреплять через url - оставлю так, понимаю, что решение хранить их в uploads - не лучшая идея

"Мои барты" - вещи которые юзер готов обменять 

Запуск локально: 

1. docker-compose build
2. docker-compose up 