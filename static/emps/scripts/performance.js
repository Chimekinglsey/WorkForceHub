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
  });
  