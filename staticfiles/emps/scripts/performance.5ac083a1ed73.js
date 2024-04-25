$(document).ready(function() {
    $('#review-btn').click(function() {
      $('#review-modal').show(10);
    });
  
    $('#update-rev-btn').click(function() {
      $('#update-rev-modal').slideToggle();
    });
  
    $('#performanceHistory-btn').click(function() {
      $('#performanceHistory-modal').slideToggle();
    });

    // remove scroll from background when modals open and close
    $('.action-button').click(function (){
      $('body').addClass('no-scroll')
    })

    $('.close').click(function (){
      $('body').removeClass('no-scroll')
    })

    // For Organization Reports
    $('#create-report-btn').click(function() {
      $('#create-report-modal').show(10);
    });
  
    $('#update-report-btn').click(function() {
      $('#update-report-modal').slideToggle();
    });
  
    $('#report-history-btn').click(function() {
      $('#report-history-modal').slideToggle();
    });
    $("input[type='search']").attr('placeholder', 'Enter search text')
  });
  