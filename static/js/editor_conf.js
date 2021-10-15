// referencia a codemirror: https://codemirror.net/doc/manual.html
CodeMirror.fromTextArea(document.getElementById("default"),{
    lineNumbers : true,
    theme : "material-darker",
    mode : "julia",
    matchBrackets: true
});