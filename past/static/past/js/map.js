var map;
var showAllCategories = true;

// add all your code to this method, as this will ensure that page is loaded
AmCharts.ready(function() {
    // create AmMap object
    map = new AmCharts.AmMap();
    // set path to images
    map.pathToImages = "../static/ammap/images/"; //"http://www.ammap.com/lib/images/";

    var dataProvider = {
        mapURL: "../static/ammap/worldLow.svg",
        getAreasFromMap: true,          
    }; 
    // pass data provider to the map object
    map.dataProvider = dataProvider;

    map.areasSettings = {
        autoZoom: false,
        selectable: true,
        color: "#FFCC33",
        colorSolid: "#FFFFCC",
        outlineColor: "#33bcff",
        rollOverOutlineColor: "#FFFFFF",
    };

    var zoomColor = "#FFFF00";
    map.zoomControl.buttonColor = zoomColor;
    map.zoomControl.buttonFillColor = zoomColor;
    map.zoomControl.buttonIconColor = "#000000";
    map.zoomControl.gridColor = "#000000";
    map.zoomControl.homeIconColor = "#000000";
    map.zoomControl.zoomControlEnabled = false;
    map.zoomControl.panControlEnabled = false;

    map.colorSteps = 3;
    map.height = "100%";
    map.mouseWheelZoomEnabled = true;

    map.balloon.color = "#000000";

    map.allowClickOnSelectedObject = true;
    map.addListener("clickMapObject", function (event) {
        map.selectObject(null);
        ShowMenu(event);
    });
    
    showAllCategories = true;
    loadData();

    map.dataProvider.zoomLongitude = 0;
    map.dataProvider.zoomLatitude = 24;
    map.dataProvider.zoomLevel = 1.2;
    
    // write the map to container div
    map.write("mapdiv");
});


function ShowMenu(e) {
    $.fancybox({
        type: 'iframe',
        href: '/past/country/'+event.mapObject.id,
        width: "400",
        height: "400",
        closeClick: true,
        autoDimensions: false,
    });
}


function setData(data) {
    var parsedData = JSON.parse(data);

    SetYearDisplayText(parsedData.minYear, parsedData.maxYear);

    map.dataProvider.areas = parsedData.areas;
    map.validateData();

    $("#searchloadingtext").text("");
}


function SetYearDisplayText(minYear, maxYear)
{
    $("#yearDisplay").text(GetLabelForYear(minYear) + " - " + GetLabelForYear(maxYear));
}


var searchMinYear = null;
var searchMaxYear = null;
var selectedCategories = []


function loadData(){
    file = "mapdata.json";

    var queryParams = {
        minYear: searchMinYear,
        maxYear: searchMaxYear,
        filterCategories: selectedCategories,
        showAll: showAllCategories,
    };

    file = file + "?" + $.param(queryParams);

    var request;
    if (window.XMLHttpRequest) {
        request = new XMLHttpRequest();
        // load
        request.open('GET', file, false);
        request.send();
        setData(request.responseText);
    }
}


var lastCountryCode = null;
var lastArticleID = null;


function ShowMenu(event) {
    lastCountryCode = event.mapObject.id;
    lastArticleID = null;
    OpenCountryListFancybox();
}


function OpenCountryListFancybox()
{
    $.fancybox.open({
        type: 'iframe',
        href: '/past/country/'+lastCountryCode,
        width: "400px",
        height: "400px",
        padding: "0px",
        closeClick: true,
    });
}


function OpenArticle(url, articleID)
{
    lastArticleID = articleID;

    $.fancybox.open({
        href: url,
        type: "iframe",
        padding: "0px",
        afterClose: function() {
            ReOpenList();
        },
    });
}


function ReOpenList()
{
    OpenCountryListFancybox();
}


function GetLabelForYear(year) {
    var label = "AD";
    if (year < 0) {
        label = "BC";
    }
    return Math.abs(year).toString() + " " + label
}

//  SETUP SHIT

function SetupSliderBar(minYear, maxYear)
{
    var $sliderbar = $("#sliderbar").slider({
        range: true, 
        min: minYear, 
        max: maxYear, 
        values: [minYear, maxYear],
        step: 100,
    });

    $sliderbar.on({
        slidechange: function(event, ui){
            var range = ui.values;

            searchMinYear = parseInt(range[0]).toString();
            searchMaxYear = parseInt(range[1]).toString();

            loadData();
        }
    });

    $('.ui-slider .ui-slider-handle').eq(0).append("<img src='../static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
    $('.ui-slider .ui-slider-handle').eq(1).append("<img src='../static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
}


$(function(){
    $('.slide-out-div').tabSlideOut({
        tabHandle: '.handle',                     
        pathToTabImage: "../static/images/search.png",
        imageHeight: '122px',                     
        imageWidth: '40px',                       
        tabLocation: 'right',
        speed: 300,
        action: 'click',
        topPos: '200px',
        leftPos: '20px',
        fixedPosition: false
    });

});


var searchTimeout = null;


function AutoSearch()
{
    searchTimeout = null;
    loadData();
}


$('#auto-checkboxes').bonsai({
    expandAll: true,
    checkboxes: true,
    createCheckboxes: true,
});

$("#auto-checkboxes :checkbox").change( function(event) {
    showAllCategories = false;
    newSelectedCategories = []
    $("input:checkbox").each( function(event) {
        var categoryName = $(this).attr("value");
        var checked = $(this).is(":checked");
        if (checked) {
            newSelectedCategories.push(categoryName);
        }
    });
    selectedCategories = newSelectedCategories;

    if (searchTimeout != null)
    {
        window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(AutoSearch, 500);
    $("#searchloadingtext").text("Please wait...");
});