
function init(){
	document.onmousemove = function(e){getMouseXY;if(rightDown==1){ dragZoom();}};
	document.onscroll=function(){return false;};
	
	document.onmousedown=function(e) {checkMouse;};
	document.onmouseup=function(){rightDown=0;};
	
	checkExt();
	
	imgBlockObj=document.getElementById("imgBlock");
	var attribList=['offX','offY','curSizeW','curSizeH',"curScale"];
	attribList.checkAttrs("imgBlock");
	resize(0);
}
function noContextMenu(){
	window.oncontextmenu = function () {
		return false;
	}
	rightClick=0;
}

//if (!IE) document.captureEvents(Event.MOUSEMOVE);
function getMouseXY(e) {
	prevMouseX=mouseX;
	prevMouseY=mouseY;
	if(touchScreen==0){
		if (IE) {
			mouseX = event.clientX;
			mouseY = event.clientY;
		} else {
			mouseX = e.pageX;
			mouseY = e.pageY;
		}
	}else{
		touch = e.touches[0];
		mouseX = touch.pageX;
		mouseY = touch.pageY;
	}
}
// I use global variable 'doubleClick' to check if the user is double clicking within 600 ms here
// if doubleClick==1, that means the user has clicked once, the countdown function will set doubleClick back to 0
// mButton is the previous mouse button the user clicked
// 1 - Left click
// 2 - Middle wheel click
// 3 - Right click
function checkMouse(e){
	var button=e.which;
	if(mButton != button && doubleClick==1){ // If the user clicks a different button within that initial 600 ms, cancel double click
		doubleClick=0;
	}
	mButton=button;
//$("#verbText").html(mButton+" - "+button +" -- ");
	if(button == 1){
		dragging=1;
		startDrag(curThumb);
		if(doubleClick==1){
			zoomLayers("touchData", "imgBlock",[],[],-1,0);
			updateCanvas();
		}
		if(doubleClick==0){
			doubleClick=1;
			countdown("doubleClick=0;",15);
		}
	}
	if(button == 2){
		if(doubleClick==1){
			resetZoomPan();
		}
		if(doubleClick==0){
			doubleClick=1;
			countdown("doubleClick=0;",15);
		}
	}
	if(button == 3 && rightClick==1 ){
		
		if(doubleClick==1){
			resetZoomPan();
			rightDown=0;
		}
		if(doubleClick==0){
			rightDown=1;
			doubleClick=1;
			countdown("doubleClick=0;",15);
		}
	}
	return false;
}

/*
q=81
z=90
s=83
f=70
d=68
c=67
n=78
m=77
h=72
r=82
shift=16
ctrl=17
alt=18
tab=9
1=49
2=50
3=51
4=52
5=53
6=54
7=55
8=56
9=57
0=48
-=173
+=61
`=192
[=219
]=221
<=188
>=190
left=37
up=38
right=39
down=40
del=46
ins=45
home=36
end=35
pgUp=33
pgDown=34
*
For numbers, check focus is not in text field-
* document.activeElement
*/


/*$(document).on('keypress', function(e){
	keyHit=e.keyCode || e.which;
	returnMessage(keyHit);
});*/
//document.addEventListener('keypress', function(e){
document.onkeyup=function(e){
	keyHit=e.keyCode || e.which;
	var nullKeys=[9,38,40];
	if(nullKeys.indexOf(keyHit) != -1){
		return false;
	}
	// Left
	if(keyHit == 37){
		returnMessage("Left");
		return false;
	}
	// Right
	if(keyHit == 39){
		returnMessage("Right");
		return false;
	}
	//Space & H & Return
	var resetKeys=[32,72,13];
	if(resetKeys.indexOf(keyHit) != -1){
		resize(0);
		return false;
	}
	// R
	if(keyHit == 82){
		refreshImage();
		return false;
	}
	// F
	if(keyHit == 70){
		returnMessage("toggleFullScreen");
		return false;
	}
	// Alt
	if(keyHit == 18){
		returnMessage("toggleMenuBarVis");
		return false;
	}
};
