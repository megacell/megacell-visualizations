var minFrameTime = 200;

function renderjson(json) {
    var map = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM(),
                opacity: 0.3
            })
        ],
        target: 'map',
        view: new ol.View({
            center: ol.proj.transform([-118.0026926,34.098475], 'EPSG:4326', 'EPSG:3857'),
            zoom: 11
        })
    });
    var pos = 0;
    var lastFrameTime = (new Date()).getTime();
    map.on('postcompose', function(event) {
        var vectorContext = event.vectorContext;
        var frameState = event.frameState;

        var completed = [];
        var traveling = [];
        for (var i = 0; i < json.length; i++) {
            var cur = json[i][pos];
            if (cur) {
                traveling.push(cur);
            } else {
                completed.push(json[i][json[i].length - 1]);
            }
        }

        if (frameState.time - lastFrameTime > minFrameTime) {
            pos += 1;
            lastFrameTime = frameState.time;
        }

        vectorContext.setImageStyle(travelingStyle);
        vectorContext.drawMultiPointGeometry(
            new ol.geom.MultiPoint(traveling), null);
        vectorContext.setImageStyle(completedStyle);
        vectorContext.drawMultiPointGeometry(
            new ol.geom.MultiPoint(completed), null);
        map.render();
    });
    map.render();
}
//

$.getJSON('data/timed_trajectories.json', function(json) {
    renderjson(json);
});
