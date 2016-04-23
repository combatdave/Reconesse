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

var scrollWrappers, smallScrollWrappers, articleContent, relatedArticles,
	articleInfo, searchResultWrappers;
function resizeScrollWrappers()
{
	var height = $(document).height();
	var bodyheight = height / 2 + 20;
	var bh2 = height * 0.7;
	scrollWrappers.height(bh2);
	searchResultWrappers.height(bh2);
	smallScrollWrappers.height(bh2 - 224);

	articleContent.height(height * 0.8 - 52);
	//articleInfo.height(height * 0.8 - 100);
	relatedArticles.height(height * 0.8 - 466);
}

// On resize, we want to set the size on .md-scroll-wrapper
$(window).resize(function() {
	resizeScrollWrappers();
});

$(document).ready(function() {
	articleInfo = $('.article-info');
	scrollWrappers = $('.md-scroll-wrapper');
	searchResultWrappers = $('.search-result-wrapper');
	smallScrollWrappers = $('.md-scroll-wrapper-small');
	articleContent = $('.article-content');
	relatedArticles = $('.related-articles');
	resizeScrollWrappers();
});
