window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
                return L.circleMarker(latlng, {
                    radius: 9.9,
                    fillOpacity: 1.00,
                    weight: 1.5
                });
            }

            ,
        function1: function(feature, context) {
            const selected_city = context.hideout.selected_city;
            if (selected_city === feature.properties.name) {
                return {
                    fillColor: "red",
                    color: "red"
                }
            }
            return {
                fillColor: "blue",
                color: "blue"
            }
        }

    }
});