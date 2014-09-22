// Initialize modal window effects
var ModalEffects = (function() {

	function init() {

		var overlay = document.querySelector( '.md-overlay' );

		[].slice.call( document.querySelectorAll( '.md-trigger' ) ).forEach( function( el, i ) {

			var modal = document.querySelector( '#' + el.getAttribute( 'data-modal' ) ),
				close = modal.querySelector( '.md-close' );

			function removeModal( hasPerspective ) {
				classie.remove( modal, 'md-show' );

				if( hasPerspective ) {
					classie.remove( document.documentElement, 'md-perspective' );
				}
			}

			function removeModalHandler() {
				removeModal( classie.has( el, 'md-setperspective' ) ); 
			}

			el.addEventListener( 'click', function( ev ) {
				classie.add( modal, 'md-show' );
				overlay.removeEventListener( 'click', removeModalHandler );
				overlay.addEventListener( 'click', removeModalHandler );

				if( classie.has( el, 'md-setperspective' ) ) {
					setTimeout( function() {
						classie.add( document.documentElement, 'md-perspective' );
					}, 25 );
				}
			});

		} );

	}

	init();

})();

var scrollWrappers;
var smallScrollWrappers;
var articleContent;
function resizeScrollWrappers()
{
	var height = $(document).height();
	var bodyheight = height / 2 - 140;
	scrollWrappers.height(bodyheight);
	smallScrollWrappers.height(bodyheight - 140);

	articleContent.height(height * 0.75 - 190);
}

// On resize, we want to set the size on .md-scroll-wrapper
$(window).resize(function() {
	resizeScrollWrappers();
});

$(document).ready(function() {
	scrollWrappers = $('.md-scroll-wrapper');
	smallScrollWrappers = $('.md-scroll-wrapper-small');
	articleContent = $('.article-content');
	resizeScrollWrappers();
});