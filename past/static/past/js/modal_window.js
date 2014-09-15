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
function resizeScrollWrappers()
{
	var bodyheight = $(document).height() / 2 - 150;
	scrollWrappers.height(bodyheight);
}

// On resize, we want to set the size on .md-scroll-wrapper
$(window).resize(function() {
	resizeScrollWrappers();
});

$(document).ready(function() {
	scrollWrappers = $('.md-scroll-wrapper');
	resizeScrollWrappers();
});