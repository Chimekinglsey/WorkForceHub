$(document).ready(function() {
    // Convert input to 2 decimal places on blur
    $('input[type="number"]').on('blur', function() {
        $(this).val(parseFloat($(this).val()).toFixed(2));
    });

    $("input[type='search']").attr('placeholder', 'Search  finance reports...')

    // For Finance Reports
    $('#basicReport-btn').click(function() {
      $('#basicReport-modal').show(10);
    });
  
    $('#detailedReport-btn').click(function() {
      $('#detailedReport-modal').slideToggle();
    });
  
    $('#reportHistory-btn').click(function() {
      $('#reportHistory-modal').slideToggle();
    });
    $('#financeStats-btn').click(function() {
    $('.financeContainer').hide();
    $('#financeStats-modal').slideDown();
    });

    // toggle finance container
    $('#close').click(function() {
    $('#financeStats-modal').hide();
      $('.financeContainer').slideToggle();
    });
});
