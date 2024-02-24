$(document).ready(function() {
    $('#review-btn').click(function() {
      $('#review-modal').show(10);
    });
  
    $('#project-btn').click(function() {
      $('#project-modal').slideToggle();
    });
  
    $('#otherPerf-btn').click(function() {
      $('#otherPerf-modal').slideToggle();
    });

    $('#performanceHistory-btn').click(function() {
      $('#performanceHistory-modal').slideToggle();
    });
    // Add event listeners for other buttons and modals
  });
  