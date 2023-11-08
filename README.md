## The kopf-based operator is focused on an event-oriented model

Цель при изменении CRD ClickhouseDevopsui реагировать и создавать пользователя согласно описанию  в spec 

Вся логика описана в ./app

1. Собрать образ 
```sh
docker build . -t ghcr.io/coroot/coroot-operator:0.1
docker push ghcr.io/coroot/coroot-operator:0.1
```

2. тут уже работаем с .kube или перенести ее в свой CI/CD 

2.1. networkpolice.yaml чтобы был доступ к api кубера для отлова события создания объекта и послед. дейтсвия 

2.2. rbac.yaml права на api взамойдействия 

2.3. secret.yaml секрет для подключения к БД clickhouse с привелегированными правами для модификаций учеток (секрет интегрируем в CI/CD свой)

2.4. simple_app.yaml описание самого деплоймента 


3. После того как загрузилось и он корректно стартовал. Можно применять сам CRD. Пример clickhouse.yaml (!!! обратите вниманеи что он прорсто показа для примера , своей корректируем под CI/CD).

Проверить корректность работы можно в логах  
```sh
kubectl logs -n coroot-clickhouse clickhouse-operator-69b5644dc9-vfst4
```

выдаст такое при создании CRD
```
[2023-11-08 07:33:42,743] kopf.objects         [INFO    ] [coroot-clickhouse/otladka-test] Пользователь teeeest создан в coroot-clickhouse
[2023-11-08 07:33:42,748] kopf.objects         [INFO    ] [coroot-clickhouse/otladka-test] Handler 'create_fn' succeeded.
[2023-11-08 07:33:42,749] kopf.objects         [INFO    ] [coroot-clickhouse/otladka-test] Creation is processed: 1 succeeded; 0 failed.
```

при удалении CRD

```
[2023-11-08 07:35:54,494] kopf.objects         [INFO    ] [coroot-clickhouse/otladka-test] Пользователь teeeest удален в coroot-clickhouse
[2023-11-08 07:35:54,498] kopf.objects         [INFO    ] [coroot-clickhouse/otladka-test] Handler 'delete_custom_resource' succeeded.
[2023-11-08 07:35:54,499] kopf.objects         [INFO    ] [coroot-clickhouse/otladka-test] Deletion is processed: 1 succeeded; 0 failed.
```