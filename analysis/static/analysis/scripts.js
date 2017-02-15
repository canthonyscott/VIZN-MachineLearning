/**
 * Created by anthony on 2/11/17.
 */

var response;

$(document).ready(function () {
    console.log("Ready");
    $body = $("body");


    $('#upload_frm').submit(function () {
       console.log("form Submit");
        $body.addClass("loading");
    });

    $('#prob_btn').click(function () {
        console.log('prob btn clicked');
        var url = "/analysis/probabilities/?id=" + item_id;
        console.log(url);
        $.get(url, function (values) {
            console.log(values)
        });



    });

});

