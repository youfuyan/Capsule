function loadMoreContent() {
  // show the loading indicator
  document.getElementById('container').style.display = 'block';

  // fetch the additional content
  // once the content is fetched, append it to the content container
  // and hide the loading indicator
}


window.addEventListener('scroll', function() {
  // check if the user has scrolled to the bottom of the page
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    loadMoreContent();
  }
});



function debounce(func, wait = 20, immediate = true) {
  let timeout;
  return function() {
    const context = this, args = arguments;
    const later = function() {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    const callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
}

window.addEventListener('scroll', debounce(function() {
  // check if the user has scrolled to the bottom of the page
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
    loadMoreContent();
  }
}));