$(function(){

    $('#history')
        .click(function(){
            $('#popup-container').fadeIn();
        });

    $('#popup-container').click(function(event){
        if(event.target == this) {
            $(this).fadeOut();
        }
    })
});


$(function(){

    $('.error')
        .click(function(){
            if(confirm('Вы не можете добавить товар в корзину, пока не авторизованы.\n\n'+
            'К счастью, войти или зарегистрироваться очень просто:\n'+
            'Нажмите "ОК" и вас перебросит на страницу авторизации\n'+
            'Или нажмите "Отмена", чтобы остаться на этой странице.\n'+
            '\nА ещё: если вы зарегистрируетесь, то сможете полностью ознакомиться '+
            'с функционалом сайта и даже оставлять комментарии :)')) {

                window.location.href = 'http://127.0.0.1:8000/login/'
                return false;
            } else {
                window.location.href = ''
                return false;
            };

        });
});


jQuery(function($){
    $(document).ready(function(){
        $('.slickSlider').slick({
            dots: true,
            infinite: true,
            speed: 300,
            slidesToShow: 1,
            adaptiveHeight: true,
            centerPadding: '50px',
            arrows: true,
            prevArrow:"<button type='button' class='slick-prev '></button>",
            nextArrow:"<button type='button' class='slick-next'></button>"
        });
    });
});