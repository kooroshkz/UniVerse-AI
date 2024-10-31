const $messages = $('.messages-content');
let m, i = 0;

const fakeMessages = [
  'Hello, how can I assist you today?',
  'Fetching contact information for university staff...',
  'Found the email for Guilherme Perin: guilherme.perin@universiteitleiden.nl',
  'The latest update in your MyTimetable is: "AI lecture moved to Room 1.15 on October 27th."',
  'Would you like me to add this update to your personal schedule?',
  'I can help you with scraping more staff profiles or checking new updates. What would you like to do next?',
  'Goodbye! If you need further assistance, just let me know.',
  ':)'
];

$(window).on('load', () => {
  $messages.mCustomScrollbar();
  setTimeout(fakeMessage, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate() {
  const d = new Date();
  if (m !== d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  const msg = $('.message-input').val().trim();
  if (!msg) return;

  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();

  setTimeout(fakeMessage, 1000 + Math.random() * 2000);
}

$('.message-submit').on('click', insertMessage);
$(window).on('keydown', (e) => {
  if (e.which === 13) {
    insertMessage();
    return false;
  }
});

function fakeMessage() {
  if ($('.message-input').val() !== '') return;

  $('<div class="message loading new"><span></span></div>').appendTo($('.mCSB_container'));
  updateScrollbar();

  setTimeout(() => {
    $('.message.loading').remove();
    $('<div class="message new">' + fakeMessages[i] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();
    i = (i + 1) % fakeMessages.length;
  }, 1000 + Math.random() * 2000);
}
