$(document).ready(function () {
    // Get references to the checkboxes
    let selectAllCheck = $("#select-all-check");
    let otherCheckboxes = $('input[name="selected_records"]');

    // Add a change event handler to the "Select All" checkbox
    selectAllCheck.change(function () {
        otherCheckboxes.prop('checked', selectAllCheck.prop('checked'));
    });
  
    // Add a change event handler to the other checkboxes
    otherCheckboxes.change(function () {
        selectAllCheck.prop('checked', otherCheckboxes.length === otherCheckboxes.filter(':checked').length);
    });
});