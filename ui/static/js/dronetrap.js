//TEST
$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
$(function() {
    $(window).bind("load resize", function() {
        console.log($(this).width())
        if ($(this).width() < 768) {
            $('div.sidebar-collapse').addClass('collapse')
        } else {
            $('div.sidebar-collapse').removeClass('collapse')
        }
    })
})



$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
$(function() {
    $(window).bind("load resize", function() {
        console.log($(this).width())
        if ($(this).width() < 768) {
            $('div.sidebar-collapse').addClass('collapse')
        } else {
            $('div.sidebar-collapse').removeClass('collapse')
        }
    })
})

var interval = 5000;
var map_markers = [];
var map_hardware = [];
var map_notams = [];
var map ;
var bounds;



function detections() {

    $.ajax({
        type: "GET",
        url: '/api/v01/get/targets/',
        dataType: 'json',
        success: function (data) {
            var rows = '';
            $("#sidebar-detections").empty();
            delete_markers();

            if (data["total"]>=1){
                if ($("#sidebar-detections").length !=0){
                    rows +='<li id="detected-list-group-item" class="list-group-item">';

                    $.each(data["targets"], function(idx,msg){
                        console.log(msg);
                        if (msg.error == "No drones found.") {
                            rows +='<div class="col-lg-12 col-md-12"><div class="panel panel-default"><div class="panel-heading"><div class="row"><div class="col-xs-2"><i class="fa fa-times fa-2x text-muted"></i></div><div class="col-xs-8 text-right"><div class="huge text-muted">NO DRONS</div></div></div></div><div class="panel-footer"><div class="row"><div class="col-xs-4"><i class="fa fa-gamepad fa-2x text-muted"></i></div><div class="col-xs-4"><i class="fa fa-video-camera fa-2x text-muted"></i></div><div class="col-xs-4"><i class="fa fa-crosshairs fa-2x text-muted"></i></div></div></div></div></div>';
                        }
                        else {
                        
                        paneltype = "primary";
                        camtext = "text-muted";
                        ctrltext = "text-muted";
                        gpstext = "text-muted";
                        conntext = "text-muted"; 
                        alert_bg = "danger";
                        if (msg.knowed) {
                          alert_bg = "warning";  
                        }
                        alert_status ="danger blink ";
                        rows +='<div class="row toggle" id="dropdown-detail-" data-toggle="detail-">';
                        rows +='<div class="panel panel-default "><div class="panel-heading bg-'+alert_bg+'"><div class="row">';
                        rows +='<div class="col-lg-5 col-xs-5 p-1 "><img src="/static/images/models/'+msg.vendor+"_"+msg.model+'.jpg" class="img-responsive"></div>';
                        rows +='<div class="col-xs-7 text-left"><div class="huge">Vendor: <strong>'+ msg.vendor +'</strong></div><div>Model: <strong>'+ msg.model+'</strong></div><div>Signal: <strong>'+ msg.rssi+'</strong></div></div></div></div>';
                        rows +='<div id="attack_button" class=" bg-'+alert_status+' panel-footer"><div id='+msg.sensorid+' class="attack_button row btn btn-sm btn-default center-block";>Attack</div></div></div></a></div>';

                        add_drone_marker_map(msg);
                        }});

                    rows +='</div></li>';
                    $("#sidebar-detections").append(rows);
                }

                $("#alert-label").addClass("label-danger blink").removeClass("label-success");
                $("#alert-label").text("DRONE DETECTED");
                $("#alert-number").text(data["active"]);
                $("#alert-number").removeClass("d-none");

              }else{

                $("#alert-label").addClass("label-success").removeClass("label-danger blink");
                $("#alert-label").text("NO ALERTS");
                $("#alert-number").addClass("d-none");

              }
            

        },
		complete: function (data){
			setTimeout(detections, interval);
		},
        error: function(jqXHR, textStatus, errorThrown){
        // handle any errors here
        }
    });
}

function attack_thread(id){
    alert("click al boto function "+id);
    $.ajax({
        type: "GET",
        url: '/api/v01/attack/'+id,
        dataType: 'json',
        success: function (data) {
            if (data=="OK"){
                
            }
        },
        complete: function (data){
        },
        error: function(jqXHR, textStatus, errorThrown){
        // handle any errors here
        }
    }); 
}

$(document).ready(function() {
    $(document).on('click','.attack_button',function()
    {
        alert("click al boto "+this.id);
        $.ajax({
            type: "GET",
            url: '/api/v01/attack/'+this.id,
            dataType: 'json',
            success: function (data) {
                if (data=="OK"){
                    alert("attack started");
                }
            },
            complete: function (data){
            },
            error: function(jqXHR, textStatus, errorThrown){
            // handle any errors here
            }
        });  
    }
    );
});

function show_devices() {

    $.ajax({
        type: "GET",
        url: '/api/v01/get/devices/',
        dataType: 'json',
        success: function (data) {
            var rows = '';
                console.log("[devices]"+data);
                $("#data-body").empty();
                $.each(data, function(idx,submsg){
                    $.each(submsg, function(idy,msg){
                    console.log(msg);
                    if (msg.error == "No devices found.") {
                        rows +='<div class="col-lg-12 col-md-12"><div class="panel panel-default"><div class="panel-heading"><div class="row"><div class="col-xs-2"><i class="fa fa-times fa-2x text-muted"></i></div><div class="col-xs-8 text-right"><div class="huge text-muted">NO DRONS</div></div></div></div><div class="panel-footer"><div class="row"><div class="col-xs-4"><i class="fa fa-gamepad fa-2x text-muted"></i></div><div class="col-xs-4"><i class="fa fa-video-camera fa-2x text-muted"></i></div><div class="col-xs-4"><i class="fa fa-crosshairs fa-2x text-muted"></i></div></div></div></div></div>';
                    }
                    else {
                        paneltype = "primary";
                        camtext = "text-muted";
                        ctrltext = "text-muted";
                        gpstext = "text-muted";
                        conntext = "text-muted";
                        if (msg.active){
                            _state = '<span class="label label-success">ACTIVE</span>';
                        }else{
                            _state = '<span class="label label-danger">INACTIVE</span>';
                            }
                        rows +='<tr data-item-id="item1" class="item">';
                        rows +='<td>'+msg.alias+'</td>';
                        rows +='<td>'+msg.serialnum+'</td>';
                        rows +='<td>'+msg.model+'</td>';
                        rows +='<td>'+msg.version+'</td>';
                        rows +='<td>'+_state+'</td>';
                        rows +='<td> -- </td>';
                        rows +='<td>'+msg.system_asigned+'</td>';
                        rows +='<td><a href="/devices/'+msg.deviceid+'" role="button" class="btn btn-sm btn-primary">Edit</a>';
                        rows +='</td></tr>';
                        }
                    });
                });
            
                $("#data-body").append(rows);

        },
        complete: function (data){
        },
        error: function(jqXHR, textStatus, errorThrown){
        // handle any errors here
        }
    });
}

function show_alerts() {

    $.ajax({
        type: "GET",
        url: '/api/v01/get/alerts/',
        dataType: 'json',
        success: function (data) {
            var rows = '';
                console.log("[alerts]"+data);
                $("#data-body").empty();
                $.each(data, function(idx,submsg){
                    $.each(submsg, function(idy,msg){
                    console.log(msg);
                    if (msg.error == "No drones found.") {
                        rows +='<div class="col-lg-12 col-md-12"><div class="panel panel-default"><div class="panel-heading"><div class="row"><div class="col-xs-2"><i class="fa fa-times fa-2x text-muted"></i></div><div class="col-xs-8 text-right"><div class="huge text-muted">NO DRONS</div></div></div></div><div class="panel-footer"><div class="row"><div class="col-xs-4"><i class="fa fa-gamepad fa-2x text-muted"></i></div><div class="col-xs-4"><i class="fa fa-video-camera fa-2x text-muted"></i></div><div class="col-xs-4"><i class="fa fa-crosshairs fa-2x text-muted"></i></div></div></div></div></div>';
                    }
                    else {
                    
                    paneltype = "primary";
                    camtext = "text-muted";
                    ctrltext = "text-muted";
                    gpstext = "text-muted";
                    conntext = "text-muted";
                    if (msg.active){
                        _state = '<span class="label label-success">ACTIVE</span>';
                    }else{
                        _state = '<span class="label label-danger">INACTIVE</span>';
                    }
                    rows +='<tr data-item-id="item1" class="item">';
                    rows +='<td>'+msg.id+'</td>';
                    rows +='<td>'+msg.model+'</td>';
                    rows +='<td>'+msg.first_time+'<br>'+msg.last_time+'</td>';
                    rows +='<td>'+diff_minutes(msg.last_time,msg.first_time)+'</td>';
                    rows +='<td>'+_state+'</td>';
                    rows +='<td>'+msg.active+'</td>';
                    rows +='<td><a href="/alerts/'+msg.id+'" role="button" class="btn btn-sm btn-primary">View</a>';
                    rows +='</td></tr>';
                    }});
                 

                });
            
                $("#data-body").append(rows);

        },
        complete: function (data){
        },
        error: function(jqXHR, textStatus, errorThrown){
        // handle any errors here
        }
    });
}

function get_alert_details() {
    $.ajax({
        type: "GET",
        url: '/api/v01/get/target/'+dataId,
        dataType: 'json',
        success: function (data) {
            if (data.error){
            $(".detail").text("---");
            }
            else {
            console.log("[get_alert_details]"+data);
            $("#serialnum_txt").text(data.serialnum);
            $("#speed_txt").text(data.speed);
            $("#orientation_txt").text(data.orientation);
            $("#latitude_txt").text(data.latitude);
            $("#longitude_txt").text(data.longitude);
            $("#home_latitude_txt").text(data.home_latitude);
            $("#home_longitude_txt").text(data.home_longitude);
            $("#rssi_txt").text(data.rssi);
            $("#precision_txt").text(data.precision);
            $("#detections_count_txt").text((data.detections_count));
            $("#last_time_txt").text(data.last_time);
            delete_markers();
            add_home_marker_map(data);
            add_drone_marker_map(data);
            show_markers(map);
            // setTimeout(get_alert_details(), interval);
            }
        },
        complete: function (data){
            
        },
        error: function(jqXHR, textStatus, errorThrown){
        // handle any errors here
        }
    });
}




function show_hardware(map){
	for (var i=0; i < map_hardware.length; i++) {
		map_hardware[i].setMap(map);
	}
}

// Global map varaible
var map;






function show_markers(map){
	for (var i=0; i < map_markers.length; i++) {
		map_markers[i].setMap(map);
	}
}

function show_track(map){
    for (var i=0; i < map_tracks.length; i++) {
        map_tracks[i].setMap(map);
    }
}

function clear_markers(){
	show_markers(null);
}

function delete_markers(){
	clear_markers();
	for (_marker in map_markers){
        map_markers[_marker].setMap(null);

    }
}

function show_map( _center,_zoom,_type){
	map = new google.maps.Map(document.getElementById('map_canvas'), {
	  zoom: _zoom,
	  center: _center,
	  mapTypeId: google.maps.MapTypeId.ROADMAP,
	  disableDefaultUI: true
	});
    bounds  = new google.maps.LatLngBounds();
}


function add_home_marker_map(data){
    var homeLatLng = {lat: parseFloat(data.home_latitude), lng: parseFloat(data.home_longitude) };
    //var pilotLatLng = {lat: trinfo.data.plat, lng: trinfo.data.plng};

    // Home Marker Image
    var home_image = {
      url: '/static/images/pilot_mrk_32.png',
      size: new google.maps.Size(32, 32),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(16, 16)
    };

    var home_marker = new google.maps.Marker({
              position: homeLatLng,
              map: map,
              title: 'Home',
              icon: home_image
            });

    map_markers.push(home_marker);
}

function add_drone_marker_map(data){
	var droneLatLng = {lat: parseFloat(data.latitude), lng: parseFloat(data.longitude) };
	//var pilotLatLng = {lat: trinfo.data.plat, lng: trinfo.data.plng};

	// Drone Marker Image
    var drone_image = {
      url: '/static/images/drone_mrk_32.png',
      size: new google.maps.Size(32, 32),
      origin: new google.maps.Point(0, 0),
      anchor: new google.maps.Point(16, 16)
    };

	var drone_marker = new google.maps.Marker({
	          position: droneLatLng,
	          map: map,
	          title: data.vendor+" "+data.model,
	          icon: drone_image
	        });

	map_markers.push(drone_marker);


	var range_circle = new google.maps.Circle({
		strokeColor: '#FF0000',
		strokeOpacity: 0.2,
		strokeWieight: 1,
		fillColor: '#FF0000',
		map:map,
		center: droneLatLng,
		radius: Math.sqrt( data.precision) * 10

	})
	map_markers.push(range_circle);
    bounds.extend(droneLatLng);
	var infowindow = new google.maps.InfoWindow();
    //map.fitBounds(bounds);
    if ($("#autocenter").is(":checked")){
           map.setCenter(droneLatLng);
    }
 

}


var elem = document.documentElement;

/* View in fullscreen */
function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) { /* Firefox */
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE/Edge */
    elem.msRequestFullscreen();
  }
}

/* Close fullscreen */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) { /* Firefox */
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) { /* Chrome, Safari and Opera */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE/Edge */
    document.msExitFullscreen();
  }
}

function diff_minutes(dt1,dt2)
{
    time2 = new Date(Date.parse(dt2));
    time1 = new Date(Date.parse(dt1));
    var diff =(time2.getTime() - time1.getTime())/1000;
    diff/=60;
    console.log("Resultat de diff "+diff)
    return Math.abs(Math.round(diff));
}





