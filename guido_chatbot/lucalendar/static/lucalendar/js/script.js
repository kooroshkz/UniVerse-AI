$('a.nextDay').click(function() { 
  $('li.current').next().addClass('current').prev().removeClass('current');
});
  $('a.prevDay').click(function() { 
  $('li.current').prev().addClass('current').next().removeClass('current');
});
$('a.today').click(function(){
  $('li.current').removeClass('current');
  $('li.today').addClass('current');
});
$('a.expand').click(function(){
  $(this).parent().toggleClass('open');
  $(this).toggleClass('open');
});