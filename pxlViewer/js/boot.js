
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


/*
$(document).on('keypress', function(e){
	//if((openDialogue != "contactMe" || dialogueOpen==0) && typingFocus==0){
	if(dialogueOpen==0 && typingFocus==0){
		keyHit=e.keyCode || e.which;
		if(printKey==1){
			$("#alertFeed1").html(keyHit);
		}
		var nullKeys=[9,13,32,37,38,39,40,81,83,90,102]; // Do nothing keys
		if(nullKeys.indexOf(keyHit) != -1){
			return false;
		}
		if(active == 1){
			var numKeys=[49,50,51,52,53,54,55,56,57,48]; // Number keys
			if(numKeys.indexOf(keyHit) != -1){
				if(storeKeyHold==0){
					storeKeyHold=1;
					keyHoldCheck("storeSwatchColorSphere('colorSphereCanvas',"+keyHit+");");
				}
				return false;
			}
			// ` ~
			if(keyHit===96){
				if(storeKeyHold==0){
					storeKeyHold=1;
					keyHoldCheck("resetColorSphere('colorSphereCanvas',1,0);");
				}
				return false;
			}
		}
	}
});*/
$(document).on('keyup', function(e){
	keyHit=e.keyCode || e.which;
	var nullKeys=[9,37,38,39,40];
	if(nullKeys.indexOf(keyHit) != -1){
		return false;
	}
	//Space & H & Return
	var resetKeys=[32,72,13];
	if(resetKeys.indexOf(keyHit) != -1){
		resize(0);
		return false;
	}
});
