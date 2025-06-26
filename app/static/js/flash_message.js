
document.addEventListener('DOMContentLoaded', function () {
  const messages = document.querySelectorAll('.flash-message');

  messages.forEach((msg) => {
    setTimeout(() => {
      msg.style.transition = 'opacity 0.5s ease-out';
      msg.style.opacity = '0';
      setTimeout(() => {
        msg.remove();
      }, 500);
    }, 3000); // tempo antes de desaparecer
  });
});
