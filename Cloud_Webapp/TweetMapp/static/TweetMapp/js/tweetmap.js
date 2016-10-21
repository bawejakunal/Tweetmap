var map;

//Draw a world map
function initMap()
{

  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 3,
    center: {lat: 15, lng: -10}
  });
}

//plot points on map
function plotmap(data)
{
    var locations = [];
        $.each(data, function(key, value){
            var coordinates = {};
            coordinates.lat = value[0]; //latitude
            coordinates.lng = value[1]; //longitude
            locations.push(coordinates);
        });

        // Create an array of alphabetical characters used to label the markers.
        var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

        var markers = locations.map(function(location, i) {
            return new google.maps.Marker({
                position: location,
                label: labels[i % labels.length]
            });
        });

        var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
}

//search query_string
function wordsearch(query_string)
{
    //load all points from default search
    // null means get all records
    $.getJSON("wordsearch", {query: query_string})
    .done(function(data){
        plotmap(data);
    })
    .fail(function(error){
        console.log(error);
    });
}

// Trigger default search if map has loaded
window.onload = wordsearch(null); 
