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
    window.onhashchange = function() {
        var hash = location.hash;
        if (hash == '#link-flow-errors') {
            renderjson('data/results_error.geojson');
        } else if (hash == '#link-flows') {
            renderjson('data/results_links.geojson');
        } else if (hash == '#routes-through-link') {
            renderjson('data/routes_through_link.geojson');
        } else if (hash == '#routes-ods') {
            renderjson('data/routes_paths.geojson');
        } else if (hash == '#ods') {
            renderjson('data/od_geom.geojson');
        } else if (hash.startsWith('#cellpaths')) {
            var index = hash.slice(10);
            console.log('data/cellpaths'+ index +'.geojson');
            renderjson('data/cellpaths'+ index +'.geojson');
        }
    };
});

renderjson('data/results_links.geojson');
