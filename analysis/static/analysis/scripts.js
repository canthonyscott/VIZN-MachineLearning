/**
 * Created by anthony on 2/11/17.
 */

$(document).ready(function () {
    console.log("Ready");
    $body = $("body");


    $('#upload_frm').submit(function () {
       console.log("form Submit");
        $body.addClass("loading");
    });


});

