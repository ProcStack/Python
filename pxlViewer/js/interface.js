

function displaywheel(e){
	getMouseXY(e);
	var evt=window.event || e 
	var delta=evt.detail? evt.detail*(-120) : evt.wheelDelta
	//$("#touchData").html("<span style='color:#ffffff;font-size:150%;'>"+scroller+"  -</span>");
	scrollGallery(delta,0);
}
	
function scrollGallery(delta, abs){
	var toScroll;
	dragCount=0;
	var imgW=origImgW;
	var imgH=origImgH;
	var imgX=origImgX;
	var imgY=origImgY;
	var xMove=(delta);
	var yMove=(delta);
	scroller+=delta;
	scroller=Math.max(-1800,scroller);
	dragCount+=scroller/120;
	dragDist=scroller;
	var zoomPerc=delta/10;
	zoomLayers("touchData", "imgBlock",[],[],-2,zoomPerc);
	updateCanvas();
	return false;
}

if (document.attachEvent)
    document.attachEvent("on"+mousewheelevt, displaywheel)
else if (document.addEventListener)
    document.addEventListener(mousewheelevt, displaywheel, false)

// Thumbnail Start Drag
function startDrag() {

	//getMouseXY;
	mouseX=mouseX;
	mouseY=mouseY;
	prevMouseX = mouseX;
	prevMouseY = mouseY;
	origMouseX = mouseX;
	origMouseY = mouseY;
	$("#imgBlock").attr('offX', parseInt($("#imgBlock").css('left')) );
	$("#imgBlock").attr('offY', parseInt($("#imgBlock").css('top')) );
	$("#imgBlock").attr('curSizeW', parseInt($("#imgBlock").width()) );
	$("#imgBlock").attr('curSizeH', parseInt($("#imgBlock").height()) );


	//dragCount=0;
	
}
// Thumbnail Do Drag
function doDrag() {
	dragCount+=1;
	//getMouseXY;
	
	//if(Number.isInteger(m)){
	//	m=[mouseX,mouseY];
	//}
	if(mButton == 2){
		zoomLayers("touchData", "imgBlock",[],[],-2,-1);
		updateCanvas();
	}else{
		var imgW=$("#imgBlock").width();
		var imgH=$("#imgBlock").height();
		var imgX=parseInt($("#imgBlock").attr('offX'));
		var imgY=parseInt($("#imgBlock").attr('offY'));
		var xMove=(mouseX-origMouseX);
		var yMove=(mouseY-origMouseY);
			var dragDist=Math.sqrt(Math.pow(xMove,2)+Math.pow(yMove,2));
			dragDist=mouseX-origMouseX;
			calc[0]=(imgX)+xMove;
			calc[1]=(imgY)+yMove;
			$("#imgBlock").css({"left":calc[0],"top":calc[1]});
	}
	/*if(dragging>0){ // Get onmousedrag function to work on entire page, not individual items for setTimeout
		setTimeout(function(e){doDrag(m)},20);
	}*/
}
// Thumbnail End Drag
function endDrag() {
	$("#imgBlock").attr('offX', parseInt($("#imgBlock").css('left')) );
	$("#imgBlock").attr('offY', parseInt($("#imgBlock").css('top')) );
	$("#imgBlock").attr('curSizeW', parseInt($("#imgBlock").width()) );
	$("#imgBlock").attr('curSizeH', parseInt($("#imgBlock").height()) );
	dragCount=0;
	$("#touchData").attr("curScale", dynScale);
}


////////////////
// More documentation on zooming and panning functions can be found at www.github.com/ProcStack
// Required global variables-
// mouseX, mouseY
////////////////

// zoomLayers("touchData", "imgBlock",[],[],1,zoomPerc);
function zoomLayers(id,asset, mPos,cPos,init, zoomOffset){

	// Gather information about the reference object to move the given asset
	// This is a cor	relative zooming, based on where the mouse is to the reference object, to zoom the given asset
	// Separating this allows for different DOM objects to control the zooming object
	var galWidth=$("#"+id).width();
	var galHeight=$("#"+id).height();
	var galPos=$("#"+id).offset();
	var galTop=galPos.top;
	var galLeft=galPos.left;
	var imgPos=$("#"+asset).offset();
	 var imgLeft=imgPos.left;  // You'll most likely use offset, not absX and absY
	 var imgTop=imgPos.top;
	//var imgLeft=$("#"+asset).attr('absX'); // This is specific for this image gallery
	//var imgTop=$("#"+asset).attr('absY');
	var imgHeight=parseInt($("#"+asset).attr("heightdef"));
	var imgWidth=parseInt($("#"+asset).attr("widthdef"));
	
	// Prep zoomable asset
	if($("#"+asset).css("transform") == null || $("#"+asset).css("transition") == null){ // Asset object; Address transform css requirements
	    $("#"+asset).css({'transform':'scale(1, 1)','-moz-transform':'scale(1, 1)','-webkit-transform':'scale(1, 1)','-ms-transform':'scale(1, 1)','-o-transform':'scale(1, 1)'});
	}
	if($("#"+id).attr('doubleTouch') == null){ // Reference object; Address double click requirements
		$("#"+id).attr('doubleTouch',0);
	}
	if($("#"+id).attr('curScale') == null){  // Reference object; Address current scale requirements
		$("#"+id).attr('curScale',1);
	}
	var curScale=$("#"+id).attr('curScale');
	if(init==-2){
		mPos=[mouseX,mouseY];
		//mPos=[mouseX-imgLeft,mouseY-imgTop];
		//mPos=[mouseX-imgLeft,mouseY-imgTop];
		
		// cPos is an array to maintain required math between iterations
		// Doing it this way allows for additional information without needing to update function calls through out the javascript
		// cPos = [ Asset left position, Asset top position, Asset width, Asset height ];
		//cPos=[parseInt($("#"+asset).css('left'))+galLeft,parseInt($("#"+asset).css('top'))+galTop,$("#"+asset).width(),$("#"+asset).height()];
		cPos=[parseInt($("#"+asset).css('left')),parseInt($("#"+asset).css('top')),$("#"+asset).width(),$("#"+asset).height()];
		
		// If you are using the zoom function as a scrolling zoom with middle mouse, this sets to apply a zoom and stop the function
		// If you have a zoomOffset of -1, its assuming for a click drag zoom
		// Such as using a wheel to zoom -vs- using two fingers on a phone
		if(zoomOffset != -1){
			storeKeyHold=0;
			$("#"+id).attr('doubleTouch',0);
		}
		init=0;
	}
	var placeX,placeY;
	var mag;
	var minMag=.08;
	if(init != -1){
		if(zoomOffset == -1){
			mag=mouseX-mPos[0]; // Dragging zoom ammount
		}else{
			mag=zoomOffset; // Set zoom ammount
		}
	}
	if(($("#"+id).attr('doubleTouch')==1 && Math.abs(mag)<10) || init==-1){  // Double zoom (Double click, double two-finger tap) to reset zoom
		mag=1;
		var imgRatio=imgHeight/imgWidth;
		var displayRatio=galHeight/galWidth;
		//print("img",imgRatio);
		//print("display",displayRatio);

		if(imgRatio<displayRatio){ // Set img width to display
			mag=galWidth/imgWidth;
			placeX=0;
			placeY=galHeight/2-(imgHeight*mag)/2;
		}else{ // Set img height to display
			mag=galHeight/imgHeight;
			placeX=galWidth/2-(imgWidth*mag)/2;
			placeY=0;
		}
		//$("#"+asset).css({'top':'0px','left':'0px'});
//////////////////////////////////////////////////////////////
	}else{ // Zoom math
		if(mButton!= 2){
			// Set zoom rate
			var distScale=200;
			if(mouseX<mPos[0]){
				distScale=500;
			}
			mag=Math.max(.1,(distScale+mag)/distScale); // Zoom rate math
		}else{
			var dx=origMouseX-mouseX;
			dx= dx=0?1:dx
			var dy=origMouseY-mouseY;
			dy= dy=0?1:dy
			mag=Math.sqrt(dx*dx + dy*dy)*(Math.abs(dx)/dx);
			mag=1-(mag/500);
			mPos=[origMouseX,origMouseY];
			cPos[0]=parseInt($("#imgBlock").attr('offX'));
			cPos[1]=parseInt($("#imgBlock").attr('offY'));
			cPos[2]=$("#imgBlock").attr('curSizeW');
			cPos[3]=$("#imgBlock").attr('curSizeH');

		}
		var curPercX=(mPos[0]-cPos[0])/cPos[2];
		var curPercY=(mPos[1]-cPos[1])/cPos[3];
		
		
		var origPosX=cPos[2]*curPercX;//(curPercX*(cPos[2]*mag)-cPos[0]*((mag)))/(mag);
		var origPosY=cPos[3]*curPercY;//(curPercY*(cPos[3]*mag)-cPos[1]*((mag)))/(mag);
		var offX=-origPosX*mag+mPos[0];//(curPercX*(cPos[2]*curScale)-cPos[0]*curScale)/(mag*curScale);
		var offY=-origPosY*mag+mPos[1];//(curPercY*(cPos[3]*curScale)-cPos[1]*curScale)/(mag*curScale);
		var mult=Math.sin( Math.min(1,Math.max(0,(mag-curScale)/3)) * (3.14159265/2) );
		//placeX=Math.max(-cPos[2], Math.min( sW, offX));
		//placeY=Math.max(-cPos[3], Math.min( sH, offY));
		placeX= offX;
		placeY= offY;
		mag=Math.max(.08,mag*curScale);

		dynScale=mag;
	}
	//$("#"+asset).css({"transition": "all .03s linear","-moz-transition": "all .03s linear","-webkit-transition":"all .03s linear","-ms-transition": "all .03s linear","-o-transition": "all .03s linear"});
	
	if(mag != minMag){
		//tickVerboseCounter();
		//$("#verbText").html(mag+" - "+curScale+" -- "+minMag);
		$("#"+asset).css({'left':(placeX)+'px','top':(placeY)+'px'});
		$("#"+asset).css({'height':(imgHeight*mag)+'px','width':(imgWidth*mag)+'px'});
	}
    //$("#"+asset).css({'transform':'scale('+mag+', '+mag+')','-moz-transform':'scale('+mag+', '+mag+')','-webkit-transform':'scale('+mag+', '+mag+')','-ms-transform':'scale('+mag+', '+mag+')','-o-transform':'scale('+mag+', '+mag+')'});

	$("#scaleText").text((parseInt(mag*100*100)/100)+" %");
	if(storeKeyHold==1 && $("#"+id).attr('doubleTouch')==0){
		setTimeout(function(){zoomLayers(id,asset, mPos,cPos,init, zoomOffset);},100);
	}else{
		if(Math.abs(curScale-mag)<.05){
			$("#"+id).attr('doubleTouch',0);
		}
		if(mButton!=2){
			$("#"+id).attr('curScale',mag);	
		}
	}
}
function tickVerboseCounter(){
	var curcount=$("#verbText").text();
	if(curcount==""){
		curcount=0;
	}
	curcount=parseInt(curcount)+1;
	$("#verbText").html(curcount);
}

function print(){
	if(arguments.length>1){
		for(var x=0;x<arguments.length/2;++x){
			console.log("-- -- "+arguments[x*2]+" -- --");
			console.log(arguments[x*2+1]);
		}
	}else{
		console.log(arguments[0]);
	}
}

function resize(full){
	var sW=window.innerWidth;
	var sH=window.innerHeight;
	var pwidth=$(document).width();
	var pheight=$(document).height();
	var valW,valH,valLeft,valTop;
	lw=$("#imgBlock").width();
	lh=$("#imgBlock").height();
	
	$("#viewPane").css({"height":pheight,"width":pwidth, "left":"0", "top":"0"});

	var iheight=$("#imgBlock").height();
	var topMove=Math.max(0,parseInt((pheight-iheight)/2));
	////
	$("#imgBlock").css({"width":lw,"height":lh,"top":valTop,"left":valLeft,"visibility":"visible"});
	$("#imgDisp").css({"visibility":"visible"});
	//$("#imgBlock").attr({"widthDef":lw,"heightDef":lh,"topDef":0,"leftDef":0});
	$("#imgBlock").attr({"topDef":0,"leftDef":0});
	
	$("#touchData").css({"width":pwidth,"height":pheight,"left":"0","top":"0"}); 
	origImgW=valW;
	origImgH=valH;
	var pos=$("#imgBlock").position();
	origImgX=pos.left;
	origImgY=pos.top;
	curScale=1;
	zoomLayers("touchData", "imgBlock",[],[],-1,0);
}
function loadImg(url,lw,lh){
	//resetZoomPan();
	//var tempPrevThumb=updateThumbs(id);
	var pwidth=$(document).width();
	var pheight=$(document).height();
	var paneRatio=pwidth/pheight;
	var valW,valH,valLeft,valTop;
	var src,mid,url;
	
	
	//altText=$("#"+id).attr("alt");
	var imgRatio=lw/lh;
	//alert("#"+id+"-"+url+"-"+lw+"-"+lh);

	//$("#viewPane").html("<div id='imgBlock' style=\"background-image:url('"+src+"');background-size:cover;-webkit-background-size: cover;-moz-background-size:cover;-o-background-size:cover;width:"+lw+";height:"+lh+";position:absolute;top:"+valTop+";left:"+valLeft+";border:0;\" widthdef='"+lw+"' heightdef="+lh+"' topDef='0' leftDef='0' absX='0' absY='0' offX='0' offY='0' url='"+url+"'><img id='imgSource' src='"+mid+"' height='100%' width='100%'></div>");
	$("#viewPane").html("<div id='imgDisp' style=\"width:"+lw+";height:"+lh+";position:absolute;top:"+valTop+";left:"+valLeft+";border:0;\" widthdef='"+lw+"' heightdef="+lh+"' topDef='0' leftDef='0' absX='0' absY='0' offX='0' offY='0'><img id='imgSource' src='"+url+"' height='100%' width='100%'></div>");
	//$("#viewPane").attr("curImg", id);
	//window.location.replace("#"+id);
	var imgPos=$("#imgBlock").offset();
	var imgLeft=imgPos.left;
	var imgTop=imgPos.top;
	$("#imgBlock").attr({'absX':imgLeft,'absY':imgTop});

	
	origImgW=valW;
	origImgH=valH;
	curScale=1;
	//updateGalleryText(altText,url);
	
	zoomLayers("touchData", "imgBlock",[],[],-1,0);
}

window.onresize=function(event){resize(0);}

//
// For letting up of key
/*
storeKeyHold=0;
if(storeKeyHit==0){
	resetColorSphere('colorSphereCanvas',1,1);
}
storeKeyHit=0;
 
// For holding the key

if(storeKeyHold==0){
	storeKeyHold=1;
	keyHoldCheck("resetColorSphere('colorSphereCanvas',1,0);");
}
*/			
//

function keyHoldCheck(runFunc){
	if(storeKeyHold>0){
		storeKeyHold+=1;
		if(storeKeyHold==20){
			storeKeyHit=1;
			eval(runFunc);
		}else{
			setTimeout(function(){keyHoldCheck(runFunc);},35);
		}
	}
}

function resetZoomPan(){
	var id="touchData";
	var asset="imgBlock";
	var canvas="imgOverlay";
	$("#"+id).attr('doubleTouch',0);
	$("#"+id).attr('curScale',1);
    $("#"+asset).css({'transform':'scale(1, 1)','-moz-transform':'scale(1, 1)','-webkit-transform':'scale(1, 1)','-ms-transform':'scale(1, 1)','-o-transform':'scale(1, 1)'});
	$("#"+asset).css({'left':parseInt($("#"+asset).attr("leftDef"))+'px','top':parseInt($("#"+asset).attr("topDef"))+'px'});
    $("#"+canvas).css({'transform-origin':'top left', 'transform':'scale(1, 1)','-moz-transform':'scale(1, 1)','-webkit-transform':'scale(1, 1)','-ms-transform':'scale(1, 1)','-o-transform':'scale(1, 1)'});

}
function updateCanvas(){

	var curScale=parseFloat($("#touchData").attr('curScale'));
	var canvas="imgOverlay";
    $("#"+canvas).css({'transform-origin':'top left','transform':'scale('+curScale+', '+curScale+')','-moz-transform':'scale('+curScale+', '+curScale+')','-webkit-transform':'scale('+curScale+', '+curScale+')','-ms-transform':'scale('+curScale+', '+curScale+')','-o-transform':'scale('+curScale+', '+curScale+')'});
	
}
// Function for timed countdown to run a function; used for double click detection on this site
function countdown(func,countDown){
	var exitVal=1;
	countDown-=1;
	if(countDown==0){
		eval(func);
	}else{
		setTimeout(function(){countdown(func,countDown)},100);
	}
}
function setEntryImage(imgPath, w,h){
	imgPathDate=imgPath+"?"+new Date().getTime();
	$("#imgDisp").attr("src", imgPathDate);
	//loadImg(imgPathDate,w,h);
	var imgName=imgPath.split("/")
	imgName=imgName[imgName.length-1]
	setEntryText(imgName);
}
function setEntryText(txt){
	$("#entryText").text(txt);
}
function returnValue(variable,value){
	opWin.varValue("["+variable+","+value+"]");
}
function returnMessage(msg){
	opWin.showMessage(msg);
}


//////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////


//drawGeo("geoDrawTest",[100,100],0,10,[0,0,255],1,1);
function drawGeo(canvas,loc,eCount,size,color,alpha,filled){
	var comp=0;
	var flip=0;
	var x=loc[0];
	var y=loc[1];
	var R=color[0];
	var G=color[1];
	var B=color[2];
	hex="rgb("+Math.floor(R)+","+Math.floor(G)+","+Math.floor(B)+")"; // Prep for coloring solid geometry
	var csW=document.getElementById(canvas).offsetWidth;
	var csH=document.getElementById(canvas).offsetHeight;
	
	docCanvas=document.getElementById(canvas);
	draw=docCanvas.getContext('2d');
	var runCount=1;
	var flippers=[1,1];
	draw.globalAlpha=alpha;
	draw.beginPath();
	draw.lineWidth=Math.max(1,filled);
	if(filled==1){
		draw.fillStyle=hex;
	}else{
		draw.strokeStyle=hex;
	}
	if(eCount<=2){ // Draw a circle
		if(eCount==1){ // Draw a circle fading out
			var grad=draw.createRadialGradient(x,y,1,x,y,size/2);
			grad.addColorStop(0,'rgba('+Math.floor(color[0])+','+Math.floor(color[1])+','+Math.floor(color[2])+',1)');
			if(color.length>4){
				grad.addColorStop(1,'rgba('+Math.floor(color[3])+','+Math.floor(color[4])+','+Math.floor(color[5])+',0)');
			}else{
				grad.addColorStop(1,'rgba('+Math.floor(color[0])+','+Math.floor(color[1])+','+Math.floor(color[2])+',0)');
			}
			draw.fillStyle=grad;
		}else if(eCount==2){ // Draw a circle fading in
			var grad=draw.createRadialGradient(x,y,1,x,y,size/2);
			grad.addColorStop(0,'rgba('+Math.floor(color[0])+','+Math.floor(color[1])+','+Math.floor(color[2])+',0)');
			if(color.length>4){
				grad.addColorStop(1,'rgba('+Math.floor(color[3])+','+Math.floor(color[4])+','+Math.floor(color[5])+',1)');
			}else{
				grad.addColorStop(1,'rgba('+Math.floor(color[0])+','+Math.floor(color[1])+','+Math.floor(color[2])+',1)');
			}
			draw.fillStyle=grad;
		}
		draw.arc(x,y,size/2,0,Math.PI*2); // Draw circle
	}else{ // Draw lines
		if(loc.length>2){ // Make sure its not a single point
			if(eCount==3){ // Draw a linear curve
				draw.moveTo(x,y);
				for(var v=2; v<loc.length; v+=2){
					draw.lineTo(loc[v],loc[v+1]);
				}
				draw.lineJoin = 'round';
				if(size==1 && filled!=-1){
					draw.closePath();
				}else{
					draw.lineJoin = 'miter';
				}
			}else{ // Draw a quadratic curve
				draw.lineJoin = 'round';
				draw.moveTo(x,y);
				for(var v=2; v<loc.length; v+=4){
					draw.quadraticCurveTo(loc[v],loc[v+1], loc[v+2],loc[v+3]);
				}
				if(size==1){
					draw.quadraticCurveTo(loc[loc.length-2],loc[loc.length-1], loc[0],loc[1]);
				}
				if(size==1 && filled!=-1){
					draw.closePath();
				}else{
					draw.lineJoin = 'miter';
				}
			}
		}
	}
	if(filled==1){ // Fill object
		draw.fill();
	}else{ // Stroke object
		draw.stroke();
	}
}
