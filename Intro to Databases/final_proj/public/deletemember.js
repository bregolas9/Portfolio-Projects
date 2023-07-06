function deleteMember(id){
    $.ajax({
        url: '/members/' + id,
        type: 'DELETE',
        success: function(result){
            window.location.reload(true);
        }
    })
};
