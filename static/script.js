document.addEventListener('DOMContentLoaded', function () {
  const form = document.querySelector('form');
  const nameInput = document.querySelector('input[name="name"]');
  const weightInput = document.querySelector('input[name="weight"]');

  // Real-time input validation
  form.addEventListener('submit', function (e) {
      const name = nameInput.value.trim();
      const weight = parseFloat(weightInput.value);

      if (!name || name.length < 2) {
          alert('Please enter a valid cargo name with at least 2 characters.');
          nameInput.focus();
          e.preventDefault();
          return;
      }

      if (isNaN(weight) || weight <= 0) {
          alert('Please enter a valid cargo weight (greater than 0).');
          weightInput.focus();
          e.preventDefault();
          return;
      }
  });

  // Optional: Confirm CSV export
  const exportBtn = document.querySelector('.export-btn');
  if (exportBtn) {
      exportBtn.addEventListener('click', function () {
          const confirmExport = confirm('Do you want to download the cargo list as CSV?');
          if (!confirmExport) {
              event.preventDefault();
          }
      });
  }
});
