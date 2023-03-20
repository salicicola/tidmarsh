	OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
	OpenLayers.Util.onImageLoadErrorColor = "transparent";
	
	boxes_layer = null; // for boxes, to clear
	centers_layer = null;
	dots_layer = null; // not needed here? = vectorLayer
	function init(){	
		var pos1 = new OpenLayers.LonLat(-70.72964,41.91684).transform(fromProj, toProj);
		var pos2 = new OpenLayers.LonLat(-70.61806,41.79947).transform(fromProj, toProj);
		var bounds = new OpenLayers.Bounds();
		bounds.extend(pos1);
		bounds.extend(pos2);
						
		var fromProj = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
		var toProj   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
		
		var map = new OpenLayers.Map('map', { controls: [], maxExtent: bounds });
		var osm_map = new OpenLayers.Layer.OSM();	
		var map_center = new OpenLayers.LonLat(-70.56928, 41.90544 ).transform( fromProj, toProj);
		var zoom = {{ map_zoom }}; // 12; // 13 or 7  in older version
		map.addLayer(osm_map);
		map.setCenter(map_center, zoom ); //FIXME ? use static center
		
		var layer_style = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);     
		var marker_style = OpenLayers.Util.extend({}, layer_style);
		marker_style.strokeColor = "red";
		marker_style.fillColor = "red";
		marker_style.graphicName = "circle"; 
		marker_style.pointRadius = 4;
		marker_style.strokeWidth = 1; // 3 (1 tonshe, 3 tolshe border)
		
		other_marker_style = OpenLayers.Util.extend({}, layer_style);
		other_marker_style.strokeColor = "red";
		other_marker_style.fillColor = "black";
		other_marker_style.graphicName = "triangle"; 
		other_marker_style.pointRadius = 8;
		other_marker_style.strokeWidth = 1; // 3 (1 tonshe, 3 tolshe border)


var tidmarsh_map = new OpenLayers.Layer.Vector("Tidmarsh Farms (MassGIS)", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/tidmarsh_oliver.kml.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				}); 
tidmarsh_map.setVisibility(true);	
map.addLayer(tidmarsh_map);

			var tidmarsh_cells_map = new OpenLayers.Layer.Vector("Tidmarsh cells (part)", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/TidmarshPlantingPlan.kml.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				}); 
tidmarsh_cells_map.setVisibility(false);	
map.addLayer(tidmarsh_cells_map);
			var acidic_peatlands_map = new OpenLayers.Layer.Vector("NHESP: acidic peatlands", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/acidic_peatlands.kml.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				});
acidic_peatlands_map.setVisibility(false);
map.addLayer(acidic_peatlands_map);

			var priority_habitats_map = new OpenLayers.Layer.Vector("NHESP: priority habitats", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/prihab.kml.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				});
priority_habitats_map.setVisibility(false);
map.addLayer(priority_habitats_map);


			var sandplain_map = new OpenLayers.Layer.Vector("NHESP: sandplain", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/GISDATA.VCSANDPLAIN_POLY.kml.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				});
sandplain_map.setVisibility(false);
map.addLayer(sandplain_map);

// FIXME:: shows nothing, also empty tax parcels, pine barrens
/*			var upland_forest_map = new OpenLayers.Layer.Vector("NHESP: upland forest", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/GISDATA.VCFOREST_POLY.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				});
upland_forest_map.setVisibility(true);
map.addLayer(upland_forest_map);
*/

var salicicola_sites = new OpenLayers.Layer.Vector("Salicicola gallery locations", {
				    strategies: [new OpenLayers.Strategy.Fixed()],
				    protocol: new OpenLayers.Protocol.HTTP({
					url: "/gis/kml/tidmarsh.kml.xml",
					format: new OpenLayers.Format.KML({
					    extractStyles: true, 
					    extractAttributes: true,
					    maxDepth: 10
					})
				    })
				});
salicicola_sites.setVisibility(false);
map.addLayer(salicicola_sites);


		
      var vectorLayer = new OpenLayers.Layer.Vector('reserved: {{ head }}');
      centers_layer = new OpenLayers.Layer.Vector('bbox center');
{% if method != 'list' %}
			var start_point = new OpenLayers.Geometry.Point({{start.0}}, {{start.1}}).transform(fromProj, toProj);
			var start_pointFeature = new OpenLayers.Feature.Vector(start_point, null, other_marker_style);
			centers_layer.addFeatures([start_pointFeature]);
{% endif %}			
		{% for p in points %}
			var point = new OpenLayers.Geometry.Point({{ p.0 }}, {{ p.1 }}).transform(fromProj, toProj);
			var pointFeature = new OpenLayers.Feature.Vector(point,null, marker_style);
			//pointFeature.attributes = { "orig_coord": "{{ p.1 }} {{ p.0 }}" }
			vectorLayer.addFeatures([pointFeature]);
		{% endfor %}
		
		map.addLayer(vectorLayer);
		map.addLayer(centers_layer);

boxes_layer = new OpenLayers.Layer.Vector("box (studied area)");
var polygonStyle = new OpenLayers.Style();
polygonStyle.fillColor = "yellow";
{% if method == 'bbox' %}
	polygonStyle.fillOpacity = 0.1;
{% else %}
	polygonStyle.fillOpacity = 0.5;
{% endif %}
polygonStyle.strokeColor = "black";
polygonStyle.strokeWidth = 1;
{% for box in boxes %}		
	var points = [
	   new OpenLayers.Geometry.Point({{box.0}}, {{box.1}}).transform(fromProj, toProj),
	    new OpenLayers.Geometry.Point({{box.0}}, {{box.3}}).transform(fromProj, toProj),
	    new OpenLayers.Geometry.Point({{ box.2 }}, {{box.3}}).transform(fromProj, toProj),
	    new OpenLayers.Geometry.Point({{ box.2 }}, {{box.1}}).transform(fromProj, toProj)
	];
	var ring = new OpenLayers.Geometry.LinearRing(points);
	var polygon = new OpenLayers.Geometry.Polygon([ring]);
	var attributes = {};
	var feature = new OpenLayers.Feature.Vector(polygon, attributes, polygonStyle);
	boxes_layer.addFeatures([feature]);
{% endfor %}
map.addLayer(boxes_layer); 

	
				
		map.addControl(new OpenLayers.Control.PanZoomBar());
		map.addControl(new OpenLayers.Control.ScaleLine());  
		map.addControl(new OpenLayers.Control.LayerSwitcher())
	
		//www.peterrobins.co.uk	with modifications
		function formatLonlats(lonLat) {
		    var lat = lonLat.lat;
		    var long = lonLat.lon;
		    var ns = OpenLayers.Util.getFormattedLonLat(lat);
		    var ew = OpenLayers.Util.getFormattedLonLat(long,'lon');
		    return ns + ', ' + ew + ' (' + (Math.round(lat * 10000) / 10000) + ', ' + (Math.round(long * 10000) / 10000) + ')';
		}
		
		map.addControl(new OpenLayers.Control.MousePosition( {id: "ll_mouse", formatOutput: formatLonlats, displayProjection: new OpenLayers.Projection("EPSG:4326")}));

{% if method != 'list' %}
	   map.events.register("dblclick", map, function(e) {
                var toProjection = new OpenLayers.Projection("EPSG:4326");
                var position = map.getLonLatFromPixel(e.xy).transform(map.getProjectionObject(), toProjection);
                OpenLayers.Util.getElement("lat").value = position.lat;
                OpenLayers.Util.getElement("lon").value = position.lon;
                centers_layer.removeFeatures([start_pointFeature]);
 		var new_point = new OpenLayers.Geometry.Point(position.lon, position.lat).transform(fromProj, toProj);
		start_pointFeature = new OpenLayers.Feature.Vector(new_point, null, other_marker_style);
		centers_layer.addFeatures([start_pointFeature]);
            });
{% else %}
	   map.events.register("dblclick", map, function(e) {
                var toProjection = new OpenLayers.Projection("EPSG:4326");
                var position = map.getLonLatFromPixel(e.xy).transform(map.getProjectionObject(), toProjection);
                //OpenLayers.Util.getElement("lat").value = position.lat;
                //OpenLayers.Util.getElement("lon").value = position.lon;
                var value =  OpenLayers.Util.getElement("lonlats").value;
                value += position.lon + ' ' + position.lat + ',';
                OpenLayers.Util.getElement("lonlats").value = value;
                //vectorLayer.removeFeatures([start_pointFeature]);
 		var new_point = new OpenLayers.Geometry.Point(position.lon, position.lat).transform(fromProj, toProj);
		start_pointFeature = new OpenLayers.Feature.Vector(new_point, null, other_marker_style);
		centers_layer.addFeatures([start_pointFeature]);
            });		
		
{% endif %}
           
	} // end of init()
	
	function clear_entry() {
		boxes_layer.removeAllFeatures();
		centers_layer.removeAllFeatures();
		document.getElementById('lonlats').value='';
		document.getElementById('fname').value='';
	}
