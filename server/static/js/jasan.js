
function genUserIdentifier() {
  function randString() {
    return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
  }
  return randString() + "-" + randString() + "-" + randString() + "-" + randString();
}

function setCookie(name, value, days) {
    date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));

    document.cookie = name + "=" + value + "; expires=" + date.toUTCString() + "; path=/";
}

function getCookie(name) {
    var i, x, y, cookies = document.cookie.split(";");
    for (i = 0; i < cookies.length; i++) {
        x = cookies[i].substr(0, cookies[i].indexOf("="));
        y = cookies[i].substr(cookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x == name)
            return unescape(y);
    }
}
