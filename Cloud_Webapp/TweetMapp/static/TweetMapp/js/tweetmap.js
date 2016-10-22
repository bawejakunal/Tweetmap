var map;
var markers = [];
var markerCluster;

// Sets the map on all markers in the array.
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
  setMapOnAll(null);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
  clearMarkers();
  markers = [];
}

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
    var tweet_id = [];
    $.each(data, function(key, value){
        var coordinates = {};
        coordinates.lat = value[0]; //latitude
        coordinates.lng = value[1]; //longitude
        locations.push(coordinates);
        tweet_id.push(key);
    });

    // Create an array of alphabetical characters used to label the markers.
    var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

    markers = locations.map(function(location, i) {
        var marker = new google.maps.Marker({
            position: location,
            label: labels[i % labels.length],
            id: tweet_id[i] //store tweet id in marker
        });

        //add listener
        marker.addListener('click', function(){
            fetch_tweet(marker);
        });
        return marker;
    });

    markerCluster = new MarkerClusterer(map, markers,
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


//Call every 5 seconds
window.setInterval(function(){
  // call your function here
  query_string = $('#search-box').val();
  //remove markers
  deleteMarkers();
  //remove clusters
  markerCluster.clearMarkers();
  //perform new search
  wordsearch(query_string);
}, 10000);

//trigger on click
$('#search-button').click(function(){

    // new map for new search
    deleteMarkers();
    markerCluster.clearMarkers();
    map.setCenter({lat: 15, lng: -10});
    map.setZoom(3);
    var query_string = $('#search-box').val();
    wordsearch(query_string);
});


//Display tweet
function fetch_tweet(marker)
{
    $.get("fetchtweet", {id: marker.id})
    .done(function(data){
        // Display Tweet in a window near marker
        var infowindow = new google.maps.InfoWindow({
          content: data,
          maxWidth: 200
        });
        infowindow.open(map, marker)
    })
    .fail(function(error){
        console.log(error);
    });
}