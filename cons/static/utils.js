$(document).ready(function(){
    $("ul.flashes li").each(function(){
        $(this).animate({
            visibility:'hidden',
            opacity: 0,
        },
        2000,
        function(){
        });
    });
});
