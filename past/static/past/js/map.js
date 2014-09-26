var map;
var showAllCategories = true;

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
    $('#country_name').text(countries[countryCode]);
    $('#article-list-button').click();
}

function setData(data) {
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
    $('input[name=tag]').val(tags);
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
            saveSettings();
        },
        error   : function(jqXHR)
        {
            console.log(jqXHR);
        }
    });
}

function GetLabelForYear(year) {
    var label = "AD";
    if (year < 0) {
        label = "BC";
    }
    return Math.abs(year).toString() + " " + label
}

function applySettings(s)
{
    $('input:checkbox').removeAttr('checked');
    if (s.minYear && s.maxYear)
    {
        $(".sliderbar").slider("values", [s.minYear, s.maxYear]);
        searchMinYear = s.minYear;
        searchMaxYear = s.maxYear;
    }
    if (s.categories)
    {
        selectedCategories = s.categories;
        for (var i = 0; i < selectedCategories.length; ++i)
        {
            $(":checkbox[value='" + selectedCategories[i] + "']").prop("checked","true");
        }
    }
    if (s.countries)
    {
        selectedCountries = s.countries;
        for (var i = 0; i < selectedCountries.length; ++i)
        {
            $(":checkbox[value='" + selectedCountries[i] + "']").prop("checked","true");
        }
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
    if (s.keywords)
    {
        keywords = s.keywords;
        var kwString = "";
        for (var i = 0; i < keywords.lenght; ++i)
        {
            kwString += (keywords[i] + ', ');
        }
        $('#keyword-box').val(kwString);
    }
    // TODO
    /*
    if (s.tags)
    {
        tags = s.tags;

    }
    */
}

function saveSettings()
{
    if (storage.support())
    {
        storage.settings.minYear = $('#minYear').text();
        storage.settings.maxYear = $('#maxYear').text();
        storage.settings.categories = selectedCategories;
        storage.settings.countries = selectedCountries;
        storage.settings.keywords = keywords;
        console.log(storage);
        localStorage['settings'] = JSON.stringify(storage.settings);
        console.log('Settings saved')
    }
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

    $('.ui-slider .ui-slider-handle').eq(0).append("<img src='/static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
    $('.ui-slider .ui-slider-handle').eq(1).append("<img src='/static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
    $('.ui-slider .ui-slider-handle').eq(2).append("<img src='/static/images/sliderhandleleft.png' class='ui-slider-handle-left'/>");
    $('.ui-slider .ui-slider-handle').eq(3).append("<img src='/static/images/sliderhandleright.png' class='ui-slider-handle-right'/>");
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
    $("input:checkbox[name=search]").each( function(event) {
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
    saveCheckboxes();
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

    saveCheckboxes();
});


function saveCheckboxes()
{
    var newSelectedCountries = []
    $('.countries-checkbox').each(function() {
        var countryCode = $(this).attr("value");
        var checked = $(this).is(":checked");
        if (checked) {
            newSelectedCountries.push(countryCode);
        }
    });
    selectedCountries = newSelectedCountries;
    if (searchTimeout != null)
    {
        window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(AutoSearch, 500);
}


$('#keyword-box').on('keydown', function(e)
{
    var ENTER_KEY = 13, SPACE_KEY = 32;
    var kw = $(this).val();
    var k = e.keyCode;
    if (k === ENTER_KEY || k === SPACE_KEY)
    {
        parseKeywords(kw);
    }
});

$('#keyword-box').on('focusout', function()
{
    var kw = $(this).val();
    parseKeywords(kw);
});


function parseKeywords(kw)
{
    keywords = kw.split(/(?:,| |;)+/);
    if (searchTimeout != null)
    {
        window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(AutoSearch, 500);
}

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

    // BOOKMARKS
    if (storage.support())
    {
        // If localStorage is supported by client browser
        if (typeof localStorage['bookmarks'] === 'undefined')
            localStorage['bookmarks'] = JSON.stringify([]);

        storage.bookmarks = JSON.parse(localStorage['bookmarks']);
        //renderBookmarkArray(storage.bookmarks)
        console.log(localStorage['settings'])
        if (typeof localStorage['settings'] === 'undefined')
            localStorage['settings'] = JSON.stringify({});
        console.log(localStorage['settings'])
        storage.settings = JSON.parse(localStorage['settings']);
        applySettings(storage.settings);
    }
});