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
  const hours = d.getHours();
  const minutes = d.getMinutes();
  // Format the timestamp as "HH:MM"
  const timestamp = $('<div class="timestamp">' + hours + ':' + (minutes < 10 ? '0' : '') + minutes + '</div>');
  
  // Always add the timestamp for each message
  $('.message:last').append(timestamp);
}

function insertMessage() {
  const msg = $('.message-input').val().trim();
  if (!msg) return;

  // Append user's message
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();  // Add timestamp for the user's message
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
		if (data.error) {
            alert(`Error: ${data.error}`);
            console.log(`Max tokens: ${data.max_tokens}`);
            console.log(`User input tokens: ${data.user_input_tokens}`);
			loader.replaceWith('');
        } else {
            // Replace loader with the response message
			loader.replaceWith('<div class="message new">' + data.response + '</div>');
			setDate();  // Add timestamp for the bot's message
			updateScrollbar();
        }
      
    },
    error: function() {
      // Replace loader with error message
      loader.replaceWith('<div class="message new">Error: Could not process your request at the moment.</div>');
      setDate();  // Add timestamp for the error message
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
