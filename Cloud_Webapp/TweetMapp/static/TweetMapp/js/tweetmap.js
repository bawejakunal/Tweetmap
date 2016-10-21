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

    var markers = locations.map(function(location, i) {
        var marker = new google.maps.Marker({
            position: location,
            label: labels[i % labels.length],
            id: tweet_id[i] //store tweet id in marker
        });

        //add listener
        marker.addListener('click', function()
            {
                fetch_tweet(marker);
            });
        return marker;
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

//trigger on click
$('#search-button').click(function(){

    // new map for new search
    initMap();
    var query_string = $('#search-box').val();
    wordsearch(query_string);
});

//Display tweet
function fetch_tweet(marker)
{
    $.get("fetchtweet", {id: marker.id})
    .done(function(data){
        var infowindow = new google.maps.InfoWindow({
          content: data,
          maxWidth: 200,
          wrap: true
        });
        infowindow.open(map, marker)
    })
    .fail(function(error){
        console.log(error);
    });
}