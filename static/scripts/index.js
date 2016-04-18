$(document).on('mouseenter', '.title-container', function () {
  $('.title').addClass('hidden');
}).on('mouseleave', '.title-container', function () {
  $('.title').removeClass('hidden');
});

$(document).on('mouseenter', '.call-to-action-container', function () {
  $('.call-to-action').addClass('hidden');
}).on('mouseleave', '.call-to-action-container', function () {
  $('.call-to-action').removeClass('hidden');
});
