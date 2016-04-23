var map;
var showAllCategories = true;

AmCharts.ready(function() {
    // create AmMap object
    map = new AmCharts.AmMap();
    // set path to images
    map.pathToImages = '/static/ammap/images/'; //'http://www.ammap.com/lib/images/';

    var dataProvider = {
        map: 'worldLow',
        getAreasFromMap: true,
    };
    // pass data provider to the map object
    map.dataProvider = dataProvider;

    map.areasSettings = {
        autoZoom: false,
        selectable: true,
        color: '#FFFFCC',
        colorSolid: '#FFCC33',
        outlineColor: '#33bcff',
        rollOverOutlineColor: '#FFFFFF',
    };

    var zoomColor = '#FFFF00';
    map.zoomControl.buttonColor = zoomColor;
    map.zoomControl.buttonFillColor = zoomColor;
    map.zoomControl.buttonIconColor = '#000000';
    map.zoomControl.gridColor = '#000000';
    map.zoomControl.homeIconColor = '#000000';
    map.zoomControl.zoomControlEnabled = false;
    map.zoomControl.panControlEnabled = false;

    map.colorSteps = 3;
    map.height = '100%';
    map.mouseWheelZoomEnabled = true;

    map.balloon.color = '#000000';

    map.allowClickOnSelectedObject = true;
    map.addListener('clickMapObject', function (e) {
        map.selectObject(null);
        showCountryArticles(e.mapObject.id);
        //ShowMenu(e);
    });

    loadData();

    map.dataProvider.zoomLongitude = 0;
    map.dataProvider.zoomLatitude = 24;
    map.dataProvider.zoomLevel = 1.2;

    // write the map to container div
    map.write('mapdiv');
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
        };

        if (articles[i].deathYearUnknown)
        {
            argv["yearTo"] = "unknown";
        }
        else if (articles[i].death == null)
        {
            argv["yearTo"] = "present";
        }

        for (var j = 0; j < articles[i].tags.length; ++j)
        {
            argv.tags += '#' + articles[i].tags[j] + ' ';
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

    $('#searchloadingtext').text('');
}


function SetYearDisplayText(minYear, maxYear)
{
    $('#yearDisplay').text(GetLabelForYear(minYear) + ' - ' + GetLabelForYear(maxYear));
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
    $('input[name=category]').val(JSON.stringify(selectedCategories));
    $('input[name=countrycode]').val(JSON.stringify(selectedCountries));
    $('input[name=keyword]').val(JSON.stringify(keywords));
    $('input[name=tag]').val(JSON.stringify(tags));
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
            populateAllEntries();
            setData(data);
            //saveSettings();
        },
        error   : function(jqXHR)
        {
            console.log(jqXHR);
        }
    });
}

function tagSearch(tag)
{
    $.ajax({
        url     : '/past/tagsearch/',
        type    : 'GET',
        data    : {tag: tag},
        success : function(data)
        {
            $('#country_name').text(data.tag);
            var node = $('#list-country-articles');
            for (var i = 0; i < data.articles.length; ++i)
            {
                var argv = data.articles[i];
                argv = {
                    name : argv.name,
                    slug : argv.slug,
                    yearFrom: GetLabelForYear(argv.birth),
                    yearTo: GetLabelForYear(argv.death)
                };
                node.append(person_template(argv));
            }
            $('.md-overlay').click();
            $('#article-list-button').click();
        },
        error   : function(jqXHR)
        {
            console.log(jqXHR);
        }
    });
}
$('.hashtag').on('click', function()
{
    tagSearch($(this).attr('tag'));
});

function populateAllEntries()
{
    var node = $('.all-entries');
    node.empty();
    var keys = [];
    for (var key in articlesByCountry)
    {
        if (articlesByCountry.hasOwnProperty(key))
        {
            keys.push(key);
        }
    }

    keys.sort();

    len = keys.length;

    for (var j = 0; j < keys.length; ++j)
    {
        var obj = articlesByCountry[keys[j]];
        for (var i = 0; i < obj.length; ++i)
        {
            var argv = {
                slug: obj[i].slug,
                name: obj[i].name,
                yearFrom: GetLabelForYear(obj[i].birth),
                yearTo: GetLabelForYear(obj[i].death)
            };
            node.append(person_template(argv));
        }
    }
}

function GetLabelForYear(year) {
    var label = '';
    if (typeof year == 'number' && year < 0)
    {
        label = 'BCE';
    }
    return Math.abs(year).toString() + ' ' + label;
}

// NOTE:
// Settings are currently not being used
function applySettings(s)
{
    $('input:checkbox').removeAttr('checked');
    if (s.minYear && s.maxYear)
    {
        $('.sliderbar').slider('values', [s.minYear, s.maxYear]);
        searchMinYear = s.minYear;
        searchMaxYear = s.maxYear;
    }
    if (s.categories)
    {
        selectedCategories = s.categories;
        for (var i = 0; i < selectedCategories.length; ++i)
        {
            $(':checkbox[value=' + selectedCategories[i] + ']').prop('checked','true');
        }
    }
    if (s.countries)
    {
        selectedCountries = s.countries;
        for (var i = 0; i < selectedCountries.length; ++i)
        {
            $(':checkbox[value=' + selectedCountries[i] + ']').prop('checked','true');
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
    if (s.categories)
    {
        selectedCategories = s.categories;
        for (var i = 0; i < selectedCategories.length; ++i)
        {
            $(':checkbox[value=' + selectedCategories[i] + ']').prop('checked','true');
        }
        var allChecked = true;
        $('.categories-checkbox').each(function() {
            if ($(this).attr('id') != 'select-all-categories' && !this.checked)
            {
                allChecked = false;
            }
        });
        if (allChecked)
        {
            $('#select-all-categories').prop('checked', true);
        }
    }
    if (s.keywords)
    {
        keywords = s.keywords;
        var kwString = '';
        for (var i = 0; i < keywords.length; ++i)
        {
            kwString += (keywords[i] + ', ');
        }
        $('#keyword-box').val(kwString);
    }
}

function applySettings()
{
    // Overwrite the other applySettings to turn off the parameter storage
}

// NOTE:
// Settings are currently not being used
function saveSettings()
{
    if (storage.support())
    {
        storage.settings.minYear = $('#minYear').text();
        storage.settings.maxYear = $('#maxYear').text();
        storage.settings.categories = selectedCategories;
        storage.settings.countries = selectedCountries;
        storage.settings.keywords = keywords;

        localStorage['settings'] = JSON.stringify(storage.settings);
    }
}

/*
 * ==========
 * SETUP SHIT
 * ==========
 */

function SetupSliderBar(minYear, maxYear)
{
    $('.sliderbar').each(function() {
        $(this).empty().slider({
            values: [minYear, maxYear],
            min: minYear,
            max: maxYear,
            step: 100,
            range: true,
            orientation: 'horizontal',
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
        $('.sliderbar').slider('values', range);
        if (searchTimeout != null)
        {
            window.clearTimeout(searchTimeout);
        }
        searchTimeout = window.setTimeout(AutoSearch, 500);
    };

    $('.ui-slider .ui-slider-handle').eq(0).append('<img src=\'/static/images/sliderhandleleft.png\' class=\'ui-slider-handle-left\'/>');
    $('.ui-slider .ui-slider-handle').eq(1).append('<img src=\'/static/images/sliderhandleright.png\' class=\'ui-slider-handle-right\'/>');
    $('.ui-slider .ui-slider-handle').eq(2).append('<img src=\'/static/images/sliderhandleleft.png\' class=\'ui-slider-handle-left\'/>');
    $('.ui-slider .ui-slider-handle').eq(3).append('<img src=\'/static/images/sliderhandleright.png\' class=\'ui-slider-handle-right\'/>');
}


var searchTimeout = null;


function AutoSearch()
{
    searchTimeout = null;
    loadData();
}


$('#categories-list > ol li a').click(function() {
    $(this).parent().children('ol').toggle();
    $(this).parent().children('a').toggle();
});


function DoCategorySearch()
{
    // Save selected categories
    newSelectedCategories = []
    $('.categories-checkbox').each( function(event) {
        if ($(this).attr('id') != 'select-all-categories')
        {
            var categoryName = $(this).attr('value');
            var checked = $(this).is(':checked');
            if (checked) {
                newSelectedCategories.push(categoryName);
            }
        }
    });
    selectedCategories = newSelectedCategories;

    // Now do the search
    if (searchTimeout != null)
    {
        window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(AutoSearch, 500);
    $('#searchloadingtext').text('Please wait...');
}


function CheckParent(checkbox)
{
    // Called when a checkbox has changed, so we can see if the parent needs to change state.
    // If this *does* cause a state change, then we call this function again to check the next parent up.

    var parentLabel = $(checkbox).parent().parent().parent().siblings('.categories-label')[0];
    var parentCheckbox = $(parentLabel).children('.categories-checkbox')[0];

    if (parentCheckbox)
    {
        var allChecked = true;
        $(parentCheckbox).parent().parent().find('.categories-checkbox').each(function() {
            if (this != parentCheckbox)
            {
                allChecked = allChecked && this.checked;
            }
        });

        if (parentCheckbox.checked != allChecked)
        {
            // This checkbox has changed, so do the change then check it's parent to see if it should change
            parentCheckbox.checked = allChecked;
            CheckParent(parentCheckbox);
        }
    }

    DoCategorySearch();
}


$('.categories-checkbox').on('click', function(e)
{
    var modified = this;
    $(this).parent().parent().find('.categories-checkbox').each(function() {

        this.checked = modified.checked;
    });

    CheckParent(this);
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
        var countryCode = $(this).attr('value');
        var checked = $(this).is(':checked');
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

// =================
// BOOKMARK HANDLING
// =================

$('#list-country-articles').on('click', '.bookmark-container', function(e)
{
    e.preventDefault();
    e.stopPropagation();
    var data = $(this).attr('bookmark-data');
    var obj = JSON.parse(data);
    saveBookmarks(obj);
});

$('#list-bookmark-entries').on('click', '.bookmark-container', function(e)
{
    e.preventDefault();
    e.stopPropagation();
    var data = $(this).attr('bookmark-data');
    var obj = JSON.parse(data);
    removeBookmark(obj.slug);
});

function saveBookmarks(obj)
{
    if (obj)
    {
        if (!slugInBookmarks(obj.slug)) storage.bookmarks.push(obj);
    }
    if (storage.support())
        localStorage['bookmarks'] = JSON.stringify(storage.bookmarks);
    renderBookmarks();
}

function removeBookmark(slug)
{
    for (var i = 0; i < storage.bookmarks.length; ++i)
    {
        if (storage.bookmarks[i].slug == slug)
        {
            storage.bookmarks.splice(i, 1);
            saveBookmarks();
        }
    }
    renderBookmarks();
}

function slugInBookmarks(slug)
{
    for (var i = 0; i < storage.bookmarks.length; ++i)
    {
        if (storage.bookmarks[i].slug == slug)
        {
            return true;
        }
    }
    return false;
}

function renderBookmarks()
{
    var node = $('#list-bookmark-entries');
    node.empty();
    for (var i = 0; i < storage.bookmarks.length; ++i)
    {
        var obj = storage.bookmarks[i];
        var argv = {
            name: obj.name,
            yearFrom: obj.birth,
            yearTo: obj.death,
            slug: obj.slug
        };
        node.append(bookmark_template(argv));
    }
}

// ========
// KEYWORDS
// ========

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

$('.md-close-button').on('click', function()
{
    $('.md-overlay').click();
});

$('.md-back-button').on('click', function()
{
    window.history.go(-1);
});

$('.md-forward-button').on('click', function()
{
    window.history.go(1);
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

// ============================
// SINGLE ARTICLE VIEW SPECIFIC
// ============================
// If we are looking at a single article, we open the corresponding modal window
(function()
{
    var btn = $('#article-button');
    if (btn)
    {
        btn.click();
    }
})();

// ===================
// TEMPLATES AND SETUP
// ===================
var person_template, bookmark_template;
$(document).ready(function()
{
    person_template = _.template($('#person-list-entry').html());
    bookmark_template = _.template($('#bookmark').html());

    // BOOKMARKS
    if (storage.support())
    {
        // If localStorage is supported by client browser
        if (typeof localStorage['bookmarks'] === 'undefined')
            localStorage['bookmarks'] = JSON.stringify([]);

        storage.bookmarks = JSON.parse(localStorage['bookmarks']);


        if (typeof localStorage['settings'] === 'undefined')
        {
            saveSettings();
        }

        storage.settings = JSON.parse(localStorage['settings']);
        //applySettings(storage.settings);
    }
    renderBookmarks();

    $('#categories-list > ol li a').parent().find('ol').hide();
});

$(document).on('keydown', function(e)
{
    if (e.keyCode == 27)
        $('.md-overlay').click();
})
