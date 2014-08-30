var pageIndex;
var totalCount;
var totalSize;
var pageSize=20;
function init()
{
	$.ajax({
		url:url,
		data:{cmd:"getAllCount",userid:""},
		cache:false,
		async:false,
		success:function(data){
			pageIndex=1;
			totalCount=parseInt(data);
			totalSize=totalCount % pageSize==0?parseInt(totalCount/pageSize):parseInt(totalCount/pageSize+1);
			}
		});
		if(pageIndex>1){
			$("#prePage")[0].style.display="inline";
			}
			if (pageIndex<totalSize){
			$("#nextPage")[0].style.display="inline";
			$("#selectpage")[0].style.display="inline";
			for(var i=0;i<totalSize;i++){
				$("#selectpage")[0].options.add(new Option((i+1),i));
				}
			}
		}
		
function nextPage(){
	pageIndex+=1;
	if(currli!=''){
		getNoteByType(currentType,currli);
		}else{
			getNoteByType(currentType);
			}
			select();
	}
function prePage()
{
	pageIndex-=1;
	if(currli!=''){
		getNoteByType(currentType,currli);
		}else{
			getNoteByType(currentType);
			}
	select();		
	}
function selectPage(page){
	for(var i=0;i<page.options.length;i++)
	{
		if(page.Options[i].selected){
			pageIndex=parseInt(page.options[i].text);
			}
		}
		if(currli!=''){
			getNoteByType(currentType,currli);
			}else{
				getNoteByType(currentType);
				}
				select();
		}	
function select(){
	for(var i=0;i<$("#selectpage1")[0].options.length;i++)
	{
		if($("#selectpage1")[0].options[i].text==(pageIndex+''))
		$("#selectpage1")[0].options[1].selected=true;
		}
	}	