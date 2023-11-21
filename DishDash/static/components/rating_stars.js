
document.addEventListener('DOMContentLoaded', function () {
    const ratingStarsContainers = document.querySelectorAll('.rating-stars');
    ratingStarsContainers.forEach(container => {
      const rating = container.getAttribute('data-rating');
      const stars = createStars(rating);
      container.innerHTML = stars;
    });

    function createStars(rating) {
      let fullStars = Math.floor(rating);
      let hasHalfStar = rating % 1 !== 0;
      let fullStarHTML = '<img class="star" src="/static/icons/star-full.svg"" alt="Full Star">';
      let halfStarHTML = hasHalfStar ? '<img class="star" src="/static/icons/star-half.svg" alt="Half Star">' : '';
      let emptyStarHTML = '<img class="star" src="/static/icons/star-empty.svg" alt="Empty Star">';
      let emptyStarsCount = Math.floor(5 - rating);
      let starsHTML = `${fullStarHTML.repeat(fullStars)}${halfStarHTML}${emptyStarHTML.repeat(emptyStarsCount)}`;

      return starsHTML;
    }
  });