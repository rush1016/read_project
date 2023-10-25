function getPassageInfo(passageId) {
    return $.ajax({
        url: '/get_passage_info/' + passageId,
        type: 'GET',
    })
    .then(function(response) {
        return response.passage_data;
    })
    .fail(function(error) {
        console.error('Error fetching student data:', error);
    });
}