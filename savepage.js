// console.log("test");

var args = require('system').args;

if (args.length === 1) {
    console.log('Try to pass some arguments when invoking this script!');
    phantom.exit();
} else {
    args.forEach(function(arg, i) {
        // console.log(i + ': ' + arg);
    });
}

var url = args[1];
var output = args[2];

// phantom.exit();

var page = require('webpage').create();
var fs = require('fs');// File System Module
page.open(url, function() { // open the file 
    // console.log("Writing output to " + output);
    fs.write(output, page.content, 'w'); // Write the page to the local file using page.content
    phantom.exit(); // exit PhantomJs
});
