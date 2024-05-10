// Инициализация карты
var map = new ymaps.Map('map', {
    center: [55.76, 37.64],
    zoom: 10,
    controls: []
}, {
    searchControlProvider: 'yandex#search'
});
var myPosition = new ymaps.Placemark([55.76, 37.64]);
map.geoObjects.add(myPosition);

myPosition.events.add('click', function (event, myPosition) {
    // Получаем координаты выбранного места
    var point = event.target.geometry.getCoordinates();

    // Добавляем маркер на карту
    var marker = new ymaps.Placemark(point);
    map.geoObjects.add(marker);
});
var saveButton = document.getElementById('save-button');
saveButton.addEventListener('click', function () {
    // Получаем координаты маркера
    var point = marker.geometry.getCoordinates();

    // Сохраняем координаты в объект reference points
    referencePoints.push(point);
});
var multiRouter = new ymaps.multiRouter.MultiRouter({
    referencePoints: referencePoints
});

var route = multiRouter.route(from, to);

map.geoObjects.add(route);




// Объявляем набор опорных точек и массив индексов транзитных точек.
var referencePoints = [
    "Москва, Тверская",
    "Москва, Льва Толстого, 16",
    "Москва, Кремлевская набережная",
    "Москва, Новокузнецкая"
    // "Москва, парк Сокольники"
];

function init() {
    viaIndexes = [2];

    // Создаем мультимаршрут и настраиваем его внешний вид с помощью опций.
    var multiRoute = new ymaps.multiRouter.MultiRoute({
        referencePoints: referencePoints,
        params: {viaIndexes: viaIndexes}
    }, {
        // Внешний вид путевых точек.
        wayPointStartIconColor: "#333",
        wayPointStartIconFillColor: "#0000ff",
        // Задаем собственную картинку для последней путевой точки.
        wayPointFinishIconLayout: "default#image",
        wayPointFinishIconImageHref: "images/sokolniki.png",
        wayPointFinishIconImageSize: [30, 30],
        wayPointFinishIconImageOffset: [-15, -15],
        // Позволяет скрыть иконки путевых точек маршрута.
        // wayPointVisible:false,

        // Внешний вид транзитных точек.
        viaPointIconRadius: 10,
        viaPointIconFillColor: "#0000ff",
        viaPointActiveIconFillColor: "#0000ff",
        // Транзитные точки можно перетаскивать, при этом
        // маршрут будет перестраиваться.
        viaPointDraggable: true,
        // Позволяет скрыть иконки транзитных точек маршрута.
        // viaPointVisible:false,

        // Внешний вид точечных маркеров под путевыми точками.
        pinIconFillColor: "#000088",
        pinActiveIconFillColor: "#B3B3B3",
        // Позволяет скрыть точечные маркеры путевых точек.
        // pinVisible:false,

        // Внешний вид линии маршрута.
        routeStrokeWidth: 2,
        routeStrokeColor: "#000088",
        routeActiveStrokeWidth: 6,
        routeActiveStrokeColor: "#E63E92",

        // Внешний вид линии пешеходного маршрута.
        routeActivePedestrianSegmentStrokeStyle: "solid",
        routeActivePedestrianSegmentStrokeColor: "#00CDCD",

        // Автоматически устанавливать границы карты так, чтобы маршрут был виден целиком.
        boundsAutoApply: true
    });

    // Настраиваем внешний вид второй точки через прямой доступ к ней.
    customizeSecondPoint();

    // Создаем кнопки.
    var removePointsButton = new ymaps.control.Button({
            data: {content: "Удалить промежуточные точки"},
            options: {selectOnClick: true}
    });

    // Объявляем обработчики для кнопок.
    removePointsButton.events.add('select', function () {
        multiRoute.model.setReferencePoints([
            referencePoints[0],
            referencePoints[referencePoints.length - 1]
        ], []);
    });

    removePointsButton.events.add('deselect', function () {
        multiRoute.model.setReferencePoints(referencePoints, viaIndexes);
        // Т.к. вторая точка была удалена, нужно заново ее настроить.
        customizeSecondPoint();
    });

    multiRoute.events.add('click', function (event, myPosition) {
        // Получаем координаты выбранного места
        var point = event.target.geometry.getCoordinates();
    
        // Добавляем маркер на карту
        var marker = new ymaps.Placemark(point);
        map.geoObjects.add(marker);
        console.log("Hello Point");
        console.log(marker);
    });

    // Функция настройки внешнего вида второй точки.
    function customizeSecondPoint() {
        /**
         * Ждем, пока будут загружены данные мультимаршрута и созданы отображения путевых точек.
         * @see https://tech.yandex.ru/maps/doc/jsapi/2.1/ref/reference/multiRouter.MultiRouteModel-docpage/#event-requestsuccess
         */
        multiRoute.model.events.once("requestsuccess", function () {
            var yandexWayPoint = multiRoute.getWayPoints().get(1);
            // Создаем балун у метки второй точки.
            ymaps.geoObject.addon.balloon.get(yandexWayPoint);
            yandexWayPoint.options.set({
                preset: "islands#grayStretchyIcon",
                iconContentLayout: ymaps.templateLayoutFactory.createClass(
                    '<span style="color: red;">Я</span>ндекс'
                ),
                balloonContentLayout: ymaps.templateLayoutFactory.createClass(
                    '{{ properties.address|raw }}'
                )
            });
        });
    }

    // Создаем карту с добавленной на нее кнопкой.
    var myMap = new ymaps.Map('map', {
            center: [55.739625, 37.54120],
            zoom: 7,
            controls: [removePointsButton]
        }, {
            buttonMaxWidth: 300
        });

    // Добавляем мультимаршрут на карту.
    myMap.geoObjects.add(multiRoute);
}

ymaps.ready(init);