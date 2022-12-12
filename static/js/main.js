const canvas = document.getElementById('c')
let ctx = canvas.getContext('2d')

//地図画像
let img  = document.getElementById('map')
window.addEventListener("DOMContentLoaded",() => {    
    animloop()   
})
const getMousePosition = (canvas,evt) => {
    let rect = canvas.getBoundingClientRect()
    return {
            x: evt.clientX - rect.left,
            y: evt.clientY - rect.top
        };
}
//参照渡し防止
const copyPosition = (pos) => {
    return {
        x:pos.x,
        y:pos.y
    }
}
let move_flag = false
let mousePos = {x:0,y:0}
let prev_MousePos = copyPosition(mousePos) 
let d_cameraPos ={} = {x:0,y:0}
let cameraPos = copyPosition(d_cameraPos)
let click_cameraPos = copyPosition(cameraPos)
let prev_cameraPos = copyPosition(cameraPos)
let cameraPosMax
let eps = 0.0001
let imageScale = 0.3
let imageScaleMax=2.0
let imageScaleMin=0.3
const cameraPositionFix = () => {
    cameraPos.x = cameraPos.x > 0 ? cameraPos.x : 0
    cameraPos.x = cameraPosMax.x > cameraPos.x ? cameraPos.x : cameraPosMax.x
    cameraPos.y = cameraPos.y > 0 ? cameraPos.y : 0
    cameraPos.y = cameraPosMax.y > cameraPos.y ? cameraPos.y : cameraPosMax.y
}
canvas.addEventListener('mousedown', evt => {
    move_flag=true;
    prev_MousePos = getMousePosition(canvas,evt)
    click_cameraPos = copyPosition(cameraPos)
    console.log(convert_cv_pos(prev_MousePos))
}, false);
canvas.addEventListener('mouseup', () => {
    move_flag=false;
}, false);
canvas.addEventListener('mouseleave', () => {
    move_flag=false;
}, false);
canvas.addEventListener('mousemove', evt => {
    mousePos = getMousePosition(canvas, evt);
}, false);
//マウスホイール操作のの拡大・縮小率
let SCALE_STEP = 0.025
canvas.addEventListener('mousewheel', evt => {
    let incdec = 1 - (evt.deltaY < 0) * 2
    imageScale += incdec * SCALE_STEP
    imageScale = imageScale > imageScaleMin ? imageScale : imageScaleMin
    imageScale = imageScaleMax > imageScale ? imageScale : imageScaleMax
    let mouse = getMousePosition(canvas,evt)
    cameraPos.x += mouse.x*SCALE_STEP / (imageScale * (imageScale - SCALE_STEP))*incdec
    cameraPos.y += mouse.y*SCALE_STEP / (imageScale * (imageScale - SCALE_STEP))*incdec
}, false);

//グリッドの画面比率
const gridWidthMag = 0.8
//main文の最初
const ini = () => {
    ctx.beginPath();
	ctx.globalAlpha = 1;
    ctx.fillStyle = '#fff';
	ctx.fillRect(0,0,canvas.width,canvas.height);
    cameraPosMax = {
        x:imageScale*3000-window.innerWidth*gridWidthMag,
        y:imageScale*3000-window.innerHeight
    }
}
//マウスドラッグ中の動作
const mouse_drag = () => {
    cameraPos.x = prev_MousePos.x+click_cameraPos.x-mousePos.x
    cameraPos.y = prev_MousePos.y+click_cameraPos.y-mousePos.y
    d_cameraPos.x = cameraPos.x-prev_cameraPos.x
    d_cameraPos.y = cameraPos.y-prev_cameraPos.y
    prev_cameraPos = copyPosition(cameraPos)
}
//マウスドラッグ後の余韻(勢いよくドラッグすると動作に余韻が出る)
const mouse_drag_after = () => {
    d_cameraPos.x = Math.abs(d_cameraPos.x)>eps ? d_cameraPos.x*0.9 : 0
    d_cameraPos.y = Math.abs(d_cameraPos.y)>eps ? d_cameraPos.y*0.9 : 0
    cameraPos.x+= d_cameraPos.x
    cameraPos.y+= d_cameraPos.y
}
//画像上の座標変換用の原点座標
const base = {
    // x:-119,
    // y:-21,
    x:-114,
    y:-16,
    scale:5.9
    /* 根拠なし　適当に調整したらこうなった */
}
//openCVの画像上の座標に変換
const convert_cv_pos = pos => {
    return {
        x: (pos.x+cameraPos.x)/imageScale/base.scale-base.x,
        y: (pos.y+cameraPos.y)/imageScale/base.scale-base.y
    }
}
//バックエンドから受け取った座標リストをプロットする
const drawPlotAll = () => {
    //座標リストの座標を画面上の座標に変換
    let convert = list_data.map((pos) => {
        return {x:(pos[1]+base.x)*imageScale*base.scale-cameraPos.x,y:(pos[0]+base.y)*imageScale*base.scale-cameraPos.y}
    })
    ctx.strokeStyle = '#16f'
    ctx.fillStyle = '#39f'
    convert.forEach((pos,index)=> {
        ctx.beginPath()
        ctx.lineWidth = 5*imageScale
        ctx.arc( pos.x, pos.y, 8*imageScale, 0 * Math.PI / 180, 360 * Math.PI / 180, false ) ;
        ctx.fill()
        ctx.stroke()
        ctx.closePath()
    })
}
//main文
const all = () => {
    ini()
    //マウスがクリックされている時
    if(move_flag) {
        //マウスドラッグ中の操作
        mouse_drag()
    } else {
        //マウスを離した時の余韻
        mouse_drag_after()
    }
    cameraPositionFix()
    ctx.drawImage(img, cameraPos.x*-1, cameraPos.y*-1, imageScale*3000, imageScale*3000);
    drawPlotAll()
}
//無限ループ用関数
const animloop = () =>{
	all();
	window.requestAnimationFrame(animloop);
}