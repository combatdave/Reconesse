(function () {
  'use strict';

  // Initialize templating functions
  var profileCard = _.template($('#profile-card-template').html());

  // Setup
  window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
      loadArticles(function (res) {
        if (!atEnd) {
          offset += res.length;
        }
        if (res.length < pageSize) {
          atEnd = true;
        }
      });
    }
  };

  var searchTimeout = null,
      selectedCategories = [],
      selectedCountries = [];

  // Pagination vars
  var offset = 0,
      pageSize = 25,
      atEnd = false;

  $('#filter-search').on('click', function () {
    $('#grid').toggleClass('center');
    $('#filter').toggleClass('hide');
  });

  // Select all checkbox logic
  $('#select-all-countries').on('click', function(e) {
    if(this.checked) {
      $('.countries-checkbox').each(function() {
        this.checked = true;
      });
    }
    else {
      $('.countries-checkbox').each(function() {
        this.checked = false;
      });
    }
  });

  $('.countries-checkbox').on('change', function(e) {
    if(!this.checked) {
      $('#select-all-countries').prop('checked', false);
    } else {
      var allChecked = true;
      $('.countries-checkbox').each(function() {
        if (!this.checked) {
          allChecked = false;
        }
      });
      if (allChecked) {
        $('#select-all-countries').prop('checked', true);
      }
    }

    checkboxSearch();
  });

  $('#categories-list > ol li a').click(function() {
    $(this).parent().children('ol').toggle();
    $(this).parent().children('a').children('img').toggleClass('rotate');
  });

  $('.plus-tree').click();


  function categorySearch() {
    // Save selected categories
    var newSelectedCategories = [];
    $('.categories-checkbox').each( function(event) {
      if ($(this).attr('id') != 'select-all-categories') {
        var categoryName = $(this).attr('value');
        var checked = $(this).is(':checked');
        if (checked) {
          newSelectedCategories.push(categoryName);
        }
      }
    });
    selectedCategories = newSelectedCategories;

    // Now do the search
    if (searchTimeout !== null) {
      window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(autoSearch, 500);
  }

  function checkboxSearch() {
    var newSelectedCountries = [];
    $('.countries-checkbox').each(function() {
      var countryCode = $(this).attr('value');
      var checked = $(this).is(':checked');
      if (checked) {
        newSelectedCountries.push(countryCode);
      }
    });
    selectedCountries = newSelectedCountries;
    if (searchTimeout !== null) {
      window.clearTimeout(searchTimeout);
    }
    searchTimeout = window.setTimeout(autoSearch, 500);
  }

  function autoSearch () {
    offset = 0;
    atEnd = false;
    $('#grid').empty();
    salvattore.init();
    searchTimeout = null;
    loadArticles(function () { return; });
  }


  function checkParent(checkbox) {
    // Called when a checkbox has changed, so we can see if the parent needs to change state.
    // If this *does* cause a state change, then we call this function again to check the next parent up.

    var parentLabel = $(checkbox).parent().parent().parent().siblings('.categories-label')[0];
    var parentCheckbox = $(parentLabel).children('.categories-checkbox')[0];

    if (parentCheckbox) {
      var allChecked = true;
      $(parentCheckbox).parent().parent().find('.categories-checkbox').each(function() {
        if (this != parentCheckbox) {
          allChecked = allChecked && this.checked;
        }
      });

      if (parentCheckbox.checked != allChecked) {
        // This checkbox has changed, so do the change then check it's parent to see if it should change
        parentCheckbox.checked = allChecked;
        checkParent(parentCheckbox);
      }
    }
  }

  $('.categories-checkbox').on('click', function(e) {
    var modified = this;
    $(this).parent().parent().find('.categories-checkbox').each(function() {
      this.checked = modified.checked;
    });

    checkParent(this);
    categorySearch();
  });

  function renderCards(cards) {
    var grid = document.querySelector('#grid');
    salvattore.appendElements(grid, _.map(cards, function (c) {
      var item = document.createElement('div');
      var imgUrl = c.image;
      if (!imgUrl)
      {
        imgUrl = '/static/images/blank.gif'
      }
      item.innerHTML = (profileCard({
        image: imgUrl,
        name: c.name,
        summary: c.summary,
        url: '/past/' + c.slug + '/'
      }));
      return item;
    }));
  }

  function loadArticles(callback) {
    $.ajax({
      url: '/past/articles/',
      method: 'POST',
      data: {
        query: JSON.stringify({
          startindex: offset,
          num: pageSize,
          categories: selectedCategories,
          countrycodes: selectedCountries
        })
      },
      success: function (data) {
        renderCards(data.results);
        callback(data.results);
      }
    });
  }

  loadArticles(function () { return; });
})();
