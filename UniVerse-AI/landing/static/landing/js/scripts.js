/*!
* Start Bootstrap - Grayscale v7.0.6 (https://startbootstrap.com/theme/grayscale)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-grayscale/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

const $messages = $('.messages-content');
let m;

$(window).on('load', () => {
  $messages.mCustomScrollbar();
});

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

  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  updateScrollbar();

  const loader = $('<div class="message new"><figure class="avatar"><img src="loader.gif" /></figure><span></span></div>');
  loader.appendTo($('.mCSB_container')).addClass('new');
  updateScrollbar();

  $.ajax({
    type: 'POST',
    url: '/chatbot/response/',
    data: {
      message: msg,
      csrfmiddlewaretoken: getCSRFToken()
    },
    success: function (data) {
      loader.remove();
      $('<div class="message new">' + data.response + '</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
    },
    error: function () {
      loader.remove();
      $('<div class="message new">Error processing your request.</div>').appendTo($('.mCSB_container')).addClass('new');
      setDate();
      updateScrollbar();
    }
  });
}

// Handle first message
$(document).ready(() => {
  if (typeof firstMessage !== 'undefined' && firstMessage.trim()) {
    insertMessage(firstMessage);
  }
});
