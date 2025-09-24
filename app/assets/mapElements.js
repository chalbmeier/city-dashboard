window.mapElements = Object.assign(window.mapElements || {}, {
    pointToLayer: function(feature, latlng, context) {
        const r = context?.hideout?.marker?.radius ?? 10;
        return L.circleMarker(latlng, {radius: r, fillOpacity: 1.00, weight: 1.5});
},
    styleHandle: function(feature, context) {
        const h = context?.hideout || {};
        const colors = h.colors || {};
        const selected = h.selected_city === feature.properties.name;
        return {
            fillColor: selected ? (colors.selected || "red") : (colors.default || "blue"),
            color: colors.border || "black"
        };
    }
});