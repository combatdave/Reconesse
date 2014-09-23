var map;
var showAllCategories = true;

// add all your code to this method, as this will ensure that page is loaded
AmCharts.ready(function() {
    // create AmMap object
    map = new AmCharts.AmMap();
    // set path to images
    map.pathToImages = "/static/ammap/images/"; //"http://www.ammap.com/lib/images/";

    var dataProvider = {
        mapURL: "/static/ammap/worldLow.svg",
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
    map.addListener("clickMapObject", function (e) {
        map.selectObject(null);
        showCountryArticles(e.mapObject.id);
        //ShowMenu(e);
    });
    
    loadData();

    map.dataProvider.zoomLongitude = 0;
    map.dataProvider.zoomLatitude = 24;
    map.dataProvider.zoomLevel = 1.2;
    
    // write the map to container div
    map.write("mapdiv");
});

function showCountryArticles(countryCode)
{
    var articleList = $('#list-country-articles');
    articleList.empty();
    articles = articlesByCountry[countryCode];
    for (var i = 0; i < articles.length; ++i)
    {
        var argv = {
            slug        : articles[i].slug,
            name        : articles[i].name,
            yearFrom    : GetLabelForYear(articles[i].birth),
            yearTo      : GetLabelForYear(articles[i].death),
            tags        : ''
        }

        for (var j = 0; j < articles[i].tags.length; ++j)
        {
            argv.tags += articles[i].tags[j] + " "
        }
        articleList.append(person_template(argv));   
    }
    $('#article-list-button').click();
}

/*
function ShowMenu(e) {
    $.fancybox({
        type: 'iframe',
        href: '/past/country/'+e.mapObject.id,
        width: "400",
        height: "400",
        closeClick: true,
        autoDimensions: false,
    }); 
}
*/

function setData(data) {
    //var parsedData = JSON.parse(data);

    SetYearDisplayText(data.minYear, data.maxYear);

    map.dataProvider.areas = data.areas;
    map.validateData();

    $("#searchloadingtext").text("");
}


function SetYearDisplayText(minYear, maxYear)
{
    $("#yearDisplay").text(GetLabelForYear(minYear) + " - " + GetLabelForYear(maxYear));
}


/*
 * ======
 * SEARCH
 * ======
 */

// Search parameters
var searchMinYear = null,
    searchMaxYear = null,
    selectedCategories = [],
    selectedCountries = [],
    keywords = [],
    tags = [];

// Global data
var articlesByCountry;

function loadData()
{
    $('input[name=category]').val(selectedCategories);
    $('input[name=countrycode]').val(selectedCountries);
    $('input[name=keyword]').val(keywords);
    $('input[name=tag').val(tags);
    $('input[name=minyear]').val(searchMinYear);
    $('input[name=maxyear]').val(searchMaxYear);

    var form = $('#query');
    $.ajax({
        url     : form.attr('action'),
        type    : form.attr('method'),
        data    : form.serialize(),
        success : function(data)
        {
            articlesByCountry = data.articles;
            setData(data);
        },
        error   : function(jqXHR)
        {
            console.log(jqXHR);
        }
    });
}

/*
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
*/


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

/*
 * ==========
 * SETUP SHIT
 * ==========
 */

function SetupSliderBar(minYear, maxYear)
{
    $(".sliderbar").each(function() {
        $(this).empty().slider({
            values: [minYear, maxYear],
            min: minYear,
            max: maxYear,
            step: 100,
            range: true,
            orientation: "horizontal",
            slide: updateSliders,
            change: updateSliders
        });
    });

    function updateSliders(e, ui) {
        if (!e.originalEvent) return;
        var range = ui.values;
        searchMinYear = parseInt(range[0]).toString();
        searchMaxYear = parseInt(range[1]).toString();
        $('.minYear').text(GetLabelForYear(range[0]));
        $('.maxYear').text(GetLabelForYear(range[1]));
        var activeSlider = this;
        $(".sliderbar").slider("values", range);
    };

    // Terrible, terrible hack.
    // Should definitely be done some other way.
    if (!article)
    {
        $('.ui-slider .ui-slider-handle').eq(0).append("<img src='/static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
        $('.ui-slider .ui-slider-handle').eq(1).append("<img src='/static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
        $('.ui-slider .ui-slider-handle').eq(2).append("<img src='/static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
        $('.ui-slider .ui-slider-handle').eq(3).append("<img src='/static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
    }
    else
    {
        $('.ui-slider .ui-slider-handle').eq(0).append("<img src='/static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
        $('.ui-slider .ui-slider-handle').eq(1).append("<img src='/static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
        $('.ui-slider .ui-slider-handle').eq(2).append("<img src='/static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
        $('.ui-slider .ui-slider-handle').eq(3).append("<img src='/static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
    }
    
}


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



$('#select-all-countries').on('click', function(e) { 
    if(this.checked) {
        $('.countries-checkbox').each(function() {
            this.checked = true;                        
        });
    }
    else
    {
        $('.countries-checkbox').each(function() {
            this.checked = false;                        
        });
    }
});

$('.countries-checkbox').on('change', function(e)
{
    if(!this.checked)
    {
        $('#select-all-countries').prop('checked', false);
    }
    else
    {
        var allChecked = true;
        $('.countries-checkbox').each(function() {
            if (!this.checked)
            {
                allChecked = false;
            }
        });
        if (allChecked)
        {
            $('#select-all-countries').prop('checked', true);
        }
    }
});

// If we are looking at a single article, we open the corresponding modal window
(function()
{
    var btn = $('#article-button');
    if (btn)
    {
        btn.click();
    }
})();

// TEMPLATES
var person_template;
$(document).ready(function()
{
    person_template = _.template($('#person-list-entry').html());
});