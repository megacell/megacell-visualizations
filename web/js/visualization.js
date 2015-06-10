var mapid = 'map';

function renderjson(url) {
    $('#map').empty();

    var vectorLayer = new ol.layer.Vector({
        source: new ol.source.GeoJSON({
            projection : 'EPSG:3857',
            url: url
        }),
        style: styleFunction
    });
    //var center = new ol.LonLat();
    //var proj = new ol.Projection("EPSG:4326");

    var map = new ol.Map({
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM(),
                opacity: 0.3,
                eventListeners: {
                    featureclick: function(e) {
                        console.log(e.feature.getProperties());
                    }
                }
            }),
            vectorLayer
        ],
        target: mapid,
        controls: ol.control.defaults({
            attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                collapsible: false
            })
        }),
        view: new ol.View({
            center: ol.proj.transform([-118.0026926,34.098475], 'EPSG:4326', 'EPSG:3857'),
            zoom: 11
        })
    });
}

$(function () {
    $("#link-flow-errors").click(function(){
        renderjson('data/results_error.geojson');});
    $("#link-flows").click(function(){
        renderjson('data/results_links.geojson');});
    $("#routes-through-link").click(function(){
        renderjson('data/routes_through_link.geojson');});
    $("#routes-ods").click(function(){
        renderjson('data/routes_paths.geojson');});
    $("#ods").click(function(){
        renderjson('data/od_geom.geojson');});
});

renderjson('data/results_links.geojson');
