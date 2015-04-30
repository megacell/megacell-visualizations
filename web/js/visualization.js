function makeLineStyle(color){
    return new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: color,
            width: 2
        })
    });
}

function makePolyStyle(color){
    return new ol.style.Style({
        fill: new ol.style.Fill({
            color: color
        })
    });
}

var styleFunction = function(feature, resolution) {
    var prop = feature.getProperties();
    var type = feature.getGeometry().getType();
    if (prop.weight) {
        var map = RedGreenColorMapper([0, 1], LogScaler);
        if (type == 'LineString' || type == 'MultiLineString') {
            return [makeLineStyle(map(prop.weight, 0.9))];
        } else if (type == 'Polygon' || type == 'MultiPolygon') {
            return [makePolyStyle(map(prop.weight, 0.5))];
        }

    }
    return styles[type];
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
                opacity: 0.3,
                eventListeners: {
                    featureclick: function(e) {
                        console.log(e.feature.getProperties());
                    }
                }
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
            center: ol.proj.transform([-118.0026926,34.098475], 'EPSG:4326', 'EPSG:3857'),
            zoom: 11
        })
    });
}
//

//renderjson('data/routes_paths.geojson');
renderjson('data/routes_through_link.geojson');
