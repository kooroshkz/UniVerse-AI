const $messages = $('.messages-content');
let tokenLimitExceeded = false;

$(window).on('load', () => {
  $messages.mCustomScrollbar();

  // Process the first_message if provided
  const firstMessage = getFirstMessage();
  if (firstMessage) {
    insertMessage(firstMessage);
  }
});

// Function to get the first_message from the DOM
function getFirstMessage() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('first_message') || '';
}

// Function to get CSRF token
function getCSRFToken() {
  return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0,
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
  $('.message-input').val(null);
  updateScrollbar();

  // Append loader
  const loader = $(
    '<div class="message new"><img src="https://mywatchcdm.com/cdn/shop/t/3/assets/loading.gif?v=101112957014615068991674848327" class="loader" alt="Loading..."></div>'
  );
  loader.appendTo($('.mCSB_container')).addClass('new');
  updateScrollbar();

  // Send message to Django backend for processing
  $.ajax({
    type: 'POST',
    url: '/chatbot/response/',
    data: {
      message: msg,
      csrfmiddlewaretoken: getCSRFToken(), // Include CSRF token
    },
    success: function (data) {
      loader.replaceWith('<div class="message new">' + (data.error ? 'Error: ' + data.error : data.response) + '</div>');
      setDate();
      updateScrollbar();
    },
    error: function (xhr, status, error) {
      console.error("AJAX Error:", status, error);
      loader.replaceWith('<div class="message new">Error: Could not process your request at the moment.</div>');
      setDate();
      updateScrollbar();
    },
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
    success: function (data) {
      const submitButton = $('.message-submit');
      const tokenWarningMessage = $('.token-warning-message');
      tokenLimitExceeded = data.exceeds_limit;

      if (data.exceeds_limit) {
        submitButton.prop('disabled', true).css({
          backgroundColor: '#696969',
          cursor: 'not-allowed',
          pointerEvents: 'none',
        });
        tokenWarningMessage.text(`Token limit exceeded: ${data.token_count} / ${data.max_tokens}`).show();
      } else {
        submitButton.prop('disabled', false).css({
          backgroundColor: '#003366',
          cursor: 'pointer',
          pointerEvents: 'auto',
        });
        tokenWarningMessage.hide();
      }
    },
    error: function () {
      console.error("Error checking token limit.");
    },
  });
}

// Event listener for input changes
$('.message-input').on('input', checkTokenLimitServer);

$('.example-question').on('click', function () {
  const exampleMsg = $(this).text();
  insertMessage(exampleMsg);

  $('.example-questions').css({
    transition: 'all 0.6s ease',
    opacity: 0,
  });

  setTimeout(() => {
    $('.example-questions').hide();
  }, 600);
});

$('.message-submit').on('click', function () {
  const msg = $('.message-input').val();
  insertMessage(msg);

  if ($('.example-questions').is(':visible')) {
    $('.example-questions').css({
      transition: 'all 0.6s ease',
      opacity: 0,
    });

    setTimeout(() => {
      $('.example-questions').hide();
    }, 600);
  }
});

$(window).on('keydown', (e) => {
  if (e.which === 13 && !tokenLimitExceeded) {
    const msg = $('.message-input').val();
    insertMessage(msg);

    if ($('.example-questions').is(':visible')) {
      $('.example-questions').css({
        transition: 'all 0.6s ease',
        opacity: 0,
      });

      setTimeout(() => {
        $('.example-questions').hide();
      }, 600);
    }

    return false;
  } else if (e.which === 13 && tokenLimitExceeded) {
    e.preventDefault();
    return false;
  }
});

// Modal for adding timetable
document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('addMyTimeTableModal');
  const openModalButton = document.querySelector('.add-my-timetable');
  const closeButton = document.querySelector('.close-button');
  const submitButton = document.getElementById('submitMyTimeTable');
  const feedbackDiv = document.getElementById('submissionFeedback');
  const loader = document.getElementById('loader');

  openModalButton.addEventListener('click', () => {
    modal.style.display = 'block';
    feedbackDiv.textContent = '';
    feedbackDiv.className = '';
  });

  closeButton.addEventListener('click', () => {
    modal.style.display = 'none';
    feedbackDiv.textContent = '';
    feedbackDiv.className = '';
  });

  window.addEventListener('click', (event) => {
    if (event.target === modal) {
      modal.style.display = 'none';
      feedbackDiv.textContent = '';
      feedbackDiv.className = '';
    }
  });

  submitButton.addEventListener('click', () => {
    const link = document.getElementById('myTimeTableLink').value;

    feedbackDiv.textContent = ''; // Clear previous feedback messages
    loader.style.display = 'block'; // Show loader

    if (link.startsWith('https://rooster.universiteitleiden.nl/')) {
      fetch('/chatbot/add-timetable/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCSRFToken(),
        },
        body: JSON.stringify({ link: link }),
      })
        .then((response) => response.json())
        .then((data) => {
          loader.style.display = 'none'; // Hide loader after response
          if (data.success) {
            feedbackDiv.textContent = data.success;
            feedbackDiv.className = 'feedback-success';
          } else {
            feedbackDiv.textContent = data.error || 'An error occurred. Please try again.';
            feedbackDiv.className = 'feedback-error';
          }
        })
        .catch((error) => {
          loader.style.display = 'none'; // Hide loader if an error occurs
          feedbackDiv.textContent = 'An unexpected error occurred. Please try again.';
          feedbackDiv.className = 'feedback-error';
          console.error('Error:', error);
        });
    } else {
      loader.style.display = 'none'; // Hide loader for invalid URL
      feedbackDiv.textContent =
        'Invalid URL format. Please ensure it starts with "https://rooster.universiteitleiden.nl/".';
      feedbackDiv.className = 'feedback-error';
    }
  });
});