api (USE powershell)
Получить все товары (GET)

    Invoke-RestMethod -Uri "http://localhost:8080/api/products" -Method GET

Добавить товар (POST)

    $json = @'
    {
        "name": "New item",
        "price": 999,
        "description": "Text description",
        "categories": ["TEST"]
    }
    '@

    Invoke-RestMethod -Uri "http://localhost:8080/api/products" `
        -Method POST `
        -Body $json `
        -ContentType "application/json"

Обновить товар по ID (PUT)

    $json = @'
    {
    "name": "New name",
    "price": 1999,
    "categories": ["New category"]
    }
    '@

    # Замените 1 на нужный ID товара
    Invoke-RestMethod -Uri "http://localhost:8080/api/products/1" `
    -Method PUT `
    -Body $json `
    -ContentType "application/json"

Удалить товар по ID (DELETE)

    # Замените 1 на нужный ID товара
    Invoke-RestMethod -Uri "http://localhost:8080/api/products/1" -Method DELETE


Советы:
Если нужно отправить несколько товаров сразу (POST), используйте массив:
    $json = @'
    [
    {
        "name": "Товар 1",
        "price": 100,
        "description": "Описание 1",
        "categories": ["Категория 1"]
    },
    {
        "name": "Товар 2",
        "price": 200,
        "description": "Описание 2",
        "categories": ["Категория 2"]
    }
    ]
    '@

Чтобы увидеть сырой ответ (вместо автоматического парсинга), добавьте параметр:

    -ResponseHeadersVariable response

    Затем выведите результат:

        $response


Для отладки добавьте параметр -StatusCodeVariable status, чтобы посмотреть код ответа:

    Write-Host "Status code: $status"