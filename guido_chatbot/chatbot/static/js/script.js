const $messages = $('.messages-content');
let m;

$(window).on('load', () => {
  $messages.mCustomScrollbar();
});

// Function to get CSRF token
function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

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

  // Append user's message
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();

  // Append loader
  const loader = $(
    '<div class="message new"><img src="https://mywatchcdm.com/cdn/shop/t/3/assets/loading.gif?v=101112957014615068991674848327" class="loader" alt="Loading..."></div>'
  );
  loader.appendTo($('.mCSB_container')).addClass('new');
  updateScrollbar();

  // Send message to Django backend for OpenAI API processing
  $.ajax({
    type: 'POST',
    url: '/chatbot_response/', // URL should match your Django URL configuration
    data: {
      message: msg,
      csrfmiddlewaretoken: getCSRFToken() // Include CSRF token
    },
    success: function(data) {
      // Replace loader with the response message
      loader.replaceWith('<div class="message new">' + data.response + '</div>');
      setDate();
      updateScrollbar();
    },
    error: function() {
      // Replace loader with error message
      loader.replaceWith('<div class="message new">Error: Could not process your request at the moment.</div>');
      updateScrollbar();
    }
  });
}


// Event listeners for sending messages
$('.message-submit').on('click', insertMessage);
$(window).on('keydown', (e) => {
  if (e.which === 13) {
    insertMessage();
    return false;
  }
});
