(function () {
  'use strict';

  // Initialize templating functions
  var profileCard = _.template($('#profile-card-template').html());

  // Setup
  window.onscroll = function(ev) {
    if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
      loadArticles(offset, pageSize);
    }
  };

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
    saveCheckboxes();
  });

  $('.countries-checkbox').on('change', function(e) {
    if(!this.checked) {
      $('#select-all-countries').prop('checked', false);
    }
    else
    {
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
  });

  function renderCards(cards) {
    var grid = document.querySelector('#grid');
    salvattore.appendElements(grid, _.map(cards, function (c) {
      var item = document.createElement('div');
      item.innerHTML = (profileCard({
        image: c.image,
        name: c.name,
        summary: c.summary,
        url: '/past/' + c.slug + '/'
      }));
      return item;
    }));
  }

  function loadArticles() {
    $.ajax({
      url: '/past/articles/',
      method: 'POST',
      data: {
        query: JSON.stringify({
          startindex: offset,
          num: pageSize
        })
      },
      success: function (data) {
        offset += pageSize;
        console.log(offset);
        if (data.results.length < pageSize) {
          atEnd = true;
        }
        renderCards(data.results);
      }
    });
  }

  loadArticles();
})();
