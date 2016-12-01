$(document).ready(function(){
  var altura = $('.navbar').offset().top;
  var vLargo = $(window).width();
  
  $(window).on('scroll', function(){
    if($(window).scrollTop() > altura){
      $('.navbar').addClass('navbar-fixed-top');
    }else{
      $('.navbar').removeClass('navbar-fixed-top');
    }
  });
});
