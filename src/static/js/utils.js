function getCanvasSize(x, y, ratio){
    let result;
    switch (ratio){
        case "1":
            // 1:1
            v = Math.max(x, y);
            result = [v, v];
            break;
        case "2":
            // 4:5
            if (x/4*5 > y){
                result = [x, x/4*5];
            } else {
                result = [y/5*4, y];
            }
            break;
        case "3":
            // 5:4            
            if (x/5*4 > y){
                result = [x, x/5*4];
            } else {
                result = [y/4*5, y];
            }
            break;
    }
    return result;
}

function getImagePosition(canvas, x, y){
    var minus = (r, a) => r.map((b, i) => a[i] - b);
    diff = [[canvas.width, canvas.height], [x, y]].reduce(minus)
    return [Math.abs(diff[0])/2, Math.abs(diff[1])/2]
}

function getRadioValue(radio){
    for(let i=0;i<radio.length;i++){
        if (radio[i].checked){
            return radio[i].value
        }
    };
}

function getXY(element, img){
    // 둘중 작은것에 사이즈를 맞춤
    const MAX_WIDTH = element.parentElement.offsetWidth-50;
    const MAX_HEIGHT = MAX_WIDTH;

    let width = img.width;
    let height = img.height;

    if (width > height) {
        if (width > MAX_WIDTH) {
            height *= MAX_WIDTH / width;
            width = MAX_WIDTH;
        }
    } else {
        if (height > MAX_HEIGHT) {
            width *= MAX_HEIGHT / height;
            height = MAX_HEIGHT;

        }
    }
    return [width, height]
}