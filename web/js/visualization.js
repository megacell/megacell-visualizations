function renderjson(url) {
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
                source: new ol.source.OSM()
            }),
            vectorLayer
        ],
        target: 'map',
        controls: ol.control.defaults({
            attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                collapsible: false
            })
        }),
        view: new ol.View({
            center: ol.proj.transform([-118.0226926,34.098475], 'EPSG:4326', 'EPSG:3857'),
            zoom: 11
        })
    });
}
//

renderjson('data/routes_paths.geojson');