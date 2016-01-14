$('.js-infinite-item').hover(function() {
        $(this).find('.note-option').show();
    },
    function () {
        $(this).find('.note-option').hide();
    }
);

$(window).load(function() {
    $('.js-infinite-layout')
        .infinitescroll({
            itemSelector: '.js-infinite-item',
            nextSelector: "div.js-infinite-navigation a:first",
            navSelector: "div.js-infinite-navigation"
        },
        // callback to handle binding events on newly added elements
        function(newElements) {
            // iterate across the elements just added
            for (var i = 0; i < newElements.length; i++) {
                var thisElement = newElements[i];

                $(thisElement).hover(function() {
                        $(this).find('.note-option').show();
                    },
                    function () {
                        $(this).find('.note-option').hide();
                    }
                );
            }
        });
});

$(window).load(function() {
$('.alert').delay(3000).fadeOut('slow');
});
