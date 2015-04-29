var styleFunction = function(feature, resolution) {
    var prop = feature.getProperties();
    if (prop.weight) {
        var map = RedGreenColorMapper([0, 20], LogScaler);
        console.log(map(prop.weight));
        var sty = new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: map(prop.weight),
                width: 2
            })
        });
        return [sty];
    }
    return styles[feature.getGeometry().getType()];
};

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
                source: new ol.source.OSM(),
                opacity: 0.3
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
