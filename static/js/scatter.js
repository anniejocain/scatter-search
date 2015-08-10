$(document).ready(function() {
  $('#query').focus();
  //var params = getParams();

  if(query) {
    $("#query").val(query);
    getResults();
  }
  
  $('#cross-search').submit(function() {
		getResults();
		return false;
	});

});

function getResults(){
  var query = $("#query").val();
  query = query.replace(' ', '+');
	$.getJSON(web_base + "/api/hollis/" + query, function(data) {
    if(data.results.length > 0) {
    	var source = $("#catalog-template").html();
    	var template = Handlebars.compile(source);
    	$('#catalog').html(template(data));
    }
    else {
    	var source = $("#catalog-template").html();
    	var template = Handlebars.compile(source);
    	$('#catalog').html(template({alert: 'No results'}));
    }
  });
  $.getJSON(web_base + "/api/libguides/" + query, function(data) {
    if(data.results.length > 0) {
    	var source = $("#libguides-template").html();
    	var template = Handlebars.compile(source);
    	$('#libguides').html(template(data));
    }
    else {
    	var source = $("#libguides-template").html();
    	var template = Handlebars.compile(source);
    	$('#libguides').html(template({alert: 'No results'}));
    }
  });
  $.getJSON(web_base + "/api/journals/" + query, function(data) {
  	if(data.journals.length > 0) {
    	var source = $("#journals-template").html();
    	var template = Handlebars.compile(source);
    	$('#journals').html(template(data));
    }
    else {
    	var source = $("#journals-template").html();
    	var template = Handlebars.compile(source);
    	$('#journals').html(template({alert: 'No results'}));
    }
  });
  $.getJSON(web_base + "/api/databases/" + query, function(data) {
  	if(data.databases.length > 0) {
    	var source = $("#databases-template").html();
    	var template = Handlebars.compile(source);
    	$('#databases').html(template(data));
    }
    else {
    	var source = $("#databases-template").html();
    	var template = Handlebars.compile(source);
    	$('#databases').html(template({alert: 'No results'}));
    }
  });
  $.getJSON(web_base + "/api/website/" + query, function(data) {
  	if(data.results.length > 0) {
    	var source = $("#website-template").html();
    	var template = Handlebars.compile(source);
    	$('#website').html(template(data));
    }
    else {
    	var source = $("#website-template").html();
    	var template = Handlebars.compile(source);
    	$('#website').html(template({alert: 'No results'}));
    }
  });
  $.getJSON(web_base + "/api/via/" + query, function(data) {
		if(data.results.length > 0) {
    	var source = $("#image-template").html();
    	var template = Handlebars.compile(source);
    	$('#image').html(template(data));
    }
    else {
    	var source = $("#image-template").html();
    	var template = Handlebars.compile(source);
    	$('#image').html(template({alert: 'No results'}));
    }
  });
}

function getParams() {
	    var vars = [], hash;

        var hashes = window.location.href.slice(inArray('?', window.location.href) + 1).split('&');

	    // create array for each key
	    for(var i = 0; i < hashes.length; i++) {
	    	hash = hashes[i].split('=');
	    	vars[hash[0]] = [];
	    }

	    // populate newly created entries with values 
	    for(var i = 0; i < hashes.length; i++) {
	        hash = hashes[i].split('=');
	        if (hash[1]) {
	        	vars[hash[0]].push(decodeURIComponent(hash[1].replace(/\+/g, '%20')));
	        }
	    }

	    return vars;
}

function inArray( elem, array ) {
        if ( array.indexOf ) {
            return array.indexOf( elem );
        }

        for ( var i = 0, length = array.length; i < length; i++ ) {
            if ( array[ i ] === elem ) {
                return i;
            }
        }
        return -1;
    }