'use strict';

var svgWrapper;
var positionDot;
var gProfileHint;
var posMarker;
var posMarkerCurrentAlt;
var posMarkerCurrentPos;

function showSpotOnTrackNoElev(offsetX)
{
  var ep_width = svgWrapper.width();
  var ep_point=0;
  var ep_vertex;
  var ep_pc = (offsetX *100/ep_width) | 0;
  var ep_currentDistance=0;
  if (gpoly)
  {
    var polyPath =gpoly.getPath();
    ep_point = (ep_pc * polyPath.length / 100) | 0;
    ep_vertex = polyPath.getAt(ep_point);	//getVertex

    //distancia
    ep_currentDistance = ( trinfo.l / ep_width) * offsetX;
    if(trinfo.units.x == 1)//nautical miles
      $('#pm-pos').text( (Math.round( (ep_currentDistance / 1852) *10)/10).toLocaleString(isoLang) + trinfo.units.lx);
    else if(trinfo.units.x == 2)//miles
      $('#pm-pos').text( (Math.round( (ep_currentDistance * 0.621371192) /100)/10).toLocaleString(isoLang) + trinfo.units.lx);
    else//km
      $('#pm-pos').text( (Math.round(ep_currentDistance /100)/10).toLocaleString(isoLang) + trinfo.units.lx);

    if (gProfileHint.getMap() == null){
      gProfileHint.setMap(map);
    }
    else if (!map.getBounds().contains(ep_vertex))
      map.panTo(ep_vertex);
    gProfileHint.setPosition(ep_vertex);
    gProfileHint.setVisible(true);

  }

}

function showSpotOnTrack(offsetX)
{
  var pmAlt = $('#pm-alt');
  var pmPos = $('#pm-pos');
  var ep_width = svgWrapper.width();
  var ep_point  = Math.round(( offsetX * trinfo.data.ncoords ) / ep_width);
  var ep_vertex = new  google.maps.LatLng( trinfo.data.lat[ep_point], trinfo.data.lng[ep_point] );

  //alçada
  if(trinfo.units.y == 1)//feets
    pmAlt.text( (Math.round(trinfo.data.ele[ep_point]* 3.2808399)).toLocaleString(isoLang)  + trinfo.units.ly);
  else//meters
    pmAlt.text( trinfo.data.ele[ep_point].toLocaleString(isoLang) + trinfo.units.ly);

  //distancia
  var ep_currentDistance = ( trinfo.l / ep_width) * offsetX;
  if(trinfo.units.x == 1)//nautical miles
    pmPos.text( (Math.round( (ep_currentDistance / 1852) *10)/10).toLocaleString(isoLang) +" "+ trinfo.units.lx);
  else if(trinfo.units.x == 2)//miles
    pmPos.text( (Math.round( (ep_currentDistance * 0.621371192) /100)/10).toLocaleString(isoLang) +" "+ trinfo.units.lx);
  else//km
    pmPos.text( (Math.round(ep_currentDistance /100)/10).toLocaleString(isoLang) +" "+ trinfo.units.lx);

  positionDot
    .attr('cx', trinfo.data.polylineCoods[ep_point][0])
    .attr('cy', trinfo.data.polylineCoods[ep_point][1]);

  if (typeof gProfileHint === 'object' && gProfileHint.getMap() == null)
    gProfileHint.setMap(map);
  else if (!map.getBounds().contains(ep_vertex))
    map.panTo(ep_vertex);

  if (typeof gProfileHint === 'object'){
    gProfileHint.setPosition(ep_vertex);
    gProfileHint.setVisible(true);
  }
}


function getOffsetX(e, self) {
  var offsetX;
  if (window.TouchEvent && e.originalEvent instanceof TouchEvent) {
    offsetX = Math.floor(e.originalEvent.touches[0].pageX
        - self.offset().left);
  } else {
    offsetX = Math.floor(e.pageX - self.offset().left); //offset().left torna decimals a firefox
  }
  return offsetX;
}

function setDroneMarker(e, self) {
  posMarker.show();
  posMarkerCurrentAlt.show();
  posMarkerCurrentPos.show();
  positionDot.show();

  var offsetX;
  if (e) {
    offsetX = getOffsetX(e, self);
  } else {
    offsetX = parseInt(posMarker.css('left'), 10);
  }

  if (offsetX >= 0 && offsetX < svgWrapper.width()) {
    if (trinfo && trinfo.data) {
      showSpotOnTrack(offsetX);
    } else {
      showSpotOnTrackNoElev(offsetX);
    }

    var widthPosMarkerCurrentAlt = parseInt(
        posMarkerCurrentAlt.css('width'), 10);
    var widthPosMarkerCurrentPos = parseInt(
        posMarkerCurrentPos.css('width'), 10);
    var svgWrapperWidth = svgWrapper.width();
    if (offsetX - widthPosMarkerCurrentPos / 2 < 0) {
      posMarkerCurrentPos.css('left', 0);
    } else if (offsetX + widthPosMarkerCurrentPos / 2 > svgWrapperWidth) {
      posMarkerCurrentPos.css('left', svgWrapperWidth
          - widthPosMarkerCurrentPos);
    } else {
      posMarkerCurrentPos.css('left', offsetX - widthPosMarkerCurrentPos / 2);
    }
    if (offsetX - widthPosMarkerCurrentAlt / 2 < 0) {
      posMarkerCurrentAlt.css('left', 0);
    } else if (offsetX + widthPosMarkerCurrentAlt / 2 > svgWrapperWidth) {
      posMarkerCurrentAlt.css('left', svgWrapperWidth
          - widthPosMarkerCurrentAlt);
    } else {
      posMarkerCurrentAlt.css('left', offsetX - widthPosMarkerCurrentAlt / 2);
    }
    // posMarkerCurrentAlt.css('top', positionDot.offset().top
    //     - self.offset().top - 24);
    // posMarkerCurrentPos.css('top', positionDot.offset().top
    //     - self.offset().top + 14);
    posMarker.css('left', offsetX);
  }
}

function initElevationProfile() {
  elevationProfileSvg.render({
    el: elevationChartContainer,
    width: elevationChartContainer.offsetWidth,
    height: elevationChartContainer.offsetHeight,
    elevations: trinfo.data.ele,
    minElevation: minElevation,
    maxElevation: maxElevation
  });

  /* elevation profile */
  posMarker = $('#pos-marker');
  posMarkerCurrentAlt = $('#pos-marker-current-alt');
  posMarkerCurrentPos = $('#pos-marker-current-pos');
  positionDot = $('#position-dot');
  svgWrapper = $(".map_svg-wrapper");

  if (trinfo && trinfo.data) {
    trinfo.data.polylineCoods = elevationProfileSvg.getPolylineCoords();
    trinfo.data.polylineCoods.shift();
    trinfo.data.polylineCoods.pop();
  }

  svgWrapper.off();
  svgWrapper.on('mouseover', function (e) {
    posMarkerCurrentAlt.show();
    posMarkerCurrentPos.show();
    positionDot.show();

    if (!trinfo.data) {
      posMarkerCurrentAlt.hide();
      svgWrapper.css("background-image",
          "url('https://sc.wklcdn.com/images/profile-pending.png') ").css(
          "background-position", "45% 50%").css("background-repeat",
          "no-repeat");
    }
  }).on('mouseout', function (e) {
    posMarker.hide();
    posMarkerCurrentAlt.hide();
    posMarkerCurrentPos.hide();
    positionDot.hide();
    if (gProfileHint) {
      gProfileHint.setVisible(false);
    }
  }).on('mousemove touchmove', function (e) {
    setDroneMarker(e, $(this));
  });
}

$(document).ready(function () {
  initElevationProfile();

  $(".el-button").click(function (e) {
    $('#elevation-profile').toggle();
    $('#elevation-profile-but').toggle();
    e.stopPropagation();
  });
  $("#elevation-profile-but").on('click', function (e) {
    $('#elevation-profile').toggle();
    $('#elevation-profile-but').toggle();
  });
});
