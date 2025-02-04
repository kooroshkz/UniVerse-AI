const $messages = $('.messages-content');
let m;
let tokenLimitExceeded = false;


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
  const timestamp = $('<div class="timestamp">' + hours + ':' + (minutes < 10 ? '0' : '') + minutes + '</div>');
  
  $('.message:last').append(timestamp);
}

function insertMessage(msg) {
  msg = msg.trim();
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
    url: '/chatbot/response/',
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
			loader.replaceWith('<div class="message new">' + data.response + '</div>');
			setDate();
			updateScrollbar();
        }
      
    },
    error: function() {
      loader.replaceWith('<div class="message new">Error: Could not process your request at the moment.</div>');
      setDate();  // Add timestamp for the error message
      updateScrollbar();
    }
  });
}

// Function to check token count on the backend
function checkTokenLimitServer() {
  const msg = $('.message-input').val();

  $.ajax({
    type: 'POST',
    url: '/validate_tokens/',
    data: {
      message: msg,
      csrfmiddlewaretoken: getCSRFToken(),
    },
    success: function(data) {
		
	  const submitButton = $('.message-submit');
	  const tokenWarningMessage = $('.token-warning-message');
	  tokenLimitExceeded = data.exceeds_limit; 

      if (data.exceeds_limit) {
        submitButton.prop('disabled', true); // Disable button
		submitButton.css({
          'background-color': '#696969', // Set the gray background color
          'cursor': 'not-allowed', // Show a "not-allowed" cursor
          'pointer-events': 'none' // Prevent the button from being clicked
        });
		tokenWarningMessage.text(`Token limit exceeded: ${data.token_count} / ${data.max_tokens}`).show();
        console.log(`Limit Exceeded (${data.token_count}/${data.max_tokens})`);
      } else {
        submitButton.prop('disabled', false); // Enable button
        submitButton.css({
          'background-color': '#003366', // Reset the background color (Parliament Blue)
          'cursor': 'pointer', // Restore the normal cursor
          'pointer-events': 'auto' // Enable clicking again
        });
		tokenWarningMessage.hide();
      }
    },
    error: function() {
      console.error("Error checking token limit.");
    }
  });
}

// Event listener for input changes
$('.message-input').on('input', checkTokenLimitServer);

$('.example-question').on('click', function() {
  const exampleMsg = $(this).text(); // Get the text of the clicked example question
  insertMessage(exampleMsg); // Send the example question to the chatbot

  // Animate and hide the entire example-questions container
  $('.example-questions').css({
    transition: 'all 0.6s ease',  // Smooth transition for all properties
    opacity: 0,                   // Fade out
  });

  // After animation ends, hide the container
  setTimeout(() => {
    $('.example-questions').hide(); // Hide the entire container
  }, 600);  // Match the duration of the animation
});

// Updated event listeners for sending user-typed messages
$('.message-submit').on('click', function() {
  const msg = $('.message-input').val();
  insertMessage(msg);

  // Ensure the predefined questions are hidden if the user starts typing
  if ($('.example-questions').is(':visible')) {
    $('.example-questions').css({
      transition: 'all 0.6s ease',  // Smooth transition for all properties
      opacity: 0,                   // Fade out
    });

    setTimeout(() => {
      $('.example-questions').hide(); // Hide the entire container
    }, 600);  // Match the duration of the animation
  }
});

$(window).on('keydown', (e) => {
  if (e.which === 13 && !tokenLimitExceeded) {
    const msg = $('.message-input').val();
    insertMessage(msg);

    // Ensure the predefined questions are hidden if the user starts typing
    if ($('.example-questions').is(':visible')) {
      $('.example-questions').css({
        transition: 'all 0.6s ease',  // Smooth transition for all properties
        opacity: 0,                   // Fade out
      });

      setTimeout(() => {
        $('.example-questions').hide(); // Hide the entire container
      }, 600);  // Match the duration of the animation
    }

    return false;
  } else if (e.which === 13 && tokenLimitExceeded) {
    e.preventDefault(); // Prevent the default action (sending message)
    return false; // Ensure no further action is taken
  }
});

