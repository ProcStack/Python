
function init(){
	document.onmousemove = function(e){getMouseXY;if(rightDown==1){ dragZoom();}};
	document.onscroll=function(){return false;};
	
	document.onmousedown=function(e) {console.log('etest');checkMouse;};
	document.onmouseup=function(){rightDown=0;};
	
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
