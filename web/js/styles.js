var image = new ol.style.Circle({
    radius: 5,
    fill: null,
    stroke: new ol.style.Stroke({color: 'red', width: 1})
});

var styles = {
    'Point': [new ol.style.Style({
        image: image
    })],
    'LineString': [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'green',
            width: 2
        })
    })],
    'MultiLineString': [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'green',
            width: 2
        })
    })],
    'MultiPoint': [new ol.style.Style({
        image: image
    })],
    'MultiPolygon': [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'yellow',
            width: 1
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255, 255, 0, 0.1)'
        })
    })],
    'Polygon': [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'blue',
            width: 3
        }),
        fill: new ol.style.Fill({
            color: 'rgba(0, 0, 255, 0.3)'
        })
    })],
    'GeometryCollection': [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'magenta',
            width: 2
        }),
        fill: new ol.style.Fill({
            color: 'magenta'
        }),
        image: new ol.style.Circle({
            radius: 10,
            fill: null,
            stroke: new ol.style.Stroke({
                color: 'magenta'
            })
        })
    })],
    'Circle': [new ol.style.Style({
        stroke: new ol.style.Stroke({
            color: 'red',
            width: 2
        }),
        fill: new ol.style.Fill({
            color: 'rgba(255,0,0,0.2)'
        })
    })]
};

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
        var map = RedGreenColorMapper([0, 1], LinearScaler);
        if (type == 'LineString' || type == 'MultiLineString') {
            return [makeLineStyle(map(prop.weight, 0.9))];
        } else if (type == 'Polygon' || type == 'MultiPolygon') {
            return [makePolyStyle(map(prop.weight, 0.5))];
        }

    }
    return styles[type];
};


var travelingStyle = new ol.style.Circle({
    radius: 5,
    snapToPixel: false,
    fill: new ol.style.Fill({color: 'green'})
});

var completedStyle = new ol.style.Circle({
    radius: 5,
    snapToPixel: false,
    fill: new ol.style.Fill({color: 'orange'})
});
