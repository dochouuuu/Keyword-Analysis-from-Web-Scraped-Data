var WordCloud = function(canvas, options) {
    var $ = canvas.getContext('2d');
    options = options || {};
    var settings = {
        list: [],
        fontFamily: 'Arial',
        fontWeight: 'normal',
        gridSize: 8,
        color: 'random-dark',
        backgroundColor: '#fff',
        rotateRatio: 0.5,
        rotationSteps: 2,
        shape: 'circle',
        drawOutOfBound: false,
        drawMask: false,
        maskColor: 'rgba(255,0,0,0.3)',
        maskGridWidth: 0,
        maskGridHeight: 0,
        hover: null,
        click: null
    };
    for (var key in options) {
        settings[key] = options[key];
    }
    var g = settings.gridSize;
    var f = function () {
        var e = {
            width: canvas.width,
            height: canvas.height
        };
        var d = function (p) {
            var s = $.measureText(p).width;
            return [Math.ceil(g * (s + 2) / e.width), Math.ceil(g * (s + 2) / e.height)];
        };
        var t = function (p) {
            return Math.random() * (e.width - g * p[0]);
        };
        var q = function (p) {
            return Math.random() * (e.height - g * p[1]);
        };
        var r = function (p, s) {
            var o = t(p);
            var n = q(p);
            return [Math.floor(o), Math.floor(n)];
        };
        var u = function (p) {
            return $.measureText(p).width * g / e.width;
        };
        var v = function (n, m, k) {
            var l = document.createElement('canvas');
            l.width = g * n;
            l.height = g * m;
            var j = l.getContext('2d');
            j.font = g + 'px ' + settings.fontFamily;
            j.fillStyle = '#000';
            j.fillRect(0, 0, l.width, l.height);
            return j;
        };
        var w = function (n, m, k) {
            var l = Math.floor(e.width / g);
            var j = Math.floor(e.height / g);
            for (var o = 0; o < j; o++) {
                for (var i = 0; i < l; i++) {
                    var p = (o * l + i) * 4;
                    var q = (o + Math.floor(m / g)) * l + i + Math.floor(n / g);
                    var r = (o + Math.ceil(m / g)) * l + i + Math.ceil(n / g);
                    if (k.data[p + 3] === 0) {
                        k.data[p + 3] = 1;
                    } else {
                        k.data[p + 3] = 0;
                    }
                }
            }
        };
        var x = function (n, m, k) {
            var l = Math.floor(e.width / g);
            var j = Math.floor(e.height / g);
            for (var o = 0; o < j; o++) {
                for (var i = 0; i < l; i++) {
                    var p = (o * l + i) * 4;
                    var q = (o + Math.floor(m / g)) * l + i + Math.floor(n / g);
                    var r = (o + Math.ceil(m / g)) * l + i + Math.ceil(n / g);
                    if (k.data[p + 3] === 0) {
                        k.data[p + 3] = 1;
                    } else {
                        k.data[p + 3] = 0;
                    }
                }
            }
        };
        var y = function (j, k) {
            var l = g * (settings.rotateRatio > Math.random() ? 1 : 0);
            var m = r(k, u(j));
            $.save();
            $.translate(m[0], m[1]);
            $.rotate(Math.PI / 2 * l);
            $.translate(-m[0], -m[1]);
            $.fillStyle = settings.color;
            $.fillText(j, m[0], m[1]);
            $.restore();
        };
        return {
            setOptions: function (o) {
                for (var key in o) {
                    settings[key] = o[key];
                }
            },
            setCanvas: function (p) {
                canvas = p;
                $ = canvas.getContext('2d');
            },
            createWordCloud: function () {
                $.clearRect(0, 0, e.width, e.height);
                var o = settings.list;
                o.sort(function (q, p) {
                    return p[1] - q[1];
                });
                $.font = g + 'px ' + settings.fontFamily;
                for (var p = 0; p < o.length; p++) {
                    var q = o[p];
                    y(q[0], q[1]);
                }
            }
        };
    };
    return f();
};